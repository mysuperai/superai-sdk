from typing import BinaryIO
from unittest import mock

import pytest

from superai import settings
from superai.client import Client


@pytest.fixture(scope="module")
def client():
    yield Client()


@pytest.fixture(scope="module", autouse=True)
def set_dev_env():
    with settings.using_env("dev"):
        yield


def test_upload_ai_task_data(client, mocker):
    dummy_file_object = BinaryIO()
    dummy_file_object.write(b"test")
    dummy_file_object.seek(0)

    client.api_key = "KEY"
    request_mock = mock.MagicMock()
    client.request = request_mock
    request_mock.return_value = {"uploadUrl": "http://upload.url", "path": "data://1005/ai-task/558513/test.csv"}

    put_mock = mocker.patch("superai.apis.data.requests.put")
    put_mock.return_value.status_code = 200

    response = client.upload_ai_task_data(
        ai_task_id=558513,
        file=dummy_file_object,
        path="test.csv",
        mime_type="text/csv",
    )
    assert response
    assert "path" in response
    assert request_mock.called
    assert put_mock.called


def test_download_ai_task_data(client: Client, mocker):
    client.api_key = "KEY"

    request_mock = mock.MagicMock()
    client.request = request_mock
    request_mock.return_value = {"signedUrl": "http://download.url"}

    get_mock = mocker.patch("superai.apis.data.requests.get")
    get_mock.return_value.status_code = 200
    get_mock.return_value.json.return_value = {"test": True}

    file_content = client.download_ai_task_data(ai_task_id=558513, path="data://1005/ai-task/558513/test.json").json()
    assert file_content == {"test": True}
    assert file_content
    assert request_mock.called
    assert get_mock.called

    # Test with wrong path
    with pytest.raises(ValueError):
        client.download_ai_task_data(ai_task_id=1, path="default/test2.csv")

    # Test bytes return value
    get_mock.return_value.content = b"test"
    file_content = client.download_ai_task_data(ai_task_id=558513, path="data://1005/ai-task/558513/test.json").content
    assert file_content == b"test"

    # Test string return value
    get_mock.return_value.text = "test"
    file_content = client.download_ai_task_data(ai_task_id=558513, path="data://1005/ai-task/558513/test.json").text
    assert file_content == "test"
