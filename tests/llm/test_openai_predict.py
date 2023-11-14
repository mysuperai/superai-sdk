import datetime
from unittest.mock import Mock, patch

from openai.error import RateLimitError, ServiceUnavailableError
from pytest import raises

from superai.data_program.protocol.rate_limit import cache
from superai.llm.foundation_models.openai import MAX_ERRORS, ChatGPT
from tests.llm.helpers import OpenAIMockResponse, patch_chatgpt_settings


def return_mock(second_finish_reason):
    def helper(filtered_params):
        if filtered_params.get("frequency_penalty", 0) == 1.0:
            return {"choices": [{"finish_reason": "stop", "message": {"content": "penalty 1"}}]}, None, 0
        elif filtered_params.get("frequency_penalty", 0) == 0.5:
            return (
                {"choices": [{"finish_reason": second_finish_reason, "message": {"content": "penalty 0.5"}}]},
                None,
                0,
            )
        else:
            return {"choices": [{"finish_reason": "length", "message": {"content": "no penalty"}}]}, None, 0

    return helper


@patch("superai.llm.foundation_models.openai.get_wait_time", return_value=0)
@patch_chatgpt_settings
def test_stop_criterion(*args, **kwargs):
    model = ChatGPT()
    model._openai_call = return_mock("length")
    assert model.predict("test") == "penalty 1"
    model._openai_call = return_mock("stop")
    assert model.predict("test") == "penalty 0.5"


@patch("superai.llm.foundation_models.openai.get_wait_time", return_value=0)
@patch_chatgpt_settings
def test_select_model_priority(*args, **kwargs):
    with patch("openai.ChatCompletion.create") as chat_mock:
        chat_mock.return_value = OpenAIMockResponse(
            {"choices": [{"finish_reason": "length", "message": {"content": "smart response"}}]}
        )

        model = ChatGPT()
        model.predict("smart question")
        assert chat_mock.call_args.kwargs["api_base"] == "https://superai-openai-dev-eu2.openai.azure.com/"


@patch("superai.llm.foundation_models.openai.get_wait_time")
@patch("time.sleep")
@patch("openai.ChatCompletion.create")
@patch_chatgpt_settings
def test_select_model_wait_time(chat_mock, sleep_mock, get_wait_time_mock, **kwargs):
    def get_time_mock(entity, *argc, **kwargs):
        return 60 if "mock2" in entity else 0

    get_wait_time_mock.side_effect = get_time_mock
    chat_mock.return_value = OpenAIMockResponse(
        {"choices": [{"finish_reason": "stop", "message": {"content": "smart response"}}]}
    )
    model = ChatGPT()
    model.predict("smart question")

    # first model is called because of the priority model is overloaded
    assert chat_mock.call_args.kwargs["api_base"] == "https://superai-openai-dev-eu1.openai.azure.com/"
    sleep_mock.assert_not_called()


@patch("superai.llm.foundation_models.openai.get_wait_time", return_value=0)
@patch("time.sleep")
@patch("openai.ChatCompletion.create")
@patch_chatgpt_settings
def test_select_model_using_errors(chat_mock, *args, **kwargs):
    chat_mock.side_effect = [
        ServiceUnavailableError(),
        OpenAIMockResponse({"choices": [{"finish_reason": "stop", "message": {"content": "smart response"}}]}),
    ]
    model = ChatGPT()
    model.predict("smart question")

    # start with the second model because of priority
    assert chat_mock.mock_calls[0].kwargs["api_base"] == "https://superai-openai-dev-eu2.openai.azure.com/"

    # after the first error switch to the first model
    assert chat_mock.mock_calls[1].kwargs["api_base"] == "https://superai-openai-dev-eu1.openai.azure.com/"


@patch("superai.llm.foundation_models.openai.get_wait_time", return_value=0)
@patch("time.sleep")
@patch("openai.ChatCompletion.create")
@patch_chatgpt_settings
def test_exit_after_max_recoverable_error_tries(chat_mock, *args, **kwargs):
    chat_mock.side_effect = ServiceUnavailableError()
    model = ChatGPT()
    with raises(ServiceUnavailableError):
        model.predict("smart question")

    assert len(chat_mock.mock_calls) == 2 * MAX_ERRORS


