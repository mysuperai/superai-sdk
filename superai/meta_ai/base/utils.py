import os
import tarfile
from urllib.parse import urlparse

from superai.log import get_logger
from superai.utils.files import pull_s3_folder, s3_download_file

log = get_logger(__name__)


def pull_weights(weights_uri: str, output_path: str) -> str:
    """Helper function to pull weights from S3 bucket
    Supports loading tar.gz files or whole directories

    Args:
        weights_uri: S3 URI of the weights to be loaded
        output_path: Path to the output directory

    Returns:
        Name of the folder where weights where downloaded / extracted to
    """
    log.info(f"Downloading weights from {weights_uri} to {output_path}")
    parsed_url = urlparse(weights_uri, allow_fragments=False)
    bucket_name = parsed_url.netloc
    path_to_object = parsed_url.path
    path_to_object = path_to_object.strip("/")
    object_name = os.path.basename(path_to_object)
    log.debug(f"Bucket name: {bucket_name}, path to object: {path_to_object}, tar name: {object_name}")

    local_tar_path = os.path.join(output_path, object_name)
    if object_name.endswith(".tar.gz"):
        log.info(f"Downloading tar.gz file to path `{local_tar_path}`")
        s3_download_file(path_to_object, local_tar_path, bucket_name)
        with tarfile.open(local_tar_path) as tar:
            log.debug(f"Extracting tar.gz file to path `{output_path}`")
            tar.extractall(path=output_path)
    else:
        log.info("Downloading weights folder")
        pull_s3_folder(weights_uri, output_path)
    log.info(f"Successfully downloaded weights folder to path `{output_path}`")
    return output_path
