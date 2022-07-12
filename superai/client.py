from typing import Optional

import requests

from superai.apis.auth import AuthApiMixin
from superai.apis.data import DataApiMixin
from superai.apis.data_program import DataProgramApiMixin
from superai.apis.ground_truth import GroundTruthApiMixin
from superai.apis.jobs import JobsApiMixin
from superai.apis.meta_ai import AiApiMixin
from superai.apis.project import ProjectApiMixin
from superai.apis.tasks import TasksApiMixin
from superai.config import settings
from superai.exceptions import (
    SuperAIAuthorizationError,
    SuperAIEntityDuplicatedError,
    SuperAIError,
)
from superai.log import logger
from superai.utils import update_cognito_credentials

BASE_URL = settings.get("base_url")

# Set up logging
logger = logger.get_logger(__name__)


class Client(
    JobsApiMixin,
    AuthApiMixin,
    GroundTruthApiMixin,
    DataApiMixin,
    DataProgramApiMixin,
    ProjectApiMixin,
    AiApiMixin,
    TasksApiMixin,
):
    def __init__(self, api_key: str = None, auth_token: str = None, id_token: str = None, base_url: str = None):
        super(Client, self).__init__()
        self.api_key = api_key
        self.auth_token = auth_token
        self.id_token = id_token
        if base_url is None:
            self.base_url = BASE_URL
        else:
            self.base_url = base_url

    def request(
        self,
        endpoint: str,
        method: str = "GET",
        query_params: dict = None,
        body_params: dict = None,
        required_api_key: bool = False,
        required_auth_token: bool = False,
        required_id_token: bool = False,
    ) -> Optional[dict]:
        headers = {}
        if required_api_key:
            if not self.api_key:
                logger.warning("API key is required, but not present")
            headers["API-KEY"] = self.api_key
        if required_auth_token:
            if not self.auth_token:
                logger.warning("AUTH token is required, but not present")
            headers["AUTH-TOKEN"] = self.auth_token
        if required_id_token:
            if not self.id_token:
                logger.warning("ID token is required, but not present")
            headers["ID-TOKEN"] = self.id_token

        resp = requests.request(
            method, f"{self.base_url}/{endpoint}", params=query_params, json=body_params, headers=headers
        )
        try:
            resp.raise_for_status()
            if resp.status_code == 204:
                return None
            else:
                return resp.json()
        except requests.exceptions.HTTPError as http_e:
            try:
                message = http_e.response.json()["message"]
            except:
                message = http_e.response.text

            if http_e.response.status_code == 401:
                # In this case the token is expired but the refresh token
                # might still be valid. Check and update the secrets.
                if message == "Token is expired.":
                    # Set the class variables with the new tokens.
                    self.auth_token, self.id_token = update_cognito_credentials()
                    # Retry the request.
                    return self.request(
                        endpoint,
                        method,
                        query_params,
                        body_params,
                        required_api_key,
                        required_auth_token,
                        required_id_token,
                    )
                else:
                    # In this case, it is actually an authorization error and
                    # the token is not valid.
                    raise SuperAIAuthorizationError(
                        message, http_e.response.status_code, endpoint=f"{self.base_url}/{endpoint}"
                    )
            elif http_e.response.status_code == 409:
                raise SuperAIEntityDuplicatedError(
                    message, http_e.response.status_code, base_url=self.base_url, endpoint=endpoint
                )
            raise SuperAIError(message, http_e.response.status_code)
