import os
import subprocess
from functools import lru_cache
from typing import Generator, Optional

from pydantic import BaseModel
from requests import RequestException
from sgqlc.endpoint.requests import RequestsEndpoint
from sgqlc.endpoint.websocket import WebSocketEndpoint
from sgqlc.operation import Operation

from superai.config import settings
from superai.exceptions import SuperAIAuthorizationError
from superai.log import get_logger
from superai.utils.apikey_manager import load_api_key
from superai.utils.decorators import retry
from superai.utils.opentelemetry import tracer

log = get_logger(__name__)


class GraphQlException(Exception):
    pass


class MetaAISession(RequestsEndpoint):
    """Session class for requests based connections to the MetaAI backend.
    Allows querying and mutation via the GraphQL API.
    """

    def __init__(self, app_id: str = None, timeout: int = 60):
        self.base_url = f"{settings.get('meta_ai_request_protocol')}://{settings.get('meta_ai_base')}"
        if os.getenv("LOCAL_META_AI"):
            self.base_url = self._get_local_endpoint()
            log.warning(f"Using local MetaAI endpoint at {self.base_url}")
        api_key = load_api_key()
        headers = {"x-api-key": api_key, "x-app-id": app_id, "Accept-Encoding": "gzip"}
        super().__init__(self.base_url, headers, timeout=timeout)

    @lru_cache(maxsize=1)
    def _get_local_endpoint(self):
        """Get the local endpoint for MetaAI GraphQL API. Used for local development."""
        try:
            # get hasura port using docker client
            hasura_port = (
                subprocess.check_output(["docker", "port", "meta-ai_hasura_1", "8080"], stderr=subprocess.DEVNULL)
                .decode()
                .strip()
                .split(":")[1]
            )
        except subprocess.CalledProcessError:
            # If not found try spelling with all dashes
            try:
                hasura_port = (
                    subprocess.check_output(["docker", "port", "meta-ai-hasura-1", "8080"], stderr=subprocess.DEVNULL)
                    .decode()
                    .strip()
                    .split(":")[1]
                )
            except subprocess.CalledProcessError:
                return None

        hasura_endpoint = f"http://localhost:{hasura_port}/v1/graphql"

        return hasura_endpoint

    @retry((TimeoutError, RequestException))  # noqa: F821
    @tracer.start_as_current_span("MetaAISession.perform_op")
    def perform_op(self, op: Operation, timeout: int = 60):
        data = self(op, timeout=timeout)
        if not data.get("errors", False):
            return data
        error = data["errors"][0]
        if "Endpoint request timed out" in str(error):
            raise TimeoutError()
        elif "Authentication hook unauthorized" in str(error):
            raise SuperAIAuthorizationError(error, error_code=401, endpoint=self.base_url)
        elif "not a valid graphql query" in str(error):
            # Print out query for debugging
            log.debug(f"Query: {op}")
            raise GraphQlException(error)
        else:
            raise GraphQlException(data)


class MetaAIWebsocketSession(WebSocketEndpoint):
    """Session class for websocket connection to MetaAI backend.
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
        """Performs an operation and yields the result to enable streaming of events in the websocket.

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
