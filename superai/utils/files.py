from __future__ import absolute_import, division, print_function, unicode_literals

import unicodedata
import urllib.error
import urllib.request
from pathlib import Path
from typing import Optional, Union
from urllib.parse import urlparse

import boto3
import botocore
from boto3.s3.transfer import TransferConfig
from rich.progress import (
    BarColumn,
    DownloadColumn,
    Progress,
    TextColumn,
    TimeRemainingColumn,
    TransferSpeedColumn,
)

from superai.log import logger

log = logger.get_logger(__name__)


def download_file_to_directory(url: str, filename: str, path: Union[Path, str]) -> str:
    """
    Download a file from a url to a path

    Parameters
    ----------
    url : str
        The url of the file to download
    filename : str
        The name of the file to download
    path : Path
        The path to download the file to

    """
    path = Path(path)
    destination = path / filename
    destination.parent.mkdir(exist_ok=True)
    destination.touch()
    progress = Progress(
        TextColumn("[bold blue]{task.fields[filename]}", justify="right"),
        BarColumn(bar_width=None),
        "[progress.percentage]{task.percentage:>3.1f}%",
        "•",
        DownloadColumn(),
        "•",
        TransferSpeedColumn(),
        "•",
        TimeRemainingColumn(),
    )

    normalized_filename = unicodedata.normalize("NFC", filename)
    t = progress.add_task("Downloading", filename=normalized_filename, start=False)

    def update(blocknum, bs, size):
        progress.update(t, completed=blocknum * bs, total=size)

    try:
        with progress:
            progress.start_task(t)
            urllib.request.urlretrieve(url, destination, update)
    except urllib.error.HTTPError as e:
        destination.unlink()
        raise RuntimeError(f"Could not download file. Status code {e.code}.")

    return str(destination)


def s3_download_file(
    s3_key: str,
    destination: str,
    bucket: Optional[str] = None,
    s3_bucket: object = None,
    session_profile_name: str = None,
    force_download: bool = False,
):
    """Download a file from S3 to a local path with a progress bar.

    This function downloads a file from an Amazon S3 bucket to a local path,
    displaying a progress bar during the download process.

    Args:
        s3_key (str): The key of the file to download within the S3 bucket.
        destination (str): The local path where the downloaded file should be saved.
        bucket (Optional[str]): The name of the S3 bucket. Either bucket or s3_bucket must be provided.
        s3_bucket (object, Optional): S3 Bucket object. Allows reuse of the same bucket object for multiple downloads.
        session_profile_name (str, Optional): The name of the AWS session profile to use for authentication.
        force_download (bool, Optional): If True, the file will be downloaded even if it already exists locally with same filesize.


    Raises:
        Exception: If the download fails for any reason.

    Example:
        s3_download_file('path/to/file.txt', '/local/path/to/file.txt', s3_bucket='my-bucket')
    """

    # Either bucket or s3_bucket must be provided
    if not bucket and not s3_bucket:
        raise ValueError("Either bucket or s3_bucket must be provided")
    if not s3_bucket:
        session = boto3.session.Session(profile_name=session_profile_name)
        s3 = session.resource("s3")
        s3_bucket = s3.Bucket(bucket)
    bucket_name = s3_bucket.name
    log.info(f'Pulling "{s3_key}" from bucket "{bucket_name}" to "{destination}"')

    # Check if the local file exists and has the same size as the remote file
    local_file_path = Path(destination)
    if not force_download and local_file_path.exists():
        s3_object = s3_bucket.Object(s3_key)
        size_bytes = s3_object.content_length
        if local_file_path.stat().st_size == size_bytes:
            log.info(f'File "{s3_key}" already exists locally and has the same size. Skipping download.')
            return

    try:
        # Use Rich progress bar to track download progress
        size_bytes = s3_bucket.Object(s3_key).content_length
        with Progress(*Progress.get_default_columns(), DownloadColumn(), TransferSpeedColumn()) as progress:
            download_task = progress.add_task("Downloading", total=size_bytes, unit="B")

            def work_done(chunk):
                progress.update(download_task, advance=chunk)

            # Disable threading during transfer to mitigate Python 3.9 threading issues
            import sys

            is_python_39 = sys.version_info.major == 3 and sys.version_info.minor == 9
            config = TransferConfig(use_threads=not is_python_39)
            s3_bucket.download_file(s3_key, destination, Config=config, Callback=work_done)

    except botocore.exceptions.ClientError as e:
        log.error(f"Error downloading file from S3: {e}")
        if e.response["Error"]["Code"] in ["404", "403"]:
            log.error(f"prefix {bucket_name} and filename {s3_key} does not exist or aws access is forbidden")
        if e.response["Error"]["Code"] == "400":
            log.error("S3 Operation not possible. Is AWS session token still valid?")
        raise e


def pull_s3_folder(s3_folder_uri: str, local_dir: Union[Path, str]):
    """Download all files from an S3 folder to a local directory"""
    local_dir = Path(local_dir)
    s3 = boto3.resource("s3")
    bucket_name = urlparse(s3_folder_uri).hostname
    s3_path = urlparse(s3_folder_uri).path.lstrip("/")
    s3_folder_path = Path(s3_path)

    bucket = s3.Bucket(bucket_name)

    for obj in bucket.objects.filter(Prefix=s3_path):
        target = local_dir / Path(obj.key).relative_to(s3_folder_path)

        if obj.key[-1] == "/":
            continue

        target.parent.mkdir(parents=True, exist_ok=True)
        s3_download_file(s3_key=obj.key, destination=str(target), s3_bucket=bucket)
