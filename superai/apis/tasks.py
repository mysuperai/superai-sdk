import json
import time
from abc import ABC, abstractmethod
from datetime import datetime
from io import BytesIO
from typing import List, Optional
from zipfile import ZipFile

import requests

from superai.log import logger

log = logger.get_logger(__name__)


class TasksApiMixin(ABC):
    @abstractmethod
    def request(self, uri, method, body_params=None, query_params=None, required_api_key=False):
        pass

    def download_tasks(
        self,
        app_id: str,
        createdStartDate: datetime = None,
        createdEndDate: datetime = None,
        completedStartDate: datetime = None,
        completedEndDate: datetime = None,
        statusIn: List[str] = None,
    ) -> dict:
        """
        Trigger download of tasks data that can be retrieved using task operation id.
        :param app_id: Application id
        :param createdStartDate: Filter by created start date of tasks
        :param createdEndDate: Filter by created end date of tasks
        :param completedStartDate: Filter by completed start date of tasks
        :param completedEndDate: Filter by completed end date of tasks
        :param statusIn: Filter by status of tasks
        :return: Dict with task operationId key to track status
        """
        uri = f"apps/{app_id}/tasks-download"
        query_params = {}
        if createdStartDate is not None:
            query_params["createdStartDate"] = createdStartDate.strftime("%Y-%m-%dT%H:%M:%SZ")
        if createdEndDate is not None:
            query_params["createdEndDate"] = createdEndDate.strftime("%Y-%m-%dT%H:%M:%SZ")
        if completedStartDate is not None:
            query_params["completedStartDate"] = completedStartDate.strftime("%Y-%m-%dT%H:%M:%SZ")
        if completedEndDate is not None:
            query_params["completedEndDate"] = completedEndDate.strftime("%Y-%m-%dT%H:%M:%SZ")
        if statusIn is not None:
            query_params["statusIn"] = statusIn
        return self.request(uri, method="POST", query_params=query_params, required_api_key=True)

    def get_tasks_operation(self, app_id: str, operation_id: int):
        """
        Fetch status of task operation given application id and operation id
        :param app_id: Application id
        :param operation_id: operation_id
        :return: Dict with operation information (id, status, and other fields)
        """
        uri = f"task-operations/{app_id}/{operation_id}"
        return self.request(uri, method="GET", required_api_key=True)

    def generates_downloaded_tasks_url(self, app_id: str, operation_id: int, secondsTtl: int = None):
        """
        Generates url to retrieve downloaded zip tasks given application id and
        operation id
        :param app_id: Application id
        :param operation_id: operation_id
        :param seconds_ttl: Seconds ttl for generated url. Default 60
        :return: Dict with field downloadUrl
        """
        uri = f"task-operations/{app_id}/{operation_id}/download-url"
        query_params = {}
        if secondsTtl is not None:
            query_params["secondsTtl"] = secondsTtl
        return self.request(uri, method="POST", query_params=query_params, required_api_key=True)

    def download_tasks_full_flow(
        self,
        app_id: str,
        createdStartDate: datetime = None,
        createdEndDate: datetime = None,
        completedStartDate: datetime = None,
        completedEndDate: datetime = None,
        statusIn: List[str] = None,
        timeout: int = 120,
        poll_interval: int = 3,
    ) -> Optional[List[dict]]:
        """
        Trigger download of tasks and polls every poll_interval seconds until it
        returns the list of tasks or None in case of timeout
        :param app_id: Application id
        :param createdStartDate: Filter by created start date of tasks
        :param createdEndDate: Filter by created end date of tasks
        :param completedStartDate: Filter by completed start date of tasks
        :param completedEndDate: Filter by completed end date of tasks
        :param statusIn: Filter by status of tasks
        :param timeout: Timeout in seconds
        :param poll_interval: Poll interval in seconds
        :return: List of dict of tasks
        """
        operation_id = self.download_tasks(
            app_id, createdStartDate, createdEndDate, completedStartDate, completedEndDate, statusIn
        )["operationId"]
        operation_completed = False
        start_poll_date = datetime.now()
        while not operation_completed or (datetime.now() - start_poll_date).seconds >= timeout:
            operation = self.get_tasks_operation(app_id, operation_id)
            log.info(f"Poll result: Operation {operation['id']} in status: {operation['status']}")
            if operation["status"] == "COMPLETED":
                operation_completed = True
            else:
                time.sleep(poll_interval)
        if not operation_completed:
            return None
        download_tasks_url = self.generates_downloaded_tasks_url(app_id, operation_id)["downloadUrl"]
        resp = requests.get(download_tasks_url)
        zipfile = ZipFile(BytesIO(resp.content))
        return json.load(zipfile.open(zipfile.namelist()[0]))
