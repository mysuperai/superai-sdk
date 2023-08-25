import atexit
import webbrowser
from typing import Dict, List, Union

from superai.client import Client
from superai.config import get_current_env
from superai.log import logger
from superai.utils import load_api_key, load_auth_token, load_id_token

from . import WorkerType
from .base import DataProgramBase
from .data_program import DataProgram
from .utils import IgnoreInAgent

log = logger.get_logger(__name__)


class Project:
    def __init__(
        self,
        dp_name: str = None,
        dataprogram: DataProgram = None,
        quality=None,
        cost=None,
        latency=None,
        name=None,
        description=None,
        dp_definition: Dict = None,
        uuid: str = None,
        force_update: bool = None,
        run_dataprogram=True,
        client: Client = None,
        organisation=None,
        **kwargs,
    ):
        self.quality = quality
        self.cost = cost
        self.latency = latency
        self.__dict__.update(kwargs)
        self.dataprogram: DataProgram = dataprogram
        self.dp_name = dp_name
        self.client = client or Client(
            api_key=load_api_key(),
            auth_token=load_auth_token(),
            id_token=load_id_token(),
        )
        # If the dp_name is not specified we assume that the data programmer's intention is to create a basic data
        # program dataprogram in order to quickly check how the data annotation works. Therefore we create a dataprogram from
        # the dp_definition
        if not self.dataprogram and dp_definition:
            self.dataprogram = DataProgram(name=dp_name, definition=dp_definition)

        # TODO: 1. Load dataprogram if exists
        # else:
        #     self.dataprogram = load_template()

        # Last thing we do is running the dataprogram
        if run_dataprogram:
            self.dataprogram.start()

        # Everything after this line can be ignored once the data program™ is already deployed
        # FIXME: Is this necessary?
        # Commenting this out  for making DP work
        # if os.environ.get("IN_AGENT"):
        #    log.info(f"[Project.__create_project] ignoring because IN_AGENT = " f"{os.environ.get('IN_AGENT')}")
        #    return

        performance_dict = {"quality": quality, "cost": cost, "latency": latency}
        log.info("[Project.__init__] loading/creating instance")

        self.__project_obj = self.__create_project(
            parameters=kwargs,
            performance=performance_dict,
            name=name,
            description=description,
            uuid=uuid,
            organisation=organisation,
        )
        log.info(f"[Project.__init__] DataProgram: {self.__project_obj}")

        # TODO: Use sys.excepthook
        try:
            assert "uuid" in self.__project_obj
            if self.dataprogram:
                assert self.dataprogram.template_name == self.__project_obj["templateName"], (
                    f"Project is already registered to dataprogram {self.__project_obj['templateName']} "
                    f"but expected {self.dataprogram.template_name}"
                )

            if uuid:
                assert uuid == self.__project_obj["uuid"]
        except Exception as e:
            atexit.unregister(DataProgramBase.run_thread)
            raise e
        self.project_uuid = self.__project_obj["uuid"]
        self.name = self.__project_obj["name"]

        self.ai = None

    def __create_project(
        self,
        parameters: Dict = None,
        template_uuid: Union[int, float] = None,
        performance: Dict = None,
        name: str = None,
        description: str = None,
        uuid: str = None,
        organisation: str = None,
    ) -> Dict:
        """Creates a Data Program instance.

        Args:
            parameters:
            performance:
            name:
            description:
        """
        if template_uuid is not None:
            raise NotImplementedError(
                "Current version doesn't offer support to create DataPrograms using only the dataprogram uuid"
            )

        body_json = {}
        if not self.dataprogram:
            if not self.dp_name:
                raise ValueError(
                    "Dataprogram or dataprogram name needs to be defined for the current version to create a project"
                )
            if not name:
                raise ValueError("You need to provide a name for the project if the dataprogram is not defined")

        if self.dataprogram:
            template_name = self.dataprogram._name
        else:
            template_name = self.dp_name

        body_json["templateName"] = f"{template_name}.router"
        body_json["appName"] = name if name else f"{self.dataprogram._name}"
        if parameters is not None:
            # TODO: Send only schema values until the rest of the infrastructure supports self contained schemas (definition_v1,v2)
            body_json["appParams"] = self._sanitize_params(parameters)
        if performance is not None:
            body_json["appMetrics"] = (
                {"metrics": performance}
                if performance.get("quality") or performance.get("latency") or performance.get("cost")
                else {"metric": {}}
            )

        # TODO: Add parameter
        body_json["canoticCrowd"] = False

        # TODO: Add description support in nacelle
        # if description is not None:
        #     body_json['description'] = description

        if uuid:
            return self.client.get_project(uuid)
        else:
            return self.client.create_project(body=body_json, org=organisation)

    # TODO: Implementation
    def _sanitize_params(self, parameters):
        """Given the following json-schema object:
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

    @IgnoreInAgent
    def process(
        self,
        inputs: List[Dict],
        worker: WorkerType = WorkerType.me,
        open_browser: bool = False,
        force_single_submission: bool = False,
    ) -> Dict:
        """
        Args:
            inputs:
        """
        # TODO: 1. The result of this API should be an http request that the sdk/use can call to get the answer. We
        #       already get the job_uuid we just need to be able to display it in dash. Q: How to differentiate if the
        #       job should be annotated or if we just should show the result
        log.info(f"Labeling {len(inputs)} jobs with WorkerType {worker}")
        labels = []
        if len(inputs) > 20 and not force_single_submission:
            labels.append(self.client.create_jobs(app_id=self.project_uuid, inputs=inputs, worker=worker.value()))
        else:
            labels.extend(
                self.client.create_jobs(app_id=self.project_uuid, inputs=[inp], worker=worker.value()) for inp in inputs
            )
        log.info(f"Labels response: {labels}")

        url = self.get_url()
        if open_browser:
            url = f"{url}/tasks" if worker == worker.me else f"{url}/jobs"
            log.info(f"Open {url} to see your jobs")
            webbrowser.open(
                url,
                new=2,
            )

        log.info(f"Click here to go to your Dashboard: {url}/jobs")

        return labels

    def get_url(self):
        current_env = get_current_env()
        prefix = f"{current_env}." if current_env != "prod" else ""
        return f"https://{prefix}super.ai/dashboard/projects/{self.project_uuid}"

    def add_ai(self, ai, active_learning: bool = False):
        """Adds an AI to the project. You can use AI as a worker or for `active_learning`.

        Args:
            ai: an object of "superai.meta_ai.AI" class
            active_learning: If active_learning is to be used.
        """
        self.ai = ai
