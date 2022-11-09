from abc import ABC, abstractmethod
from typing import BinaryIO, Generator, List

import requests

from superai.exceptions import SuperAIStorageError


class DataApiMixin(ABC):
    _resource = "data"

    @abstractmethod
    def request(self, uri, method, body_params=None, query_params=None, required_api_key=False):
        pass

    @property
    def resource(self):
        return self._resource

    def list_data(
        self,
        data_ids: List[str] = None,
        paths: List[str] = None,
        recursive: bool = False,
        signedUrl: bool = False,
        secondsTtl: int = 600,
        page: int = None,
        size: int = None,
    ) -> dict:
        """Gets a paginated list of datasets that can be filtered using an array of IDs or an array of paths.

        Args:
            data_ids: Array of data IDs.
            paths: Array of paths.
            recursive: Get all datasets from recursive path (only takes first path of array).
            signedUrl: Get signed URL for each dataset.
            secondsTtl: Time to live for signed URL.
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
        if signedUrl:
            query_params["signedUrl"] = signedUrl
            query_params["secondsTtl"] = secondsTtl
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
        signedUrl: bool = False,
        secondsTtl: int = 600,
    ) -> Generator[dict, None, None]:
        """Generator that retrieves all data filtered using an array of IDs or an array of paths.

        Args:
            data_ids: Array of data IDs.
            paths: Array of paths.
            recursive: Get all datasets from recursive path (only takes first path of array).
            signedUrl: Get signed URL for each dataset.
            secondsTtl: Time to live for signed URL.

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
                signedUrl=signedUrl,
                secondsTtl=secondsTtl,
                page=page,
                size=500,
            )
            for d in paginated_data["content"]:
                yield d
            page = page + 1

    def get_signed_url(self, path: str, secondsTtl: int = 600) -> dict:
        """Gets signed URL for a dataset given its path.

        Args:
            path: Dataset's path e.g., `"data://.."`.
            secondsTtl: Time to live for signed URL. Maximum is 7 days.

        Returns:
            Dictionary in the form {
                        ownerId": int # The data owner.
                      "path": str # The data path.
                       "signedUrl": str # Signed URL.
                   }
        """
        uri = f"{self.resource}/url"
        return self.request(
            uri, method="GET", query_params={"path": path, "secondsTtl": secondsTtl}, required_api_key=True
        )

    def download_data(self, path: str, timeout: int = 5):
        """Downloads data given a `"data://..."` or URL path.

        Args:
        path: Dataset's path.

        Returns:
            URL content.
        """
        signed_url = self.get_signed_url(path)
        res = requests.get(signed_url.get("signedUrl"), timeout=timeout)

        if res.status_code == 200:
            return res.json()
        else:
            raise Exception(res.reason)

    def delete_data(self, path: str) -> dict:
        """Deletes a dataset given its path.

        Args:
            path: Dataset's path.

        Returns:
            Dict with details of deleted dataset.
        """
        return self.request(self.resource, method="DELETE", query_params={"path": path}, required_api_key=True)

    def upload_data(self, path: str, description: str, mimeType: str, file: BinaryIO) -> dict:
        """Creates or updates a dataset given its path using file and mimeType.

        Args:
            path: Path of dataset.
            description: Description of dataset.
            mimeType: Type of file.
            file: Binary File value.

        Returns:
            The dataset created or updated.
        """
        dataset = self.request(
            self.resource,
            method="POST",
            query_params={"path": path, "description": description, "mimeType": mimeType, "uploadUrl": True},
            required_api_key=True,
        )
        try:
            resp = requests.put(dataset.pop("uploadUrl"), data=file.read(), headers={"Content-Type": mimeType})
            if resp.status_code == 200 or resp.status_code == 201:
                return dataset
            else:
                raise SuperAIStorageError(
                    f'File {str(file)} referenced by dataset {dataset["path"]} couldn\'t be uploaded to super.AI '
                    f"Storage"
                )
        except Exception as e:
            raise SuperAIStorageError(
                f'File {str(file)} referenced by dataset {dataset["path"]} couldn\'t be uploaded to super.AI Storage '
                f"Error: {str(e)}"
            )
