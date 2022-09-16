import os
import shutil
import subprocess
import time
from typing import Optional, Tuple

import boto3  # type: ignore
import docker  # type: ignore
import requests
from boto3.session import Session  # type: ignore
from botocore.exceptions import ClientError  # type: ignore
from docker import DockerClient  # type: ignore
from docker.errors import DockerException  # type: ignore
from jinja2 import Template
from rich.progress import BarColumn, DownloadColumn, Progress, Task, Text

from superai.log import logger

from ... import config
from ..exceptions import ModelDeploymentError
from .sagemaker_endpoint import (
    create_endpoint,
    invoke_local,
    invoke_sagemaker_endpoint,
    upload_model_to_s3,
)

log = logger.get_logger(__name__)
ECR_MODEL_ROOT_PREFIX = "models"


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
        docker_client = get_docker_client()
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


def ecr_full_name(image_name, version, model_id, region: str = "us-east-1") -> Tuple[str, str, str]:
    boto_session = get_boto_session(region_name=region)
    account = boto_session.client("sts").get_caller_identity()["Account"]
    full_suffix, repository_name = ecr_registry_suffix(image_name, model_id, version)
    registry_prefix = f"{account}.dkr.ecr.{region}.amazonaws.com"
    full_name = f"{registry_prefix}/{full_suffix}"
    return full_name, registry_prefix, repository_name


def ecr_registry_suffix(image_name: str, model_id: str, tag: str) -> Tuple[str, str]:
    env = config.settings.get("name")
    full_suffix = f"{ECR_MODEL_ROOT_PREFIX}/{env}/{model_id}/{image_name}"
    if len(full_suffix + str(tag)) > 255:
        # AWS allows 256 characters for the name
        logger.warning("Image name is too long. Truncating to 255 characters...")
        full_suffix = full_suffix[: 255 - len(str(tag))]
    full_suffix_with_version = f"{full_suffix}:{tag}"
    return full_suffix_with_version, full_suffix


def aws_ecr_login(region: str, registry_name: str) -> Optional[int]:
    log.info("Logging in to ECR...")

    # aws --version | awk '{print $1}' | awk -F/ '{ print $2}'
    aws_version = subprocess.check_output(["aws", "--version"]).decode("utf-8").strip().split(" ")[0].split("/")[1]
    aws_major = aws_version.split(".")[0]

    def aws_cli_v1_login():
        return subprocess.Popen(
            ["aws", "ecr", "get-login", "--region", region, "--no-include-email"], stdout=subprocess.PIPE
        )

    def aws_cli_v2_login():
        return subprocess.Popen(["aws", "ecr", "get-login-password", "--region", region], stdout=subprocess.PIPE)

    ecr_login_proc = aws_cli_v1_login() if int(aws_major) < 2 else aws_cli_v2_login()
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


def get_docker_client() -> DockerClient:
    """
    Returns a Docker client, raising a ModelDeploymentError if the Docker server is not accessible.
    """
    try:
        client = docker.from_env(timeout=10)
        client.ping()
    except (DockerException, requests.ConnectionError) as e:
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
