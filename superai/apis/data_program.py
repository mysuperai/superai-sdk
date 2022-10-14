from __future__ import absolute_import

import logging
from abc import abstractmethod

from superai.apis.workflow import WorkflowApiMixin
from superai.log import logdecorator


class DataProgramApiMixin(WorkflowApiMixin):
    @abstractmethod
    def request(self, uri, method, body_params=None, query_params=None, required_api_key=False):
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
        """Fetch a data program dataprogram

        :param str template_name: The data program dataprogram name (required)
        :param str x_fields: An optional fields mask
        :return: DataProgram
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
        """Create or update a dataprogram given its full qualified name

        If the dataprogram already exists and it is owned by  somebody else then if will throw a 409

        :param DataProgram body: (required)
        :param str template_name: The dataprogram identifier (required)
        :param str x_fields: An optional fields mask
        :return: DataProgram
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
        """Create or update a dataprogram given its full qualified name

        If the dataprogram already exists and it is owned by  somebody else then if will throw a 409

        :param DataProgram body: (required)
        :param str template_name: The dataprogram identifier (required)
        :param str x_fields: An optional fields mask
        :return: DataProgram
        """
        template_name = f"{template_name}.router" if not "." in template_name else template_name
        return self.create_workflow(workflow_name=template_name, body=body, **kwargs)
