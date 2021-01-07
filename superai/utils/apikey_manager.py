import os
import warnings

from superai.config import add_secret_settings, get_config_dir, settings
from superai.log import logger

BASE_FOLDER = get_config_dir()

log = logger.get_logger(__name__)

_api_key_file = os.path.expanduser(f"{BASE_FOLDER}/apikey")


def save_api_key(api_key: str):
    _save_api_key_file(api_key)
    _save_api_key_secrets(api_key)


def _save_api_key_file(api_key: str):
    if not os.path.exists(os.path.dirname(_api_key_file)):
        log.debug(f"Creating path {os.path.dirname(_api_key_file)}")
        os.makedirs(os.path.dirname(_api_key_file))
    with open(_api_key_file, "w") as f:
        f.write(api_key)


def _save_api_key_secrets(api_key: str):
    env = settings.current_env
    secret = {env: {"user": {"api_key": api_key}}}
    add_secret_settings(secret)
    log.info(f"Api key added to env {env}")


def load_api_key() -> str:
    # First load from env variable
    api_key = settings.get("user", {}).get("api_key")

    # Try to load from file (higher priority)
    try:
        with open(_api_key_file) as f:
            api_key = f.readline()
            log.debug(f"Using api_key from {_api_key_file}")
    except Exception as e:
        log.debug(
            f"Error loading api_key from file: {_api_key_file}. Using user__api_key from "
            f"{BASE_FOLDER}/.secrets.yaml?: {api_key is None}"
        )

    if not api_key:
        warnings.warn("Api key is not initialized. Run superai login --username <email> to retrieve your api key")

    return api_key
