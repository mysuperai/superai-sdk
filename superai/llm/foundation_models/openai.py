import json

import openai

from superai.llm.configuration import Configuration
from superai.llm.data_types.message import ChatMessage
from superai.llm.foundation_models.base import (
    FoundationModel,
    check_open_ai_api_key,
    retry,
)

config = Configuration()


class ChatGPT(FoundationModel):
    engine: str = config.smart_foundation_model_engine
    temperature: float = 0
    max_tokens: int = None
    top_p: int = None
    n: int = None
    stream: bool = None
    logprobs: int = None
    presence_penalty: float = None
    frequency_penalty: float = None
    logit_bias: dict = None
    user: str = None
    token_limit: int = 8000 if engine == "gpt-4" else 4096

    @retry
    def predict(self, input: ChatMessage):
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
            raise Exception("Invalid input type: must be ChatMessage, str, dict or list of ChatMessage, str, or dict")

        # Filter out None values
        params = {
            "model": self.engine,
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

        response = openai.ChatCompletion.create(**filtered_params)

        if "choices" in response:
            output = response["choices"][0]["message"]["content"]
            # try:
            #     output_json = json.loads(output)
            #     return output_json
            # except json.JSONDecodeError:
            #     # If the output is not valid JSON, return the original output string
            return output
        else:
            raise Exception("No choices in response")

    def check_api_key(self, api_key):
        check_open_ai_api_key(api_key)


class OpenAIEmbedding(FoundationModel):
    engine: str = config.embedding_model_engine
    user: str = None
    token_limit: int = 8191 if engine == "gpt-4" else 4096

    @retry
    def predict(self, input):

        if isinstance(input, str):
            input = [input]

        params = {
            "model": self.engine,
            "input": input,
            "user": self.user,
        }
        # filter out None values
        filtered_params = {k: v for k, v in params.items() if v is not None}
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
        check_open_ai_api_key(api_key)
