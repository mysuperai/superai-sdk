import datetime
from unittest.mock import Mock, patch

import httpx
from openai import InternalServerError, RateLimitError
from openai.types.chat.chat_completion_chunk import ChatCompletionChunk
from pytest import raises

from superai.llm.foundation_models.openai import MAX_ERRORS, ChatGPT, cache
from tests.llm.helpers import OpenAIMockResponse, patch_chatgpt_settings


def return_mock(second_finish_reason):
    def helper(filtered_params, best_model_idx, stream):
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


def return_mock_for_token_limitation(finish_reason):
    def helper(filtered_params, best_model_idx, stream):
        if filtered_params.get("max_tokens", 0) < 5:
            return {"choices": [{"finish_reason": finish_reason, "message": {"content": "restricted"}}]}, None, 0
        else:
            return {"choices": [{"finish_reason": "stop", "message": {"content": "relaxed"}}]}, None, 0

    return helper


@patch("superai.llm.foundation_models.openai.AzureOpenAIModelEndpoint.get_wait_time", return_value=0)
@patch_chatgpt_settings
def test_restrictive_token_limits(*args, **kwargs):
    model = ChatGPT()
    # The first call will limit to 1 token. We expect that in the second call the
    # token limit is relaxed
    model._openai_call = return_mock_for_token_limitation("length")
    assert model.predict("test") == "relaxed"
    # The first call will limit to 1 token. If we generate successfully we will not call
    # again
    model._openai_call = return_mock_for_token_limitation("stop")
    assert model.predict("test") == "restricted"


@patch("superai.llm.foundation_models.openai.AzureOpenAIModelEndpoint.get_wait_time", return_value=0)
@patch_chatgpt_settings
def test_stop_criterion(*args, **kwargs):
    model = ChatGPT()
    model._openai_call = return_mock("length")
    assert model.predict("test") == "penalty 1"
    model._openai_call = return_mock("stop")
    assert model.predict("test") == "penalty 0.5"


@patch("superai.llm.foundation_models.openai.AzureOpenAIModelEndpoint.get_wait_time", return_value=0)
@patch_chatgpt_settings
def test_select_model_priority(*args, **kwargs):
    with patch("superai.llm.foundation_models.openai.ChatGPT._openai_call") as chat_mock:
        response = {"choices": [{"finish_reason": "stop", "message": {"content": "smart response"}}]}
        chat_mock.return_value = response, None, 0

        model = ChatGPT()
        model.predict("smart question")
        model_id = str(model.model_endpoints[chat_mock.call_args_list[0].args[1]].id)
        assert model_id == "mock2"


@patch("superai.llm.foundation_models.openai.AzureOpenAIModelEndpoint.get_wait_time")
@patch("time.sleep")
@patch("superai.llm.foundation_models.openai.ChatGPT._openai_call")
@patch_chatgpt_settings
def test_select_model_wait_time(chat_mock, sleep_mock, get_wait_time_mock, **kwargs):
    get_wait_time_mock.side_effect = [0, 60]
    response = {"choices": [{"finish_reason": "stop", "message": {"content": "smart response"}}]}
    chat_mock.return_value = response, None, 0
    model = ChatGPT()
    model.predict("smart question")

    # first model is called because of the priority model is overloaded
    model_id = str(model.model_endpoints[chat_mock.call_args_list[0].args[1]].id)
    assert model_id == "mock1"
    sleep_mock.assert_not_called()


@patch("superai.llm.foundation_models.openai.AzureOpenAIModelEndpoint.get_wait_time", return_value=0)
@patch("time.sleep")
# @patch("openai.resources.chat.completions.Completions.create")
@patch("superai.llm.foundation_models.openai.ChatGPT._openai_call")
@patch_chatgpt_settings
def test_select_model_using_errors(chat_mock, *args, **kwargs):
    response = Mock(spec=httpx.Response)
    response.status_code = 502
    error = InternalServerError(message="IE", body=None, response=response)
    chat_mock.side_effect = [
        (None, error, 0),
        (
            OpenAIMockResponse({"choices": [{"finish_reason": "stop", "message": {"content": "smart response"}}]}),
            None,
            0,
        ),
    ]
    model = ChatGPT()
    model.predict("smart question")

    # start with the second model because of priority
    model_id = str(model.model_endpoints[chat_mock.call_args_list[0].args[1]].id)
    assert model_id == "mock2"

    # after the first error switch to the first model
    model_id = str(model.model_endpoints[chat_mock.call_args_list[1].args[1]].id)
    assert model_id == "mock1"


