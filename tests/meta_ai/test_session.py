import logging
import os
import subprocess
from unittest.mock import patch

import pytest
from requests.exceptions import RequestException

from superai.apis.meta_ai.session import (
    GraphQlException,
    MetaAISession,
    SuperAIAuthorizationError,
)


# Mock out time.sleep
@pytest.fixture(autouse=True)
def patch_sleep(mocker):
    mocker.patch("time.sleep", return_value=None)


class TestMetaAISession:
    @patch("superai.apis.meta_ai.session.RequestsEndpoint.__init__")
    @patch.object(os, "getenv")
    @patch.object(MetaAISession, "_get_local_endpoint")
    # @patch("superai.utils.apikey_manager.load_api_key")
    def test_init(self, mock_get_local, mock_getenv, mock_requests_init):
        mock_getenv.return_value = True
        mock_get_local.return_value = "http://localhost:8000"
        MetaAISession()
        mock_requests_init.assert_called_once()

    @patch.object(subprocess, "check_output")
    def test_get_local_endpoint(self, mock_check_output):
        mock_check_output.return_value = b"0.0.0.0:8000"
        session = MetaAISession()
        endpoint = session._get_local_endpoint()
        assert endpoint == "http://localhost:8000/v1/graphql"

    @patch.object(MetaAISession, "__call__")
    def test_perform_op_success(self, mock_call):
        mock_call.return_value = {"data": "success"}
        session = MetaAISession()
        result = session.perform_op("test_operation")
        assert result == {"data": "success"}

    @patch.object(MetaAISession, "__call__")
    def test_perform_op_timeout_error(self, mock_call):
        mock_call.return_value = {"errors": ["Endpoint request timed out"]}
        session = MetaAISession()
        with pytest.raises(TimeoutError):
            session.perform_op("test_operation")

    @patch.object(MetaAISession, "__call__")
    def test_perform_op_auth_error(self, mock_call):
        mock_call.return_value = {"errors": ["Authentication hook unauthorized"]}
        session = MetaAISession()
        with pytest.raises(SuperAIAuthorizationError):
            session.perform_op("test_operation")

    @patch.object(MetaAISession, "__call__")
    def test_perform_op_invalid_query(self, mock_call):
        mock_call.return_value = {"errors": ["not a valid graphql query"]}
        session = MetaAISession()
        with pytest.raises(GraphQlException):
            session.perform_op("test_operation")

    @patch.object(MetaAISession, "__call__")
    def test_perform_op_general_error(self, mock_call):
        mock_call.return_value = {"errors": ["Some random error"]}
        session = MetaAISession()
        with pytest.raises(GraphQlException):
            session.perform_op("test_operation")

    @patch.object(MetaAISession, "__call__")
    def test_request_exception(self, mock_call, caplog):
        mock_call.side_effect = RequestException
        session = MetaAISession()

        with caplog.at_level(logging.WARNING):
            with pytest.raises(RequestException):
                session.perform_op("test_operation")

        # Checking that "Retrying" from the retry decorator is logged.
        assert "Retrying" in caplog.text
