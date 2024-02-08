from abc import ABC, abstractmethod
from typing import Generator


class GroundTruthApiMixin(ABC):
    @abstractmethod
    def request(self, uri, method, body_params=None, query_params=None, required_api_key=False, header_params=None):
        pass

    def create_ground_truth(
        self, app_id: str, input_json: dict = None, label: dict = None, tag: str = None, metadata: dict = None
    ) -> dict:
        """Submits fresh ground truth data.

        Args:
            app_id: Application instance ID.
            input_json: Input that should match input schema of Data Program.
            label: Label, or output that should match output schema of Data Program.
            tag: Tag to identify ground truth data.
            metadata: Metadata of ground truth.

        Returns:
            The ground truth data object.
        """
        body_json = {}
        if input_json is not None:
            body_json["input"] = input_json
        if label is not None:
            body_json["label"] = label
        if tag is not None:
            body_json["tag"] = tag
        if metadata:
            body_json["metadata"] = metadata
        uri = f"apis/{app_id}/baselineData"
        return self.request(uri, "POST", body_params=body_json, required_api_key=True)

    def update_ground_truth(
        self,
        ground_truth_data_id: str,
        input_json: dict = None,
        label: dict = None,
        tag: str = None,
        metadata: dict = None,
    ) -> dict:
        """Uploads (PATCH) ground truth data.

        Args:
            ground_truth_data_id: ID of ground truth data.
            input_json: Input that should match input schema of Data Program.
            label: Label, or output that should match output schema of Data Program.
            tag: Tag to identify ground truth data.
            metadata: Metadata of ground truth.

        Returns:
            The updated ground truth data object.
        """
        body_json = {}
        if input_json is not None:
            body_json["input"] = input_json
        if label is not None:
            body_json["label"] = label
        if tag is not None:
            body_json["tag"] = tag
        if metadata is not None:
            body_json["metadata"] = metadata
        uri = f"baselineData/{ground_truth_data_id}"
        return self.request(uri, "PATCH", body_params=body_json, required_api_key=True)

    def list_ground_truth_data(self, app_id: str, page: int = None, size: int = None) -> dict:
        """Lists all ground truth data for an application.

        Args:
            app_id: Application ID.
            page: Page number of results.
            size: Page size of results.

        Returns:
            A paginated list of ground truth data objects.
        """
        uri = f"apis/{app_id}/baselineData"
        q_params = {}
        if page is not None:
            q_params["page"] = page
        if size is not None:
            q_params["size"] = size
        return self.request(uri, "GET", required_api_key=True, query_params=q_params)

    def get_all_ground_truth_data(self, app_id: str) -> Generator[dict, None, None]:
        """Generator that retrieves all ground truth data given an application ID.

        Args:
            app_id: Application ID.

        Yields:
            A generator that yields a complete list of dicts with ground truth data objects.
        """
        page = 0
        paginated_ground_truth = {"last": False}
        while not paginated_ground_truth["last"]:
            paginated_ground_truth = self.list_ground_truth_data(app_id, page=page, size=500)
            yield from paginated_ground_truth["content"]
            page = page + 1

    def get_ground_truth_data(self, ground_truth_data_id: str) -> dict:
        """Fetches a single ground truth data object.

        Args:
            ground_truth_data_id: ID of ground truth data.

        Returns:
            The ground truth data object.
        """
        uri = f"baselineData/{ground_truth_data_id}"
        return self.request(uri, "GET", required_api_key=True)

    def delete_ground_truth_data(self, ground_truth_data_id) -> dict:
        """Marks ground truth data as deleted.

        Args:
            ground_truth_data_id: ID of the ground truth data.

        Returns:
            The deleted ground truth daata object.
        """
        uri = f"baselineData/{ground_truth_data_id}"
        return self.request(uri, "DELETE", required_api_key=True)

    def create_ground_truth_from_job(self, app_id: str, job_id: str) -> dict:
        """Converts a completed job to ground truth data.

        Args:
            app_id: Application ID
            job_id: Job ID

        Returns:
            The ground truth data object.
        """
        uri = f"apis/{app_id}/baselineData/job/{job_id}"
        return self.request(uri, "POST", required_api_key=True)
