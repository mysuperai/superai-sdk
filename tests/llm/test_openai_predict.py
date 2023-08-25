from superai.llm.foundation_models.openai import ChatGPT


def return_mock(second_finish_reason):
    def helper(filtered_params, token_count):
        if filtered_params.get("frequency_penalty", 0) == 1.0:
            return {"choices": [{"finish_reason": "stop", "message": {"content": "penalty 1"}}]}
        elif filtered_params.get("frequency_penalty", 0) == 0.5:
            return {"choices": [{"finish_reason": second_finish_reason, "message": {"content": "penalty 0.5"}}]}
        else:
            return {"choices": [{"finish_reason": "length", "message": {"content": "no penalty"}}]}

    return helper


def test_stop_criterion():
    model = ChatGPT()
    model._openai_call = return_mock("length")
    assert model.predict("test") == "penalty 1"
    model._openai_call = return_mock("stop")
    assert model.predict("test") == "penalty 0.5"
