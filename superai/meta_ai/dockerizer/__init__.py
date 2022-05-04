import os
import shutil
import time

import boto3  # type: ignore
import docker  # type: ignore
import requests
from boto3.session import Session  # type: ignore
from botocore.exceptions import ClientError  # type: ignore
from docker import DockerClient  # type: ignore
from docker.errors import APIError  # type: ignore
from jinja2 import Template
from rich.progress import BarColumn, DownloadColumn, Progress, Task, Text

from superai.exceptions import ModelDeploymentError
from superai.log import logger

from ... import config
from .sagemaker_endpoint import (
    create_endpoint,
    invoke_local,
    invoke_sagemaker_endpoint,
    upload_model_to_s3,
)

log = logger.get_logger(__name__)


class UploadColumn(DownloadColumn):
    """Renders uploaded and total layer size, e.g. 0.4/1.8 GB"""

    def render(self, task: Task) -> Text:
        # do not display column if no total size is available
        if int(task.total) == 1:
            return Text()
        return super(UploadColumn, self).render(task)


server_script = """
import subprocess
import sys
import shlex
import os
from retrying import retry
from subprocess import CalledProcessError
from sagemaker_inference import model_server

def _retry_if_error(exception):
    return isinstance(exception, CalledProcessError or OSError)

@retry(stop_max_delay=1000 * 50,
       retry_on_exception=_retry_if_error)
def _start_mms():
    os.environ['SAGEMAKER_MODEL_SERVER_WORKERS'] = "{{worker_count}}"
    model_server.start_model_server(handler_service='/home/model-server/{{entry_point_file}}:{{entry_point_method}}')

def main():
    if sys.argv[1] == "{{command}}":
        _start_mms()
    else:
        subprocess.check_call(shlex.split(' '.join(sys.argv[1:])))

    # prevent docker exit
    subprocess.call(['tail', '-f', '/dev/null'])

main()
"""

standard_dockerfile_content = """FROM python:3.7.10-slim-stretch
"""


def update_docker_file(
    dockerfile: str = ".dockerizer/Dockerfile", command: str = "serve", has_requirements_file=False
) -> None:
    """
    Updates the input docker file to include certain sagemaker endpoint specific instructions.
    :param dockerfile: Path to Dockerfile
    :param command: Command to be passed to entrypoint
    :param has_requirements_file: Does the parent folder have a requirements.txt file. If yes, then install the contents
    """
    with open(dockerfile, "r") as f:
        no_entrypoint = "ENTRYPOINT" in f.read()

    lines = [
        "\nRUN mkdir -p /usr/share/man/man1",
        "\nRUN apt-get update "
        "&& apt-get -y install --no-install-recommends build-essential ca-certificates default-jdk curl "
        "&& rm -rf /var/lib/apt/lists/*",
        "\nLABEL com.amazonaws.sagemaker.capabilities.multi-models=true",
        "LABEL com.amazonaws.sagemaker.capabilities.accept-bind-to-port=true",
        "COPY dockerd-entrypoint.py /usr/local/bin/dockerd-entrypoint.py",
        "RUN chmod +x /usr/local/bin/dockerd-entrypoint.py",
        "RUN pip --no-cache-dir install multi-model-server sagemaker-inference retrying awscli~=1.18.195",
        "RUN mkdir -p /home/model-server/",
        f"COPY model_server/ /home/model-server/",
    ]
    lines.extend(
        [
            "ARG AWS_DEFAULT_REGION=us-east-1",
            f"RUN --mount=type=secret,id=aws,target=/root/.aws/credentials,required=true,uid=1000,gid=1000 "
            f"--mount=type=cache,target=/root/.cache/pip "
            f"aws codeartifact login --tool pip --domain superai --repository pypi-superai",
            "RUN pip install superai_schema",
        ]
    )
    if has_requirements_file:
        log.info("Adding requirements.txt...")
        lines.extend(
            [
                "RUN python -m pip install --no-cache-dir -r /home/model-server/requirements.txt",
            ]
        )
    if not no_entrypoint:
        lines.extend(
            [
                'ENTRYPOINT ["python", "/usr/local/bin/dockerd-entrypoint.py"]',
            ]
        )
    lines.extend(
        [
            f'CMD ["{command}"]',
        ]
    )

    with open(dockerfile, "a") as d_file:
        d_file.write("\n".join(lines))
    log.info(f"Updated Dockerfile @ `{dockerfile}`")


def create_dockerfile(dockerfile_path: str = ".dockerizer/Dockerfile") -> None:
    """
    This method creates a template Dockerfile which has all basic functionality to run a sagemaker container
    :param dockerfile_path: Path to docker file
    """
    with open(dockerfile_path, "w") as file:
        file.write(standard_dockerfile_content)
    log.info(f"Created a new Dockerfile @ `{dockerfile_path}`")


