from sgqlc.endpoint.requests import RequestsEndpoint
from sgqlc.operation import Operation
from superai.config import settings
from superai.utils.apikey_manager import load_api_key
from superai.utils.decorators import retry


class GraphQlException(Exception):
    pass


class MetaAISession(RequestsEndpoint):
    def __init__(self, app_id: str = None, timeout: int = 60):
        base_url = settings.get("meta_ai_base")
        # base_url = "http://localhost:52619/v1/graphql"
        api_key = load_api_key()
        headers = {"x-api-key": api_key, "x-app-id": app_id, "Accept-Encoding": "gzip"}
        super().__init__(base_url, headers, timeout=timeout)

    @retry(TimeoutError)
    def perform_op(self, op: Operation, timeout: int = 60):
        data = self(op, timeout=timeout)
        if data.get("errors", False):
            error = data["errors"][0]
            if "Endpoint request timed out" in str(error):
                raise TimeoutError()
            else:
                raise GraphQlException(data)
        else:
            return data
