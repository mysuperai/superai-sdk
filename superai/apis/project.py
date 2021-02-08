from __future__ import absolute_import

import logging
import re  # noqa: F401
from abc import ABC, abstractmethod

# python 2 and python 3 compatibility library
import six
from colorama import Fore, Style

from superai.log import logdecorator


class ProjectApiMixin(ABC):
    @abstractmethod
    def request(self, uri, method, body_params=None, query_params=None, required_api_key=False):
        pass

    @logdecorator.log_on_start(
        logging.DEBUG,
        Fore.CYAN + "Project get {uuid}" + Style.RESET_ALL,
    )
    @logdecorator.log_on_end(
        logging.DEBUG,
        Fore.CYAN + "Project get {uuid} response: {result!s}" + Style.RESET_ALL,
    )
    @logdecorator.log_exception(
        logging.ERROR,
        Fore.RED + "Error on Project get {uuid} {e!r}" + Style.RESET_ALL,
        on_exceptions=Exception,
        reraise=True,
    )
    def get_project(self, uuid, **kwargs):
        """Fetch a given resource

        :param str workflow_name: The superai identifier (required)
        :param str x_fields: An optional fields mask
        :return: A Superai
        """

        all_params = ["uuid", "x_fields"]
        all_params.append("_return_http_data_only")
        all_params.append("_preload_content")
        all_params.append("_request_timeout")

        params = locals()
        for key, val in six.iteritems(params["kwargs"]):
            if key not in all_params:
                raise TypeError("Got an unexpected keyword argument '%s'" " to method get_template" % key)
            params[key] = val
        del params["kwargs"]
        if "uuid" not in params or params["uuid"] is None:
            raise ValueError("Missing the required parameter `uuid` when calling `get_instance`")

        collection_formats = {}

        path_params = {}
        if "uuid" in params:
            path_params["uuid"] = params["uuid"]

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
            required_api_key=True,
        )

    @logdecorator.log_on_start(
        logging.DEBUG,
        Fore.CYAN + "Project get selected workflow {uuid:s}" + Style.RESET_ALL,
    )
    @logdecorator.log_on_end(
        logging.DEBUG,
        Fore.CYAN + "Project get selected workflow {uuid:s} response: {result!s}" + Style.RESET_ALL,
    )
    @logdecorator.log_exception(
        logging.ERROR,
        Fore.RED + "Error on Project get selected workflow {uuid:s} {e!r}" + Style.RESET_ALL,
        on_exceptions=Exception,
        reraise=True,
    )
    def get_selected_workflow(self, uuid, **kwargs):
        """Fetch a given resource

        :param str uuid: The superai identifier (required)
        :param str x_fields: An optional fields mask
        :return: Qualified workflow name
        """

        all_params = ["uuid", "x_fields"]
        all_params.append("_return_http_data_only")
        all_params.append("_preload_content")
        all_params.append("_request_timeout")

        params = locals()
        for key, val in six.iteritems(params["kwargs"]):
            if key not in all_params:
                raise TypeError("Got an unexpected keyword argument '%s'" " to method get_template" % key)
            params[key] = val
        del params["kwargs"]

        if "uuid" not in params or params["uuid"] is None:
            raise ValueError("Missing the required parameter `uuid` when calling `get_instance`")

        collection_formats = {}

        path_params = {}
        if "uuid" in params:
            path_params["uuid"] = params["uuid"]

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
            required_api_key=True,
        )

    @logdecorator.log_on_start(
        logging.DEBUG,
        Fore.CYAN + "List instances" + Style.RESET_ALL,
    )
    @logdecorator.log_on_end(
        logging.DEBUG,
        Fore.CYAN + "List instances response: {result!s}" + Style.RESET_ALL,
    )
    @logdecorator.log_exception(
        logging.ERROR,
        Fore.RED + "Error on list instances {e!r}" + Style.RESET_ALL,
        on_exceptions=Exception,
        reraise=True,
    )
    def list_projects(self, **kwargs):
        """List all superAIs (Tags param is mock)

        :param int page:
        :param int size:
        :param str sort_by:
        :param str order_by:
        :param bool only_owned_or_group:
        :param list[str] input_types:
        :param list[str] output_types:
        :param list[str] tags:
        :param str x_fields: An optional fields mask
        :return: List of SuperAIs
        """

        all_params = [
            "page",
            "size",
            "sort_by",
            "order_by",
            "only_owned_or_group",
            "input_types",
            "output_types",
            "tags",
            "x_fields",
        ]
        all_params.append("_return_http_data_only")
        all_params.append("_preload_content")
        all_params.append("_request_timeout")

        params = locals()
        for key, val in six.iteritems(params["kwargs"]):
            if key not in all_params:
                raise TypeError("Got an unexpected keyword argument '%s'" " to method list_templates" % key)
            params[key] = val
        del params["kwargs"]

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
        if "only_owned_or_group" in params:
            query_params.append(("only_owned_or_group", params["only_owned_or_group"]))
        if "input_types" in params:
            query_params.append(("inputTypes", params["input_types"]))
            collection_formats["inputTypes"] = "multi"
        if "output_types" in params:
            query_params.append(("outputTypes", params["output_types"]))
            collection_formats["outputTypes"] = "multi"
        if "tags" in params:
            query_params.append(("tags", params["tags"]))
            collection_formats["tags"] = "multi"

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

        return self.request(
            endpoint="apps",
            method="GET",
            query_params=query_params,
            body_params=body_params,
            required_api_key=True,
        )

    @logdecorator.log_on_start(
        logging.DEBUG,
        Fore.CYAN + "Project update {workflow_name:s} with body {body}" + Style.RESET_ALL,
    )
    @logdecorator.log_on_end(
        logging.DEBUG,
        Fore.CYAN + "Project update {workflow_name:s} response: {result!s}" + Style.RESET_ALL,
    )
    @logdecorator.log_exception(
        logging.ERROR,
        Fore.RED + "Error on Project update {workflow_name:s} {e!r}" + Style.RESET_ALL,
        on_exceptions=Exception,
        reraise=True,
    )
    def update_project(self, uuid, body, **kwargs):
        """Update a superai given its full qualified name

        If the superai already exists and it is owned by  somebody else then if will throw a 409

        :param Project body: (required)
        :param str uuid: The Project identifier (required)
        :param str x_fields: An optional fields mask
        :return: Project updated
        """

        all_params = ["body", "uuid", "x_fields"]
        all_params.append("_return_http_data_only")
        all_params.append("_preload_content")
        all_params.append("_request_timeout")

        params = locals()
        for key, val in six.iteritems(params["kwargs"]):
            if key not in all_params:
                raise TypeError("Got an unexpected keyword argument '%s'" " to method update_template" % key)
            params[key] = val
        del params["kwargs"]
        # verify the required parameter 'body' is set
        if "body" not in params or params["body"] is None:
            raise ValueError("Missing the required parameter `body` when calling `update_instance`")

        if "uuid" not in params or params["uuid"] is None:
            raise ValueError("Missing the required parameter `uuid` when calling `update_instance`")

        collection_formats = {}

        path_params = {}
        if "uuid" in params:
            path_params["uuid"] = params["uuid"]

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
            required_api_key=True,
        )

    @logdecorator.log_on_start(
        logging.DEBUG,
        Fore.CYAN + "Project update with body {body}" + Style.RESET_ALL,
    )
    @logdecorator.log_on_end(
        logging.DEBUG,
        Fore.CYAN + "Project update response: {result!s}" + Style.RESET_ALL,
    )
    @logdecorator.log_exception(
        logging.ERROR,
        Fore.RED + "Error on Project update {e!r}" + Style.RESET_ALL,
        on_exceptions=Exception,
        reraise=True,
    )
    def create_project(self, body, **kwargs):
        """Update a superai given its uuid

        If the dataprogram already exists and it is owned by  somebody else then if will throw a 409

        :param DataProgram body: (required)
        :param str x_fields: An optional fields mask
        :return: Project
        """

        all_params = ["body", "x_fields"]
        all_params.append("_return_http_data_only")
        all_params.append("_preload_content")
        all_params.append("_request_timeout")

        params = locals()
        for key, val in six.iteritems(params["kwargs"]):
            if key not in all_params:
                raise TypeError("Got an unexpected keyword argument '%s'" " to method update_template" % key)
            params[key] = val
        del params["kwargs"]
        # verify the required parameter 'body' is set
        if "body" not in params or params["body"] is None:
            raise ValueError("Missing the required parameter `body` when calling `update_instance`")

        collection_formats = {}

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

        uri = "apps"
        return self.request(
            endpoint=uri,
            method="POST",
            query_params=query_params,
            body_params=body_params,
            required_api_key=True,
        )
