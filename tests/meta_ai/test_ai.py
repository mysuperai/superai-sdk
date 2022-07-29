import json
import os
import shutil
from pathlib import Path

import pytest

from superai.meta_ai import AI, AITemplate
from superai.meta_ai.ai_helper import PREDICTION_METRICS_JSON, load_and_predict
from superai.meta_ai.parameters import Config
from superai.meta_ai.schema import Schema, TaskBatchInput, TaskElement, TaskInput


@pytest.fixture(scope="module")
def clean():
    # clean before
    if os.path.exists(".AISave"):
        shutil.rmtree(".AISave")
    yield
    # clean after
    if os.path.exists(".AISave"):
        shutil.rmtree(".AISave")


@pytest.fixture(scope="module")
def local_ai(clean):
    model_path = Path(__file__).parent / "fixtures" / "model"
    template = AITemplate(
        input_schema=Schema(),
        output_schema=Schema(),
        configuration=Config(),
        name="pytest_test_template",
        description="Template for my dummy template used for testing",
        model_class="DummyModel",
        model_class_path=str(model_path.absolute()),
    )
    ai = AI(
        ai_template=template,
        input_params=template.input_schema.parameters(),
        output_params=template.output_schema.parameters(choices=map(str, range(0, 10))),
        name="pytest_test_model",
        version=1,
    )
    yield ai


def test_predict_legacy(local_ai):
    response = local_ai.predict(inputs=[{"input": "test"}])
    assert response
    assert response[0]["prediction"]
    assert response[0]["score"]


def test_predict(local_ai):
    inputs = [
        TaskElement(type="text", value="test"),
    ]
    response = local_ai.predict(inputs=inputs)
    assert response
    assert response[0]["prediction"]
    assert response[0]["score"]

    ti = TaskInput.parse_obj(inputs)
    response = local_ai.predict(inputs=ti)
    assert response
    assert response[0]["prediction"]
    assert response[0]["score"]


def test_predict_batch(local_ai):
    inputs = [
        TaskElement(type="text", value="test"),
        TaskElement(type="text", value="test"),
    ]
    response = local_ai.predict_batch(inputs=inputs)
    assert response
    # We unpack two lists
    # One list for each prediction in batch
    # One list for each instance in prediction
    assert response[0][0]["prediction"]
    assert response[0][0]["score"]
    assert response[1][0]["prediction"]
    assert response[1][0]["score"]

    ti = TaskInput.parse_obj(inputs)
    ti_batch = TaskBatchInput.parse_obj([ti, ti])
    response = local_ai.predict_batch(inputs=ti_batch)
    assert response
    assert response[0][0]["prediction"]
    assert response[0][0]["score"]
    assert response[1][0]["prediction"]
    assert response[1][0]["score"]


def test_load_and_predict(local_ai, tmp_path: Path, monkeypatch):
    """
    Tests that we can load and predict an existing stored model (in .AISave folder) without relying on any local source code files
    Args:
        local_ai: preinitialized AI object which was stored in .AISave folder
        tmp_path: tmp path for this test

    """
    # Store absolute location of AISave folder
    absolute_location = Path(local_ai._location).absolute()
    # Change to temporary folder to ensure no relative context to AISave folder for testing
    monkeypatch.chdir(tmp_path)

    # Test with json input
    dummy_input = TaskElement(type="text", schema_instance="test")
    dummy_input = TaskInput(__root__=[dummy_input])
    result = load_and_predict(
        model_path=str(absolute_location), weights_path=local_ai.weights_path, json_input=dummy_input.json()
    )
    assert result
    assert result[0]["prediction"]

    # Test with file input
    with open(tmp_path / "input.json", "w") as f:
        f.write(dummy_input.json())
    result = load_and_predict(
        model_path=str(absolute_location), weights_path=local_ai.weights_path, data_path=tmp_path / "input.json"
    )
    assert result
    assert result[0]["prediction"]


def test_predict_dataset(local_ai, tmp_path: Path, monkeypatch):
    """
    Tests that we can load and predict an existing stored model (in .AISave folder) without relying on any local source code files
    Args:
        local_ai: preinitialized AI object which was stored in .AISave folder
        tmp_path: tmp path for this test

    """
    # Store absolute location of AISave folder
    absolute_location = Path(local_ai._location).absolute()
    # Change to temporary folder to ensure no relative context to AISave folder for testing
    monkeypatch.chdir(tmp_path)

    npz_file_path = Path(__file__).parent / "fixtures" / "dataset.npz"
    result = load_and_predict(
        model_path=str(absolute_location),
        weights_path=local_ai.weights_path,
        data_path=npz_file_path,
        metrics_output_dir=tmp_path,
    )
    assert result
    assert result[0][0]["prediction"]

    metric_file = tmp_path / PREDICTION_METRICS_JSON
    assert metric_file.exists()
    with open(metric_file, "r") as f:
        metrics = json.load(f)
    assert metrics["score"]
    assert metrics["score"] == 1.0
