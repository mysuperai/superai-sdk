import time
from abc import ABC, abstractmethod
from functools import wraps

import tiktoken
from openai.error import RateLimitError
from pydantic import BaseModel, Extra
from requests.exceptions import ConnectionError
from tiktoken.model import MODEL_TO_ENCODING

# TODO: remove when tiktoken model registry will be updated
MODEL_TO_ENCODING.setdefault("gpt-35-turbo", "cl100k_base")


class FoundationModel(ABC, BaseModel):
    class Config:
        """Configuration for this pydantic object."""

        extra = Extra.allow
        arbitrary_types_allowed = True

    @abstractmethod
    def check_api_key(self, api_key):
        raise NotImplementedError

    @abstractmethod
    def predict(self, prompt_instance):
        raise NotImplementedError

    def count_tokens(self, messages):
        # TODO: generalize to other foundation models
        num_tokens = 0
        encoding = tiktoken.encoding_for_model(self.engine)
        for message in messages:
            if isinstance(message, str):
                len(encoding.encode(message))
            elif isinstance(message, dict):
                for key, value in message.items():
                    num_tokens += len(encoding.encode(str(value)))
                    if key == "name":
                        num_tokens += 1
            num_tokens += len(encoding.encode(str(message)))
        num_tokens += 3  # every reply is prefixed with <|start|>assistant<|message|>
        return num_tokens

    def check_token_limit(self, messages):
        if self.token_limit is not None:
            total_tokens = self.count_tokens(messages)
            if total_tokens > self.token_limit:
                raise ValueError(f"Token limit exceeded: {total_tokens} tokens in input, limit is {self.token_limit}")


def call_ai_function(function: str, args: list, description: str, foundation_model=None) -> str:
    """Call an AI function
    This is a magic function that can do anything with no-code. See
    https://github.com/Torantulino/AI-Functions for more info.
    Args:
        function (str): The function to call
        args (list): The arguments to pass to the function
        description (str): The description of the function
        model (str, optional): The model to use. Defaults to None.
    Returns:
        str: The response from the function
    """

    # For each arg, if any are None, convert to "None":
    args = [str(arg) if arg is not None else "None" for arg in args]
    # parse args to comma separated string
    args = ", ".join(args)
    messages = [
        {
            "role": "system",
            "content": f"You are now the following python function: ```# {description}"
            f"\n{function}```\n\nOnly respond with your `return` value.",
        },
        {"role": "user", "content": args},
    ]

    return foundation_model.predict(messages)


def retry(
    func,
    max_retries=3,
    retry_factor=2,
    retry_min_timeout=1000,
    retry_max_timeout=10000,
    allowed_exceptions=(ConnectionError, RateLimitError),
):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        retries = max_retries
        while retries > 0:
            try:
                return func(self, *args, **kwargs)
            # except allowed_exceptions as e:
            except Exception as e:
                print(e)
                if retries == 1:
                    raise e
                timeout = min(retry_max_timeout, retry_min_timeout * (retry_factor ** (max_retries - retries)))
                time.sleep(timeout / 1000)
                retries -= 1

    return wrapper