def build_image(
    image_name: str,
    entry_point: str,
    dockerfile: str = "Dockerfile",
    command: str = "serve",
    worker_count=1,
    entry_point_method="handle",
    use_shell=False,
) -> None:
    """
    Build a Sagemaker endpoint image
    :param image_name: Name of the image
    :param entry_point: Entrypoint to the image. Which script should be run in the container.
    :param dockerfile: Path to Dockerfile
    :param command: Command to be executed inside the server script.
    :param worker_count: Number of workers on the instance
    :param entry_point_method: Which method to run in the entry point script.
                               This method is/calls the predict method based on context
    :param use_shell: Use shell for execution.
    :return:
    """
    if os.path.exists(".dockerizer"):
        log.info("Removing existing `.dockerizer` folder...")
        shutil.rmtree(".dockerizer")
    os.makedirs(".dockerizer")

    with open(".dockerizer/dockerd-entrypoint.py", "w") as ep_file:
        template = Template(server_script)
        args = dict(
            worker_count=worker_count,
            entry_point_file=os.path.basename(entry_point),
            entry_point_method=entry_point_method,
            command=command,
        )
        file_str = template.render(args)
        ep_file.write(file_str)
    log.info(f"Created server script and copied to -> `.dockerizer/dockerd-entrypoint.py`")

    # Process Dockerfile
    if not os.path.exists(dockerfile):
        create_dockerfile(".dockerizer/Dockerfile")
    else:
        shutil.copyfile(dockerfile, ".dockerizer/Dockerfile")
        log.info(f"Copied existing Dockerfile from `{dockerfile}` -> `.dockerizer/Dockerfile`")
    dockerfile = ".dockerizer/Dockerfile"

    # copy all contents of target folder
    head_folder = os.path.split(os.path.abspath(entry_point))[0]
    shutil.copytree(head_folder, ".dockerizer/model_server", ignore=shutil.ignore_patterns(".dockerizer"))
    log.info(f"Copied contents of `{head_folder}` -> `.dockerizer/model_server`")

    has_requirements_file = os.path.exists(".dockerizer/model_server/requirements.txt")
    update_docker_file(dockerfile, command, has_requirements_file)

    start = time.time()
    log.info("Starting docker container build...")

    if use_shell:
        docker_command = (
            f"docker build --progress=plain -t {image_name} -f {dockerfile} "
            f"--secret id=aws,src=$HOME/.aws/credentials .dockerizer"
        )
        log.info(f"Running {docker_command}")
        os.system(docker_command)
    else:
        docker_client = docker.from_env()
        build = docker_client.images.build(path=".dockerizer", tag=image_name)
        log.info(f"Docker_api build : {build}")
    end = time.time()
    log.info(f"Image `{image_name}:latest`" f" was built successfully. Elapsed time: {end - start:.3f} secs.")


def push_image(
    image_name: str,
    model_id: str,
    version: str = "latest",
    region: str = "us-east-1",
    show_progress: bool = True,
    verbose: bool = False,
) -> str:
    """
    Push container to ECR
    :param image_name: Name of the locally built image
    :param model_id: UUID of the model/AI (in `AI` given by `id` property)
    :param version: Version string for docker container
    :param region: AWS region
    :param show_progress: Enable / disable progress bar
    :param verbose: Whether to log the image push stream
    """
    boto_session = get_boto_session(region_name=region)
    account = boto_session.client("sts").get_caller_identity()["Account"]
    env = config.settings.get("name")
    MODEL_ROOT = "models"

    full_suffix = f"{MODEL_ROOT}/{env}/{model_id}/{image_name}"
    if len(full_suffix + str(version)) > 255:
        # AWS allows 256 characters for the name
        logger.warn("Image name is too long. Truncating to 255 characters...")
        full_suffix = full_suffix[: 255 - len(str(version))]
    full_name = f"{account}.dkr.ecr.{region}.amazonaws.com/{full_suffix}:{version}"
    logger.info(f"Pushing image to ECR: {full_name}")

    docker_client = docker.from_env()
    ecr_client = boto_session.client("ecr")
    try:
        ecr_client.describe_repositories(registryId=account, repositoryNames=[full_suffix])
    except Exception as e:
        log.info(e)
        ecr_client.create_repository(repositoryName=full_suffix)
        log.info(f"Created repository for `{full_suffix}`.")

    log.info("Logging in to ECR...")
    os.system(f"$(aws ecr get-login --region {region} --no-include-email)")

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


def get_docker_client() -> DockerClient:
    """
    Returns a Docker client, raising a ModelDeploymentError if the Docker server is not accessible.
    """
    client = docker.from_env()
    try:
        client.ping()
    except (requests.ConnectionError, APIError) as e:
        raise ModelDeploymentError("Could not find a running Docker daemon. Is Docker running?")
    return client


def get_boto_session(profile_name="default", region_name="us-east-1") -> Session:
    """
    Get a boto3 session with the given profile name. For the superai profile, an error message will be raised if
    credentials are expired
    :param profile_name: Name of the profile
    :param region_name: Name of the region
    :return: Boto3 session
    """
    try:
        session = boto3.session.Session(region_name=region_name, profile_name=profile_name)
        _ = session.client("sts").get_caller_identity()["Account"]
        return session
    except ClientError as client_error:
        if "ExpiredToken" in str(client_error):
            log.error(f"Obtained error : {client_error}")
            raise Exception("Please log in to superai by performing 'superai login -u <username>'")
        else:
            log.error(f"Unexpected Exception: {client_error}")
            raise client_error
