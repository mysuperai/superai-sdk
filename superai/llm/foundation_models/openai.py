import datetime
import json
import os
import random
import tempfile
import time
from itertools import count
from operator import itemgetter
from typing import List, Optional, TypedDict, Union

import boto3
import diskcache as dc
import tiktoken
from openai import (
    APIConnectionError,
    APIError,
    AzureOpenAI,
    InternalServerError,
    RateLimitError,
    Timeout,
)
from openai.types.chat import ChatCompletion, ChatCompletionMessage
from openai.types.chat.chat_completion import Choice

from superai.config import settings
from superai.llm.configuration import Configuration
from superai.llm.data_types.message import ChatMessage
from superai.llm.foundation_models.base import FoundationModel
from superai.llm.foundation_models.llm_cache_manager import check_cache, store_in_cache
from superai.log import logger

config = Configuration()

log = logger.get_logger(__name__)


def load_params_from_aws_secrets():
    """
    Loads parameters of different OpenAI foundation models from AWS secrets.
    It's supposed that the format of settings is the following:
    {"llm": {"modelname_1": [{<settings1>}, {settings2}, ...], "modelname_1": [{<settings1>}, ...], ...}}
    """
    secrets_client = boto3.client("secretsmanager", region_name="eu-central-1")

    secret_string = secrets_client.get_secret_value(SecretId="dataprogram-openai")["SecretString"]
    llm_config = json.loads(secret_string)

    # for backward compatibility
    llm_config = {
        key: value if type(value) is list else [add_missing_information(key, value)]
        for key, value in llm_config["llm"].items()
    }
    settings.update({"llm": llm_config})


def add_missing_information(llm_key, llm_config_values):
    """Add missing information for backwards compatibility"""
    if llm_key == "chatgpt":
        # No explicit support for chatgpt
        return llm_config_values

    rpm_by_model = {
        "gpt-4": 200,
        "gpt-4-32k": 200,
        "gpt-35-turbo": 3500,
        "gpt-35-turbo-16k": 3500,
    }

    tpm_by_model = {
        "gpt-4": 20000,
        "gpt-4-32k": 200,
        "gpt-35-turbo": 240000,
        "gpt-35-turbo-16k": 240000,
    }

    token_limit_by_model = {
        "gpt-4": 8192,
        "gpt-4-32k": 32768,
        "gpt-35-turbo": 4097,
        "gpt-35-turbo-16k": 16385,
    }

    llm_config_values["id"] = llm_key + "_legacy"
    llm_config_values["rpm"] = rpm_by_model[llm_key]
    llm_config_values["tpm"] = tpm_by_model[llm_key]
    llm_config_values["token_limit"] = token_limit_by_model[llm_key]
    llm_config_values["priority"] = 1

    return llm_config_values


class FoundationModelParams(TypedDict):
    id: str
    completion_model_engine: str
    api_type: str
    api_key: str
    api_base: str
    api_version: str
    token_limit: int
    rpm: int
    tpm: int
    priority: float


MAX_ERRORS = 5

RECOVERABLE_DOWNSTREAM_ERRORS = [
    APIConnectionError,
    APIError,
    Timeout,
    InternalServerError,
]

# Cache to save wait times for model endpoints.
cache = dc.Cache(os.path.join(tempfile.gettempdir(), "rate"))


class AzureOpenAIModelEndpoint:
    """
    Model Endpoint of an Azure OpenAI Model Deployment.

    Captures meta-information for each endpoint. In case of waiting times due to rate
    limitation will provide accounting mechanism for this as well.

    """

    id: str
    client: AzureOpenAI
    priority: int
    model_errors: int = 0

    def __init__(self, id: str, priority: int, client: AzureOpenAI):
        self.id = id
        self.priority = priority
        self.client = client

    def set_wait_time(self, wait_time: int):
        end_time = datetime.datetime.now() + datetime.timedelta(0, wait_time)
        cache.set(self.id, end_time.timestamp(), wait_time + 60)

    def get_wait_time(self) -> int:
        now = datetime.datetime.now()
        wait_time = cache.get(self.id, 0)
        return max(0, wait_time - now.timestamp())


