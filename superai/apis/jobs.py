import json
import time
from abc import ABC, abstractmethod
from datetime import datetime
from io import BytesIO
from typing import Generator, List, Optional
from zipfile import ZipFile

import requests
from rich.console import Console

from superai.log import logger

log = logger.get_logger(__name__)


class JobsApiMixin(ABC):
    @abstractmethod
    def request(self, uri, method, body_params=None, query_params=None, required_api_key=False, header_params=None):
        pass

    def create_jobs(
        self,
        app_id: str,
        callback_url: str = None,
        inputs: List[dict] = None,
        inputs_file_url: str = None,
        metadata: dict = None,
        worker: str = None,
        parked: bool = None,
        tags: str = None,
    ) -> dict:
        """Submits jobs.

        Args:
            app_id: Application ID
            callback_url: A URL that should be sent a POST request once the job is completed for the response data.
            inputs: A list of objects that represent the input of the job (based on the particular app type).
            inputs_file_url: A URL of a JSON file containing list of input objects.
            metadata: Object you can attach to job.
            worker:
            parked: Whether the job should be created in the parked (pending) state
        Returns:
            Confirmation message of submission, batch ID of submission, UUID of job if len(input) == 1.
        """
        body_json = {}
        if callback_url is not None:
            body_json["callbackUrl"] = callback_url
        if inputs is not None:
            body_json["inputs"] = inputs
        if inputs_file_url is not None:
            body_json["inputsFileUrl"] = inputs_file_url
        if metadata is not None:
            body_json["metadata"] = metadata
        if worker is not None:
            body_json["labeler"] = worker
        if parked is not None:
            body_json["pending"] = parked
        if tags is not None:
            body_json["tags"] = tags

        uri = f"apps/{app_id}/jobs"
        return self.request(uri, method="POST", body_params=body_json, required_api_key=True)

    def fetch_job(self, job_id: str) -> dict:
        """Gets job given job ID.

        Args:
            job_id: Job ID.

        Returns:
            Dict with job data.
        """
        uri = f"jobs/{job_id}"
        return self.request(uri, method="GET", required_api_key=True)

    def fetch_batches_job(self, app_id) -> dict:
        """Gets unprocessed batches of submitted jobs given application ID.

        Args:
            app_id: Application ID.

        Returns:
            A dict with batch data.
        """
        uri = f"apps/{app_id}/batches"
        return self.request(uri, method="GET", required_api_key=True)

    def fetch_batch_job(self, app_id: str, batch_id: str) -> dict:
        """Gets batch of submitted jobs given batch ID and application ID.

        Args:
            app_id: Application ID.
            batch_id: Batch ID.
        Returns:
            A dict with batch data.
        """
        uri = f"apps/{app_id}/batches/{batch_id}"
        return self.request(uri, method="GET", required_api_key=True)

    def get_job_response(self, job_id: str) -> dict:
        """Gets job response given job ID.

        Args:
            job_id:

        Returns:
            A dict with the job response.
        """
        uri = f"jobs/{job_id}/response"
        return self.request(uri, method="GET", required_api_key=True)

    def cancel_job(self, job_id: str) -> dict:
        """Cancels a job given job ID. Only for jobs in SCHEDULED, IN_PROGRESS or SUSPENDED states.

        Args:
            job_id: Job ID.

        Returns:
            A dict with job data.
        """

        uri = f"jobs/{job_id}/cancel"
        return self.request(uri, method="POST", required_api_key=True)

    def add_tags(
        self,
        app_id: str,
        tags: str,
        search_id: str,
    ) -> dict:
        """Add tags to job given an application ID and search_id.

        Args:
            app_id: Application ID.
            tags: job tags.
            search_id: job_id
        Returns:
            None
        """
        uri = f"apps/{app_id}/jobs/tags"
        query_params = {}
        if search_id is not None:
            query_params["idSearch"] = search_id
        body_json = {}
        if tags is not None:
            body_json["tags"] = tags
        return self.request(uri, method="PUT", query_params=query_params, body_params=body_json, required_api_key=True)

    def delete_tags(
        self,
        app_id: str,
        tags: str,
        created_start_date: datetime = None,
        batch_id: str = None,
        search_id: str = None,
    ) -> dict:
        """Deletes the tags from jobs given an application ID and tag. Can be filtered by batch_id.

        Args:
            app_id: Application ID.
            tags: job tags.
        Returns:
            None
        """
        uri = f"apps/{app_id}/jobs/tags"
        query_params = {}
        if batch_id is not None:
            query_params["batchId"] = batch_id
        if search_id is not None:
            query_params["idSearch"] = search_id
        if created_start_date is not None:
            query_params["createdStartDate"] = created_start_date.strftime("%Y-%m-%dT%H:%M:%SZ")
        body_json = {}
        if tags is not None:
            body_json["tags"] = tags
        return self.request(
            uri, method="DELETE", query_params=query_params, body_params=body_json, required_api_key=True
        )

    def list_jobs(
        self,
        app_id: str,
        page: int = None,
        size: int = None,
        sort_by: str = "id",
        order_by: str = "asc",
        created_start_date: datetime = None,
        created_end_date: datetime = None,
        completed_start_date: datetime = None,
        completed_end_date: datetime = None,
        status_in: List[str] = None,
        tags: str = None,
        correct: str = None,
    ) -> dict:
        """Gets a paginated list of jobs (without job responses) given an application ID.

        Args:
            app_id: Application ID.
            page: Page number [0..N].
            size: Size of page.
            sort_by: Job field to sort by.
            order_by: Sort direction (asc or desc).
            created_start_date: Created start date.
            created_end_date: Created end date.
            completed_start_date: Completed start date.
            completed_end_date: Completed end date.
            status_in: Status of jobs.

        Returns:
            Paginated list of dicts with jobs data.
        """
        uri = f"apps/{app_id}/jobs"
        query_params = {}
        if page is not None:
            query_params["page"] = page
        if size is not None:
            query_params["size"] = size
        if sort_by is not None:
            query_params["sortBy"] = sort_by
        if order_by is not None:
            query_params["orderBy"] = order_by
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
        if tags is not None:
            query_params["tags"] = tags
        if correct is not None:
            query_params["correct"] = correct
        return self.request(uri, method="GET", query_params=query_params, required_api_key=True)

    def download_jobs(
        self,
        app_id: str,
        created_start_date: datetime = None,
        created_end_date: datetime = None,
        completed_start_date: datetime = None,
        completed_end_date: datetime = None,
        status_in: List[str] = None,
        send_email: bool = None,
        with_history: bool = None,
        batch_id: str = None,
        id_search: str = None,
    ) -> dict:
        """
        Trigger processing of jobs responses that are sent to customer email (default) once is finished.

        Args:
            app_id: Application ID.
            created_start_date: Created start date.
            created_end_date: Created end date.
            completed_start_date: Completed start date.
            completed_end_date: Completed end date.
            status_in: Status of jobs.
            send_email: Whether to send an email.
            with_history: Adds job history to downloaded data.

        Returns:
            Dict with operationId key to track status
        """
        uri = f"apps/{app_id}/job_responses"
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
        if send_email is not None:
            query_params["sendEmail"] = send_email
        if with_history is not None:
            query_params["withHistory"] = with_history
        if batch_id is not None:
            query_params["batchId"] = batch_id
        if id_search is not None:
            query_params["idSearch"] = id_search
        return self.request(uri, method="POST", query_params=query_params, required_api_key=True)

    def get_all_jobs(
        self,
        app_id: str,
        sort_by: str = "id",
        order_by: str = "asc",
        created_start_date: datetime = None,
        created_end_date: datetime = None,
        completed_start_date: datetime = None,
        completed_end_date: datetime = None,
        status_in: List[str] = None,
    ) -> Generator[dict, None, None]:
        """Generator that retrieves all jobs (without job responses) given an application ID.

        Args:

            app_id: Application ID.
            sort_by: Job field to sort by.
            order_by: Sort direction (asc or desc).
            created_start_date: Created start date.
            created_end_date: Created end date.
            completed_start_date: Completed start date.
            completed_end_date: Completed end date.
            status_in: Status of jobs.

        Returns:
            Generator that yields complete list of dicts with jobs data.
        """
        page = 0
        paginated_jobs = {"pages": 1}
        while page <= paginated_jobs["pages"] - 1:
            paginated_jobs = self.list_jobs(
                app_id,
                page=page,
                size=500,
                sort_by=sort_by,
                order_by=order_by,
                created_start_date=created_start_date,
                created_end_date=created_end_date,
                completed_start_date=completed_start_date,
                completed_end_date=completed_end_date,
                status_in=status_in,
            )
            yield from paginated_jobs["jobs"]
            page += 1

    def get_jobs_operation(self, app_id: str, operation_id: int):
        """Fetch status of job operation given application id and operation id

        Args:
          app_id: Application id
          operation_id: operation_id

        Returns:
          Dict with operation information (id, status, and other fields)

        """
        uri = f"operations/{app_id}/{operation_id}"
        return self.request(uri, method="GET", required_api_key=True)

    def generates_downloaded_jobs_url(self, app_id: str, operation_id: int, seconds_ttl: int = None):
        """Generates url to retrieve downloaded zip jobs given application id and operation id

        Args:
          app_id: Application id
          operation_id: operation_id
          seconds_ttl: Seconds ttl for generated url. Default 60

        Returns:
          Dict with field downloadUrl

        """
        uri = f"operations/{app_id}/{operation_id}/download-url"
        query_params = {}
        if seconds_ttl is not None:
            query_params["secondsTtl"] = seconds_ttl
        return self.request(uri, method="POST", query_params=query_params, required_api_key=True)

    def download_jobs_full_flow(
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
        """Trigger download of jobs and polls every poll_interval seconds until it
        returns the list of jobs or None in case of timeout

        Args:
          app_id: Application id
          created_start_date: Filter by created start date of jobs
          created_end_date: Filter by created end date of jobs
          completed_start_date: Filter by completed start date of jobs
          completed_end_date: Filter by completed end date of jobs
          status_in: Filter by status of jobs
          timeout: Timeout in seconds
          poll_interval: Poll interval in seconds

        Returns:
          List of dict of job

        """
        console = Console()
        operation_id = self.download_jobs(
            app_id, created_start_date, created_end_date, completed_start_date, completed_end_date, status_in, False
        )["operationId"]
        operation_completed = False
        last_operation_status = None
        start_poll_date = datetime.now()
        with console.status(f"Polling for operation [cyan]{operation_id}[/cyan]...") as status:
            while not operation_completed and (datetime.now() - start_poll_date).seconds < timeout:
                operation = self.get_jobs_operation(app_id, operation_id)
                operation_id, operation_status = operation["id"], operation["status"]
                if operation_status != last_operation_status:
                    status_msg = f"Download Job [cyan]{operation_id}[/cyan] in status [green]{operation_status}[/green]"
                    status.update(status=status_msg)
                    console.log(f"[magenta]Poll status:[/magenta] {status_msg}")
                    last_operation_status = operation_status
                if operation_status == "COMPLETED":
                    operation_completed = True
                else:
                    time.sleep(poll_interval)
            if not operation_completed:
                return None
            status.update(status="[green]Downloading jobs...")
            download_jobs_url = self.generates_downloaded_jobs_url(app_id, operation_id)["downloadUrl"]
            resp = requests.get(download_jobs_url)
            zipfile = ZipFile(BytesIO(resp.content))
            return json.load(zipfile.open(zipfile.namelist()[0]))

    def review_job(
        self,
        job_id: int,
        response: dict = None,
        correct: bool = None,
    ) -> dict:
        """Review jobs

        Args:
          job_id: Job id
          response: New job response. If not present
          correct: Whether the current job id should be marked as correct. If None no action would be taken.

        Returns:
          Status code

        """
        if not response and correct is None:
            raise ValueError("Review flow requires either `response` or `correct` parameters")

        body_json = {}
        if response is not None:
            body_json["response"] = response
        if correct is not None:
            body_json["correct"] = correct

        uri = f"jobs/{job_id}/review"
        return self.request(uri, method="PATCH", body_params=body_json, required_api_key=True)
