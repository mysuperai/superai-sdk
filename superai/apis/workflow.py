from __future__ import absolute_import

import logging
import re  # noqa: F401
from abc import ABC, abstractmethod

# python 2 and python 3 compatibility library
import six
from colorama import Fore, Style

from superai.log import logdecorator


class WorkflowApiMixin(ABC):
    @abstractmethod
    def request(self, uri, method, body_params=None, query_params=None, required_api_key=False):
        pass

    @logdecorator.log_on_start(
        logging.DEBUG,
        Fore.CYAN + "Workflow get {workflow_name:s}" + Style.RESET_ALL,
    )
    @logdecorator.log_on_end(
        logging.DEBUG,
        Fore.CYAN + "Workflow get {workflow_name:s} {result!s}" + Style.RESET_ALL,
    )
    @logdecorator.log_exception(
        logging.ERROR,
        Fore.RED + "Error on Workflow get {workflow_name:s} {e!r}" + Style.RESET_ALL,
        on_exceptions=Exception,
        reraise=True,
    )
    def get_workflow(self, workflow_name, **kwargs):
        """Fetch a given resource

        :param str workflow_name: The workflow identifier (required)
        :param str x_fields: An optional fields mask
        :return: DataProgram
        """

        all_params = ["workflow_name", "x_fields"]
        all_params.append("_return_http_data_only")
        all_params.append("_preload_content")
        all_params.append("_request_timeout")

        params = locals()
        for key, val in six.iteritems(params["kwargs"]):
            if key not in all_params:
                raise TypeError("Got an unexpected keyword argument '%s'" " to method get_template" % key)
            params[key] = val
        del params["kwargs"]
        # verify the required parameter 'workflow_name' is set
        if "workflow_name" not in params or params["workflow_name"] is None:
            raise ValueError("Missing the required parameter `workflow_name` when calling `get_template`")

        collection_formats = {}

        path_params = {}
        if "workflow_name" in params:
            path_params["template_name"] = params["workflow_name"]

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
        uri = "templates/{template_name}".format(**path_params)
        return self.request(
            endpoint=uri,
            method="GET",
            query_params=query_params,
            body_params=body_params,
            required_api_key=True,
        )

    @logdecorator.log_on_start(
        logging.DEBUG,
        Fore.CYAN + "List workflows" + Style.RESET_ALL,
    )
    @logdecorator.log_on_end(
        logging.DEBUG,
        Fore.CYAN + "List workflows response: {result!s}" + Style.RESET_ALL,
    )
    @logdecorator.log_exception(
        logging.ERROR,
        Fore.RED + "Error on list workflow {e!r}" + Style.RESET_ALL,
        on_exceptions=Exception,
        reraise=True,
    )
    def list_workflows(self, **kwargs):
        """List all templates (Tags param is mock)

        :param int page:
        :param int size:
        :param str sort_by:
        :param str order_by:
        :param bool only_owned_or_group:
        :param list[str] input_types:
        :param list[str] output_types:
        :param list[str] tags:
        :param str x_fields: An optional fields mask
        :return: TemplatesList
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
            endpoint="templates",
            method="GET",
            query_params=query_params,
            body_params=body_params,
            required_api_key=True,
        )

    @logdecorator.log_on_start(
        logging.DEBUG,
        Fore.CYAN + "Workflow put {workflow_name:s} with body {body}" + Style.RESET_ALL,
    )
    @logdecorator.log_on_end(
        logging.DEBUG,
        Fore.CYAN + "Workflow put {workflow_name:s} {result!s}" + Style.RESET_ALL,
    )
    @logdecorator.log_exception(
        logging.ERROR,
        Fore.RED + "Error on Workflow put {workflow_name:s} {e!r}" + Style.RESET_ALL,
        on_exceptions=Exception,
        reraise=True,
    )
    def put_workflow(self, workflow_name, body, **kwargs):
        """Create or update a workflow given its full qualified name

        If the workflow already exists and it is owned by  somebody else then if will throw a 409

        :param Workflow body: (required)
        :param str workflow_name: The workflow identifier (required)
        :param str x_fields: An optional fields mask
        :return: Workflow
        """

        all_params = ["body", "workflow_name", "x_fields"]
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
            raise ValueError("Missing the required parameter `body` when calling `update_template`")
        # verify the required parameter 'workflow_name' is set
        if "workflow_name" not in params or params["workflow_name"] is None:
            raise ValueError("Missing the required parameter `workflow_name` when calling `update_template`")

        collection_formats = {}

        path_params = {}
        if "workflow_name" in params:
            path_params["template_name"] = params["workflow_name"]

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

        uri = "templates/{template_name}".format(**path_params)
        response = self.request(
            endpoint=uri,
            method="PUT",
            query_params=query_params,
            body_params=body_params,
            required_api_key=True,
            required_auth_token=True,
        )
        return response

    @logdecorator.log_on_start(
        logging.DEBUG,
        Fore.CYAN + "Workflow update {workflow_name:s} with body {body}" + Style.RESET_ALL,
    )
    @logdecorator.log_on_end(
        logging.DEBUG,
        Fore.CYAN + "Workflow update {workflow_name:s} {result!s}" + Style.RESET_ALL,
    )
    @logdecorator.log_exception(
        logging.ERROR,
        Fore.RED + "Error on Workflow update {workflow_name:s} {e!r}" + Style.RESET_ALL,
        on_exceptions=Exception,
        reraise=True,
    )
    def update_workflow(self, workflow_name, body, **kwargs):
        """
        This is a proxy method for put_workflow. See above

        :param Workflow body: (required)
        :param str workflow_name: The workflow identifier (required)
        :param str x_fields: An optional fields mask
        :return: Workflow
        """
        return self.put_workflow(workflow_name, body)

    @logdecorator.log_on_start(
        logging.DEBUG,
        Fore.CYAN + "Workflow create {workflow_name:s} with body {body}" + Style.RESET_ALL,
    )
    @logdecorator.log_on_end(
        logging.DEBUG,
        Fore.CYAN + "Workflow create {workflow_name:s} {result!s}" + Style.RESET_ALL,
    )
    @logdecorator.log_exception(
        logging.ERROR,
        Fore.RED + "Error on Workflow create {workflow_name:s} {e!r}" + Style.RESET_ALL,
        on_exceptions=Exception,
        reraise=True,
    )
    def create_workflow(self, workflow_name, body, **kwargs):
        """
        This is a proxy method for put_workflow. See above

        :param Workflow body: (required)
        :param str workflow_name: The workflow identifier (required)
        :param str x_fields: An optional fields mask
        :return: Workflow
        """
        return self.put_workflow(workflow_name, body)
