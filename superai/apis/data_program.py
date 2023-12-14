from __future__ import absolute_import

import logging
from abc import abstractmethod

from superai.apis.workflow import WorkflowApiMixin
from superai.log import logdecorator


class DataProgramApiMixin(WorkflowApiMixin):
    @abstractmethod
    def request(self, uri, method, body_params=None, query_params=None, required_api_key=False, header_params=None):
        pass

    @logdecorator.log_on_start(
        logging.DEBUG,
        "DataProgram get {template_name:s}",
    )
    @logdecorator.log_on_end(
        logging.DEBUG,
        "DataProgram get {template_name:s} {result!s}",
    )
    @logdecorator.log_exception(
        logging.ERROR,
        "Error on DataProgram get {template_name:s} {e!r}",
        on_exceptions=Exception,
        reraise=True,
    )
    def get_template(self, template_name, **kwargs):
        """Fetches a Data Program's dataprogram.

        Args:
            template_name: The Data Program dataprogram name (required)
            x_fields: An optional fields mask

        Returns:
            DataProgram
        """

        return self.get_workflow(template_name, **kwargs)

    @logdecorator.log_on_start(
        logging.DEBUG,
        "DataProgram list",
    )
    @logdecorator.log_exception(
        logging.ERROR,
        "Error on DataProgram list {e!r}",
        on_exceptions=Exception,
        reraise=True,
    )
    def list_templates(self, **kwargs):
        """Lists all templates (Tags param is mock).

        Args:
            page:
            size:
            sort_by:
            order_by:
            only_owned_or_group:
            input_types:
            output_types:
            tags:
            x_fields: An optional fields mask.

        Returns:
            TemplatesList.
        """
        # TODO: Filter all router workflows
        return self.list_workflows()

    @logdecorator.log_on_start(
        logging.DEBUG,
        "DataProgram update {template_name:s} with body {body}",
    )
    @logdecorator.log_on_end(logging.DEBUG, "DataProgram update {template_name:s} {result!s}")
    @logdecorator.log_exception(
        logging.ERROR,
        "Error on DataProgram update {template_name:s} {e!r}",
        on_exceptions=Exception,
        reraise=True,
    )
    def update_template(self, template_name, body, **kwargs):
        """Creates or updates a Data Program given its full qualified name. If the Data Program already exists and it is owned by somebody else, then if will return a 409.

        Args:
            DataProgram body: (required)
            template_name: The Data Program identifier (required).
            x_fields: An optional fields mask.

        Returns:
            DataProgram.
        """
        return self.update_workflow(workflow_name=template_name, body=body, **kwargs)

    @logdecorator.log_on_start(
        logging.DEBUG,
        "DataProgram create {template_name:s} with body {body}",
    )
    @logdecorator.log_on_end(logging.DEBUG, "DataProgram create {template_name:s} {result!s}")
    @logdecorator.log_exception(
        logging.ERROR,
        "Error on DataProgram create {template_name:s} {e!r}",
        on_exceptions=Exception,
        reraise=True,
    )
    def create_template(self, body, template_name, **kwargs):
        """Creates or updates a Data Program given its full qualified name. If the Data Program already exists, and it
        is owned by somebody else, then it will return a 409.

        Args:
            body: (required)
            template_name: The Data Program identifier (required).
            x_fields: An optional fields mask.

        Returns:
            DataProgram.
        """
        template_name = f"{template_name}.router" if "." not in template_name else template_name
        return self.create_workflow(workflow_name=template_name, body=body, **kwargs)