@patch("superai.llm.foundation_models.openai.get_wait_time", return_value=0)
@patch("time.sleep")
@patch("openai.ChatCompletion.create")
@patch_chatgpt_settings
def test_exit_after_first_unknown_error(chat_mock, *args, **kwargs):
    chat_mock.side_effect = ValueError()
    model = ChatGPT()
    with raises(ValueError):
        model.predict("smart question")

    assert len(chat_mock.mock_calls) == 1


@patch("superai.llm.foundation_models.openai.get_wait_time", return_value=0)
@patch("time.sleep")
@patch("openai.ChatCompletion.create")
@patch_chatgpt_settings
def test_run_frequency_penalties(chat_mock, *args, **kwargs):
    chat_mock.return_value = OpenAIMockResponse(
        {"choices": [{"finish_reason": "length", "message": {"content": "smart response"}}]}
    )
    model = ChatGPT()
    prediction = model.predict("smart question")

    assert prediction == "smart response"
    # we have three different frequency penalties to try
    assert len(chat_mock.mock_calls) == 3


@patch("superai.data_program.protocol.rate_limit.datetime")
@patch("superai.llm.foundation_models.openai.time")
@patch("openai.ChatCompletion.create")
@patch_chatgpt_settings
def test_wait_time_from_api(chat_mock, time_mock, datetime_mock, **kwargs):
    cache.clear()
    # Fixes time, to make tests consistent
    datetime_mock.datetime.now = Mock(return_value=datetime.datetime(2023, 2, 26, 0, 10, 0, 0))
    datetime_mock.timedelta = datetime.timedelta

    # this is an intentionally incorrect implementation of sleep - it always waits one minute
    def inc_time(*args):
        now = datetime_mock.datetime.now()
        datetime_mock.datetime.now = Mock(return_value=datetime.datetime(2023, 2, 26, 0, now.minute + 1, 0, 0))

    rate_limit_exception = RateLimitError()
    rate_limit_exception.headers = {
        "x-ratelimit-reset-requests": "30s",
    }
    chat_mock.side_effect = [
        rate_limit_exception,
        rate_limit_exception,
        OpenAIMockResponse({"choices": [{"finish_reason": "stop", "message": {"content": "smart response"}}]}),
    ]

    time_mock.sleep = Mock(side_effect=inc_time)

    model = ChatGPT()
    model.predict("smart question")

    # we waited one minute > 30s
    assert len(time_mock.sleep.mock_calls) == 1


@patch("boto3.client")
def test_load_aws_secrets(boto_session_mock):
    import superai.llm.foundation_models.openai as myopenai

    mock_client = Mock()
    old_format = '{"llm":{"gpt-35-turbo": {"api_type": "azure", "completion_model_engine": "gpt-35-turbo"}}}'
    mock_client.get_secret_value.return_value = {"SecretString": old_format}
    boto_session_mock.return_value = mock_client
    myopenai.settings = {}
    myopenai.load_params_from_aws_secrets()
    assert type(myopenai.settings["llm"]["gpt-35-turbo"]) == list
    assert "priority" in myopenai.settings["llm"]["gpt-35-turbo"][0]
    assert "token_limit" in myopenai.settings["llm"]["gpt-35-turbo"][0]

    mock_client = Mock()
    new_format = (
        '{"llm":{"gpt-35-turbo": [{"api_type": "azure", "completion_model_engine": "gpt-35-turbo", "priority": 1}]}}'
    )
    mock_client.get_secret_value.return_value = {"SecretString": new_format}
    boto_session_mock.return_value = mock_client
    myopenai.settings = {}
    myopenai.load_params_from_aws_secrets()
    assert type(myopenai.settings["llm"]["gpt-35-turbo"]) == list
    assert "priority" in myopenai.settings["llm"]["gpt-35-turbo"][0]

    # Testing compatibility with legacy contents
    mock_client = Mock()
    new_format = '{"llm":{"chatgpt": {}}}'
    mock_client.get_secret_value.return_value = {"SecretString": new_format}
    boto_session_mock.return_value = mock_client
    myopenai.settings = {}
    myopenai.load_params_from_aws_secrets()
    assert myopenai.settings["llm"]["chatgpt"] == [{}]
