"""Module for resolving data URIs to signed URLs in the Base AI."""
from __future__ import annotations

import io
import json
import re
import time
from typing import Callable, Optional, TypedDict, Union

from typing_extensions import NotRequired

from superai.apis.data import DataApiMixin
from superai.client import Client
from superai.log import get_logger
from superai.meta_ai.base.tags import PredictionTags

log = get_logger(__name__)


class DataManager:
    """
    Manages and transform the input and output data for the AI.
    Allows resolving data URIs to signed URLs during a migration period until all AIs are using signing manually for data URIs.
    Allows downloading data payload when only ref is provided.
    Replicates previous backend behaviour.
    """

    data_regex = DataApiMixin.data_regex
    client: Optional[Client] = None

    def __init__(self, task_id: int, client: Optional[Client] = None):
        self.task_id = task_id
        if DataManager.client is None:
            DataManager.client = client or Client.from_credentials()

    def preprocess_input(self, payload: PredictionInput, auto_resolve_data: bool) -> PredictionInput:
        """
        Download data payload when only ref is provided and resolve data references for backwards compatibility.
        Args:
            payload: raw payload dict
            auto_resolve_data: bool, setting to True will resolve data references
        Returns:
            PredictionInput: Input data with preprocessing applied.

        """
        try:  # TODO: Remove try catch when all models and backends are migrated to new data resolver
            payload = self.download_payload(payload)
            if auto_resolve_data:
                payload = self.resolve_input(payload)
        except Exception as e:
            log.exception(f"Failed to resolve data references: {e}")
        return payload

    def postprocess_output(
        self, output: PredictionOutput, tags: Optional[PredictionTags] = None
    ) -> Union[dict, PredictionOutputReferenced]:
        """Uploads result to data storage and pass reference to the result."""
        if tags and tags.task_id:
            try:
                prediction = output.get("prediction")
                # Upload result to data storage and pass reference
                json_bytes_file = io.BytesIO(json.dumps(prediction).encode("utf-8"))
                upload_response = self.client.upload_ai_task_data(
                    ai_task_id=tags.task_id, file=json_bytes_file, mime_type="application/json"
                )
                upload_path = upload_response["dataUrl"]
                prediction = PredictionRef(ref=upload_path)
                output = PredictionOutputReferenced(prediction=prediction, score=output.get("score"))
            except Exception as e:
                log.exception(f"Failed to upload result to data storage: {e}")
        return output

    def signer_func(self, uri: str) -> str:
        """Uses the API to resolve a signed URL for a given URI."""
        response = self.client.get_signed_url(uri, collaborator_task_id=self.task_id)
        return response.get("signedUrl")

    def download_payload(self, payload: PredictionInput) -> PredictionInput:
        """Downloads data payload when only ref is provided."""
        data = payload.get("data", {})
        input_data = data.get("input", {})
        # Get output data from lecacy location or new location
        output_data = payload.get("parameters", {}).get("output_schema") or data.get("output", {})

        input_ref = input_data.get("ref") if input_data else None
        output_ref = output_data.get("ref") if output_data else None

        if input_ref:
            input_data = self.client.download_data(path=input_ref, collaborator_task_id=self.task_id).json()
        if output_ref:
            output_data = self.client.download_data(path=output_ref, collaborator_task_id=self.task_id).json()

        payload["data"] = data
        if input_ref:
            # Override complete data for backwards compatibility
            payload["data"] = input_data

        payload["parameters"] = {"output_schema": output_data}

        return payload

    def resolve_input(self, payload: PredictionInput) -> PredictionInput:
        """
        Resolves input data (string, dictionary, or list) containing data URIs.

        Args:
            payload: Input data containing data URIs.

        Returns:
            PredictionInput: Input data with signed URLs.
        """

        log.info(f"Resolving input data for task {self.task_id}")
        now = time.time()

        resolved = self.sign_all_urls(payload, self.data_regex, self.signer_func)
        log.info(f"Resolved input data for task {self.task_id}, it took {time.time() - now} seconds")
        return resolved

    @classmethod
    def _sign_all_urls_in_dict(
        cls,
        data: dict,
        uri_regex: re.Pattern,
        replacement_func: Callable,
    ) -> dict:
        """
        Recursively signs URLs in dictionary values.

        Args:
            data (dict): Dictionary containing URLs to sign.
            uri_regex (re.Pattern): Regex pattern to match the URLs.
            replacement_func (Callable): Function to call on each matching URL.

        Returns:
            dict: Dictionary with signed URLs.
        """
        for key, value in data.items():
            if isinstance(value, dict):
                data[key] = cls._sign_all_urls_in_dict(value, uri_regex, replacement_func)
            elif isinstance(value, list):
                data[key] = [cls.sign_all_urls(item, uri_regex, replacement_func) for item in value]
            elif isinstance(value, str) and uri_regex.match(value):
                data[key] = replacement_func(uri=value)
        return data

    @classmethod
    def sign_all_urls(
        cls,
        data: Union[str, dict, list],
        uri_regex: re.Pattern,
        replacement_func: Callable,
    ) -> Optional[Union[str, dict, list]]:
        """
        Signs URLs in input data (string, dictionary, or list) using a provided function.

        Args:
            data (Union[str, dict, list]): Input data containing URLs to sign.
            uri_regex (re.Pattern): Regex pattern to match the URLs.
            replacement_func (Callable): Function to call on each matching URL.

        Returns:
            Optional[Union[str, dict, list]]: Data with signed URLs.
        """
        if data is None:
            return None

        signed_data = None
        is_string = isinstance(data, str)
        if is_string:
            if "://" not in data:
                # Most values are just strings, so we can skip the regex
                return data
            # Try to decode JSON string
            try:
                data = json.loads(data)
            except json.JSONDecodeError:
                log.warning(f"Could not decode JSON string: {data}. Returning as is.")
                return data

        if isinstance(data, dict):
            signed_data = cls._sign_all_urls_in_dict(data, uri_regex, replacement_func)

        if isinstance(data, list):
            signed_data = [cls.sign_all_urls(item, uri_regex, replacement_func) for item in data]

        if is_string:
            signed_data = json.dumps(data, ensure_ascii=False)

        return signed_data


class PredictionInput(TypedDict):
    """Prediction input dictionary passed to the predict() function as inputs.

    Using TypedDict for backwards compatibility with existing models.

    Example:
        predict(inputs: PredictionInput, ...)
    """

    data: dict
    parameters: NotRequired[dict]
    upload_url: str


class PredictionOutput(TypedDict):
    """Prediction output dictionary containing the prediction and score."""

    prediction: dict
    score: float


class PredictionRef(TypedDict):
    """Prediction output dictionary containing only ref to the payload."""

    ref: str


class PredictionOutputReferenced(TypedDict):
    """Payload getting send back to the backend after prediction and postprocessing.
    Is using only a reference to the payload in the data storage.
    Contains the data and metadata"""

    prediction: PredictionRef
    score: float
