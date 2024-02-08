from typing import Optional

import requests

from superai.apis.auth import AuthApiMixin
from superai.apis.data import DataApiMixin
from superai.apis.data_program import DataProgramApiMixin
from superai.apis.ground_truth import GroundTruthApiMixin
from superai.apis.jobs import JobsApiMixin
from superai.apis.meta_ai import MetaAiApiMixin
from superai.apis.project import ProjectApiMixin
from superai.apis.super_task import SuperTaskApiMixin
from superai.apis.tasks import TasksApiMixin
from superai.config import settings
from superai.exceptions import (
    SuperAIAuthorizationError,
    SuperAIEntityDuplicatedError,
    SuperAIError,
)
from superai.log import logger
from superai.utils import retry, update_cognito_credentials

# Set up logging
logger = logger.get_logger(__name__)

__all__ = [
    "Client",
    "AuthApiMixin",
    "DataApiMixin",
    "DataProgramApiMixin",
    "GroundTruthApiMixin",
    "JobsApiMixin",
    "ProjectApiMixin",
    "TasksApiMixin",
    "SuperTaskApiMixin",
]


class Client(
    JobsApiMixin,
    AuthApiMixin,
    GroundTruthApiMixin,
    DataApiMixin,
    DataProgramApiMixin,
    ProjectApiMixin,
    MetaAiApiMixin,
    TasksApiMixin,
    SuperTaskApiMixin,
):
    def __init__(
        self,
        api_key: str = None,
        auth_token: str = None,
        id_token: str = None,
        base_url: str = None,
        organization_name: Optional[str] = None,
    ):
        # super(Client, self).__init__()
        self.api_key = api_key
        self.auth_token = auth_token
        self.id_token = id_token
        self.base_url = base_url or settings.get("base_url")
        self._organization_id = None
        self._organization_name = organization_name
        self._user_id = None
        from superai.apis.meta_ai.session import MetaAISession

        self.ai_session: Optional[MetaAISession] = None
        if organization_name:
            self._get_org_context(organization_name)

        super(Client, self).__init__(organization_id=self._organization_id, user_id=self._user_id)

    def _get_org_context(self, organization_name: Optional[str]):
        try:
            user = self.get_user()
            self._user_id = user.id
        except requests.exceptions.ConnectionError:
            logger.warning("Could not connect to Super.AI API. Skipping user context init.")
            return

        if not organization_name:
            return
        elif organization_name == "superai":
            self._organization_id = 1
        else:
            self._organization_id = self._get_organization_id(organization_name, user=user)
        logger.info(f"Using organisation context: {organization_name}")

    @classmethod
    def from_credentials(cls, organization_name: Optional[str] = None) -> "Client":
        """Instantiate a client from the credentials stored in the config file."""
        from superai.utils import load_api_key, load_auth_token, load_id_token

        return cls(
            api_key=load_api_key(),
            auth_token=load_auth_token(),
            id_token=load_id_token(),
            organization_name=organization_name,
        )

    @retry(exceptions=(requests.exceptions.HTTPError))
    def request(
        self,
        endpoint: str,
        method: str = "GET",
        query_params: dict = None,
        body_params: dict = None,
        required_api_key: bool = False,
        required_auth_token: bool = False,
        required_id_token: bool = False,
        header_params: Optional[dict] = None,
    ) -> Optional[dict]:
        headers = header_params or {}
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

        # Enable gzip compression
        headers["Accept-Encoding"] = "gzip"
        logger.debug(f"Requesting {method} {self.base_url}/{endpoint}, headers={headers}")
        resp = requests.request(
            method, f"{self.base_url}/{endpoint}", params=query_params, json=body_params, headers=headers
        )
        try:
            resp.raise_for_status()
            return None if resp.status_code == 204 else resp.json()
        except requests.exceptions.HTTPError as http_e:
            try:
                message = http_e.response.json()["message"]
            except Exception:
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
                        message,
                        http_e.response.status_code,
                        endpoint=f"{self.base_url}/{endpoint}",
                    ) from http_e
            elif http_e.response.status_code == 409:
                raise SuperAIEntityDuplicatedError(
                    message,
                    http_e.response.status_code,
                    base_url=self.base_url,
                    endpoint=endpoint,
                ) from http_e
            elif http_e.response.status_code == 502:
                raise requests.HTTPError(message, http_e.response.status_code) from http_e

            raise SuperAIError(message, http_e.response.status_code) from http_e

    def _get_organization_id(self, organization_name: str, user: Optional[object] = None) -> int:
        """Check if the user is part of the organization"""
        user = user or self.get_user()

        if organization_name == "superai":
            # TODO: replace this with correct non-membership org resolver once we have it
            return 1

        orgs = [org for org in user.organizationMemberships if org.orgUsername == organization_name]
        if any(orgs):
            return orgs[0].orgId
        else:
            raise SuperAIAuthorizationError(f"User is not part of the organization {organization_name}", 403)

    def _get_user_id(self, user: Optional[object] = None) -> int:
        """Retrieve the user id for the current user"""
        user = user or self.get_user()
        return user.id
