import configparser
from pathlib import Path

import pytest

from superai.utils import save_aws_credentials
from superai.utils.aws_credentials_manager import _default_aws_config_path, _default_aws_credentials_path
from ..test_config import cleanup_tmp, create_tmp_file


@pytest.fixture()
def with_empty_config_file():
    ppath = Path(_default_aws_config_path).expanduser().absolute()
    tmp = create_tmp_file(ppath)
    yield str(ppath.absolute())
    cleanup_tmp(tmp, ppath)


@pytest.fixture()
def with_empty_credentials_file():
    ppath = Path(_default_aws_credentials_path).expanduser().absolute()
    tmp = create_tmp_file(ppath)
    yield str(ppath.absolute())
    cleanup_tmp(tmp, ppath)


@pytest.fixture()
def with_fake_credentials():
    """
    :return: Credentials payload
    """
    yield '{"AccessKeyId": "FAKE_ACCESS_KEY_ID", "SecretKey": "FAKE_SECRET_KEY", "SessionToken": "FAKE_SESSION_TOKEN","Expiration": "2021-02-02 15:41:11+01:00"}'


def test_save_credentials_creates_config(with_fake_credentials, with_empty_config_file, with_empty_credentials_file):
    save_aws_credentials(with_fake_credentials)
    config = configparser.ConfigParser()
    config.read(with_empty_config_file)
    assert config.has_section("profile superai")
    assert config.get("profile superai", "region") == "us-east-1"
    assert config.get("profile superai", "output") == "json"


def test_save_credentials_creates_credentials(
    with_fake_credentials, with_empty_config_file, with_empty_credentials_file
):
    save_aws_credentials(with_fake_credentials)
    config = configparser.ConfigParser()
    config.read(with_empty_credentials_file)
    assert config.has_section("superai")
    assert config.get("superai", "aws_access_key_id") == "FAKE_ACCESS_KEY_ID"
    assert config.get("superai", "aws_secret_access_key") == "FAKE_SECRET_KEY"
    assert config.get("superai", "aws_session_token") == "FAKE_SESSION_TOKEN"


def test_save_credentials_overrides_only_superai_config(
    with_fake_credentials, with_empty_config_file, with_empty_credentials_file
):
    config = configparser.ConfigParser()
    config.add_section("default")
    config.set("default", "region", "my_region")
    # save to a file
    with open(with_empty_config_file, "w") as configfile:
        config.write(configfile)
    save_aws_credentials(with_fake_credentials)
    config_after = configparser.ConfigParser()
    config_after.read(with_empty_config_file)
    assert config_after.get("default", "region") == "my_region"


def test_remove_credentials_only_removes_user_aws(
    with_fake_credentials, with_empty_config_file, with_empty_credentials_file
):
    config = configparser.ConfigParser()
    config.add_section("default")
    config.set("default", "aws_key", "my_key1")
    # save to a file
    with open(with_empty_credentials_file, "w") as configfile:
        config.write(configfile)
    save_aws_credentials(with_fake_credentials)
    config_after = configparser.ConfigParser()
    config_after.read(with_empty_credentials_file)
    assert config_after.get("default", "aws_key") == "my_key1"
