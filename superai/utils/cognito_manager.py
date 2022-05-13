import warnings
from typing import Tuple

import boto3

from superai.config import (
    add_secret_settings,
    get_config_dir,
    remove_secret_settings,
    settings,
)
from superai.log import logger

BASE_FOLDER = get_config_dir()
COGNITO_CLIENT_ID = settings.get("cognito", {}).get("client_id")
COGNITO_REGION = settings.get("cognito", {}).get("region")

log = logger.get_logger(__name__)


def save_cognito_user(authenitcated_user: dict):
    _save_cognito_credentials(
        authenitcated_user.id_token, authenitcated_user.access_token, authenitcated_user.refresh_token
    )


def _save_cognito_credentials(id_token: str, access_token: str, refresh_token: str):
    env = settings.current_env
    cognito = {
        "id_token": id_token,
        "access_token": access_token,
        "refresh_token": refresh_token,
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
    token = settings.get("user", {}).get("cognito", {}).get("id_token")

    if not token:
        warnings.warn("User id token is not initialized. Run superai login --username <email>")

    return token


def load_refresh_token() -> str:
    token = settings.get("user", {}).get("cognito", {}).get("refresh_token")

    if not token:
        warnings.warn("User id token is not initialized. Run superai login --username <email>")

    return token


def remove_cognito_user():
    env = settings.current_env
    remove_secret_settings(f"{env}__user__cognito")
    log.debug(f"Cognito tokens deleted from env {env}")


def update_cognito_credentials() -> Tuple[str, str]:
    """
    Update cognito credentials with the following tokens:
    - access token
    - id token
    - refresh token
    :return: Tuple[str, str] Tuple with id_token and access_token
    """
    # Create the boto client as the pycognito library doesn't allow to update
    # credentials.
    cog_client = boto3.client("cognito-idp", COGNITO_REGION)

    refresh_token = load_refresh_token()
    # Initate authentication with the refresh token.
    resp_auth = cog_client.initiate_auth(
        ClientId=COGNITO_CLIENT_ID, AuthFlow="REFRESH_TOKEN_AUTH", AuthParameters={"REFRESH_TOKEN": refresh_token}
    )
    id_token = resp_auth["AuthenticationResult"]["IdToken"]
    auth_token = resp_auth["AuthenticationResult"]["AccessToken"]

    _save_cognito_credentials(id_token, auth_token, refresh_token)

    return auth_token, id_token
