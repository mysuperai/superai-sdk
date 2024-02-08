from __future__ import absolute_import

import logging
import re  # noqa: F401
from abc import ABC, abstractmethod

from superai.log import logdecorator


class ProjectApiMixin(ABC):
    @abstractmethod
    def request(self, uri, method, body_params=None, query_params=None, required_api_key=False, header_params=None):
        pass

    @logdecorator.log_on_start(
        logging.DEBUG,
        "Project get {uuid}",
    )
    @logdecorator.log_on_end(
        logging.DEBUG,
        "Project get {uuid} response: {result!s}",
    )
    @logdecorator.log_exception(
        logging.ERROR,
        "Error on Project get {uuid} {e!r}",
        on_exceptions=Exception,
        reraise=True,
    )
    def get_project(self, uuid, **kwargs):
        """Fetches a given resource.

        Args:
            str workflow_name: The superai identifier (required)
            str x_fields: An optional fields mask

        Returns:
            A Superai.
        """

        all_params = ["uuid", "x_fields", "_return_http_data_only", "_preload_content", "_request_timeout"]

        params = locals()
        for key, val in params["kwargs"].items():
            if key not in all_params:
                raise TypeError(f"Got an unexpected keyword argument '{key}' to method get_template")
            params[key] = val
        del params["kwargs"]
        if "uuid" not in params or params["uuid"] is None:
            raise ValueError("Missing the required parameter `uuid` when calling `get_instance`")

        collection_formats = {}

        path_params = {"uuid": params["uuid"]}
        query_params = []

        header_params = {}
        if "x_fields" in params:
            header_params["X-Fields"] = params["x_fields"]

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params["Accept"] = "application/json"

        # Authentication setting
        auth_settings = ["apiToken"]
        uri = "apps/{uuid}".format(**path_params)
        return self.request(
            endpoint=uri,
            method="GET",
            query_params=query_params,
            body_params=body_params,
            header_params=header_params,
            required_api_key=True,
        )

    @logdecorator.log_on_start(
        logging.DEBUG,
        "Project get selected workflow {uuid:s}",
    )
    @logdecorator.log_on_end(
        logging.DEBUG,
        "Project get selected workflow {uuid:s} response: {result!s}",
    )
    @logdecorator.log_exception(
        logging.ERROR,
        "Error on Project get selected workflow {uuid:s} {e!r}",
        on_exceptions=Exception,
        reraise=True,
    )
    def get_selected_workflow(self, uuid, **kwargs):
        """Fetches a given resource.

        Args:
            str uuid: The superai identifier (required)
            str x_fields: An optional fields mask

        Returns:
            Qualified workflow name.
        """

        all_params = ["uuid", "x_fields", "_return_http_data_only", "_preload_content", "_request_timeout"]

        params = locals()
        for key, val in params["kwargs"].items():
            if key not in all_params:
                raise TypeError(f"Got an unexpected keyword argument '{key}' to method get_template")
            params[key] = val
        del params["kwargs"]

        if "uuid" not in params or params["uuid"] is None:
            raise ValueError("Missing the required parameter `uuid` when calling `get_instance`")

        collection_formats = {}

        path_params = {"uuid": params["uuid"]}
        query_params = []

        header_params = {}
        if "x_fields" in params:
            header_params["X-Fields"] = params["x_fields"]

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params["Accept"] = "application/json"

        # Authentication setting
        auth_settings = ["apiToken"]
        uri = "apps/{uuid}/selected_plan".format(**path_params)
        return self.request(
            endpoint=uri,
            method="GET",
            query_params=query_params,
            body_params=body_params,
            header_params=header_params,
            required_api_key=True,
        )

    @logdecorator.log_on_start(
        logging.DEBUG,
        "List instances",
    )
    @logdecorator.log_on_end(
        logging.DEBUG,
        "List instances response: {result!s}",
    )
    @logdecorator.log_exception(
        logging.ERROR,
        "Error on list instances {e!r}",
        on_exceptions=Exception,
        reraise=True,
    )
    def list_projects(self, **kwargs):
        """Lists all superAIs (Tags param is mock).

        Args:
            int page:
            int size:
            str sort_by:
            str order_by:
            bool only_owned_or_group:
            list[str] input_types:
            list[str] output_types:
            list[str] tags:
            str x_fields: An optional fields mask

        Returns:
            List of SuperAIs.
        """

        all_params = [
            "page",
            "size",
            "sort_by",
            "order_by",
            "status_in",
            "org",
            "x_fields",
            "_return_http_data_only",
            "_preload_content",
            "_request_timeout",
        ]

        params = locals()
        for key, val in params["kwargs"].items():
            if key not in all_params:
                raise TypeError(f"Got an unexpected keyword argument '{key}' to method list_templates")
            params[key] = val
        del params["kwargs"]

        params["order_by"] = "desc" if not params.get("order_by") else params["order_by"]
        params["sort_by"] = "created" if not params.get("sort_by") else params["sort_by"]

        collection_formats = {}

        path_params = {}

        query_params = []
        if "page" in params:
            query_params.append(("page", params["page"]))
        if "size" in params:
            query_params.append(("size", params["size"]))
        if "sort_by" in params:
            query_params.append(("sortBy", params["sort_by"]))
        if "order_by" in params:
            query_params.append(("orderBy", params["order_by"]))
        if "status_in" in params:
            query_params.append(("statusIn", params["status_in"]))

        header_params = {}
        if "x_fields" in params:
            header_params["X-Fields"] = params["x_fields"]

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params["Accept"] = "application/json"

        # Authentication setting
        auth_settings = ["apiToken"]

        org = params.get("org", None)
        endpoint = "apps" if not org else f"organizations/{org}/apps"

        return self.request(
            endpoint=endpoint,
            method="GET",
            query_params=query_params,
            body_params=body_params,
            header_params=header_params,
            required_api_key=True,
        )

    @logdecorator.log_on_start(
        logging.DEBUG,
        "Project update {workflow_name:s} with body {body}",
    )
    @logdecorator.log_on_end(
        logging.DEBUG,
        "Project update {workflow_name:s} response: {result!s}",
    )
    @logdecorator.log_exception(
        logging.ERROR,
        "Error on Project update {workflow_name:s} {e!r}",
        on_exceptions=Exception,
        reraise=True,
    )
    def update_project(self, uuid, body, **kwargs):
        """Updates a superai given its full qualified name. If the superai already exists and it is owned by somebody else then if will return a 409.

        Args:
            body: (required)
            uuid: The Project identifier (required)
            x_fields: An optional fields mask

        Returns:
            Project updated.
        """

        all_params = ["body", "uuid", "x_fields", "_return_http_data_only", "_preload_content", "_request_timeout"]

        params = locals()
        for key, val in params["kwargs"].items():
            if key not in all_params:
                raise TypeError(f"Got an unexpected keyword argument '{key}' to method update_template")
            params[key] = val
        del params["kwargs"]
        # verify the required parameter 'body' is set
        if "body" not in params or params["body"] is None:
            raise ValueError("Missing the required parameter `body` when calling `update_instance`")

        if "uuid" not in params or params["uuid"] is None:
            raise ValueError("Missing the required parameter `uuid` when calling `update_instance`")

        collection_formats = {}

        path_params = {"uuid": params["uuid"]}
        query_params = []

        header_params = {}
        if "x_fields" in params:
            header_params["X-Fields"] = params["x_fields"]

        form_params = []
        local_var_files = {}

        body_params = None
        if "body" in params:
            body_params = params["body"]
        # HTTP header `Accept`
        header_params["Accept"] = "application/json"

        # HTTP header `Content-Type`
        header_params["Content-Type"] = "application/json"

        # Authentication setting
        auth_settings = ["apiToken"]

        uri = "apps/{uuid}".format(**path_params)
        return self.request(
            endpoint=uri,
            method="PATCH",
            query_params=query_params,
            body_params=body_params,
            header_params=header_params,
            required_api_key=True,
        )

    @logdecorator.log_on_start(
        logging.DEBUG,
        "Project update with body {body}",
    )
    @logdecorator.log_on_end(
        logging.DEBUG,
        "Project update response: {result!s}",
    )
    @logdecorator.log_exception(
        logging.ERROR,
        "Error on Project update {e!r}",
        on_exceptions=Exception,
        reraise=True,
    )
    def create_project(self, body, org=None, **kwargs):
        """Updates a superai given its UUID.

        If the Data Program already exists and it is owned by somebody else, then if will return a 409.

        Args:
            DataProgram body: (required)
            x_fields: An optional fields mask

        Returns:
            Project.
        """

        all_params = ["body", "x_fields", "_return_http_data_only", "_preload_content", "_request_timeout"]

        params = locals()
        query_params = {}
        if org:
            query_params["org"] = org
        del params["org"]
        for key, val in params["kwargs"].items():
            if key not in all_params:
                raise TypeError(f"Got an unexpected keyword argument '{key}' to method update_template")
            params[key] = val
        del params["kwargs"]
        # verify the required parameter 'body' is set
        if "body" not in params or params["body"] is None:
            raise ValueError("Missing the required parameter `body` when calling `update_instance`")

        collection_formats = {}

        header_params = {}
        if "x_fields" in params:
            header_params["X-Fields"] = params["x_fields"]

        form_params = []
        local_var_files = {}

        body_params = None
        body_params = params["body"]
        # HTTP header `Accept`
        header_params["Accept"] = "application/json"

        # HTTP header `Content-Type`
        header_params["Content-Type"] = "application/json"

        # Authentication setting
        auth_settings = ["apiToken"]

        uri = "apps"
        return self.request(
            endpoint=uri,
            method="POST",
            query_params=query_params,
            body_params=body_params,
            header_params=header_params,
            required_api_key=True,
        )
