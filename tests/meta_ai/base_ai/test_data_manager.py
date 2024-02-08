import json
from unittest.mock import Mock, patch

import pytest

from superai.meta_ai.base.data_manager import DataManager


@pytest.fixture
def data_manager():
    with patch("superai.meta_ai.base.data_manager.Client") as MockClient:
        mock_client = MockClient.return_value
        mock_client.get_signed_url.return_value = {"signedUrl": "dummy_signed_url"}
        resolver = DataManager(task_id=123)
        resolver.client = mock_client
        return resolver


@pytest.mark.parametrize(
    "input_data,expected_output",
    [
        ("some_non_url_string", "some_non_url_string"),
        ({"key": "data://123/test"}, {"key": "dummy_signed_url"}),
        ({"key": "https://normal_url"}, {"key": "https://normal_url"}),
        # pass list of dicts
        (
            [
                {"key": "data://123/test"},
                {"key": "data://123/test"},
            ],
            [
                {"key": "dummy_signed_url"},
                {"key": "dummy_signed_url"},
            ],
        ),
        # pass string encoded dict
        (
            json.dumps({"key": "data://123/test"}),
            json.dumps({"key": "dummy_signed_url"}),
        ),
    ],
)
def test_sign_all_urls(data_manager, input_data, expected_output):
    result = DataManager.sign_all_urls(input_data, DataManager.data_regex, data_manager.signer_func)
    assert result == expected_output


def test_sign_all_urls_json_error(data_manager):
    data = DataManager.sign_all_urls("data://123/test", DataManager.data_regex, data_manager.signer_func)
    assert data == "data://123/test"


def test_resolve_ref(data_manager):
    payload = {"key": "value"}
    response = Mock()
    response.json.return_value = payload
    data_manager.client.download_data.return_value = response
    result = data_manager.download_payload(
        {
            "data": {"input": {"ref": "data://123/test"}, "output": {"ref": "data://123/test"}},
            "upload_url": "http://123",
        }
    )
    assert result == {
        "data": payload,
        "upload_url": "http://123",
        "parameters": {"output_schema": payload},
    }


def test_preprocess_input(data_manager):
    # preprocessor should handle case where input subkey and output subkey contain `ref` and should resolve them, too.
    response = Mock()
    response.json.return_value = {"key": "value"}
    data_manager.client.download_data.return_value = response
    result = data_manager.preprocess_input(
        {
            "data": {"input": {"ref": "data://123/test"}, "output": {"ref": "data://123/test"}},
            "upload_url": "http://123",
        },
        auto_resolve_data=True,
    )
    assert result == {
        "data": {"key": "value"},
        "upload_url": "http://123",
        "parameters": {"output_schema": {"key": "value"}},
    }
