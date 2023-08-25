import json
import os
import shutil
from pathlib import Path
from unittest.mock import patch

import boto3
import pytest
from moto import mock_s3

from superai import settings
from superai.meta_ai import AI, BaseAI
from superai.meta_ai.ai_helper import PREDICTION_METRICS_JSON, load_and_predict
from superai.meta_ai.parameters import Config
from superai.meta_ai.schema import Schema, TaskBatchInput, TaskElement, TaskInput


@pytest.fixture(scope="function")
def clean():
    # clean before
    if os.path.exists(".AISave"):
        shutil.rmtree(".AISave")
    yield
    # clean after
    if os.path.exists(".AISave"):
        shutil.rmtree(".AISave")


@pytest.fixture(scope="function")
def aws_credentials(monkeypatch):
    """Mocked AWS Credentials for moto."""
    monkeypatch.setenv("AWS_ACCESS_KEY_ID", "testing")
    monkeypatch.setenv("AWS_SECRET_ACCESS_KEY", "testing")
    monkeypatch.setenv("AWS_SECURITY_TOKEN", "testing")
    monkeypatch.setenv("AWS_SESSION_TOKEN", "testing")


@pytest.fixture(scope="function")
def s3(aws_credentials):
    with mock_s3():
        yield boto3.client("s3", region_name="us-east-1")


@pytest.fixture(scope="function")
def bucket(s3: boto3.client):
    s3.create_bucket(
        Bucket=settings["meta_ai_bucket"],
    )


@pytest.fixture(scope="function")
def local_ai(clean, bucket) -> AI:
    model_path = Path(__file__).parent / "fixtures" / "model"
    ai = AI(
        input_schema=Schema(),
        output_schema=Schema(),
        configuration=Config(),
        description="Template for my dummy template used for testing",
        model_class="DummyAI",
        model_class_path=str(model_path.absolute()),
        name="pytest_test_model",
        version="1.0",
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
    single_predict_check(local_ai, inputs)
    ti = TaskInput.parse_obj(inputs)
    single_predict_check(local_ai, ti)


def single_predict_check(local_ai, inputs):
    result = local_ai.predict(inputs=inputs)
    assert result
    assert result[0]["prediction"]
    assert result[0]["score"]

    return result


def test_predict_batch(local_ai):
    inputs = [
        TaskElement(type="text", value="test"),
        TaskElement(type="text", value="test"),
    ]
    batch_predict_test(local_ai, inputs)
    ti = TaskInput.parse_obj(inputs)
    ti_batch = TaskBatchInput.parse_obj([ti, ti])
    batch_predict_test(local_ai, ti_batch)


def batch_predict_test(local_ai, inputs):
    result = local_ai.predict_batch(inputs=inputs)
    assert result
    # We unpack two lists
    # One list for each prediction in batch
    # One list for each instance in prediction
    assert result[0][0]["prediction"]
    assert result[0][0]["score"]
    assert result[1][0]["prediction"]
    assert result[1][0]["score"]

    return result


def test_load_and_predict(local_ai, tmp_path: Path, monkeypatch):
    """
    Tests that we can load and predict an existing stored model (in .AISave folder) without relying on any local source code files
    Args:
        local_ai: preinitialized AI object which was stored in .AISave folder
        tmp_path: tmp path for this test

    """
    absolute_location = Path(local_ai._save_local(tmp_path)).absolute()
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
    absolute_location = Path(local_ai._save_local(tmp_path)).absolute()
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


def test_remove_patch_from_yaml():
    sample_dict = {"name": "some_name"}
    assert AI._remove_patch_from_version(sample_dict) == sample_dict, "No version in dict"
    dict_with_version = {"name": "some_name", "version": "1.0"}
    assert AI._remove_patch_from_version(dict_with_version) == dict_with_version, "No patch to remove"
    dict_with_patch = {"name": "some_name", "version": "1.0.0"}
    assert AI._remove_patch_from_version(dict_with_patch) != dict_with_patch, "Dictionary will be changed"
    assert AI._remove_patch_from_version(dict_with_patch) == {"name": "some_name", "version": "1.0"}


class TestBaseAI:
    class TestAI(BaseAI):
        def load_weights(self, weights_path: str):
            pass

        def train(self, *args, **kwargs):
            pass

        def predict(self, data):
            return {"result": True}

    def test_wrapped_prediction(self):
        # Mocking logger
        with patch("superai.meta_ai.base.base_ai.log") as mock_log:
            # Create instance
            test_ai = self.TestAI()

            # Inputs
            data = {"test_key": "test_value"}
            meta = {"puid": "test_puid", "tags": "test_tags"}
            inputs = {"data": data, "meta": meta}

            # Call the wrapped prediction function
            result = test_ai.predict(inputs)

            # Assertions
            assert result["data"] == {"result": True}
            assert result["meta"] == meta

            # Check that log.info has been called with the correct arguments
            mock_log.info.assert_any_call("Received prediction request for prediction_uuid=test_puid")
            mock_log.info.assert_any_call("Received tags=test_tags")

    class TestAIException(TestAI):
        def predict(self, data):
            raise Exception("Test exception")

    def test_wrapped_prediction_exception(self):
        # Create instance
        test_ai = self.TestAIException()

        # Inputs
        data = {"test_key": "test_value"}
        meta = {"puid": "test_puid", "tags": "test_tags"}
        inputs = {"data": data, "meta": meta}

        # Call the wrapped prediction function
        result = test_ai.predict(inputs)

        # Assertions
        assert result["meta"] == meta
        assert "exception" in result
        assert "Test exception" in result["exception"]


def test_s3_path_ai(clean, bucket, s3) -> AI:
    model_path = Path(__file__).parent / "fixtures" / "model"
    ai = AI(
        input_schema=Schema(),
        output_schema=Schema(),
        configuration=Config(),
        description="Template for my dummy template used for testing",
        model_class="DummyAI",
        model_class_path=str(model_path.absolute()),
        name="pytest_test_model",
        version="1.0",
        weights_path="s3://test-bucket/weights",
    )
    assert ai.weights_path == "s3://test-bucket/weights"
