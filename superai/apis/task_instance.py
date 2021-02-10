import uuid
from typing import Dict, List, Union

from superai.data_program.base import DataProgramBase


# TODO: refactor api and add to client mixin
class TaskInstance(DataProgramBase):
    def __init__(
        self,
        task_template_id: Union[int, float],
        quality=None,
        cost=None,
        latency=None,
        name=None,
        description=None,
        **kwargs,
    ):
        super().__init__()
        self.task_template_id = task_template_id
        self.quality = quality
        self.cost = cost
        self.latency = latency
        self.__dict__.update(kwargs)

        self.__task_instance_object = self.__create_task_instance(
            task_template_id=task_template_id,
            performance={"quality": quality, "cost": cost, "latency": latency},
            name=name,
            description=description,
        )

        assert "id" in self.__task_instance_object
        self.task_instance_id = self.__task_instance_object["id"]

    def __create_task_instance(
        self, task_template_id: Union[int, float], performance: Dict = None, name: str = None, description: str = None
    ) -> Dict:
        """
        Create a task instance
        :param parameters:
        :param performance:
        :param name:
        :param description:
        :return:
        """
        body_json = {}
        if performance is not None:
            body_json["performance"] = performance
        if name is None:
            body_json["name"] = f"TaskName-{uuid.uuid5()}"
        if description is not None:
            body_json["description"] = description
        uri = f"task_template/{task_template_id}/instance"
        return self._request(uri, method="POST", body_params=body_json, required_api_key=False)

    def process(self, inputs: List[Dict]) -> Dict:
        """
        :param inputs:
        :return:
        """
        body_json = {"inputs": inputs, "job_type": "normal"}
        if self.quality is not None:
            body_json["quality"] = self.quality
        if self.cost is not None:
            body_json["cost"] = self.cost
        if self.latency is not None:
            body_json["latency"] = self.latency
        uri = f"task_instance/{self.task_instance_id}/process"
        return self._request(uri, method="POST", body_params=body_json, required_api_key=False)
