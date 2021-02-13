import configparser
import os

import yaml

from superai.config import add_secret_settings, ensure_path_exists, get_config_dir, remove_secret_settings, settings
from superai.log import logger

BASE_FOLDER = get_config_dir()

log = logger.get_logger(__name__)

_default_aws_config_path = "~/.aws/config"
_default_aws_credentials_path = "~/.aws/credentials"


def _write_config_file(aws_credentials: dict, config_path: str = None):
    config_path = config_path or os.path.expanduser(_default_aws_config_path)
    ensure_path_exists(config_path, only_dir=False)

    # parse existing aws config
    config = configparser.ConfigParser()
    config.read(config_path)
    if not config.has_section("profile superai"):
        config.add_section("profile superai")

    config.set("profile superai", "region", "us-east-1")
    config.set("profile superai", "output", "json")

    # save to a file
    with open(config_path, "w") as configfile:
        config.write(configfile)


def _write_credentials_file(aws_credentials: dict):
    credentials_path = os.path.expanduser(_default_aws_credentials_path)
    ensure_path_exists(credentials_path, only_dir=False)

    # parse existing aws config
    config = configparser.ConfigParser()
    config.read(credentials_path)
    if not config.has_section("superai"):
        config.add_section("superai")

    config.set("superai", "aws_access_key_id", aws_credentials.get("AccessKeyId"))
    config.set("superai", "aws_secret_access_key", aws_credentials.get("SecretKey"))
    config.set("superai", "aws_session_token", aws_credentials.get("SessionToken"))

    # save to a file
    with open(credentials_path, "w") as configfile:
        config.write(configfile)


def _aws_configure(aws_credentials):
    _write_config_file(aws_credentials)
    _write_credentials_file(aws_credentials)


def _save_secrets(aws_credentials: dict):
    env = settings.current_env
    secret = {env: {"user": {"aws": aws_credentials}}}
    add_secret_settings(secret)
    log.info(f"AWS Credentials key added to env {env}")


def save_aws_credentials(aws_credentials: dict):
    aws_credentials = yaml.safe_load(aws_credentials) if isinstance(aws_credentials, str) else aws_credentials
    _save_secrets(aws_credentials)
    _aws_configure(aws_credentials)


def remove_aws_credentials():
    env = settings.current_env
    remove_secret_settings(f"{env}__user__aws")
    log.debug(f"AWS Credentials deleted from env {env}")
