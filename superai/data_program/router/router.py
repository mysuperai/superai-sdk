import os
from abc import ABC, abstractmethod
from typing import Dict, List

from superai import Client
from superai.data_program import Workflow
from superai.log import logger

log = logger.get_logger(__name__)


class Router(ABC):
    def __init__(
        self,
        prefix: str = os.getenv("WF_PREFIX"),
        name: str = "router",
        client: Client = None,
        dp_definition: Dict = None,
        workflows: List[Workflow] = None,
        **kwargs,
    ):
        """

        :param workflows:
        :param metrics:
        :param prefix:
        :param name:
        """
        self.prefix = prefix
        self.name = name
        self.client = client
        self.dp_definition = dp_definition
        self.workflows = workflows
        self.kkwargs = kwargs

    @abstractmethod
    def subscribe_wf(self):
        pass
