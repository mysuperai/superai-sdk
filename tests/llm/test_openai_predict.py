from superai.llm.foundation_models.openai import ChatGPT


def return_mock(filtered_params, token_count):
    if filtered_params.get("presence_penalty", 0) == 1:
        return {"choices": [{"finish_reason": "stop", "message": {"content": "penalty"}}]}
    else:
        return {"choices": [{"finish_reason": "length", "message": {"content": "no penalty"}}]}


def test_stop_criterion():
    model = ChatGPT()
    model._openai_call = return_mock
    assert model.predict("test") == "penalty"
