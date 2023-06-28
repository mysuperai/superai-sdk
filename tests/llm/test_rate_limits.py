import builtins
from unittest.mock import patch

import pytest
from openai.error import RateLimitError

from superai import settings
from superai.llm.foundation_models.openai import ChatGPT


@pytest.fixture()
def chat_gpt_model():
    return ChatGPT()


def test_rate_exceeding_handling(chat_gpt_model):
    chat_gpt_model._wait_for_rate_limits = lambda x, y: True
    with patch("openai.ChatCompletion.create") as chat_mock:
        rate_limit_exception = RateLimitError(
            "Rate limit reached for default-gpt-4 in organization org-XmP3w1BcjkaTrZ6pl7SVUydH on requests per min. Limit: 200 / min. Please try again in 300ms. Contact us through our help center at help.openai.com if you continue to have issues."
        )
        rate_limit_exception.headers = {
            "Date": "Tue, 20 Jun 2023 08:45:54 GMT",
            "Content-Type": "application/json; charset=utf-8",
            "Content-Length": "353",
            "Connection": "keep-alive",
            "vary": "Origin",
            "x-ratelimit-limit-requests": "200",
            "x-ratelimit-remaining-requests": "0",
            "x-ratelimit-reset-requests": "0.65s",
            "x-request-id": "ad79a5edd513dc752cdf540c1f672939",
            "strict-transport-security": "max-age=15724800; includeSubDomains",
            "CF-Cache-Status": "DYNAMIC",
            "Server": "cloudflare",
            "CF-RAY": "7da2bd012f62baee-MXP",
            "alt-svc": 'h3=":443"; ma=86400',
        }
        chat_mock.side_effect = [
            rate_limit_exception,
            {"choices": [{"message": {"content": "The capital of Jordan is Amman"}}]},
        ]
        result = chat_gpt_model.predict("what's the capital of Jordan?")
        assert result


def test_wait_for_rate_limits(monkeypatch, chat_gpt_model):
    settings.backend = "qumes"

    # RPM call, retrial, TPM call, RPM retrial, TPM retrial
    return_iter = iter([0.5, 0, 0.1, 0, 0])
    original_import = builtins.__import__

    class MockModule:
        @staticmethod
        def compute_api_wait_time(entity, max_tpm, current_increase=1):
            return next(return_iter)

    # Redefine import, since superai transport is not installed for testing.
    def mock_import(name, globals=None, locals=None, fromlist=(), level=0):
        if name == "superai_transport.transport.rate_limit" and "compute_api_wait_time" in fromlist:
            return MockModule
        return original_import(name, globals, locals, fromlist, level)

    with patch.object(builtins, "__import__", side_effect=mock_import):
        chat_gpt_model._wait_for_rate_limits("gpt-3.5-turbo", 50)
        with pytest.raises(StopIteration):
            next(return_iter)
