from __future__ import annotations

import importlib
import json
import os
import re
import subprocess
import sys
import tarfile
from pathlib import Path
from typing import TYPE_CHECKING, Dict, List, Optional, Tuple, Union

import boto3
import numpy as np
import pandas as pd
from boto3 import Session
from botocore.exceptions import ClientError
from rich.progress import BarColumn, DownloadColumn, Progress, Task
from rich.prompt import Confirm
from rich.text import Text
from superai_builder.docker.client import get_docker_client

from superai import Client, config, settings
from superai.log import logger
from superai.meta_ai.dataset import Dataset
from superai.meta_ai.exceptions import (
    AIException,
    ExpiredTokenException,
    ModelAlreadyExistsError,
    ModelDeploymentError,
)

PREDICTION_METRICS_JSON = "metrics.json"
ECR_MODEL_ROOT_PREFIX = "models"
SUPERAI_OWNER_ID = 1

log = logger.get_logger(__name__)

if TYPE_CHECKING:
    from .ai_instance import AIInstance


def list_models(
    ai_name: str,
    client: "Client" = None,
    raw: bool = False,
    verbose: bool = True,
) -> Union[List[Dict], pd.DataFrame]:
    """List existing models in the database, given the model name.

    Args:
        verbose: Print the output.
        raw: Return unformatted list of models.
        client: Instance of superai.client.
        ai_name: Name of the AI model.
    """
    from superai import Client

    client = client or Client.from_credentials()
    model_entries: List[Dict] = client.get_model_by_name(ai_name, to_json=True)
    if raw:
        if verbose:
            log.info(json.dumps(model_entries, indent=1))
        return model_entries
    else:
        table = pd.DataFrame.from_dict(model_entries)
        if verbose:
            pd.set_option("display.max_colwidth", None)
            log.info(table)
        return table


def get_user_model_class(model_name, save_location, subfolder: Union[str, Path] = "."):
    """Obtain a class definition given the path to the class module

    Args:
        save_location: Location of the stored model (e.g. .AISave/...)
        subfolder: Path to the class module relative to `save_location`
        model_name: Name of the model
    """
    location = Path(save_location)
    path_dir = location / subfolder
    ai_module_path_str = str(path_dir.absolute())
    # Add path to sys.path
    sys.path.append(ai_module_path_str)
    # Add parent folder to path
    sys.path.append(str(path_dir.parent.absolute()))
    parts = model_name.rsplit(".", 1)
    if len(parts) == 1:
        logger.info(f"Importing {model_name} from {subfolder} (Absolute path: {path_dir})")
        interface_file = importlib.import_module(model_name)
        user_class = getattr(interface_file, model_name)
    else:
        logger.info(f"Importing submodule {parts}")
        interface_file = importlib.import_module(parts[0])
        user_class = getattr(interface_file, parts[1])
    sys.path.remove(ai_module_path_str)
    return user_class


def get_ecr_image_name(name, version):
    """Get the ECR image name containing the account id and region."""
    boto_session = boto3.session.Session()
    region = boto_session.region_name
    account = boto_session.client("sts").get_caller_identity()["Account"]
    return f"{account}.dkr.ecr.{region}.amazonaws.com/{name}:{version}"


def upload_dir(local_dir: Union[Path, str], aws_root_dir: Union[Path, str], bucket_name: str, prefix: str = "/"):
    """from current working directory, upload a 'local_dir' with all its subcontents (files and subdirectories...)
    to a aws bucket
    Parameters
    ----------
    local_dir : local directory to be uploaded, with respect to current working directory
    aws_root_dir : prefix 'directory' in aws
    bucket_name : bucket in aws
    prefix : to remove initial '/' from file names

    https://stackoverflow.com/a/64445594/15820564
    Returns
    -------
    None
    """
    log.info(f"Uploading directory: {local_dir} to bucket: {bucket_name}")

    # Initialize S3 resource
    s3 = boto3.resource("s3")

    # Convert to Path objects if necessary
    local_dir = Path(local_dir) if isinstance(local_dir, str) else local_dir
    aws_root_dir = Path(aws_root_dir) if isinstance(aws_root_dir, str) else aws_root_dir
    log.info(f"Uploading to: {str(aws_root_dir)}")
    # Set the working directory
    working_dir = Path.cwd()

    # Get the absolute local directory path
    absolute_local_dir = working_dir / local_dir

    # Get all files in the local directory and its subdirectories
    all_files = absolute_local_dir.glob("**/*")

    # Iterate over all files
    count = 0
    for file_path in all_files:
        # Skip directories
        if file_path.is_dir():
            # Directories are implicit for S3 based on path
            continue

        # Get the relative path of the file with respect to the local directory
        relative_file_path = file_path.relative_to(absolute_local_dir)

        # Remove the prefix if it exists
        s3_file_path = str(relative_file_path)
        s3_file_path = s3_file_path.removeprefix(prefix)
        # Construct the final AWS path
        aws_path = str((aws_root_dir / s3_file_path))

        log.debug(f"Uploading file: {s3_file_path} to {aws_path}")

        # Upload the file to S3
        s3.meta.client.upload_file(str(file_path), bucket_name, aws_path)
        count += 1
    log.info(f"Finished uploading directory: {local_dir.absolute()} with {count} file(s).")


