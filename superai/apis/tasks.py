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
    def request(self, uri, method, body_params=None, query_params=None, required_api_key=False, header_params=None):
        pass

    def download_tasks(
        self,
        app_id: str,
        created_start_date: datetime = None,
        created_end_date: datetime = None,
        completed_start_date: datetime = None,
        completed_end_date: datetime = None,
        status_in: List[str] = None,
    ) -> dict:
        """Trigger download of tasks data that can be retrieved using task operation id.

        Args:
          app_id: Application id
          created_start_date: Filter by created start date of tasks
          created_end_date: Filter by created end date of tasks
          completed_start_date: Filter by completed start date of tasks
          completed_end_date: Filter by completed end date of tasks
          status_in: Filter by status of tasks

        Returns:
          Dict with task operationId key to track status

        """
        uri = f"apps/{app_id}/tasks-download"
        query_params = {}
        if created_start_date is not None:
            query_params["createdStartDate"] = created_start_date.strftime("%Y-%m-%dT%H:%M:%SZ")
        if created_end_date is not None:
            query_params["createdEndDate"] = created_end_date.strftime("%Y-%m-%dT%H:%M:%SZ")
        if completed_start_date is not None:
            query_params["completedStartDate"] = completed_start_date.strftime("%Y-%m-%dT%H:%M:%SZ")
        if completed_end_date is not None:
            query_params["completedEndDate"] = completed_end_date.strftime("%Y-%m-%dT%H:%M:%SZ")
        if status_in is not None:
            query_params["statusIn"] = status_in
        return self.request(uri, method="POST", query_params=query_params, required_api_key=True)

    def get_tasks_operation(self, app_id: str, operation_id: int):
        """Fetch status of task operation given application id and operation id

        Args:
          app_id: Application id
          operation_id: operation_id


        Returns:
          Dict with operation information (id, status, and other fields)

        """
        uri = f"task-operations/{app_id}/{operation_id}"
        return self.request(uri, method="GET", required_api_key=True)

    def generates_downloaded_tasks_url(self, app_id: str, operation_id: int, seconds_ttl: int = None):
        """Generates url to retrieve downloaded zip tasks given application id and
        operation id

        Args:
          app_id: Application id
          operation_id: operation_id
          seconds_ttl: Seconds ttl for generated url. Default 60


        Returns:
          Dict with field downloadUrl

        """
        uri = f"task-operations/{app_id}/{operation_id}/download-url"
        query_params = {}
        if seconds_ttl is not None:
            query_params["secondsTtl"] = seconds_ttl
        return self.request(uri, method="POST", query_params=query_params, required_api_key=True)

    def download_tasks_full_flow(
        self,
        app_id: str,
        created_start_date: datetime = None,
        created_end_date: datetime = None,
        completed_start_date: datetime = None,
        completed_end_date: datetime = None,
        status_in: List[str] = None,
        timeout: int = 120,
        poll_interval: int = 3,
    ) -> Optional[List[dict]]:
        """Trigger download of tasks and polls every poll_interval seconds until it
        returns the list of tasks or None in case of timeout

        Args:
          app_id: Application id
          created_start_date: Filter by created start date of tasks
          created_end_date: Filter by created end date of tasks
          completed_start_date: Filter by completed start date of tasks
          completed_end_date: Filter by completed end date of tasks
          status_in: Filter by status of tasks
          timeout: Timeout in seconds
          poll_interval: Poll interval in seconds

        Returns:
          List of dict of tasks

        """
        operation_id = self.download_tasks(
            app_id, created_start_date, created_end_date, completed_start_date, completed_end_date, status_in
        )["operationId"]
        operation_completed = False
        start_poll_date = datetime.now()
        while not operation_completed and (datetime.now() - start_poll_date).seconds < timeout:
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
