from __future__ import absolute_import

import logging
from abc import ABC, abstractmethod

from superai.log import logdecorator


class WorkflowApiMixin(ABC):
    @abstractmethod
    def request(self, uri, method, body_params=None, query_params=None, required_api_key=False, header_params=None):
        pass

    @logdecorator.log_on_start(
        logging.DEBUG,
        "Workflow get {workflow_name:s}",
    )
    @logdecorator.log_on_end(
        logging.DEBUG,
        "Workflow get {workflow_name:s} {result!s}",
    )
    @logdecorator.log_exception(
        logging.ERROR,
        "Error on Workflow get {workflow_name:s} {e!r}",
        on_exceptions=Exception,
        reraise=True,
    )
    def get_workflow(self, workflow_name, **kwargs):
        """Fetches a given resource.

        Args:
            str workflow_name: The workflow identifier (required)
            str x_fields: An optional fields mask

        Returns:
            DataProgram
        """

        all_params = ["workflow_name", "x_fields", "_return_http_data_only", "_preload_content", "_request_timeout"]

        params = locals()
        for key, val in params["kwargs"].items():
            if key not in all_params:
                raise TypeError(f"Got an unexpected keyword argument '{key}' to method get_template")
            params[key] = val
        del params["kwargs"]
        # verify the required parameter 'workflow_name' is set
        if "workflow_name" not in params or params["workflow_name"] is None:
            raise ValueError("Missing the required parameter `workflow_name` when calling `get_template`")

        collection_formats = {}

        path_params = {"template_name": params["workflow_name"]}
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
            header_params=header_params,
            required_api_key=True,
        )

    @logdecorator.log_on_start(
        logging.DEBUG,
        "List workflows",
    )
    @logdecorator.log_on_end(
        logging.DEBUG,
        "List workflows response: {result!s}",
    )
    @logdecorator.log_exception(
        logging.ERROR,
        "Error on list workflow {e!r}",
        on_exceptions=Exception,
        reraise=True,
    )
    def list_workflows(self, **kwargs):
        """Lists all templates (Tags param is mock).

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
        for key, val in params["kwargs"].items():
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
            endpoint="templates",
            method="GET",
            query_params=query_params,
            body_params=body_params,
            header_params=header_params,
            required_api_key=True,
        )

    @logdecorator.log_on_start(
        logging.DEBUG,
        "Workflow put {workflow_name:s} with body {body}",
    )
    @logdecorator.log_on_end(
        logging.DEBUG,
        "Workflow put {workflow_name:s} {result!s}",
    )
    @logdecorator.log_exception(
        logging.ERROR,
        "Error on Workflow put {workflow_name:s} {e!r}",
        on_exceptions=Exception,
        reraise=True,
    )
    def put_workflow(self, workflow_name, body, **kwargs):
        """Creates or updates a workflow given its full qualified name. If the workflow already exists and
        it is owned by somebody else, then if will return a 409.

        Args:
            Workflow body: (required)
            str workflow_name: The workflow identifier (required)
            str x_fields: An optional fields mask

        Returns:
            Workflow
        """

        all_params = [
            "body",
            "workflow_name",
            "x_fields",
            "_return_http_data_only",
            "_preload_content",
            "_request_timeout",
        ]

        params = locals()
        for key, val in params["kwargs"].items():
            if key not in all_params:
                raise TypeError(f"Got an unexpected keyword argument '{key}' to method update_template")
            params[key] = val
        del params["kwargs"]
        # verify the required parameter 'body' is set
        if "body" not in params or params["body"] is None:
            raise ValueError("Missing the required parameter `body` when calling `update_template`")
        # verify the required parameter 'workflow_name' is set
        if "workflow_name" not in params or params["workflow_name"] is None:
            raise ValueError("Missing the required parameter `workflow_name` when calling `update_template`")

        collection_formats = {}

        path_params = {"template_name": params["workflow_name"]}
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
        "Workflow update {workflow_name:s} with body {body}",
    )
    @logdecorator.log_on_end(
        logging.DEBUG,
        "Workflow update {workflow_name:s} {result!s}",
    )
    @logdecorator.log_exception(
        logging.ERROR,
        "Error on Workflow update {workflow_name:s} {e!r}",
        on_exceptions=Exception,
        reraise=True,
    )
    def update_workflow(self, workflow_name, body, **kwargs):
        """This is a proxy method for put_workflow. See above.

        Args:
            Workflow body: (required)
            str workflow_name: The workflow identifier (required)
            str x_fields: An optional fields mask

        Returns:
            Workflow
        """
        return self.put_workflow(workflow_name, body)

    @logdecorator.log_on_start(
        logging.DEBUG,
        "Workflow create {workflow_name:s} with body {body}",
    )
    @logdecorator.log_on_end(
        logging.DEBUG,
        "Workflow create {workflow_name:s} {result!s}",
    )
    @logdecorator.log_exception(
        logging.ERROR,
        "Error on Workflow create {workflow_name:s} {e!r}",
        on_exceptions=Exception,
        reraise=True,
    )
    def create_workflow(self, workflow_name, body, **kwargs):
        """This is a proxy method for put_workflow. See above.

        Args:
            Workflow body: (required)
            str workflow_name: The workflow identifier (required)
            str x_fields: An optional fields mask

        Returns:
            Workflow
        """
        return self.put_workflow(workflow_name, body)

    def delete_workflow(self, dp_qualified_name, workflow_name):
        """Workflow deletion

        Args:
            workflow_name (str): The workflow identifier (required)

        Returns:
            The new list of workflows
        """
        template = self.get_workflow(dp_qualified_name)
        workflow_list = template.get("dpWorkflows", []) or []
        if workflow_name not in workflow_list:
            raise ValueError("The workflow you want to delete is not present in the workflows of the DP you provided")

        workflow_list.remove(workflow_name)
        body = {"workflows": workflow_list}
        updated_template = self.update_workflow(workflow_name=dp_qualified_name, body=body)
        assert workflow_name not in updated_template.get("dpWorkflows")
        return workflow_list
