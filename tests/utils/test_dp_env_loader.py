import json

import boto3
import pytest
from moto import mock_secretsmanager

from superai.utils.dp_env_loader import _retrieve_secret, transform_key


@pytest.fixture(scope="function")
def secrets_client():
    with mock_secretsmanager():
        yield boto3.client("secretsmanager")


def test_retrieve_secret(secrets_client, mocker):
    secret_value = {"foo": "bar", "baz": "qux"}
    secret_name = "dataprograms-env-test-secret"
    secrets_client.create_secret(Name=secret_name, SecretString=json.dumps(secret_value))
    boto3 = mocker.patch("superai.utils.dp_env_loader.boto3", autospec=True)
    boto3.client.return_value = secrets_client
    secret = _retrieve_secret("test")
    assert secret == secret_value


def test_retrieve_secret_error(secrets_client, mocker):
    boto3 = mocker.patch("superai.utils.dp_env_loader.boto3", autospec=True)
    boto3.client.return_value = secrets_client

    with pytest.raises(Exception):
        _retrieve_secret("test2")


def test_transform_key():
    assert transform_key("SUPERAI_FOO__BAR") == "foo.bar"
    assert transform_key("SUPERAI_BAZ") == "baz"
