from abc import ABC, abstractmethod
from typing import Generator


class GroundTruthApiMixin(ABC):
    @abstractmethod
    def request(self, uri, method, body_params=None, query_params=None, required_api_key=False):
        pass

    def create_ground_truth(
        self, app_id: str, input_json: dict = None, label: dict = None, tag: str = None, metadata: dict = None
    ) -> dict:
        """
        Submit fresh ground truth data
        :param app_id: Application instance id
        :param input_json: Input that should match input schema of data program
        :param label: Label, or output that should match output schema of data program
        :param tag: Tag to identify ground truth data
        :param metadata: Metadata of ground truth
        :return: Ground truth data object
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
        """
        Upload (patch) ground truth data
        :param ground_truth_data_id: Id of ground truth data
        :param input_json: Input that should match input schema of data program
        :param label: Label, or output that should match output schema of data program
        :param tag: Tag to identify ground truth data
        :param metadata: Metadata of ground truth
        :return: Updated ground truth data object
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
        """
        List all ground truth data for an application
        :param app_id: Application id
        :param page: Page number of results
        :param size: Page size of results
        :return: Paginated list of ground truth data objects
        """
        uri = f"apis/{app_id}/baselineData"
        q_params = {}
        if page is not None:
            q_params["page"] = page
        if size is not None:
            q_params["size"] = size
        return self.request(uri, "GET", required_api_key=True, query_params=q_params)

    def get_all_ground_truth_data(self, app_id: str) -> Generator[dict, None, None]:
        """
        Generator that retrieves all ground truth data given an application id
        :param app_id: Application id
        :return: Generator that yields complete list of dicts with ground truth data objects
        """
        page = 0
        paginated_ground_truth = {"last": False}
        while not paginated_ground_truth["last"]:
            paginated_ground_truth = self.list_ground_truth_data(app_id, page=page, size=500)
            for gtd in paginated_ground_truth["content"]:
                yield gtd
            page = page + 1

    def get_ground_truth_data(self, ground_truth_data_id: str) -> dict:
        """
        Fetch single ground truth data object
        :param ground_truth_data_id: Id of ground truth data
        :return: Ground truth data object
        """
        uri = f"baselineData/{ground_truth_data_id}"
        return self.request(uri, "GET", required_api_key=True)

    def delete_ground_truth_data(self, ground_truth_data_id) -> dict:
        """
        Mark ground truth data as deleted
        :param ground_truth_data_id: If of ground truth data
        :return Deleted ground truth daata object:
        """
        uri = f"baselineData/{ground_truth_data_id}"
        return self.request(uri, "DELETE", required_api_key=True)

    def create_ground_truth_from_job(self, app_id: str, job_id: str) -> dict:
        """
        Convert completed job to ground truth data
        :param app_id: Application id
        :param job_id: Job id
        :return: Ground truth data object
        """
        uri = f"apis/{app_id}/baselineData/job/{job_id}"
        return self.request(uri, "POST", required_api_key=True)
