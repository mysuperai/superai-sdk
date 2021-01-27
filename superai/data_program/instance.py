import atexit
import os
import webbrowser
from typing import Dict, List, Union

from colorama import Fore, Style

from superai.log import logger
from .base import DataProgramBase
from .task import Worker
from .template import Template
from .utils import IgnoreInAgent
from .. import Client
from ..utils import load_api_key

log = logger.get_logger(__name__)


class SuperAI:
    def __init__(
        self,
        template_name: str = None,
        template: Template = None,
        quality=None,
        cost=None,
        latency=None,
        name=None,
        description=None,
        dp_definition: Dict = None,
        uuid: str = None,
        force_update: bool = None,
        run_template=True,
        client: Client = None,
        **kwargs,
    ):
        self.quality = quality
        self.cost = cost
        self.latency = latency
        self.__dict__.update(kwargs)
        self.template: Template = template
        self.template_name = template_name
        self.client = client if client else Client(api_key=load_api_key())
        # If the template_name is not specified we assume that the data programmer's intention is to create a basic data
        # program template in order to quickly check how the data annotation works. Therefore we create a template from
        # the dp_definition
        if not self.template:
            self.template = Template(name=template_name, definition=dp_definition)
            self.template_name = self.template.name

        # TODO: 1. Load template if exists
        # else:
        #     self.template = load_template()

        # Last thing we do is running the template
        if run_template:
            self.template.start()

        # Everything after this line can be ignored once the data program™ is already deployed
        if os.environ.get("IN_AGENT"):
            log.info(f"[SuperAI.__create_instance] ignoring because IN_AGENT = " f"{os.environ.get('IN_AGENT')}")
            return

        performance_dict = {"quality": quality, "cost": cost, "latency": latency}
        log.info("[SuperAI.__init__] loading/creating instance")

        self.__instance_object = self.__create_instance(
            parameters=kwargs,
            performance=performance_dict,
            name=name,
            description=description,
            uuid=uuid,
        )
        log.info(f"[SuperAI.__init__] DataProgram: {self.__instance_object}")

        # TODO: Use sys.excepthook
        try:
            assert "uuid" in self.__instance_object
            assert self.template.qualified_name == self.__instance_object["templateName"], (
                f"Instance is already registered to template {self.__instance_object['templateName']} "
                f"but expected {self.template.qualified_name}"
            )

            if uuid:
                assert uuid == self.__instance_object["uuid"]
        except Exception as e:
            atexit.unregister(DataProgramBase.run_thread)
            raise e
        self.instance_uuid = self.__instance_object["uuid"]
        self.name = self.__instance_object["name"]

    def __create_instance(
        self,
        parameters: Dict = None,
        template_uuid: Union[int, float] = None,
        performance: Dict = None,
        name: str = None,
        description: str = None,
        uuid: str = None,
    ) -> Dict:
        """
        TODO: 1. How can we find out that the DP has an active backend or if we need to run a local one?
                -> We could monitor ECS tasks created from containers. We would need to monitor this using a cron job
                or a lambda and store this information into a DB (probably turbine). The problem is that even with this
                information we won't know if the ECS is having any issues processing jobs
        Create a data program instance.
        :param parameters:
        :param performance:
        :param name:
        :param description:
        :return:
        """
        if template_uuid is not None:
            raise NotImplementedError(
                "Current version doesn't offer support to create DataPrograms using only the template id"
            )

        body_json = {}
        body_json["templateName"] = f"{self.template.name}.router"
        body_json["appName"] = name if name else f"{self.template.name}"
        if parameters is not None:
            # TODO: Send only schema values until the rest of the infrastructure supports self contained schemas (definition_v1,v2)
            body_json["appParams"] = self._extract_schema_values(parameters)
        if performance is not None:
            body_json["appMetrics"] = (
                {"metrics": performance}
                if performance.get("quality") or performance.get("latency") or performance.get("cost")
                else {"metric": {}}
            )

        # TODO: Add parameter
        body_json["canoticCrowd"] = True

        # TODO: Add description support in nacelle
        # if description is not None:
        #     body_json['description'] = description

        if uuid:
            return self.client.get_superai(uuid)
        else:
            return self.client.create_superai(body=body_json)

    # TODO: Implementation
    def _extract_schema_values(self, parameters):
        """

        Given the following json-schema object:
        {
           "params": {
             "type": "object",
             "properties": {
               "instructions": {
                 "type": "text",
                 "schema_instance": "My simple instruction"
               },
               "choices": [
                 {
                   "value": "0",
                   "tag": "0"
                 },
                 {
                   "value": "1",
                   "tag": "1"
                 },
               ]
             },
             "required": [
               "instructions",
               "choices"
             ]
           }
         }
         this function should return an object in the form:
             {
               "params": {
                 "instructions": "My simple instruction",
                 "choices": [
                   "0",
                   "1"
                 ]
               }
             }
        """

        return parameters

    def run_thread(self):
        # TODO:
        #  1. Get template object
        #  2. Invoke run() on template to deploy local
        pass

    @IgnoreInAgent
    def process(
        self,
        inputs: List[Dict],
        worker: Worker = Worker.me,
        open_browser: bool = False,
        force_single_submission: bool = False,
    ) -> Dict:
        """
        :param inputs:
        :return:
        """
        # TODO: 1. The result of this API should be an http request that the sdk/use can call to get the answer. We
        #       already get the job_uuid we just need to be able to display it in dash. Q: How to differentiate if the
        #       job should be annotated or if we just should show the result
        log.info(Fore.BLUE + f"Labeling {len(inputs)} jobs with Worker {worker}" + Style.RESET_ALL)
        labels = []
        if len(inputs) > 20 and not force_single_submission:
            labels.append(self.client.create_jobs(app_id=self.instance_uuid, inputs=inputs, worker=worker))
        else:
            for input in inputs:
                labels.append(self.client.create_jobs(app_id=self.instance_uuid, inputs=[input], worker=worker))
        log.info(f"Labels response: {labels}")

        url = f"https://dev.super.ai/dashboard/projects/{self.instance_uuid}"
        if open_browser:
            url = f"{url}/tasks" if worker == worker.me else f"{url}/jobs"
            log.info(Fore.BLUE + f"Open {url} to see your jobs" + Style.RESET_ALL)
            webbrowser.open(
                url,
                new=2,
            )

        log.info(f"Click here to go to your Dashboard: {Fore.BLUE}{url}{Style.RESET_ALL}/jobs")

        return labels
