from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from superai.data_program import DataProgram

from superai import Client
from superai.log import logger
from superai.utils import load_api_key, load_auth_token, load_id_token

log = logger.get_logger(__name__)


class Router(ABC):
    def __init__(
        self,
        name: str = "router",
        dataprogram: "DataProgram" = None,
        client: Client = None,
        **kwargs,
    ):
        """
        Args:
            workflows:
            metrics:
            prefix:
            name:
        """
        if name not in ["router", "training"]:
            raise AttributeError("Router name is constraint to 'router' or 'training'")

        self.name = name
        self.client = client or Client(
            api_key=load_api_key(),
            auth_token=load_auth_token(),
            id_token=load_id_token(),
        )
        self.dataprogram = dataprogram
        self.workflows = dataprogram.workflows
        self.kkwargs = kwargs

    def validate(self):
        self.validate_workflow_attribute("prefix")
        self.validate_workflow_attribute("input_schema")
        self.validate_workflow_attribute("parameter_schema")
        self.validate_workflow_attribute("output_schema")

    def validate_workflow_attribute(self, attr: str):
        if not hasattr(self, attr):
            log.warning(f"{self.name} missing attribute {attr}")

        for workflow in self.workflows:
            if not hasattr(workflow, attr):
                log.warning(f"workflow {workflow.name} missing attribute {attr}")

            if getattr(self, attr) != getattr(workflow, attr):
                log.warning(
                    f"{self.name} with {attr}: {getattr(self, attr)} has workflow {workflow.name} with"
                    f" {attr}: {getattr(workflow, attr)}"
                )

    @abstractmethod
    def subscribe_wf(self):
        pass