@patch("superai.llm.foundation_models.openai.AzureOpenAIModelEndpoint.get_wait_time", return_value=0)
@patch("time.sleep")
@patch("openai.resources.chat.completions.Completions.create")
@patch_chatgpt_settings
def test_exit_after_max_recoverable_error_tries(chat_mock, *args, **kwargs):
    response = Mock(spec=httpx.Response)
    response.status_code = 502
    chat_mock.side_effect = InternalServerError(message="IE", body=None, response=response)
    model = ChatGPT()
    with raises(InternalServerError):
        model.predict("smart question")

    assert len(chat_mock.mock_calls) == 2 * MAX_ERRORS


@patch("superai.llm.foundation_models.openai.AzureOpenAIModelEndpoint.get_wait_time", return_value=0)
@patch("time.sleep")
@patch("openai.resources.chat.completions.Completions.create")
@patch_chatgpt_settings
def test_exit_after_first_unknown_error(chat_mock, *args, **kwargs):
    chat_mock.side_effect = ValueError()
    model = ChatGPT()
    with raises(ValueError):
        model.predict("smart question")

    assert len(chat_mock.mock_calls) == 1


@patch("superai.llm.foundation_models.openai.AzureOpenAIModelEndpoint.get_wait_time", return_value=0)
@patch("time.sleep")
@patch("openai.resources.chat.completions.Completions.create")
@patch_chatgpt_settings
def test_run_frequency_penalties(chat_mock, *args, **kwargs):
    chat_mock.return_value = OpenAIMockResponse(
        {"choices": [{"finish_reason": "length", "message": {"content": "smart response"}}]}
    )
    model = ChatGPT()
    prediction = model.predict("smart question", stream=False)

    assert prediction == "smart response"
    # we have three different frequency penalties to try and one try because we run with
    # a restricted max_tokens token limit.
    assert len(chat_mock.mock_calls) == 4


@patch("superai.llm.foundation_models.openai.AzureOpenAIModelEndpoint.get_wait_time", return_value=0)
@patch("time.sleep")
@patch("openai.resources.chat.completions.Completions.create")
@patch_chatgpt_settings
def test_run_no_retry_length(chat_mock, *args, **kwargs):
    chat_mock.return_value = OpenAIMockResponse(
        {"choices": [{"finish_reason": "length", "message": {"content": "smart response"}}]}
    )
    model = ChatGPT()
    prediction = model.predict("smart question", retry_on_length=False)

    assert prediction == "smart response"
    # In this case we only want to retry if we artificially lowered the maximum token
    # limit
    assert len(chat_mock.mock_calls) == 2


@patch("superai.llm.foundation_models.openai.datetime")
@patch("superai.llm.foundation_models.openai.time")
@patch("openai.resources.chat.completions.Completions.create")
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

    response = httpx.Response(status_code=428, request=Mock())
    rate_limit_exception = RateLimitError(message="Ratelimit Error", body=None, response=response)
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


@patch("openai.resources.chat.completions.Completions.create")
@patch_chatgpt_settings
def test_lower_generation_limit(chat_mock, **kwargs):
    chat_mock.return_value = OpenAIMockResponse(
        {"choices": [{"finish_reason": "stop", "message": {"content": "smart response"}}]}
    )
    # Test if restriction worked
    m = ChatGPT(openai_model="gpt-4-1106-preview")
    m.predict("Test")
    assert chat_mock.call_args[1]["max_tokens"] == 1

    # Test if max generation tokens worked
    m.predict(" ".join(80000 * ["Test"]))
    assert chat_mock.call_args[1]["max_tokens"] < 6000

    # Test if restriction to context length works
    m.predict(" ".join(126000 * ["Test"]))
    assert chat_mock.call_args[1]["max_tokens"] < 4000


@patch("openai.resources.chat.completions.Completions.create")
@patch_chatgpt_settings
def test_call_streaming_api(chat_mock, **kwargs):
    chat_mock.return_value = [
        ChatCompletionChunk(
            choices=[{"index": 1, "delta": {"content": "smart"}}],
            model="gpt-4",
            created=1233,
            id="test",
            object="chat.completion.chunk",
        ),
        ChatCompletionChunk(
            choices=[{"index": 1, "finish_reason": "stop", "delta": {"content": " choice"}}],
            model="gpt-4",
            created=1233,
            id="test",
            object="chat.completion.chunk",
        ),
    ]

    m = ChatGPT(openai_model="gpt-4-1106-preview")
    r = m.predict("Test", stream=True)
    assert r == "smart choice"
