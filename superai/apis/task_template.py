from typing import Dict, List, Union

from superai.data_program.base import DataProgramBase


class TaskTemplate(DataProgramBase):
    def __init__(self, dp_definition: Dict, name: str = None, description: str = None):
        assert "input_schema" in dp_definition
        assert "output_schema" in dp_definition

        super().__init__()

        self.dp_definition = dp_definition
        self.__dict__.update(dp_definition)
        self.workflows = []
        self.task_templates = []

        self.description = description
        self.name = name

        # look in ~/.netrc file to find token
        # if not assume not logged in
        # self.api_key = api_key
        # self.auth_token = auth_token
        # self.base_url = BASE_URL

        self.__task_template_object = self._create_task_template(
            workflow_id=1,
            input_schema=dp_definition["input_schema"],
            output_schema=dp_definition["output_schema"],
            name=self.name,
            description=self.description,
        )
        # TODO: Reenable this once the task template REST API is fixed
        # assert "id" in self.__task_template_object
        # self.task_template_id = self.__task_template_object["id"]

    def _create_task_template(
        self,
        workflow_id: Union[int, float],
        input_schema: Dict,
        output_schema: Dict,
        name: str = None,
        description: str = None,
    ) -> Dict:
        """
        Create a task template
        :param input_schema:
        :param output_schema:
        :return:
        """
        body_json = {
            "input_schema": input_schema,
            "output_schema": output_schema,
        }
        if name is not None:
            body_json["name"] = name
        if description is not None:
            body_json["description"] = description

        ## Assuming that a workflow can get a task
        ## TODO:
        #   1.Fix: I couldn't find the appropriate API controller. I'm assuming that the task contoller has some REST methods missing
        # uri = f'workflow/{workflow_id}/task'
        # return self._request(uri, method='POST', body_params=body_json, required_api_key=False)

    def process(self, inputs: List, quality=None, cost=None, latency=None) -> Dict:
        """
        :param inputs:
        :return:
        """
        body_json = {
            "inputs": inputs,
        }
        if quality is not None:
            body_json["quality"] = quality
        if cost is not None:
            body_json["cost"] = cost
        if latency is not None:
            body_json["latency"] = latency
        uri = f"task_template/{self.task_template_id}/process"
        return self._request(uri, method="POST", body_params=body_json, required_api_key=False)
