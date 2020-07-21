from typing import List, Generator, Dict, Union
import names

from superai.apis.data_program_base import DataProgramBase


class DataProgramInstance(DataProgramBase):
    def __init__(self, template_id: Union[int, float], quality=None, cost=None, latency=None, name=None, description=None, **kwargs):
        self.template_id = template_id
        self.quality = quality
        self.cost = cost
        self.latency = latency
        self.__dict__.update(kwargs)

        self.__instance_object = self.__create_instance(template_id=template_id, parameters=kwargs, performance={
            "quality": quality,
            "cost": cost,
            "latency": latency
        }, name=name, description=description)

        assert "id" in self.__instance_object
        self.instance_id = self.__instance_object["id"]

    def __create_instance(self, template_id:Union[int, float], parameters: Dict=None, performance: Dict=None, name: str = None, description: str = None) -> Dict:
        """
        Create a data program instance
        :param parameters:
        :param performance:
        :param name:
        :param description:
        :return:
        """
        body_json = {}
        if parameters is not None:
            body_json['parameters'] = parameters
        if performance is not None:
            body_json['performance'] = performance
        if name is None:
            body_json['name'] = names.get_first_name()
        if description is not None:
            body_json['description'] = description
        uri = f'template/{template_id}/instance'
        return self._request(uri, method='POST', body_params=body_json, required_api_key=False)

    def label(self, inputs: List[Dict]) -> Dict:
        """
        :param inputs:
        :return:
        """
        body_json = {
            "inputs": inputs,
            "job_type": "normal"
        }
        if self.quality is not None:
            body_json['quality'] = self.quality
        if self.cost is not None:
            body_json['cost'] = self.cost
        if self.latency is not None:
            body_json['latency'] = self.latency
        uri = f'instance/{self.instance_id}/label'
        return self._request(uri, method='POST', body_params=body_json, required_api_key=False)