def load_and_predict(
    model_path: Union[Path, str],
    weights_path: Optional[Union[Path, str]] = None,
    data_path: Optional[Union[Path, str]] = None,
    json_input: Optional[str] = None,
    metrics_output_dir: Path = None,
):
    """Loads a model and makes a prediction on the data.
    Supports json string input or json file input.

    Parameters
    ----------
    model_path : str, Path
        Path to the model directory.
    weights_path : str, Path, optional
        Path to the weights file.
    data_path : str, Path, optional
        Path to the data file.
    json_input : str, optional
        JSON string input.
    metrics_output_dir : Path, optional
        Path to the directory where metrics will be saved.

    """
    if json_input is None and data_path is None:
        raise ValueError("No input data provided. Please provide either a JSON input or a data path")
    if data_path and json_input:
        raise ValueError("Please provide either a JSON input or a data path")

    from superai.meta_ai import AI

    if metrics_output_dir:
        try:
            from polyaxon import tracking

            tracking.init()
        except Exception:
            log.debug("Polyaxon not installed. Tracking not enabled.")

    model_path = str(Path(model_path).absolute())
    log.info(f"Loading model files from: {model_path}")
    if weights_path:
        weights_path = str(Path(weights_path).absolute())
        log.info(f"Loading model weights from: {weights_path}")
    if data_path:
        data_path = Path(data_path).absolute()
        log.info(f"Loading data from: {data_path}")
        dataset = Dataset.from_file(data_path)
    else:
        dataset = Dataset.from_json(json_input=json_input)
    log.info(f"Dataset loaded: {dataset}")

    ai_object = AI.load(model_path, weights_path=weights_path)
    task_input = dataset.X_train
    if len(task_input) > 1:
        result = ai_object.predict_batch(task_input)
        scores = [p["score"] for p in result]
    else:
        result = ai_object.predict(task_input[0])
        scores = [result["score"]]
    predict_score = np.mean(scores)
    log.info(f"Prediction score: {predict_score}")
    if metrics_output_dir:
        store_prediction_metrics(metrics_output_dir, dict(score=predict_score))
    return result


def store_prediction_metrics(
    metrics_output_dir: Union[Path, str], metrics: dict, filename: str = PREDICTION_METRICS_JSON
) -> Path:
    """Method to store prediction metrics in a json file.
    Args:
        metrics_output_dir: Path to the directory where metrics will be saved.
        metrics: dict
            Dictionary of metrics.
            Keys should be the metric names and values should be the metric values.

    Returns:

    """
    metrics_output_dir = Path(metrics_output_dir)
    metrics_output_dir.mkdir(parents=True, exist_ok=True)
    metrics_output_path = metrics_output_dir / filename

    with open(metrics_output_path, "w") as f:
        json.dump(metrics, f)
    log.info(f"Metrics saved to: {metrics_output_path}")
    return metrics_output_path


def _compress_folder(path_to_tarfile: Union[str, Path], location: Union[str, Path]):
    """Helper to compress a directory into a tarfile

    Args:
        path_to_tarfile: Path to file to be generated after compressing
        location: Path to folder to be compressed
    """

    path_to_tarfile = Path(path_to_tarfile)
    assert path_to_tarfile.suffixes == [".tar", ".gz"], "Should be a valid tarfile path"
    with tarfile.open(path_to_tarfile, "w:gz") as tar:
        for file in Path(location).iterdir():
            tar.add(file, arcname=file.name)
    assert path_to_tarfile.exists()


def _ai_name_validator(instance, attribute, name):
    """Validate that the AI name only contains _ and - and alphanumeric characters"""
    if not re.match(r"^[a-zA-Z0-9_-]*$", str(name)):
        raise AIException("AI name can only contain alphanumeric characters")


def _ai_version_validator(instance, attribute, version):
    """Validate that the AI version only has the short semantic version format 1.0 or 3.2"""
    if not re.match(r"^[0-9]+\.[0-9]+$", str(version)):
        raise AIException("AI version can only be in the format {MAJOR}.{MINOR} e.g  1.0 or 3.2")


def _path_exists_validator(instance, attribute, path):
    if isinstance(path, str) and "s3://" in path:
        return
    if not Path(path).exists():
        raise AIException(f"Path {path} does not exist")


