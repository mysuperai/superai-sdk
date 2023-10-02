import functools
from unittest.mock import patch

from dynaconf import Dynaconf

mockSettings = Dynaconf()
mockSettings.update(
    {
        "llm": {
            "gpt-35-turbo": {
                "api_type": "azure",
                "api_base": "https://superai-openai-dev-eu.openai.azure.com/",
                "api_version": "2023-03-15-preview",
                "api_key": "no_key",
                "completion_model_engine": "gpt-35-turbo",
                "embedding_model_engine": "text-embedding-ada-002",
            },
        }
    }
)


def patch_chatgpt_settings(func):
    @functools.wraps(func)
    @patch("superai.llm.foundation_models.openai.settings", mockSettings)
    def wrapper(*args, **kwargs):
        func(*args, **kwargs)

    return wrapper
