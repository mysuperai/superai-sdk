import json
import os
import shutil
import time
from typing import Optional, Dict

import boto3
import docker
import requests
import sagemaker
from botocore.exceptions import ClientError
from jinja2 import Template
from sagemaker import get_execution_role

from superai.log import logger

from .sagemaker_endpoint import create_endpoint, invoke_sagemaker_endpoint

log = logger.get_logger(__name__)


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


def push_image(image_name: str, version: str = "latest", region: str = "us-east-1") -> str:
    """
    Push container to ECR
    :param image_name: Name of the locally built image
    :param version: version string for docker container
    :param region: AWS region
    """
    boto_session = boto3.Session(region_name=region)
    account = boto_session.client("sts").get_caller_identity()["Account"]
    full_name = f"{account}.dkr.ecr.{region}.amazonaws.com/{image_name}:{version}"

    docker_client = docker.from_env()

    ecr_client = boto3.client("ecr")
    try:
        ecr_client.describe_repositories(registryId=account, repositoryNames=[image_name])
    except Exception as e:
        log.info(e)
        ecr_client.create_repository(repositoryName=image_name)
        log.info(f"Created repository for `{image_name}`.")

    log.info("Logging in to ECR...")
    os.system(f"$(aws ecr get-login --region {region} --no-include-email)")

    log.info(f"Tagging to `{full_name}`")
    docker_client.images.get(f"{image_name}:{version}").tag(full_name)

    log.info(" Pushing image...")
    for line in docker_client.images.push(repository=full_name, stream=True, decode=True):
        log.info(line)

    log.info(f" Image pushed successfully to {full_name} ")
    return full_name


def create_endpoint(
    image_name=None,
    model_url=None,
    version="latest",
    arn_role: Optional[str] = None,
    region: str = "us-east-1",
    initial_instance_count: int = 1,
    instance_type: str = "ml.p2.xlarge",
    mode: str = "SingleModel",
):
    """
    Create endpoint on AWS Sagemaker
    :param image_name: Base image name which is already pushed on ECR
    :param model_url: S3 URI of location where the model weights and params are placed.
                      for :param mode="MultiModel" this is a folder location and
                      for :param mode="SingleModel" this should be a location to a `tar.gz` file
    :param initial_instance_count: Number of instances to serve on the endpoint
    :param instance_type: Type of AWS instance to be used in the endpoint. Note that you cannot use GPU instances for
                          :param mode="MultiModel"
    :param mode: "SingleModel" or "MultiModel" type of instance to use
    """
    sm_client = boto3.client(service_name="sagemaker")
    if arn_role is not None:
        # arn_role = "arn:aws:iam::185169359328:role/service-role/AmazonSageMaker-ExecutionRole-20180117T160866"
        sts_client = boto3.client("sts")
        assumed_role_object = sts_client.assume_role(
            RoleArn=arn_role, RoleSessionName="MultiEndpointSession", ExternalId="0c18cdd7-3626-497d-8c4e-f3fb5ce76cd1"
        )
        credentials = assumed_role_object["Credentials"]
        boto_session = boto3.Session(
            aws_access_key_id=credentials["AccessKeyId"],
            aws_secret_access_key=credentials["SecretAccessKey"],
            aws_session_token=credentials["SessionToken"],
            region_name=region,
        )
        account_id = sts_client.get_caller_identity()["Account"]
        region = boto_session.region_name
        sagemaker_session = sagemaker.Session(boto_session=boto_session)
        role = get_execution_role(sagemaker_session)
    else:
        region = boto3.Session().region_name
        role = get_execution_role()
        account_id = boto3.client("sts").get_caller_identity()["Account"]

    image_name = f"{account_id}.dkr.ecr.{region}.amazonaws.com/{image_name}:{version}"
    model_name = f"DEMO-{image_name}-" + time.strftime("%Y-%m-%d-%H-%M-%S", time.gmtime())
    log.info("Container image: " + image_name)
    log.info("Model name: " + model_name)
    log.info("Model data Url: " + model_url)

    assert mode in ["SingleModel", "MultiModel"], "Mode should be one of ['SingleModel', 'MultiModel']"
    container: Dict[str, str] = {"Image": image_name, "ModelDataUrl": model_url, "Mode": mode}

    try:
        create_model_response = sm_client.create_model(
            ModelName=model_name, ExecutionRoleArn=role, Containers=[container]
        )
    except Exception as e:
        if mode == "SingleModel":
            assert model_url.endswith(".tar.gz"), "For SingleModel mode, you need to provide a path to `tar.gz`"
        log.error("Check that `model_url` is a folder for `MultiModel` mode and a `tar.gz` for `SingleModel`")
        raise e

    log.info("Model Arn: " + create_model_response["ModelArn"])

    endpoint_config_name = f"Deploy-{image_name}-" + time.strftime("%Y-%m-%d-%H-%M-%S", time.gmtime())
    log.info("Endpoint config name: " + endpoint_config_name)

    create_endpoint_config_response = sm_client.create_endpoint_config(
        EndpointConfigName=endpoint_config_name,
        ProductionVariants=[
            {
                "InstanceType": instance_type,
                "InitialInstanceCount": initial_instance_count,
                "InitialVariantWeight": 1,
                "ModelName": model_name,
                "VariantName": "AllTraffic",
            }
        ],
    )

    log.info("Endpoint config Arn: " + create_endpoint_config_response["EndpointConfigArn"])

    endpoint_name = f"DEMO-{image_name}-" + time.strftime("%Y-%m-%d-%H-%M-%S", time.gmtime())
    log.info("Endpoint name: " + endpoint_name)

    create_endpoint_response = sm_client.create_endpoint(
        EndpointName=endpoint_name, EndpointConfigName=endpoint_config_name
    )
    log.info("Endpoint Arn: " + create_endpoint_response["EndpointArn"])

    resp = sm_client.describe_endpoint(EndpointName=endpoint_name)
    status = resp["EndpointStatus"]
    log.info("Endpoint Status: " + status)

    log.info("Waiting for {} endpoint to be in service...".format(endpoint_name))
    waiter = sm_client.get_waiter("endpoint_in_service")
    waiter.wait(EndpointName=endpoint_name)
    log.info(f"{create_endpoint_response['EndpointArn']} ready for invocations")


