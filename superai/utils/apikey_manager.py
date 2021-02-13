import os
import warnings

from superai.config import add_secret_settings, get_config_dir, remove_secret_settings, settings
from superai.log import logger

BASE_FOLDER = get_config_dir()

log = logger.get_logger(__name__)


def _save_api_key_secrets(api_key: str, username: str = None):
    env = settings.current_env
    secret = {env: {"user": {"api_key": api_key, "username": username}}}
    add_secret_settings(secret)
    log.info(f"Api key added to env {env}")


def save_api_key(api_key: str, username: str = None):
    _save_api_key_secrets(api_key, username=username)


def load_api_key() -> str:
    # First load from env variable
    api_key = settings.get("user", {}).get("api_key")

    if not api_key:
        warnings.warn("Api key is not initialized. Run superai login --username <email> to retrieve your api key")

    return api_key


def remove_api_key():
    env = settings.current_env
    remove_secret_settings(f"{env}__user__api_key")
    remove_secret_settings(f"{env}__user__username")
    log.debug(f"Api key deleted from env {env}")
