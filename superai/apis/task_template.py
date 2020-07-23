from typing import List, Generator, Dict
import names

from superai.apis.data_program_base import DataProgramBase

class TaskTemplate(DataProgramBase):
    def __init__(self, dp_definition: Dict, name: str=None, description: str=None):
        assert "input_schema" in dp_definition
        assert "output_schema" in dp_definition

        self.dp_definition = dp_definition
        self.__dict__.update(dp_definition)
        self.workflows = []
        self.task_templates = []

        if name is None:
            self.name = names.get_first_name()

        self.description = description

        # look in ~/.netrc file to find token
        # if not assume not logged in
        # self.api_key = api_key
        # self.auth_token = auth_token
        # self.base_url = BASE_URL

        self.__template_object = self.__create_template(
            input_schema=dp_definition['input_schema'],
            output_schema=dp_definition['input_schema'],
            parameter_schema=dp_definition.get('parameter_schema'),
            name=self.name,
            description=self.description
        )
        assert "id" in self.__template_object
        self.template_id = self.__template_object["id"]

    def __create_template(self, input_schema: Dict, output_schema: Dict, parameter_schema: Dict = None,
                          name: str = None,
                          description: str = None) -> Dict:
        """
        Create a data program template
        :param input_schema:
        :param output_schema:
        :param parameter_schema:
        :return:
        """
        body_json = {
            "input_schema": input_schema,
            "output_schema": output_schema,
        }
        if parameter_schema is not None:
            body_json['parameter_schema'] = parameter_schema
        if name is not None:
            body_json['name'] = name
        if description is not None:
            body_json['description'] = description
        uri = f'template'
        return self._request(uri, method='POST', body_params=body_json, required_api_key=False)

    def label(self, inputs: List, quality=None, cost=None, latency=None) -> Dict:
        """
        :param inputs:
        :return:
        """
        body_json = {
            "inputs": inputs,
        }
        if quality is not None:
            body_json['quality'] = quality
        if cost is not None:
            body_json['cost'] = cost
        if latency is not None:
            body_json['latency'] = latency
        uri = f'template/{self.template_id}/label'
        return self._request(uri, method='POST', body_params=body_json, required_api_key=False)




