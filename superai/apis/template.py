from __future__ import absolute_import

import logging
import re  # noqa: F401
from abc import abstractmethod

# python 2 and python 3 compatibility library
from colorama import Fore, Style

from superai.apis.workflow import WorkflowApiMixin
from superai.log import logdecorator


class TemplateApiMixin(WorkflowApiMixin):
    @abstractmethod
    def request(self, uri, method, body_params=None, query_params=None, required_api_key=False):
        pass

    @logdecorator.log_on_start(
        logging.DEBUG,
        Fore.CYAN + "Template get {template_name:s}" + Style.RESET_ALL,
    )
    @logdecorator.log_on_end(
        logging.DEBUG,
        Fore.CYAN + "Template get {template_name:s} {result!s}" + Style.RESET_ALL,
    )
    @logdecorator.log_exception(
        logging.ERROR,
        Fore.RED + "Error on Template get {template_name:s} {e!r}" + Style.RESET_ALL,
        on_exceptions=Exception,
        reraise=True,
    )
    def get_template(self, template_name, **kwargs):
        """Fetch a data program template

        :param str template_name: The data program template name (required)
        :param str x_fields: An optional fields mask
        :return: Template
        """

        template_name = f"{template_name}.router" if not "." in template_name else template_name

        return self.get_workflow(template_name, **kwargs)

    @logdecorator.log_on_start(
        logging.DEBUG,
        Fore.CYAN + "Template list" + Style.RESET_ALL,
    )
    @logdecorator.log_exception(
        logging.ERROR,
        Fore.RED + "Error on Template list {e!r}" + Style.RESET_ALL,
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
        Fore.CYAN + "Template update {template_name:s} with body {body}" + Style.RESET_ALL,
    )
    @logdecorator.log_on_end(
        logging.DEBUG, Fore.CYAN + "Template update {template_name:s} {result!s}" + Style.RESET_ALL
    )
    @logdecorator.log_exception(
        logging.ERROR,
        Fore.RED + "Error on Template update {template_name:s} {e!r}" + Style.RESET_ALL,
        on_exceptions=Exception,
        reraise=True,
    )
    def update_template(self, template_name, body, **kwargs):
        """Create or update a template given its full qualified name

        If the template already exists and it is owned by  somebody else then if will throw a 409

        :param Template body: (required)
        :param str template_name: The template identifier (required)
        :param str x_fields: An optional fields mask
        :return: Template
        """
        template_name = f"{template_name}.router" if not "." in template_name else template_name
        return self.update_workflow(workflow_name=template_name, body=body, **kwargs)

    @logdecorator.log_on_start(
        logging.DEBUG,
        Fore.CYAN + "Template create {template_name:s} with body {body}" + Style.RESET_ALL,
    )
    @logdecorator.log_on_end(
        logging.DEBUG, Fore.CYAN + "Template create {template_name:s} {result!s}" + Style.RESET_ALL
    )
    @logdecorator.log_exception(
        logging.ERROR,
        Fore.RED + "Error on Template create {template_name:s} {e!r}" + Style.RESET_ALL,
        on_exceptions=Exception,
        reraise=True,
    )
    def create_template(self, body, template_name, **kwargs):
        """Create or update a template given its full qualified name

        If the template already exists and it is owned by  somebody else then if will throw a 409

        :param Template body: (required)
        :param str template_name: The template identifier (required)
        :param str x_fields: An optional fields mask
        :return: Template
        """
        template_name = f"{template_name}.router" if not "." in template_name else template_name
        return self.create_workflow(workflow_name=template_name, body=body, **kwargs)
