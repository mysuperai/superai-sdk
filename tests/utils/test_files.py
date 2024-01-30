import os

import boto3
from moto import mock_aws

from superai.utils.files import pull_s3_folder, s3_download_file

# Define the parameters for the test
bucket_name = "test-bucket"
s3_key = "test-file"
local_destination = "/tmp/test-file"


@mock_aws
def test_s3_download_file(tmp_path, caplog):
    # Create the mock S3 bucket and file
    s3 = boto3.client("s3", region_name="us-west-2")
    s3.create_bucket(Bucket=bucket_name, CreateBucketConfiguration={"LocationConstraint": "us-west-2"})
    s3.put_object(Bucket=bucket_name, Key=s3_key, Body="some content")

    # Test s3_download_file function
    s3_download_file(s3_key, tmp_path / "testfile", bucket_name)

    # Validate that the file was downloaded to the local destination
    assert os.path.exists(tmp_path / "testfile")
    assert "already exists" not in caplog.text

    # Test caching
    # Call download function again
    s3_download_file(s3_key, tmp_path / "testfile", bucket_name)

    expected_log_message = f'File "{s3_key}" already exists locally and has the same size. Skipping download.'
    assert expected_log_message in caplog.text


@mock_aws
def test_pull_s3_folder(tmp_path):
    # Create the mock S3 bucket and folder with files
    s3 = boto3.client("s3", region_name="us-west-2")
    s3.create_bucket(Bucket=bucket_name, CreateBucketConfiguration={"LocationConstraint": "us-west-2"})
    s3.put_object(Bucket=bucket_name, Key="folder/file1", Body="file1 content")
    s3.put_object(Bucket=bucket_name, Key="folder/file2", Body="file2 content")
    s3_folder_uri = f"s3://{bucket_name}/folder"

    # Test pull_s3_folder function
    pull_s3_folder(s3_folder_uri, tmp_path)

    # Validate that the files were downloaded to the local directory
    file1 = tmp_path / "file1"
    file2 = tmp_path / "file2"
    assert file1.exists()
    assert file2.exists()