def _not_none_validator(instance, attribute, value):
    if value is None:
        raise AIException("Value cannot be None")


def confirm_action():
    if os.getenv("JENKINS_URL") or os.getenv("FORCE_CONFIRM") == "true":
        return
    confirmed = Confirm.ask(
        "Do you [bold]really[/bold] want to overwrite a [red]production[/red] AI? "
        "This can negatively impact Data Programs relying on the existing AI."
    )
    if not confirmed:
        log.warning("Aborting action")
        raise ModelDeploymentError("Action aborted by User")


class UploadColumn(DownloadColumn):
    """Renders uploaded and total layer size, e.g. 0.4/1.8 GB"""

    def render(self, task: Task) -> Text:
        # do not display column if no total size is available
        if int(task.total) == 1:
            return Text()
        return super(UploadColumn, self).render(task)


def push_image(
    image_name: str,
    model_id: str,
    version: str = "latest",
    region: str = settings.region,
    show_progress: bool = True,
    verbose: bool = False,
) -> str:
    """Push container to ECR

    Args:
        image_name: Name of the locally built image
        model_id: UUID of the model/AI (in `AI` given by `id` property)
        version: Version string for docker container
        region: AWS region
        show_progress: Enable / disable progress bar
        verbose: Whether to log the image push stream
    """
    if ":" in image_name:
        image_name, version = image_name.split(":")
    full_name, registry_prefix, repository_name = ecr_full_name(image_name, version, model_id, region)
    boto_session = get_boto_session(region_name=region)
    account = boto_session.client("sts").get_caller_identity()["Account"]

    logger.info(f"Pushing image to ECR: {full_name}")

    # login to the ECR registry where the image will be pushed to
    aws_ecr_login(region, registry_prefix)

    docker_client = get_docker_client()
    ecr_client = boto_session.client("ecr")
    log.info(f"Checking if image repository exists with name {repository_name}")
    try:
        ecr_client.describe_repositories(registryId=account, repositoryNames=[repository_name])
    except Exception as e:
        log.info(e)
        ecr_client.create_repository(repositoryName=repository_name)
        log.info(f"Created repository for `{repository_name}`.")

    log.info(f"Tagging to `{full_name}`")
    docker_client.images.get(f"{image_name}:{version}").tag(full_name)

    log.info("Pushing image...")
    columns = [
        "[progress.description]{task.description}",
        BarColumn(),
        "[progress.percentage]{task.percentage:>3.0f}%",
        UploadColumn(),
    ]
    layers = {}  # keep track of pushed layers, keyed by layer ID
    disable_progress = not show_progress
    with Progress(*columns, disable=disable_progress) as progress:
        for line in docker_client.images.push(repository=full_name, stream=True, decode=True):
            if verbose:
                log.info(line)

            if "id" in line and "progressDetail" in line:
                layer_id, status = line["id"], line["status"]
                description = f"[blue]{layer_id}[/blue] - {status}"

                if layer_id not in layers:
                    # create a task for tracking progress for each layer
                    layers[layer_id] = progress.add_task(description, total=1)

                layer_task = layers.get(layer_id)
                progress_detail = line.get("progressDetail", {})

                params = {}
                if status == "Layer already exists":
                    params["completed"] = 1
                elif progress_detail:
                    params["completed"] = progress_detail["current"]
                    params["total"] = max(progress_detail["current"], progress_detail.get("total", 0))

                progress.update(layer_task, description=description, **params)

        if "error" in line:
            # errors in the ECR image push operation usually appear in the last line
            raise ModelDeploymentError(f"Failed to push image to ECR - {line['error']}")

    log.info(f" Image pushed successfully to {full_name} ")
    return full_name


def ecr_full_name(image_name, version, model_id, region: str = settings.region) -> Tuple[str, str, str]:
    boto_session = get_boto_session(region_name=region)
    account = boto_session.client("sts").get_caller_identity()["Account"]
    full_suffix, repository_name = ecr_registry_suffix(image_name, model_id, version)
    registry_prefix = f"{account}.dkr.ecr.{region}.amazonaws.com"
    full_name = f"{registry_prefix}/{full_suffix}"
    return full_name, registry_prefix, repository_name


def ecr_registry_suffix(image_name: str, model_id: str, tag: Union[str, int]) -> Tuple[str, str]:
    env = config.settings.get("name")
    full_suffix = f"{ECR_MODEL_ROOT_PREFIX}/{env}/{model_id}/{image_name}"
    if len(full_suffix + str(tag)) > 255:
        # AWS allows 256 characters for the name
        logger.warning("Image name is too long. Truncating to 255 characters...")
        full_suffix = full_suffix[: 255 - len(tag)]
    full_suffix_with_version = f"{full_suffix}:{tag}"
    return full_suffix_with_version, full_suffix


