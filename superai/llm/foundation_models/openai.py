import json
import random
import time
from itertools import count
from operator import itemgetter
from typing import Optional, TypedDict, Union

import boto3
import openai
import tiktoken
from openai.error import (
    APIConnectionError,
    APIError,
    OpenAIError,
    RateLimitError,
    ServiceUnavailableError,
    Timeout,
    TryAgain,
)

from superai.config import settings
from superai.data_program.protocol.rate_limit import get_wait_time, set_wait_time
from superai.llm.configuration import Configuration
from superai.llm.data_types.message import ChatMessage
from superai.llm.foundation_models.base import FoundationModel
from superai.log import logger
from superai.utils import retry

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


class OpenAIFoundation(FoundationModel):
    user: str = None
    api_key: str = config.open_ai_api_key

    def initialize_openai(self):
        openai.api_type = config.openai_api_type
        openai.api_base = config.openai_api_base
        openai.api_version = config.openai_api_version
        openai.api_key = self.api_key

    def verify_api_key(self, api_key):
        try:
            openai.api_key = api_key
            openai.Model.list()
        except Exception as e:
            raise Exception("Invalid API key. Error: " + str(e))


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
    ServiceUnavailableError,
    Timeout,
    TryAgain,
]


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
    max_tokens: int = None
    top_p: int = None
    n: int = None
    stream: bool = None
    logprobs: int = None
    presence_penalty: float = None
    frequency_penalty: float = None
    logit_bias: dict = None

    @property
    def engine(self):
        model_params = settings.get("llm").get(self.openai_model, None)
        if not model_params:
            raise Exception(f"Unknown OpenAI model: {self.openai_model}")
        # we assume that all the models have same model engine
        return model_params[0].completion_model_engine

    @property
    def token_limit(self):
        all_models_params = settings.get("llm").get(self.openai_model, None)
        if not all_models_params:
            raise Exception(f"Unknown OpenAI model: {self.openai_model}")
        return all_models_params[0]["token_limit"]

    def predict(self, input: Union[ChatMessage, str, list], manual_token_limit: Optional[int] = None):
        frequency_penalties = [None, 0.5, 1.0]
        cur_penalty_idx = 0
        latest_error = None
        restricted_max_token = False

        all_models_params = settings.get("llm").get(self.openai_model, None)
        if not all_models_params:
            raise Exception(f"Unknown OpenAI model: {self.openai_model}")
        model_errors = [0] * len(all_models_params)

        messages = self._input_to_messages(input)
        encoding = tiktoken.encoding_for_model(self.engine)
        token_count = len(encoding.encode(messages[0]["content"]))

        # We need to set the max_tokens parameter as tightly as possible. We assume that
        # the number of generated tokens should not be more than the prompt.
        remaining_token_space = (self.token_limit - 50) - token_count
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

        # There are six different variants how iteration of this circle can end:
        #   1. successful response -> return output
        #   2. Unrecoverable API error. Raise the error
        #   3. Recoverable API error. Repeat max 5 times for each model
        #   4. API returns RateLimitError -> notify rate manager and repeat
        #   5. Rate manager says to wait -> wait and repeat
        #   6. Response with finish_reason == length -> select next frequency penalty and repeat.
        #      If no penalties left, return latest response
        while True:
            best_model_idx, wait_time = self._select_most_available_model(all_models_params, model_errors)

            if best_model_idx is None:
                raise latest_error

            if wait_time > 0:
                additional_sleep = random.uniform(1, 2)
                time.sleep(wait_time + additional_sleep)
                logger.info(f"Best model {all_models_params[best_model_idx]['id']} is busy. Need to wait {wait_time}")
                continue

            model_params = all_models_params[best_model_idx]

            params = {
                "engine": model_params.completion_model_engine if model_params.api_type == "azure" else None,
                "model": model_params.completion_model_engine if model_params.api_type == "open_ai" else None,
                "api_key": model_params.api_key,
                "api_type": model_params.api_type,
                "api_base": model_params.api_base,
                "api_version": model_params.api_version,
                "n": self.n,
                "messages": messages,
                "temperature": self.temperature,
                "max_tokens": self.max_tokens,
                "top_p": self.top_p,
                "stream": self.stream,
                "logprobs": self.logprobs,
                "presence_penalty": self.presence_penalty,
                "frequency_penalty": self.frequency_penalty,
                "logit_bias": self.logit_bias,
                "user": self.user,
                "frequency_penalty": frequency_penalties[cur_penalty_idx],
            }

            # Filter out None values
            filtered_params = {k: v for k, v in params.items() if v is not None}

            log.debug(f"ChatGPT params: {filtered_params}")
            filtered_params["max_tokens"] = max_tokens
            log.info(f"Max generation token set to {filtered_params['max_tokens']}")

            response, error, sleep_time = self._openai_call(filtered_params)
            latest_error = error

            if sleep_time > 0:
                set_wait_time(model_params["id"], sleep_time)
                continue

            if error:
                if type(error) in RECOVERABLE_DOWNSTREAM_ERRORS:
                    model_errors[best_model_idx] += 1
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
            elif finish_reason == "length" and cur_penalty_idx < len(frequency_penalties) - 1:
                # In most cases running out og tokens is caused by generating infinite
                # loops. In case the generation did not come to a natural stop we will
                # not be able to parse the result. We will repeat the call with a
                # presence penalty to decrease the chance constantly repeated tokens.
                cur_penalty_idx += 1
                continue

            output = response["choices"][0]["message"]["content"]
            return output

    def _openai_call(self, openai_params: dict):
        start_time = time.time()
        error = None
        sleep_time = 0
        response = None
        try:
            response = openai.ChatCompletion.create(**openai_params)
            azure_response = {
                "azure_openai_response": {
                    "elapsed": round(time.time() - start_time, 2),
                    "response": response.to_dict_recursive(),
                    "openai_params": openai_params,
                }
            }
            log.info("Azure OpenAI call successful", extra=azure_response)
        except RateLimitError as e:
            # Maxing out requests in order to block other openai callers
            # self._wait_for_rate_limits(self.openai_model, self.rpm[self.openai_model])

            # additional_sleep = random.uniform(min_additional_sleep, max_additional_sleep)
            headers = e.headers

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
                    "error": e.error,
                    "headers": e.headers,
                    "action": "sleep",
                    "duration": sleep_time,
                    "openai_params": openai_params,
                }
            }
            log.warning("Azure OpenAI call cause RateLimitError", extra=azure_response)

            error = e

        except (APIConnectionError, APIError, ServiceUnavailableError, Timeout, TryAgain) as e:
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

        except OpenAIError as e:
            azure_response = {
                "azure_openai_response": {
                    "elapsed": round(time.time() - start_time, 2),
                    "error": e.error,
                    "headers": e.headers,
                    "action": "stop",
                }
            }
            error = e

        except Exception as e:
            log.exception(f"Exception in the openai call that wasn't an OpenAiError: {e}")
            error = e
        return response, error, sleep_time

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

    def _select_most_available_model(self, all_models_params: list[FoundationModelParams], model_errors: list[int]):
        """Selects one of foundation models. Selection criteria are the following:
        1. Smallest wait time
        2. Least number of previous recoverable errors
        3. Priority
        Models that reached MAX_ERRORS are excluded from selection
        Returns: (best_model_idx, wait_time). If no model can be selected, returns (None, 0)
        """
        wait_times = [get_wait_time(model["id"]) for model in all_models_params]
        priorities = map(itemgetter("priority"), all_models_params)

        valid_items = list(
            filter(lambda item: item[2] < MAX_ERRORS, zip(count(), wait_times, model_errors, priorities))
        )

        if not valid_items:
            return None, 0

        best_model_idx, best_wait_time, _, _ = min(valid_items, key=itemgetter(1, 2, 3))
        return (best_model_idx, best_wait_time)

    def check_api_key(self, api_key):
        self.verify_api_key(api_key)


class OpenAIEmbedding(OpenAIFoundation):
    engine: str = config.embedding_model_engine
    user: str = None
    token_limit: int = 8191 if engine == "gpt-4" else 4096

    @retry
    def predict(self, input):
        self.initialize_openai()

        if isinstance(input, str):
            input = [input]

        params = {
            "engine": self.engine if config.openai_api_type == "azure" else None,
            "model": self.engine if config.openai_api_type == "open_ai" else None,
            "input": input,
            "user": self.user,
        }

        # filter out None values
        filtered_params = {k: v for k, v in params.items() if v is not None}

        log.debug(f"OpenAIEmbedding params: {filtered_params}")
        response = openai.Embedding.create(**filtered_params)

        if "data" in response:
            output = response["data"][0]["embedding"]

            # Try to parse the output as JSON
            try:
                output_json = json.loads(json.dumps(output).replace("'", '"'))
                return output_json
            except json.JSONDecodeError:
                # If the output is not valid JSON, return the original output string
                return output
        else:
            raise Exception("No data in response")

    def check_api_key(self, api_key):
        self.verify_api_key(api_key)
