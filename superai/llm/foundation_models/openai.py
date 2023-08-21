import json
import random
import time

import openai
from openai.error import (
    APIConnectionError,
    APIError,
    OpenAIError,
    RateLimitError,
    ServiceUnavailableError,
    Timeout,
    TryAgain,
)

from superai.data_program.protocol.transport_factory import compute_api_wait_time
from superai.llm.configuration import Configuration
from superai.llm.data_types.message import ChatMessage
from superai.llm.foundation_models.base import FoundationModel
from superai.log import logger
from superai.utils import retry

config = Configuration()


log = logger.get_logger(__name__)


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


class ChatGPT(OpenAIFoundation):
    engine: str = config.smart_foundation_model_engine
    temperature: float = 0
    max_tokens: int = 3000
    top_p: int = None
    n: int = None
    stream: bool = None
    logprobs: int = None
    presence_penalty: float = None
    frequency_penalty: float = None
    logit_bias: dict = None
    token_limit: int = 8000 if engine == "gpt-4" else 4096
    rpm: dict = {"gpt-4": 200, "gpt-3.5-turbo": 3500, "gpt-35-turbo": 3500}
    tpm: dict = {"gpt-4": 20000, "gpt-3.5-turbo": 240000, "gpt-35-turbo": 240000}

    def predict(self, input: ChatMessage):
        self.initialize_openai()

        if isinstance(input, ChatMessage):
            messages = [
                {"role": input.role, "content": input.content},
            ]
        elif isinstance(input, str):
            messages = [
                {"role": "system", "content": input},
            ]
        elif isinstance(input, list):
            if all(isinstance(i, ChatMessage) for i in input):
                messages = [{"role": i.role, "content": i.content} for i in input]
            elif all(isinstance(i, dict) for i in input):
                if all("role" in i and "content" in i for i in input):
                    messages = [{"role": i["role"], "content": i["content"]} for i in input]
            elif all(isinstance(i, str) for i in input):
                messages = [{"role": "system", "content": i} for i in input]
        else:
            raise Exception(
                f"Invalid input type {type(input)}: must be ChatMessage, str, dict or list of ChatMessage, str, or dict"
            )

        # Filter out None values
        params = {
            "engine": self.engine if config.openai_api_type == "azure" else None,
            "model": self.engine if config.openai_api_type == "open_ai" else None,
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
        }

        filtered_params = {k: v for k, v in params.items() if v is not None}

        log.debug(f"ChatGPT params: {filtered_params}")
        token_count = self.count_tokens(messages)
        response = self._openai_call(filtered_params, token_count)
        log.info("Raw LLM response: " + str(response))

        if "choices" not in response:
            raise Exception("No choices in response")

        # One failure mode is to run out of tokens. In most cases this is caused by
        # generating infinite loops. In case the generation did not come to a natural
        # stop we will not be able to parse the result. We will repeat the call with a
        # presence penalty to decrease the chance constantly repeated tokens.
        for penalty in [0.5, 1.0]:
            finish_reason = response["choices"][0].get("finish_reason", "")
            if finish_reason == "length":
                log.info(f"Generated incomplete answer. Rerun prompt with presence penalty {penalty}")
                filtered_params["frequency_penalty"] = penalty
                response = self._openai_call(filtered_params, token_count)
                log.info("Raw LLM response (with penalty): " + str(response))

                if "choices" not in response:
                    raise Exception("No choices in response")

        output = response["choices"][0]["message"]["content"]
        return output

    @retry(
        (
            APIConnectionError,
            APIError,
            RateLimitError,
            ServiceUnavailableError,
            Timeout,
            TryAgain,
        ),
        tries=10,
        delay=0,
        backoff=0,
    )  # no need for backoff, we're sleeping the amount required.
    def _openai_call(
        self,
        openai_params: dict,
        token_count: int,
        min_additional_sleep: float = 1.0,
        max_additional_sleep: float = 5.0,
    ):
        try:
            self._wait_for_rate_limits(self.engine, token_count)

            response = openai.ChatCompletion.create(**openai_params)
        except RateLimitError as e:
            reset_rate_header = e.headers.get("x-ratelimit-reset-requests", "30s")

            sleep_time = 30.0
            if reset_rate_header.endswith("s") and "m" not in reset_rate_header:
                try:
                    sleep_time = float(reset_rate_header[:-1])
                except ValueError:
                    log.info(f"Could not cast {reset_rate_header[:-1]} to float")
            additional_sleep = random.uniform(min_additional_sleep, max_additional_sleep)

            sleep_time = sleep_time + additional_sleep
            log.info(f"Rate limit exceeded, request throttling will reset in {sleep_time} seconds, sleeping")

            time.sleep(sleep_time)
            raise RateLimitError

        except (APIConnectionError, APIError, ServiceUnavailableError, Timeout, TryAgain) as e:
            log.warning(f"OpenAi call raised {e.error} found headers: {e.headers} retying..")
            raise e

        except OpenAIError as e:
            log.exception(f"Found an OpenAi error that can't be retried: {e} headers: {e.headers}")
            raise e

        except Exception as e:
            log.error(f"Exception in the openai call that wasn't an OpenAiError: {e}")
            raise e
        return response

    def _wait_for_rate_limits(self, model: str, token_on_current_request: int):
        while True:
            random_additional_time = random.uniform(0.0, 1.5)

            try:
                # RPM computation
                if time_to_wait := compute_api_wait_time(model + "_RPM", self.rpm[model]):
                    time_to_wait = time_to_wait + random_additional_time
                    log.info(f"openai max RPM reached, waiting for {time_to_wait} and retrying")
                    time.sleep(time_to_wait)
                    continue

                # TPM computation
                if time_to_wait := compute_api_wait_time(model + "_TPM", self.tpm[model], token_on_current_request):
                    time_to_wait = time_to_wait + random_additional_time
                    log.info(f"openai max TPM reached, waiting for {time_to_wait} and retrying")
                    time.sleep(time_to_wait)
                    continue

            except Exception as e:
                log.error(f"Could not check RPM or TPM due to {e}")

            return

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
