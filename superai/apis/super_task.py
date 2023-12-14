from __future__ import absolute_import

import logging
import re  # noqa: F401
from abc import ABC, abstractmethod

from superai.log import logdecorator


class SuperTaskApiMixin(ABC):
    @abstractmethod
    def request(self, uri, method, body_params=None, query_params=None, required_api_key=False, header_params=None):
        pass

    @logdecorator.log_on_start(
        logging.DEBUG,
        "TaskTemplate get {task_template_name:s}",
    )
    @logdecorator.log_on_end(
        logging.DEBUG,
        "TaskTemplate get {task_template_name:s} {result!s}",
    )
    @logdecorator.log_on_error(
        logging.WARNING,
        "Error on TaskTemplate get {task_template_name:s} {e!r}",
        on_exceptions=Exception,
        reraise=True,
    )
    def get_supertask(self, task_template_name, **kwargs):
        """Fetch a given resource

        Args:
            task_template_name (str): The supertask identifier
                (required)
            x_fields (str): An optional fields mask

        Returns:
            DataProgram
        """

        all_params = [
            "task_template_name",
            "x_fields",
            "_return_http_data_only",
            "_preload_content",
            "_request_timeout",
        ]

        params = locals()
        for key, val in params["kwargs"]:
            if key not in all_params:
                raise TypeError(f"Got an unexpected keyword argument '{key}' to method get_supertask")
            params[key] = val
        del params["kwargs"]
        # verify the required parameter 'task_template_name' is set
        if "task_template_name" not in params or params["task_template_name"] is None:
            raise ValueError("Missing the required parameter `task_template_name` when calling `get_supertask`")

        collection_formats = {}

        path_params = {}
        if "task_template_name" in params:
            path_params["template_name"] = params["task_template_name"]

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
        uri = "task-templates/{template_name}".format(**path_params)
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
        "List supertasks",
    )
    @logdecorator.log_on_end(
        logging.DEBUG,
        "List supertasks response: {result!s}",
    )
    @logdecorator.log_exception(
        logging.ERROR,
        "Error on list supertask {e!r}",
        on_exceptions=Exception,
        reraise=True,
    )
    def list_supertasks(self, **kwargs):
        """List all templates (Tags param is mock)

        Args:
            page (int)
            size (int)
            sort_by (str)
            order_by (str)
            only_owned_or_group (bool)
            input_types (list[str])
            output_types (list[str])
            tags (list[str])
            x_fields (str): An optional fields mask

        Returns:
            TemplatesList
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
            "_return_http_data_only",
            "_preload_content",
            "_request_timeout",
        ]

        params = locals()
        for key, val in params["kwargs"]:
            if key not in all_params:
                raise TypeError(f"Got an unexpected keyword argument '{key}' to method list_templates")
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
            endpoint="task_templates",
            method="GET",
            query_params=query_params,
            body_params=body_params,
            header_params=header_params,
            required_api_key=True,
        )

    @logdecorator.log_on_start(
        logging.DEBUG,
        "TaskTemplate put {task_template_name:s} with body {body}",
    )
    @logdecorator.log_on_end(
        logging.DEBUG,
        "TaskTemplate put {task_template_name:s} {result!s}",
    )
    @logdecorator.log_exception(
        logging.ERROR,
        "Error on TaskTemplate put {task_template_name:s} {e!r}",
        on_exceptions=Exception,
        reraise=True,
    )
    def put_supertask(self, task_template_name, body, **kwargs):
        """Create or update a supertask given its full qualified name

        If the supertask already exists and it is owned by  somebody else then if will throw a 409

        Args:
            body (SuperTask): (required)
            task_template_name (str): The supertask identifier
                (required)
            x_fields (str): An optional fields mask

        Returns:
            SuperTask
        """

        all_params = [
            "body",
            "task_template_name",
            "x_fields",
            "_return_http_data_only",
            "_preload_content",
            "_request_timeout",
        ]

        body["type"] = "SUPER_TASK"
        params = locals()
        for key, val in params["kwargs"]:
            if key not in all_params:
                raise TypeError(f"Got an unexpected keyword argument '{key}' to method update_template")
            params[key] = val
        del params["kwargs"]
        # verify the required parameter 'body' is set
        if "body" not in params or params["body"] is None:
            raise ValueError("Missing the required parameter `body` when calling `update_template`")
        # verify the required parameter 'task_template_name' is set
        if "task_template_name" not in params or params["task_template_name"] is None:
            raise ValueError("Missing the required parameter `task_template_name` when calling `update_template`")

        collection_formats = {}

        path_params = {"template_name": params["task_template_name"]}
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

        uri = "task-templates/{template_name}".format(**path_params)
        return self.request(
            endpoint=uri,
            method="PUT",
            query_params=query_params,
            body_params=body_params,
            header_params=header_params,
            required_api_key=True,
            required_auth_token=True,
        )

    @logdecorator.log_on_start(
        logging.DEBUG,
        "TaskTemplate update {task_template_name:s} with body {body}",
    )
    @logdecorator.log_on_end(
        logging.DEBUG,
        "TaskTemplate update {task_template_name:s} {result!s}",
    )
    @logdecorator.log_exception(
        logging.ERROR,
        "Error on TaskTemplate update {task_template_name:s} {e!r}",
        on_exceptions=Exception,
        reraise=True,
    )
    def update_supertask(self, task_template_name, body, **kwargs):
        """This is a proxy method for put_supertask. See above

        Args:
            body (SuperTask): (required)
            task_template_name (str): The supertask identifier
                (required)
            x_fields (str): An optional fields mask

        Returns:
            SuperTask
        """
        return self.put_supertask(task_template_name, body)

    @logdecorator.log_on_start(
        logging.DEBUG,
        "SuperTask create {supertask_name:s} with body {body}",
    )
    @logdecorator.log_on_end(
        logging.DEBUG,
        "SuperTask create {supertask_name:s} {result!s}",
    )
    @logdecorator.log_exception(
        logging.ERROR,
        "Error on SuperTask create {supertask_name:s} {e!r}",
        on_exceptions=Exception,
        reraise=True,
    )
    def create_supertask(self, supertask_name, body, **kwargs):
        """This is a proxy method for put_supertask. See above

        Args:
            body (SuperTask): (required)
            supertask_name (str): The supertask identifier (required)
            x_fields (str): An optional fields mask

        Returns:
            SuperTask
        """
        return self.put_supertask(supertask_name, body)

    def delete_supertask(self, dp_qualified_name, supertask_name):
        """SuperTask deletion

        Args:
            supertask_name (str): The supertask identifier (required)

        Returns:
            The new list of supertasks
        """
        template = self.get_supertask(dp_qualified_name)
        supertask_list = template.get("dpSuperTasks", []) or []
        if supertask_name not in supertask_list:
            raise ValueError("The supertask you want to delete is not present in the supertasks of the DP you provided")

        supertask_list.remove(supertask_name)
        body = {"supertasks": supertask_list}
        updated_template = self.update_supertask(task_template_name=dp_qualified_name, body=body)
        assert supertask_name not in updated_template.get("dpSuperTasks")
        return supertask_list
