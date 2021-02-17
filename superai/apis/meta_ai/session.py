from sgqlc.endpoint.requests import RequestsEndpoint
from superai.config import settings
from superai.utils.apikey_manager import load_api_key


class GraphQlException(Exception):
    pass


class MetaAISession(RequestsEndpoint):
    def __init__(self, app_id=None, timeout=20):
        base_url = settings.get("meta_ai_base")
        api_key = load_api_key()
        headers = {"x-api-key": api_key, "x-app-id": app_id, "Accept-Encoding": "gzip"}
        super().__init__(base_url, headers, timeout=timeout)

    def perform_op(self, op):
        data = self(op)
        if data.get("errors", False):
            raise GraphQlException(data)
        else:
            return data
