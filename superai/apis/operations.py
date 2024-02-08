from abc import ABC, abstractmethod

from superai.log import logger

log = logger.get_logger(__name__)


class OperationsApiMixin(ABC):
    @abstractmethod
    def request(self, uri, method, body_params=None, query_params=None, required_api_key=False, header_params=None):
        pass

    def get_operation_download_info(
        self,
        app_id: str,
        operation_id: str,
    ) -> dict:
        """Get operation download info.

        Args:
            app_id: Application ID.
            operation_id: operationId.

        Returns:
            Dict with operation download info.
        """
        uri = f"operations/{app_id}/{operation_id}"
        return self.request(uri, method="GET", required_api_key=True)

    def get_operation_download_url(
        self,
        app_id: str,
        operation_id: str,
    ) -> dict:
        """Get operation download url.

        Args:
            app_id: Application ID.
            operation_id: operationId.

        Returns:
            Dict with operation download url.
        """
        uri = f"operations/{app_id}/{operation_id}/download-url"
        return self.request(uri, method="POST", required_api_key=True)
