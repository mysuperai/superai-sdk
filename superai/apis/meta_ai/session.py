from typing import Generator, Optional

from pydantic import BaseModel
from sgqlc.endpoint.requests import RequestsEndpoint
from sgqlc.endpoint.websocket import WebSocketEndpoint
from sgqlc.operation import Operation

from superai.config import settings
from superai.utils.apikey_manager import load_api_key
from superai.utils.decorators import retry


class GraphQlException(Exception):
    pass


class MetaAISession(RequestsEndpoint):
    """
    Session class for requests based connections to the MetaAI backend.
    Allows querying and mutation via the GraphQL API.
    """

    def __init__(self, app_id: str = None, timeout: int = 60):
        base_url = f"{settings.get('meta_ai_request_protocol')}://{settings.get('meta_ai_base')}"
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


class MetaAIWebsocketSession(WebSocketEndpoint):
    """
    Session class for websocket connection to MetaAI backend.
    Allows GraphQL subscriptions over open websocket connection.
    """

    def __init__(self, app_id: str = None):
        base_url = f"wss://{settings.get('meta_ai_base')}"
        api_key = load_api_key()

        # Websocket expects None values to be empty string (app_id)
        headers = {"x-api-key": api_key, "x-app-id": app_id or "", "Accept-Encoding": "gzip"}
        super().__init__(base_url, connection_payload={"headers": headers})

    class ReturnDict(BaseModel):
        data: Optional[dict]
        errors: Optional[dict]

    def perform_op(self, op: Operation) -> Generator[ReturnDict, None, None]:
        """
        Performs an operation and yields the result to enable streaming of events in the websocket.

        Args:
            op:

        Returns:

        """
        for dict in self(op):
            if dict.get("errors", False):
                error = dict["errors"]
                raise GraphQlException(error)
            else:
                yield dict
