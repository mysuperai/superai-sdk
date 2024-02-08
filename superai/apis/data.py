import re
from abc import ABC, abstractmethod
from typing import BinaryIO, Generator, List, Optional

import requests

from superai.exceptions import SuperAIStorageError


class DataApiMixin(ABC):
    _resource = "data"

    data_regex = re.compile(r"data:\/\/(?P<ownerId>\d+)\/(?P<path>.*)")

    @abstractmethod
    def request(self, uri, method, body_params=None, query_params=None, required_api_key=False, header_params=None):
        pass

    @property
    def resource(self):
        return self._resource

    def list_data(
        self,
        data_ids: List[str] = None,
        paths: List[str] = None,
        recursive: bool = False,
        signed_url: bool = False,
        seconds_ttl: int = 600,
        page: int = None,
        size: int = None,
    ) -> dict:
        """Gets a paginated list of datasets that can be filtered using an array of IDs or an array of paths.

        Args:
            data_ids: Array of data IDs.
            paths: Array of paths.
            recursive: Get all datasets from recursive path (only takes first path of array).
            signed_url: Get signed URL for each dataset.
            seconds_ttl: Time to live for signed URL.
            page: Page number [0..N].
            size: Size of page.

        Returns:
            Paginated list of datasets dicts.
        """
        query_params = {}
        if data_ids is not None:
            query_params["dataId"] = data_ids
        elif paths is not None:
            query_params["path"] = paths
            query_params["recursive"] = recursive
        if signed_url:
            query_params["signedUrl"] = signed_url
            query_params["secondsTtl"] = seconds_ttl
        if page is not None:
            query_params["page"] = page
        if size is not None:
            query_params["size"] = size
        return self.request(
            self.resource,
            method="GET",
            query_params=query_params,
            required_api_key=True,
        )

    def get_all_data(
        self,
        data_ids: List[str] = None,
        paths: List[str] = None,
        recursive: bool = False,
        signed_url: bool = False,
        seconds_ttl: int = 600,
    ) -> Generator[dict, None, None]:
        """Generator that retrieves all data filtered using an array of IDs or an array of paths.

        Args:
            data_ids: Array of data IDs.
            paths: Array of paths.
            recursive: Get all datasets from recursive path (only takes first path of array).
            signed_url: Get signed URL for each dataset.
            seconds_ttl: Time to live for signed URL.

        Returns:
            Generator that yields complete list of dicts with data objects.
        """
        page = 0
        paginated_data = {"last": False}
        while not paginated_data["last"]:
            paginated_data = self.list_data(
                data_ids=data_ids,
                paths=paths,
                recursive=recursive,
                signed_url=signed_url,
                seconds_ttl=seconds_ttl,
                page=page,
                size=500,
            )
            yield from paginated_data["content"]
            page = page + 1

    def _put_file(self, url: str, file: BinaryIO, mime_type: str) -> int:
        """Uploads a file to a given URL.
        Mainly used for uploading files to S3 signed URLs.

        Args:
            url: URL to upload file to.
            file: Binary file value.
            mime_type: Type of file.
        """
        try:
            resp = requests.put(url, data=file.read(), headers={"Content-Type": mime_type})
            if resp.status_code in [200, 201]:
                return resp.status_code
            else:
                raise SuperAIStorageError(f"File {str(file)} couldn't be uploaded to super.AI Storage")
        except Exception as e:
            raise SuperAIStorageError(f"File {str(file)} couldn't be uploaded to super.AI Storage, Error: {str(e)}")

    def get_signed_url(self, path: str, seconds_ttl: int = 600, collaborator_task_id: Optional[int] = None) -> dict:
        """Gets signed URL for a dataset given its path.

        Args:
            path: Dataset's path e.g., `"data://.."`.
            seconds_ttl: Time to live for signed URL. Maximum is 7 days.
            collaborator_task_id: Collaborator task ID. Allows access to data in the context of a Collaborator/Ai task.

        Returns:
            Dictionary in the form
                    {
                        "ownerId": int # The data owner.
                        "path": str # The data path.
                        "signedUrl": str # Signed URL.
                   }
        """
        uri = f"{self.resource}/url"
        return self.request(
            uri,
            method="GET",
            query_params={"path": path, "secondsTtl": seconds_ttl, "collabTaskId": collaborator_task_id},
            required_api_key=True,
        )

    def download_data(
        self, path: str, timeout: int = 5, collaborator_task_id: Optional[int] = None
    ) -> requests.Response:
        """Downloads data given a `"data://..."` or URL path.

        Args:
            path: Dataset's path.
            timeout: Timeout for download.
            collaborator_task_id: Collaborator task ID. Allows access to data in the context of a Collaborator/Ai task.

        Returns:
            Response object. Can be used to get the content as bytes or json.
                Example:
                    res = download_data("data://<ownerId>/<path>")
                    res.content # bytes
                    res.json() # json
                    res.text # string
        """

        signed_url = self.get_signed_url(path, collaborator_task_id=collaborator_task_id)
        res = requests.get(signed_url.get("signedUrl"), timeout=timeout, headers={"Accept-Encoding": "gzip"})

        if res.status_code == 200:
            return res
        else:
            raise SuperAIStorageError(res.reason)

    def delete_data(self, path: str) -> dict:
        """Deletes a dataset given its path.

        Args:
            path: Dataset's path.

        Returns:
            Dict with details of deleted dataset.
        """
        return self.request(self.resource, method="DELETE", query_params={"path": path}, required_api_key=True)

    def upload_data(self, path: str, description: str, mime_type: str, file: BinaryIO) -> dict:
        """Creates or updates a dataset given its path using file and mimeType.

        Args:
            path: Path of dataset.
            description: Description of dataset.
            mime_type: Type of file.
            file: Binary File value.

        Returns:
            The dataset created or updated.
        """
        dataset = self.request(
            self.resource,
            method="POST",
            query_params={"path": path, "description": description, "mimeType": mime_type, "uploadUrl": True},
            required_api_key=True,
        )
        code = self._put_file(dataset.pop("uploadUrl"), file, mime_type)
        if code:
            return dataset

    def upload_ai_task_data(
        self,
        ai_task_id: int,
        file: BinaryIO,
        path: Optional[str] = None,
        description: Optional[str] = None,
        mime_type: Optional[str] = None,
    ) -> dict:
        """Uploads a file in the context of an AI Task.
        The AI task has to exist and be in the `IN_PROGRESS` state.

        Args:
            ai_task_id: AI Task ID. Task needs to be in the `IN_PROGRESS` state.
            file: Binary File value.
            path: Path/filename of file. When not provided, a random filename will be generated.
            description: Description of file.
            mime_type: Type of file.

        Returns:
            Information about the uploaded file, e.g. the `path` or 'dataUrl'.

        """
        dataset = self.request(
            f"{self.resource}/aitask/{ai_task_id}",
            method="POST",
            query_params={"path": path, "description": description, "mimeType": mime_type, "uploadUrl": True},
            required_api_key=True,
        )
        code = self._put_file(dataset.pop("uploadUrl"), file, mime_type)
        if code:
            return dataset

    def download_ai_task_data(
        self, ai_task_id: Optional[int] = None, path: Optional[str] = None, timeout: Optional[int] = 5
    ) -> requests.Response:
        """
        Downloads data in the context of an AI Task.
        Used by the AI models to retrieve input data.
        This function only works for AI tasks in the `IN_PROGRESS` state and for data that is contained in the AI task.

        Args:
            path: Dataset's path. It should be in the form data://<ownerId>/<path>
            ai_task_id: (Optional) Task ID, is necessary when accessing data in the context of a Collaborator/Ai task.
            timeout: Timeout for download.

        Returns:
            Response object. Can be used to get the content as bytes or json.
                Example:
                    res = download_data("data://<ownerId>/<path>")
                    res.content
                    res.json()
                    res.text

        """
        # Check if path is a data path
        match = self.data_regex.match(path)
        if not match:
            raise ValueError(f"Path {path} is not a valid data path. It should be in the form data://<ownerId>/<path>")

        return self.download_data(path, timeout=timeout, collaborator_task_id=ai_task_id)
