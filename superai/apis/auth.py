from abc import ABC, abstractmethod
from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel


class StatusEnum(str, Enum):
    INVITED = "INVITED"
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"


class RoleEnum(str, Enum):
    MEMBER = "MEMBER"
    OWNER = "OWNER"


class OrganizationMember(BaseModel):
    id: int
    status: StatusEnum
    role: RoleEnum
    invited: datetime
    accepted: datetime
    created: datetime
    orgId: int
    orgUsername: str
    userId: int
    userEmail: str


class PlanEnum(str, Enum):
    FREEMIUM = "FREEMIUM"
    FULL = "FULL"


class User(BaseModel):
    email: str
    metadata: Optional[dict]
    active: bool
    id: int
    created: datetime
    apiKey: Optional[str]
    company: Optional[str]
    sysAdmin: bool
    groups: List  # or you can replace it with a list of appropriate models
    plan: PlanEnum
    username: str
    backofficeAdmin: Optional[bool]
    trialDays: Optional[int]
    organizationMemberships: List[OrganizationMember]


class AuthApiMixin(ABC):
    @abstractmethod
    def request(
        self,
        uri,
        method,
        body_params=None,
        query_params=None,
        required_auth_token=False,
        required_api_key=False,
        required_id_token=False,
    ):
        pass

    def get_apikeys(self) -> List[str]:
        """Gets the API keys of the authenticated user.

        Returns:
            A list with the API keys of the authenticated user.
        """
        uri = "users/apiKeys"
        return self.request(uri, method="GET", required_auth_token=True, required_id_token=True)

    def get_awskeys(self) -> List[str]:
        """Gets the API keys of the authenticated user.

        Returns:
            A list with the API keys of the authenticated user.
        """
        uri = "users/awsKeys"
        return self.request(uri, method="GET", required_id_token=True)

    def get_user(self) -> User:
        """Gets the authenticated user.

        Returns:
            The authenticated user model.
        """
        uri = "users"
        response = self.request(uri, method="GET", required_api_key=True)
        return User.parse_obj(response)
