import os
import warnings

from superai.config import add_secret_settings, get_config_dir, settings
from superai.log import logger

BASE_FOLDER = get_config_dir()

log = logger.get_logger(__name__)

_api_key_file = os.path.expanduser(f"{BASE_FOLDER}/apikey")


def save_api_key(api_key: str):
    _save_api_key_secrets(api_key)


def _save_api_key_secrets(api_key: str):
    env = settings.current_env
    secret = {env: {"user": {"api_key": api_key}}}
    add_secret_settings(secret)
    log.info(f"Api key added to env {env}")


def load_api_key() -> str:
    # First load from env variable
    api_key = settings.get("user", {}).get("api_key")

    if not api_key:
        warnings.warn("Api key is not initialized. Run superai login --username <email> to retrieve your api key")

    return api_key
