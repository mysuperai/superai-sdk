from abc import ABC, abstractmethod
from typing import List


class AuthApiMixin(ABC):
    @abstractmethod
    def request(self, uri, method, body_params=None, query_params=None, required_auth_token=False):
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
