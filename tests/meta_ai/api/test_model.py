from unittest.mock import Mock

import pytest

from superai import (
    Client,  # replace "your_module" and "PredictionClass" with actual values
)


def test_predict_from_endpoint_async():
    # mock the submit_prediction_request method
    submit_prediction_request_mock = Mock()
    submit_prediction_request_mock.return_value = "prediction_id"

    prediction_obj = Client()
    prediction_obj.submit_prediction_request = submit_prediction_request_mock

    # test failure when no model_id or deployment_id
    with pytest.raises(ValueError, match="Either model_id or deployment_id must be specified."):
        prediction_obj.predict_from_endpoint_async(input_data={"data": "value"})

    # test failure when no input_data
    with pytest.raises(ValueError, match="Input data must be specified."):
        prediction_obj.predict_from_endpoint_async(model_id="model_id")

    # test successful prediction submission
    prediction_id = prediction_obj.predict_from_endpoint_async(model_id="model_id", input_data={"data": "value"})
    assert prediction_id == "prediction_id"
    submit_prediction_request_mock.assert_called_once_with(
        deployment_id=None, model_id="model_id", input_data={"data": "value"}, parameters=None
    )

    # reset the mock
    submit_prediction_request_mock.reset_mock()

    # test successful prediction submission with deployment_id
    prediction_id = prediction_obj.predict_from_endpoint_async(
        deployment_id="deployment_id", input_data={"data": "value"}
    )
    assert prediction_id == "prediction_id"
    submit_prediction_request_mock.assert_called_once_with(
        deployment_id="deployment_id", model_id=None, input_data={"data": "value"}, parameters=None
    )