def aws_ecr_login(region: str, registry_name: str) -> Optional[int]:
    log.info("Logging in to ECR...")

    # aws --version | awk '{print $1}' | awk -F/ '{ print $2}'
    aws_version = subprocess.check_output(["aws", "--version"]).decode("utf-8").strip().split(" ")[0].split("/")[1]
    aws_major = aws_version.split(".")[0]
    args_awsv1 = ["aws", "ecr", "get-login", "--region", region, "--no-include-email"]
    args_awsv2 = ["aws", "ecr", "get-login-password", "--region", region]

    if "AWS_PROFILE" in os.environ:
        args_awsv1.extend(["--profile", os.environ["AWS_PROFILE"]])
        args_awsv2.extend(["--profile", os.environ["AWS_PROFILE"]])

    def aws_cli_v1_login(args_awsv1):
        return subprocess.Popen(
            args_awsv1,
            stdout=subprocess.PIPE,
        )

    def aws_cli_v2_login(args_awsv2):
        return subprocess.Popen(args_awsv2, stdout=subprocess.PIPE)

    ecr_login_proc = aws_cli_v1_login(args_awsv1) if int(aws_major) < 2 else aws_cli_v2_login(args_awsv2)
    ecr_login_code = ecr_login_proc.wait()
    if ecr_login_code != 0:
        log.warning("Failed to login to ECR")
        return ecr_login_code

    # login to ECR via the docker login command, i.e. the output of the ECR login command
    ecr_login_output, _ = ecr_login_proc.communicate()
    if int(aws_major) < 2:
        docker_login_stdin = None
        docker_login_cmd = ecr_login_output.decode("utf-8")
    else:
        docker_login_stdin = ecr_login_output
        docker_login_cmd = f"docker login --username AWS --password-stdin {registry_name}"

    docker_login_proc = subprocess.Popen(
        docker_login_cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT
    )
    docker_login_proc.communicate(docker_login_stdin)
    docker_login_code = docker_login_proc.wait()
    if docker_login_code != 0:
        log.warning("Failed to login to ECR via docker login. Is the docker daemon up and running?")

    return docker_login_code


def get_boto_session(region_name=settings.region) -> Session:
    """Get a boto3 session. For the superai profile, an error message will be raised if
    credentials are expired

    Args:
        region_name: Name of the region

    Returns:
        Boto3 session
    """
    try:
        session = boto3.session.Session(region_name=region_name)
        _ = session.client("sts").get_caller_identity()["Account"]
        return session
    except ClientError as client_error:
        if "ExpiredToken" in str(client_error):
            log.error(f"Obtained error : {client_error}")
            raise ExpiredTokenException(
                "Please log in to superai by performing 'superai login -u <username>'"
            ) from client_error
        else:
            log.error(f"Unexpected Exception: {client_error}")
            raise client_error


def get_public_superai_instance(name: str, version: str, client=None) -> Optional["AIInstance"]:
    """
    Get a public Super.AI instance.

    Is used in Dataprograms to get the public instance of the AI for task predictions.

    Args:
        name: name of the AI instance
        version: version of the AI
        client: Super.AI client

    Returns:


    """

    from superai import Client

    client = client or Client.from_credentials()
    return client.get_ai_instance_by_template_version(
        name,
        version,
        SUPERAI_OWNER_ID,
        visibility="PUBLIC",
    )


def instantiate_superai(
    ai_name: Optional[str] = None,
    ai_version: Optional[str] = None,
    new_instance_name: Optional[str] = None,
    ai_uuid: Optional[str] = None,
) -> "AIInstance":
    """Instantiate a new AI instance from a public Super.AI.

    Args:
    ai_name: name of the existing AI template
    new_instance_name: name of the new AI instance
    ai_uuid: UUID of the existing AI template

    Returns:
    AIInstance object
    """
    # Either ai_name or ai_uuid must be provided
    if not ai_name and not ai_uuid:
        raise AIException("Either ai_name or ai_uuid must be provided")
    if ai_name:
        client = Client.from_credentials()
        owner_id = client._get_user_id()
        assert owner_id, "Failed to get owner id"
        existing_instances = client.list_ai(owner_id=owner_id, name=ai_name)
        if existing_instances:
            raise ModelAlreadyExistsError(
                f"AI instance with name {ai_name} already exists for this namespace session. Please choose a different name."
            )
        from superai.meta_ai.ai_uri import AiURI

        ai_identifier = AiURI(owner_name="superai", model_name=ai_name, version=ai_version)
    else:
        ai_identifier = ai_uuid
    from superai.meta_ai import AI

    ai = AI.load_essential(str(ai_identifier))

    instance = ai.create_instance(name=new_instance_name, visibility="PRIVATE")
    if not instance:
        return AIException(f"Failed to create instance for {ai_name}")

    return instance
