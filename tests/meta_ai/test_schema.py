import pytest

from superai.meta_ai.schema import EasyPredictions


def test_general_prediction():
    pred = {"prediction": "quick brown fox", "score": 0.9}
    predictions = EasyPredictions(pred).value
    assert "prediction" in predictions
    assert predictions["prediction"] == "quick brown fox"

    assert "score" in predictions

    fancy_predictions = EasyPredictions(
        {"prediction": "quick brown fox", "score": 1.0, "other": "some fancy metadata"}
    ).value
    assert "score" in fancy_predictions and "prediction" in fancy_predictions and "other" in fancy_predictions
    assert fancy_predictions["other"] == "some fancy metadata"


def test_wrong_schema():
    with pytest.raises(ValueError) as execinfo:
        preds = EasyPredictions()
    assert str(execinfo.value) == "Unexpected type <class 'NoneType'>, needs to be a dict or list"
    with pytest.raises(AttributeError) as execinfo:
        preds = EasyPredictions({"prediction": "something"})
    assert str(execinfo.value) == "Keys `score` needs to be present and between 0 and 1"
    with pytest.raises(AttributeError) as execinfoval:
        preds = EasyPredictions({"prediction": "something", "score": 10})
    assert str(execinfoval.value) == "Keys `score` needs to be present and between 0 and 1"
    with pytest.raises(AttributeError) as execinfoval:
        preds = EasyPredictions({"prediction": "something", "score": "other"})
    assert str(execinfoval.value) == "Keys `score` needs to be present and between 0 and 1"
