from abc import ABC, abstractmethod
from typing import List


class AuthApiMixin(ABC):
    @abstractmethod
    def request(self, uri, method, body_params=None, query_params=None, required_auth_token=False):
        pass

    def get_apikeys(self) -> List[str]:
        """
        Get api-keys of authenticated user
        :return List with api-keys of authenticated user:
        """
        uri = "users/apiKeys"
        return self.request(uri, method="GET", required_auth_token=True, required_id_token=True)

    def get_awskeys(self) -> List[str]:
        """
        Get api-keys of authenticated user
        :return List with api-keys of authenticated user:
        """
        uri = "users/awsKeys"
        return self.request(uri, method="GET", required_id_token=True)
