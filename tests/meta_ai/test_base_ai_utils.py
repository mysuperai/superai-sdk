import io
import os
import tarfile

import boto3
import pytest
from moto import mock_aws

from superai.meta_ai.base.utils import pull_weights


@pytest.fixture
def s3_setup():
    with mock_aws():
        boto3.client("s3", region_name="us-west-2").create_bucket(
            Bucket="test-bucket", CreateBucketConfiguration={"LocationConstraint": "us-west-2"}
        )
        yield


def test_pull_weights_for_directory(s3_setup, tmp_path):
    bucket_name = "test-bucket"
    directory_path = "weights/"
    file_name = "file.txt"
    file_content = b"test content"

    s3_client = boto3.client("s3")
    s3_client.put_object(Bucket=bucket_name, Key=directory_path + file_name, Body=file_content)

    weights_uri = f"s3://{bucket_name}/{directory_path}"

    assert pull_weights(weights_uri, tmp_path) == tmp_path

    # Verifying the file is correctly downloaded
    with open(os.path.join(tmp_path, file_name), "rb") as file:
        assert file.read() == file_content


def test_pull_tar_gz_weights(s3_setup, tmp_path):
    bucket_name = "test-bucket"
    directory_path = "weights/"
    file_name = "archive.tar.gz"

    # Create a .tar.gz file with sample content
    tar_content = io.BytesIO()
    with tarfile.open(fileobj=tar_content, mode="w:gz") as tar:
        file_data = b"sample file inside tar.gz"
        tarinfo = tarfile.TarInfo(name="sample.txt")
        tarinfo.size = len(file_data)
        tar.addfile(tarinfo, io.BytesIO(file_data))
    tar_content.seek(0)

    s3_client = boto3.client("s3")
    s3_client.put_object(Bucket=bucket_name, Key=directory_path + file_name, Body=tar_content.getvalue())

    weights_uri = f"s3://{bucket_name}/{directory_path}"

    assert pull_weights(weights_uri, tmp_path) == tmp_path

    # Verifying the file is correctly downloaded
    archive_path = os.path.join(tmp_path, file_name)
    with tarfile.open(archive_path, "r:gz") as tar:
        with tar.extractfile("sample.txt") as file:
            assert file.read() == file_data