class ChatGPT(FoundationModel):
    """
    OpenAI ChatGPT LLM Model

    "openai_model" is a name of OpenAI model name, which we want to use.
    This name is not nessesary the "engine" or "model" parameter of OpenAI or Azure APIs.
    Instead, this parameter references a group in Dynaconf settings, where all the nessesary
    OpenAI/Azure API parameters are defined, such as "completion_model_engine", "api_key", "api_base", etc.
    Available values of "openai_model" field are defined by current settings, they are not controlled by SDK.
    Settings are read each time the "predict()" method is called. It allows to modify settings at any moment
    before this method was called
    """

    user: str = None
    openai_model: str = "gpt-35-turbo"
    temperature: float = 0
    top_p: int = None
    n: int = None
    stream: bool = None
    logprobs: int = None
    presence_penalty: float = None
    frequency_penalty: float = None
    logit_bias: dict = None
    response_format: dict = None
    # Lazy load endpoints with first prediction
    model_endpoints: List[AzureOpenAIModelEndpoint] = []

    def _init_endpoints(self):
        all_models_params = settings.get("llm").get(self.openai_model, None)
        if not all_models_params:
            raise Exception(f"Unknown OpenAI model: {self.openai_model}")
        for model_params in all_models_params:
            azure_openai_client = AzureOpenAI(
                api_version=model_params.api_version,
                api_key=model_params.api_key,
                azure_endpoint=model_params.api_base,
                max_retries=1,  # We should not take more than 20 min
            )
            endpoint = AzureOpenAIModelEndpoint(
                id=model_params.id, priority=model_params.priority, client=azure_openai_client
            )
            self.model_endpoints.append(endpoint)

    @property
    def engine(self):
        model_params = settings.get("llm").get(self.openai_model, None)
        if not model_params:
            raise Exception(f"Unknown OpenAI model: {self.openai_model}")
        # we assume that all the models have same model engine
        return model_params[0].completion_model_engine

    @property
    def token_limit(self) -> int:
        all_models_params = settings.get("llm").get(self.openai_model, None)
        if not all_models_params:
            raise Exception(f"Unknown OpenAI model: {self.openai_model}")
        return all_models_params[0]["token_limit"]

    @property
    def max_generation_tokens(self) -> Optional[int]:
        all_models_params = settings.get("llm").get(self.openai_model, None)
        if not all_models_params:
            raise Exception(f"Unknown OpenAI model: {self.openai_model}")
        return all_models_params[0].get("max_generation_tokens", None)

    def predict(
        self,
        input: Union[ChatMessage, str, list],
        manual_token_limit: Optional[int] = None,
        retry_on_length: bool = True,
        stream: bool = False,
    ):
        """
        Generates a prediction based on the given input using the best available model
        endpoint.

        This method handles various error scenarios, including API errors and rate
        limiting, by implementing a retry mechanism. It also adjusts token limits
        based on input length and optional manual limits.

        :param input: The compiled prompt for the model.
        :param manual_token_limit: An optional manual limit for the number of tokens to
        generate. If not specified, the limit is determined automatically based on model
        token limits.
        :param retry_on_length: If set to True, the function retries generation
        when the finish reason is 'length' due to reaching token limits.
        :return: The generated response from the model.
        """
        frequency_penalties = [None, 0.5, 1.0]
        cur_penalty_idx = 0
        latest_error = None

        # We lazy load the model endpoints because the credentials might not be
        # available at creation of this object. We assume that they are loaded once the
        # first prediction is called.
        if len(self.model_endpoints) == 0:
            self._init_endpoints()

        for endpoint in self.model_endpoints:
            endpoint.model_errors = 0

        messages = self._input_to_messages(input)
        max_tokens, remaining_token_space, restricted_max_token = self.compute_max_tokens(manual_token_limit, messages)

        # There are six different variants how iteration of this circle can end:
        #   1. successful response -> return output
        #   2. Unrecoverable API error. Raise the error
        #   3. Recoverable API error. Repeat max 5 times for each model
        #   4. API returns RateLimitError -> notify rate manager and repeat
        #   5. Rate manager says to wait -> wait and repeat
        #   6. Response with finish_reason == length -> select next frequency penalty and repeat.
        #      If no penalties left, return latest response
        while True:
            best_model_idx, wait_time = self._select_most_available_model()

            if best_model_idx is None:
                raise latest_error

            if wait_time > 0:
                additional_sleep = random.uniform(1, 2)
                time.sleep(wait_time + additional_sleep)
                logger.info(f"Best model {self.model_endpoints[best_model_idx].id} is busy. Need to wait {wait_time}")
                continue

            params = {
                "model": self.engine,
                "n": self.n,
                "messages": messages,
                "temperature": self.temperature,
                "top_p": self.top_p,
                "stream": self.stream,
                "logprobs": self.logprobs,
                "presence_penalty": self.presence_penalty,
                "logit_bias": self.logit_bias,
                "user": self.user,
                "response_format": self.response_format,
                "frequency_penalty": frequency_penalties[cur_penalty_idx],
            }

            # Filter out None values
            filtered_params = {k: v for k, v in params.items() if v is not None}
            # GPT-4 Turbo supports seed setting. As it is currently 18-12-23 the only
            # model to support this we hard code it to the model.
            if self.engine == "gpt-4-1106-preview":
                params["seed"] = 42

            log.debug(f"ChatGPT params: {filtered_params}")
            filtered_params["max_tokens"] = max_tokens
            log.info(f"Max generation token set to {filtered_params['max_tokens']}")

            response, error, sleep_time = self._openai_call(filtered_params, best_model_idx, stream)
            latest_error = error

            if sleep_time > 0:
                self.model_endpoints[best_model_idx].set_wait_time(sleep_time)
                continue

            if error:
                if type(error) in RECOVERABLE_DOWNSTREAM_ERRORS:
                    self.model_endpoints[best_model_idx].model_errors += 1
                    continue
                raise error

            if "choices" not in response:
                raise Exception("No choices in response")

            # One failure mode is to run out of tokens. Our max_token could have been
            # set too strictly, or we are generating too much output
            finish_reason = response["choices"][0].get("finish_reason", "")
            if finish_reason == "length" and restricted_max_token:
                # In case we set the token limit to the prompt length, and we ran out of
                # token, we will try again with the less restrictive token limit without
                # setting a frequency penalty
                logger.info(f"Hit restricted token limit. Rerunning with relaxed token limit")
                max_tokens = min(remaining_token_space, manual_token_limit or remaining_token_space)
                restricted_max_token = False
                continue
            elif finish_reason == "length" and cur_penalty_idx < len(frequency_penalties) - 1 and retry_on_length:
                # In most cases running out of tokens is caused by generating infinite
                # loops. In case the generation did not come to a natural stop we will
                # not be able to parse the result. We will repeat the call with a
                # presence penalty to decrease the chance constantly repeated tokens.
                cur_penalty_idx += 1
                continue

            if finish_reason == "length":
                logger.info("Final extraction finished with reason length")

            output = response["choices"][0]["message"]["content"]
            return output

    def compute_max_tokens(self, manual_token_limit: Optional[int], messages) -> (int, int, bool):
        """Calculates the maximum token count for model generation, considering the
        input message length, a manual token limit, and the model's inherent token
        generation constraints.

        This method first determines the token count based on the input messages. It
        then adjusts this count to adhere to the model's maximum token generation limit,
        if applicable. Additionally, it accounts for any manually specified token limit.
        The maximum tokens will be set tightly
        The method also flags whether the max token count was restricted more tightly
        to

        :param manual_token_limit: An optional integer representing a manual limit on
        the number of tokens.
        :param messages: A list of message dictionaries, with each message containing
        content to encode.
        :return: A tuple containing the calculated maximum number of tokens, the
        remaining token space after accounting for input length, and a boolean
        indicating if the max token count has been restricted based on the input
        message length.
        """
        restricted_max_token = False
        encoding = tiktoken.encoding_for_model(self.engine)
        token_count = len(encoding.encode(messages[0]["content"]))
        # We need to set the max_tokens parameter as tightly as possible. We assume that
        # the number of generated tokens should not be more than the prompt.
        remaining_token_space = (self.token_limit - 50) - token_count
        # Some models have a more restrictive generation token limit. We should not
        # generate more token
        if self.max_generation_tokens:
            remaining_token_space = min(remaining_token_space, self.max_generation_tokens)
        max_tokens = remaining_token_space
        if token_count < remaining_token_space:
            logger.info(
                f"Restricting max_tokens from {remaining_token_space} remaining token space to {token_count} token",
                extra={"remaining_token_space": remaining_token_space, "token_count": token_count},
            )
            max_tokens = token_count
            restricted_max_token = True
        # We can further manually limit the number of tokens even more.
        if manual_token_limit is not None:
            log.info(
                f"Manually token limit set to {manual_token_limit}", extra={"manual_token_limit": manual_token_limit}
            )
            max_tokens = min(max_tokens, manual_token_limit)
        return max_tokens, remaining_token_space, restricted_max_token

    def _openai_call(self, openai_params: dict, best_model_idx: int, stream: bool = False):
        start_time = time.time()
        error = None
        sleep_time = 0
        response = None
        cache_paramas = {
            "api_version": self.model_endpoints[best_model_idx].client._api_version,
            "class_name": self.__class__.__name__,
        }
        cache_paramas.update(openai_params)

        cache_response = check_cache(cache_paramas)
        if cache_response:
            return cache_response, None, 0

        try:
            if stream:
                response = self._call_streaming_api(self.model_endpoints[best_model_idx], openai_params)
            else:
                response = self.model_endpoints[best_model_idx].client.chat.completions.create(**openai_params)
            store_in_cache(cache_paramas, response.dict())
            azure_response = {
                "azure_openai_response": {
                    "elapsed": round(time.time() - start_time, 2),
                    "response": response.dict(),
                    "openai_params": openai_params,
                    "endpoint": self.model_endpoints[best_model_idx].client.base_url,
                }
            }
            log.info("Azure OpenAI call successful", extra=azure_response)
        except RateLimitError as e:
            # Maxing out requests in order to block other openai callers
            headers = e.response.headers

            sleep_time = 30.0
            if retry_after := headers.get("Retry-After", None):
                sleep_time = float(retry_after)
            elif headers.get("x-ratelimit-reset-requests", None):
                reset_rate_header = headers["x-ratelimit-reset-requests"]
                if reset_rate_header.endswith("s") and "m" not in reset_rate_header:
                    try:
                        sleep_time = float(reset_rate_header[:-1])
                    except ValueError:
                        log.info(f"Could not cast {reset_rate_header[:-1]} to float")

            azure_response = {
                "azure_openai_response": {
                    "elapsed": round(time.time() - start_time, 2),
                    "error": "RateLimitError",
                    "headers": e.response.headers,
                    "action": "sleep",
                    "duration": sleep_time,
                    "openai_params": openai_params,
                }
            }
            log.warning("Azure OpenAI call cause RateLimitError", extra=azure_response)

            error = e
        except InternalServerError as e:
            azure_response = {
                "azure_openai_response": {
                    "elapsed": round(time.time() - start_time, 2),
                    "error": "InternalServerError",
                    "action": "retrying",
                    "openai_params": openai_params,
                }
            }
            log.warning(f"Azure OpenAI call caused InternalServerError", extra=azure_response)
            error = e

        except (APIConnectionError, APIError) as e:
            azure_response = {
                "azure_openai_response": {
                    "elapsed": round(time.time() - start_time, 2),
                    "error": e.error,
                    "headers": e.headers,
                    "action": "retrying",
                    "openai_params": openai_params,
                }
            }
            log.warning(f"Azure OpenAI call caused {e.error}", extra=azure_response)
            error = e

        except Exception as e:
            log.exception(f"Exception in the openai call that wasn't an OpenAiError: {e}")
            error = e

        if response is not None:
            response = response.dict()
        else:
            response = {}

        return response, error, sleep_time

    def _call_streaming_api(self, endpoint: AzureOpenAIModelEndpoint, openai_params: dict) -> ChatCompletion:
        """Calls the streaming variant of the chat completion API. The results then are
        collected and transformed into the response format of the non-streaming variant
        """
        encoding = tiktoken.encoding_for_model(self.engine)
        prompt_tokens = len(encoding.encode(openai_params["messages"][0]["content"]))

        stream = endpoint.client.chat.completions.create(**openai_params, stream=True)
        response_tokens = []
        final_chunk = None
        for chunk in stream:
            if len(chunk.choices) > 0:
                response_tokens.append(chunk.choices[0].delta.content or "")
                final_chunk = chunk
        logger.info("Completed using streaming API")

        response = self.convert_to_chat_completion_response(final_chunk, response_tokens, prompt_tokens)
        return response

    def convert_to_chat_completion_response(
        self, final_chunk, response_tokens: List[str], prompt_tokens: int
    ) -> ChatCompletion:
        """Converts a streaming ChatCompletion into a regular one. Using information
        from the last chunk.
        """
        response = "".join(response_tokens)
        encoding = tiktoken.encoding_for_model(self.engine)
        completion_tokens = len(encoding.encode(response))

        obj = {k: v for k, v in final_chunk.dict().items() if k not in ["choices", "object"]}
        obj["usage"] = {
            "completion_tokens": completion_tokens,
            "prompt_tokens": prompt_tokens,
            "total_tokens": completion_tokens + prompt_tokens,
        }
        obj["object"] = "chat.completion"

        final_chunk_finish_reason = None if final_chunk is None else final_chunk.choices[0].finish_reason
        obj["choices"] = [
            Choice(
                index=0,
                message=ChatCompletionMessage(role="assistant", content=response),
                finish_reason=final_chunk_finish_reason or "length",
            )
        ]
        response = ChatCompletion(**obj)
        return response

    def _input_to_messages(self, input: Union[ChatMessage, str, list]):
        if isinstance(input, ChatMessage):
            return [
                {"role": input.role, "content": input.content},
            ]
        elif isinstance(input, str):
            return [
                {"role": "system", "content": input},
            ]
        elif isinstance(input, list):
            if all(isinstance(i, ChatMessage) for i in input):
                return [{"role": i.role, "content": i.content} for i in input]
            elif all(isinstance(i, dict) for i in input):
                if all("role" in i and "content" in i for i in input):
                    return [{"role": i["role"], "content": i["content"]} for i in input]
            elif all(isinstance(i, str) for i in input):
                return [{"role": "system", "content": i} for i in input]

        raise Exception(
            f"Invalid input type {type(input)}: must be ChatMessage, str, dict or list of ChatMessage, str, or dict"
        )

    def _select_most_available_model(self):
        """Selects one of foundation models. Selection criteria are the following:
        1. Smallest wait time
        2. Least number of previous recoverable errors
        3. Priority
        Models that reached MAX_ERRORS are excluded from selection
        Returns: (best_model_idx, wait_time). If no model can be selected, returns (None, 0)
        """
        wait_times = [endpoint.get_wait_time() for endpoint in self.model_endpoints]
        priorities = [endpoint.priority for endpoint in self.model_endpoints]
        model_errors = [endpoint.model_errors for endpoint in self.model_endpoints]

        valid_items = list(
            filter(lambda item: item[2] < MAX_ERRORS, zip(count(), wait_times, model_errors, priorities))
        )

        if not valid_items:
            return None, 0

        best_model_idx, best_wait_time, _, _ = min(valid_items, key=itemgetter(1, 2, 3))
        return (best_model_idx, best_wait_time)

    def check_api_key(self, api_key):
        self.verify_api_key(api_key)