def upload_model_to_s3(bucket: str, prefix: str, model: str):
    """
    Upload model file to s3, model file should end with .tar.gz
    :param bucket: Bucket name in s3
    :param prefix: Prefix name
    :param model: Path to model file
    """
    assert model.endswith(".tar.gz"), "Model path should point to a tar.gz file"
    s3 = boto3.resource("s3")
    try:
        s3.meta.client.head_bucket(Bucket=bucket)
    except ClientError:
        s3.create_bucket(Bucket=bucket, CreateBucketConfiguration={"LocationConstraint": boto3.Session().region_name})

    key = os.path.join(prefix, model)
    with open("data/" + model, "rb") as file_obj:
        s3.Bucket(bucket).Object(key).upload_fileobj(file_obj)
        log.info(f"Loaded model to bucket: {bucket}, prefix: {prefix}, with path: {model}")


def invoke_local(mime: str, body: str):
    """
    Send a post request to the locally deployed docker container
    :param mime: MIME type
    :param body: Body or path to file to be passed as payload
    """
    url = f"http://localhost/model/predict"
    headers = {"Content-Type": mime}
    if mime.endswith("json"):
        res = requests.post(url, json=body, headers=headers)
    else:
        if os.path.exists(body):
            with open(body, "rb") as f:
                payload = f.read()
        else:
            payload = body
        res = requests.post(url, data=payload, headers=headers)
    if res.status_code == 200:
        log.info(res.json())
    else:
        message = "Error , received error code {}: {}".format(res.status_code, res.text)
        log.error(message)


def invoke_sagemaker_endpoint(endpoint, mime, payload, mode="SingleModel", target_model=None, arn_role=None):
    # arn_role = "arn:aws:iam::185169359328:role/service-role/AmazonSageMaker-ExecutionRole-20180117T160866"
    assert mode in ["SingleModel", "MultiModel"], "Mode should be one of ['SingleModel', 'MultiModel']"
    if mode == "MultiModel":
        assert target_model is not None, "TargetModel is required when using 'MultiModel' mode"
        assert target_model.endswith(
            ".tar.gz"
        ), "TargetModel should point to a 'tar.gz' file. Just the file name should be enough"
    if arn_role is None:
        runtime_sm_client = boto3.client(service_name="sagemaker-runtime")
    else:
        sts_client = boto3.client("sts")
        ext_id = "0c18cdd7-3626-497d-8c4e-f3fb5ce76cd1"
        assumed_role_object = sts_client.assume_role(
            RoleArn=arn_role, RoleSessionName="MultiEndpointSession", ExternalId=ext_id
        )
        credentials = assumed_role_object["Credentials"]
        boto_session = boto3.Session(
            aws_access_key_id=credentials["AccessKeyId"],
            aws_secret_access_key=credentials["SecretAccessKey"],
            aws_session_token=credentials["SessionToken"],
            region_name="us-east-1",
        )
        runtime_sm_client = boto_session.client(service_name="sagemaker-runtime")
    body = payload
    if not mime.endswith("json"):
        if os.path.exists(payload):
            with open(payload, "rb") as f:
                body = f.read()
    if mode == "SingleModel":
        response = runtime_sm_client.invoke_endpoint(EndpointName=endpoint, ContentType=mime, Body=body)
    else:
        response = runtime_sm_client.invoke_endpoint(
            EndpointName=endpoint,
            ContentType=mime,
            TargetModel=target_model,
            Body=body,
        )
    log.info(f"Response from endpoint: {response}")
    print(*json.loads(response["Body"].read()), sep="\n")
