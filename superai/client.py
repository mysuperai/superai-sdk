from typing import Optional

import requests

from superai.apis.auth import AuthApiMixin
from superai.apis.data import DataApiMixin
from superai.apis.jobs import JobsApiMixin
from superai.apis.ground_truth import GroundTruthApiMixin
from superai.config import BASE_URL
from superai.exceptions import SuperAIError


class Client(JobsApiMixin, AuthApiMixin, GroundTruthApiMixin, DataApiMixin):

    def __init__(self, api_key: str = None, auth_token: str = None, base_url: str = None):
        self.api_key = api_key
        self.auth_token = auth_token
        if base_url is None:
            self.base_url = BASE_URL
        else:
            self.base_url = base_url

    def request(self, endpoint: str, method: str = 'GET', query_params: dict = None, body_params: dict = None,
                required_api_key: bool = False, required_auth_token: bool = False) -> Optional[dict]:
        headers = {}
        if required_api_key and self.api_key:
            headers['API-KEY'] = self.api_key
        if required_auth_token and self.auth_token:
            headers['AUTH-TOKEN'] = self.auth_token
        resp = requests.request(method, f'{self.base_url}/{endpoint}', params=query_params, json=body_params,
                                headers=headers)
        try:
            resp.raise_for_status()
            if resp.status_code == 204:
                return None
            else:
                return resp.json()
        except requests.exceptions.HTTPError as http_e:
            try:
                message = http_e.response.json()['message']
            except:
                message = http_e.response.text
            raise SuperAIError(message, http_e.response.status_code)
