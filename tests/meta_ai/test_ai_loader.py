import os
from pathlib import Path
from typing import Dict

import boto3
import pytest
from moto import mock_aws

from superai.meta_ai import AILoader
from superai.meta_ai.ai_uri import AiURI


@pytest.mark.parametrize(
    "uri, expected_components",
    [
        ("ai://user1/my_model/1.0", {"owner_name": "user1", "model_name": "my_model", "version": "1.0"}),
        ("ai://my_model/1.0", {"model_name": "my_model", "version": "1.0", "username": None}),
        ("ai://my_model", {"model_name": "my_model", "version": None, "username": None}),
        ("ai://superai/my_model", {"owner_name": "superai", "model_name": "my_model", "version": None}),
    ],
)
def test_parse_model_uri_valid(uri: str, expected_components: Dict[str, str]) -> None:
    result = AiURI.parse(uri)
    assert result.owner_name == expected_components.get("owner_name")
    assert result.model_name == expected_components.get("model_name")
    assert result.version == expected_components.get("version")


@pytest.mark.parametrize(
    "uri",
    [
        "ai://username//model_name/version",
        "ai://username/model_name/",
        "ai:///",
        "ai://",
    ],
)
def test_parse_model_uri_invalid(uri: str) -> None:
    with pytest.raises(ValueError, match="Invalid model URI format"):
        AiURI.parse(uri)


@mock_aws
@pytest.mark.parametrize("download_folder", [True, False])
def test_download_s3_weights(download_folder, tmp_path):
    # Specify the region
    region_name = "us-west-2"

    # Creating an S3 bucket and an object to simulate the weight file
    conn = boto3.resource("s3", region_name=region_name)
    bucket_name = "my-bucket"
    weights_folder = "weights"
    weights_file_name = "test_weights"
    s3_key = f"{weights_folder}/{weights_file_name}"
    conn.create_bucket(Bucket=bucket_name, CreateBucketConfiguration={"LocationConstraint": region_name})
    obj = conn.Object(bucket_name, s3_key)
    obj.put(Body=b"some content here")

    # Constructing the S3 URL for the weight file
    weights_s3_url = f"s3://{bucket_name}/{weights_folder}"

    # Call the method to download the weights
    if download_folder:
        download_folder = tmp_path
    local_file_path = AILoader._download_s3_weights(weights_s3_url, download_folder)

    # Check if the file was downloaded correctly
    assert os.path.exists(local_file_path)

    # You can add additional assertions to check the content, file size, etc.
    with open(Path(local_file_path) / weights_file_name, "rb") as f:
        content = f.read()
        assert content == b"some content here"  # Make sure content matches
