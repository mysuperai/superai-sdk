import functools
from unittest.mock import patch

from dynaconf import Dynaconf


class OpenAIMockResponse:
    def __init__(self, data):
        self.data = data

    def dict(self):
        return self.data

    def __contains__(self, key):
        return key in self.data

    def __getitem__(self, key):
        if key in self.data:
            item = self.data[key]
            # If the item itself is a dictionary, return a new MockedResponse wrapping that dictionary
            if isinstance(item, dict):
                return OpenAIMockResponse(item)
            else:
                return item
        else:
            raise KeyError(key)


def patch_chatgpt_settings(func):
    mock_settings = Dynaconf()
    mock_settings.update(
        {
            "llm": {
                "gpt-35-turbo": [
                    {
                        "id": "mock1",
                        "priority": 2,
                        "rpm": 100,
                        "tpm": 1000,
                        "token_limit": 4097,
                        "api_type": "azure",
                        "api_base": "https://superai-openai-dev-eu1.openai.azure.com/",
                        "api_version": "2023-03-15-preview",
                        "api_key": "no_key",
                        "completion_model_engine": "gpt-35-turbo",
                        "embedding_model_engine": "text-embedding-ada-002",
                    },
                    {
                        "id": "mock2",
                        "priority": 1,
                        "rpm": 100,
                        "tpm": 1000,
                        "token_limit": 4097,
                        "api_type": "azure",
                        "api_base": "https://superai-openai-dev-eu2.openai.azure.com/",
                        "api_version": "2023-03-15-preview",
                        "api_key": "no_key",
                        "completion_model_engine": "gpt-35-turbo",
                        "embedding_model_engine": "text-embedding-ada-002",
                    },
                ],
                "gpt-4-1106-preview": [
                    {
                        "id": "mock3",
                        "priority": 2,
                        "rpm": 100,
                        "tpm": 1000,
                        "token_limit": 128000,
                        "max_generation_tokens": 4096,
                        "api_type": "azure",
                        "api_base": "https://superai-openai-dev-eu1.openai.azure.com/",
                        "api_version": "2023-03-15-preview",
                        "api_key": "no_key",
                        "completion_model_engine": "gpt-4-1106-preview",
                        "embedding_model_engine": "text-embedding-ada-002",
                    }
                ],
            },
        }
    )

    @functools.wraps(func)
    @patch("superai.llm.foundation_models.openai.settings", mock_settings)
    def wrapper(*args, **kwargs):
        func(*args, **kwargs, mock_settings=mock_settings)

    return wrapper
