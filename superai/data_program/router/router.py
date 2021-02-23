import os
from abc import ABC, abstractmethod
from typing import Dict, List
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from superai.data_program import DataProgram

from superai import Client

from ..workflow import Workflow
from superai.log import logger

log = logger.get_logger(__name__)


class Router(ABC):
    def __init__(
        self,
        name: str = "router",  # Can't get overriden for now
        dataprorgam: "DataProgram" = None,
        client: Client = None,
        **kwargs,
    ):
        """

        :param workflows:
        :param metrics:
        :param prefix:
        :param name:
        """
        if name != "router":
            raise AttributeError("Router name is constraint to 'router'")

        self.name = name
        self.client = client
        self.dataprogram = dataprorgam
        self.kkwargs = kwargs

    @abstractmethod
    def subscribe_wf(self):
        pass
