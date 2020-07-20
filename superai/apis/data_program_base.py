import requests
from typing import Optional

from superai.config import BASE_URL
from superai.exceptions import SuperAIError

class DataProgramBase:
    def _request(self, endpoint: str, method: str = 'GET', query_params: dict = None, body_params: dict = None,
                required_api_key: bool = False, required_auth_token: bool = False) -> Optional[dict]:
        headers = {}
        if required_api_key and self.api_key:
            headers['API-KEY'] = self.api_key
        if required_auth_token and self.auth_token:
            headers['AUTH-TOKEN'] = self.auth_token
        resp = requests.request(method, f'{BASE_URL}/{endpoint}', params=query_params, json=body_params, headers=headers)
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