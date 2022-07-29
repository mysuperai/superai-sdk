import datetime

import pytest
from pydantic import ValidationError

from superai.apis.meta_ai.meta_ai_graphql_schema import RawPrediction
from superai.meta_ai.schema import EasyPredictions, LogMetric, ManyMetric, TrainerOutput


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


def test_raw_predictions():
    pred = RawPrediction({"output": "something", "score": 0.9})
    raw_predictions = EasyPredictions(pred).value
    assert raw_predictions.score == 0.9
    assert raw_predictions.output == "something"
    assert raw_predictions["score"] == 0.9

    preds = [RawPrediction({"output": "something", "score": 0.9})]
    raw_preds_collection = EasyPredictions(preds).value
    assert raw_preds_collection


def test_wrong_schema():
    with pytest.raises(ValidationError) as execinfo:
        preds = EasyPredictions()
    with pytest.raises(ValidationError) as execinfo:
        preds = EasyPredictions({"prediction": "something"})
    with pytest.raises(ValidationError) as execinfoval:
        preds = EasyPredictions({"prediction": "something", "score": 10})
    with pytest.raises(ValidationError) as execinfoval:
        preds = EasyPredictions({"prediction": "something", "score": "other"})


def test_trainer_output_exceptions():
    with pytest.raises(ValueError) as e:
        a = TrainerOutput()
        assert str(e.value) == "One of `metric`, `metrics`or `collection`should be present"
    with pytest.raises(ValueError) as e:
        a = TrainerOutput(
            metric=dict(key="value"),
            metrics=[LogMetric(step=1, timestamp=datetime.datetime.now(), name="metric", value="something")],
        )
        assert str(e.value) == "Only one of `metric`, `metrics`or `collection`should be present, more than one provided"
    with pytest.raises(ValueError) as e:
        a = TrainerOutput(metrics=[])
        assert str(e.value) == "`metrics` should not be an empty list"
    with pytest.raises(ValueError) as e:
        a = TrainerOutput(collection=[])
        assert str(e.value) == "`collection` should not be an empty list"


def test_trainer_output():
    a = TrainerOutput(metric=dict(key="value"))
    assert a
    assert a.metric == dict(key="value")
    a = TrainerOutput(
        metrics=[LogMetric(step=1, timestamp=datetime.datetime.now(), name="metric", value="something")],
    )
    assert a
    a = TrainerOutput(collection=[ManyMetric(step=1, timestamp=datetime.datetime.now(), metrics=[("key", "value")])])
    assert a


def test_manymetrics():
    with pytest.raises(ValueError) as e:
        m = ManyMetric()
    with pytest.raises(ValueError) as e:
        m = ManyMetric(step=1, timestamp=datetime.datetime.now(), metrics=[])
        assert str(e.value) == "`metrics` should not be an empty list"
    m = ManyMetric(step=1, timestamp=datetime.datetime.now(), metrics=[("key", "value"), ("key2", "value")])
    assert m
    assert dict(m.metrics)
