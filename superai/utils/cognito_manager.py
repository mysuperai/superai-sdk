import warnings

from superai.config import add_secret_settings, get_config_dir, remove_secret_settings, settings
from superai.log import logger

BASE_FOLDER = get_config_dir()

log = logger.get_logger(__name__)


def save_cognito_user(authenitcated_user: dict):
    env = settings.current_env
    cognito = {
        "id_token": authenitcated_user.id_token,
        "access_token": authenitcated_user.access_token,
        "refresh_token": authenitcated_user.refresh_token,
    }
    secret = {env: {"user": {"cognito": cognito}}}
    add_secret_settings(secret)
    log.info(f"Cognito credentials added to env {env}")


def load_auth_token() -> str:
    token = settings.get("user", {}).get("cognito", {}).get("access_token")

    if not token:
        warnings.warn("User access token is not initialized. Run superai login --username <email>")

    return token


def load_id_token() -> str:
    token = settings.get("user", {}).get("cognito", {}).get("access_token")

    if not token:
        warnings.warn("User id token is not initialized. Run superai login --username <email>")

    return token


def remove_cognito_user():
    env = settings.current_env
    remove_secret_settings(f"{env}__user__cognito")
    log.debug(f"Cognito tokens deleted from env {env}")
