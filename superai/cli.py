import os

import boto3
import click
import json
import signal
import sys
import yaml
from botocore.exceptions import ClientError
from datetime import datetime
from typing import List
from warrant import Cognito

from superai import __version__
from superai.client import Client
from superai.config import get_config_dir, list_env_configs, set_env_config, settings
from superai.exceptions import SuperAIAuthorizationError
from superai.log import logger
from superai.utils import load_api_key, remove_aws_credentials, save_api_key, save_aws_credentials, save_cognito_user
from superai.utils.pip_config import pip_configure
from superai.meta_ai.dockerizer import build_image, push_image
from superai.meta_ai.dockerizer.sagemaker_endpoint import (
    upload_model_to_s3,
    invoke_sagemaker_endpoint,
    create_endpoint,
    invoke_local,
)

BASE_FOLDER = get_config_dir()
COGNITO_USERPOOL_ID = settings.get("cognito", {}).get("userpool_id")
COGNITO_CLIENT_ID = settings.get("cognito", {}).get("client_id")
COGNITO_REGION = settings.get("cognito", {}).get("region")

log = logger.get_logger(__name__)


def _signal_handler(s, f):
    sys.exit(1)


@click.group()
def cli():
    pass


@cli.command()
@click.option("--verbose/--no-verbose", "-vvv", help="Verbose output", default=False)
def info(verbose):
    """Print CLI Configuration"""
    click.echo("=================")
    click.echo("Super.AI CLI Info:")
    click.echo("=================")
    load_api_key()
    click.echo(f"VERSION: {__version__}")
    click.echo(f"ENVIRONMENT: {settings.current_env}")
    click.echo(f"USER: {settings.get('user',{}).get('username')}")
    if verbose:
        click.echo(yaml.dump(settings.as_dict(env=settings.current_env), default_flow_style=False))


@cli.group()
@click.pass_context
def env(ctx):
    """
    super.AI Config operations
    """
    pass


@env.command(name="list")
@click.pass_context
def env_list(ctx):
    """

    :param ctx:
    :return:
    """
    list_env_configs(printInConsole=True)


@env.command(name="set")
@click.option("--api-key", help="Your super.AI API KEY", required=False)
@click.option("--environment", "-e", help="Set environment", required=False)
@click.pass_context
def env_set(ctx, api_key, environment):
    """
    Set configuration
    """
    if environment:
        set_env_config(name=environment)
    if api_key:
        save_api_key(api_key)


@cli.group()
@click.pass_context
def client(ctx):
    """
    super.AI API operations
    """
    api_key = ""
    try:
        api_key = load_api_key()
    except Exception as e:
        pass
    if len(api_key) == 0:
        print("User needs to login or set api key")
        exit()
    ctx.obj = {}
    ctx.obj["client"] = Client(api_key=api_key)


@client.command(name="create_jobs")
@click.option("--app_id", "-a", help="Application id", required=True)
@click.option("--callback_url", "-c", help="Callback URL for post when jobs finish")
@click.option("--inputs", "-i", help="Json list with inputs")
@click.option("--inputs_file", "-if", help="URL pointing to JSON file")
@click.pass_context
def create_jobs(ctx, app_id: str, callback_url: str, inputs: str, inputs_file: str):
    """
    Submit jobs
    """
    client = ctx.obj["client"]
    print("Submitting jobs")
    json_inputs = None
    if inputs is not None:
        try:
            json_inputs = json.loads(inputs)
        except:
            print("Couldn't read json inputs")
            exit()
    print(client.create_jobs(app_id, callback_url, json_inputs, inputs_file))


@client.command(name="fetch_job")
@click.option("--job_id", "-j", help="Job id", required=True)
@click.pass_context
def fetch_job(ctx, job_id: str):
    """
    Get Job given job id
    """
    client = ctx.obj["client"]
    print(f"Fetching job {job_id}")
    print(client.fetch_job(job_id))


@client.command(name="fetch_batches_job")
@click.option("--app_id", "-a", help="App id", required=True)
@click.pass_context
def fetch_batches_job(ctx, app_id: str):
    """
    Get not processed Batches given app id
    """
    client = ctx.obj["client"]
    print(f"Fetching batches {app_id}")
    print(client.fetch_batches_job(app_id))


@client.command(name="fetch_batch_job")
@click.option("--app_id", "-a", help="App id", required=True)
@click.option("--batch_id", "-b", help="Batch id", required=True)
@click.pass_context
def fetch_batch_job(ctx, app_id: str, batch_id: str):
    """
    Get Batch given app id and batch id
    """
    client = ctx.obj["client"]
    print(f"Fetching batch {app_id} {batch_id}")
    print(client.fetch_batch_job(app_id, batch_id))


@client.command(name="get_job_response")
@click.option("--job_id", "-j", help="Job id", required=True)
@click.pass_context
def get_job_response(ctx, job_id: str):
    """
    Get Job response given job id
    """
    client = ctx.obj["client"]
    print(f"Getting job response {job_id}")
    print(client.get_job_response(job_id))


@client.command(name="cancel_job")
@click.option("--job_id", "-j", help="Job id", required=True)
@click.pass_context
def cancel_job(ctx, job_id: str):
    """
    Cancel a job given job id. Only for jobs in SCHEDULED, IN_PROGRESS or SUSPENDED state.
    """
    client = ctx.obj["client"]
    print(f"Cancelling job {job_id}")
    print(client.cancel_job(job_id))


@client.command(name="list_jobs")
@click.option("--app_id", "-a", help="Application id", required=True)
@click.option("--page", "-p", help="Page number", type=int)
@click.option("--size", "-s", help="Size of page", type=int)
@click.option("--sort_by", "-sort", help="Job field to sort by", type=str, default="id", show_default=True)
@click.option(
    "--order_by",
    "-order",
    help="Sort direction (asc or desc)",
    type=click.Choice(["asc", "desc"]),
    default="asc",
    show_default=True,
)
@click.option(
    "--created_start_date",
    "-c0",
    help="Created start date",
    type=click.DateTime(formats=["%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%d"]),
)
@click.option(
    "--created_end_date",
    "-c1",
    help="Created end date",
    type=click.DateTime(formats=["%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%d"]),
)
@click.option(
    "--completed_start_date",
    "-e0",
    help="Completed start date",
    type=click.DateTime(formats=["%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%d"]),
)
@click.option(
    "--completed_end_date",
    "-e1",
    help="Completed end date",
    type=click.DateTime(formats=["%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%d"]),
)
@click.option(
    "--status_in",
    "-s_in",
    help="Status of jobs",
    multiple=True,
    type=click.Choice(["SCHEDULED", "IN_PROGRESS", "FAILED", "SUSPENDED", "CANCELED", "EXPIRED", "COMPLETED"]),
)
@click.pass_context
def list_jobs(
    ctx,
    app_id: str,
    page: int,
    size: int,
    sort_by: str,
    order_by: str,
    created_start_date: datetime,
    created_end_date: datetime,
    completed_start_date: datetime,
    completed_end_date: datetime,
    status_in: List[str] = None,
):
    """
    Get a paginated list of jobs (without response) given an application id
    """
    client = ctx.obj["client"]
    print(f"Fetching jobs per application {app_id}")
    if len(status_in) == 0:
        status_in = None
    print(
        client.list_jobs(
            app_id,
            page,
            size,
            sort_by,
            order_by,
            created_start_date,
            created_end_date,
            completed_start_date,
            completed_end_date,
            status_in,
        )
    )


@client.command(name="download_jobs")
@click.option("--app_id", "-a", help="Application id", required=True)
@click.option(
    "--created_start_date",
    "-c0",
    help="Created start date",
    type=click.DateTime(formats=["%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%d"]),
)
@click.option(
    "--created_end_date",
    "-c1",
    help="Created end date",
    type=click.DateTime(formats=["%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%d"]),
)
@click.option(
    "--completed_start_date",
    "-e0",
    help="Completed start date",
    type=click.DateTime(formats=["%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%d"]),
)
@click.option(
    "--completed_end_date",
    "-e1",
    help="Completed end date",
    type=click.DateTime(formats=["%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%d"]),
)
@click.option(
    "--status_in",
    "-s_in",
    help="Status of jobs",
    multiple=True,
    type=click.Choice(["SCHEDULED", "IN_PROGRESS", "FAILED", "SUSPENDED", "CANCELED", "EXPIRED", "COMPLETED"]),
)
@click.pass_context
def download_jobs(
    ctx,
    app_id: str,
    created_start_date: datetime,
    created_end_date: datetime,
    completed_start_date: datetime,
    completed_end_date: datetime,
    status_in: List[str] = None,
):
    """
    Trigger processing of job responses that is sent to customer email once is finished.
    """
    client = ctx.obj["client"]
    print(f"Triggering job responses processing per application {app_id}")
    if len(status_in) == 0:
        status_in = None
    print(
        client.download_jobs(
            app_id, created_start_date, created_end_date, completed_start_date, completed_end_date, status_in
        )
    )


@client.command(name="create_ground_truth")
@click.option("--app_id", "-a", help="Application id", required=True)
@click.option("--input_json", "-i", help="Input json of ground truth", required=True)
@click.option("--label", "-l", help="Label (or output) json of ground truth", required=True)
@click.option("--tag", "-t", help="Tag ground truth data")
@click.option("--metadata", "-m", help="Metadata json")
@click.pass_context
def create_ground_truth(
    ctx, app_id: str, input_json: str = None, label: str = None, tag: str = None, metadata: str = None
):
    """
    Submit fresh ground truth data
    """
    client = ctx.obj["client"]
    print("Submitting fresh ground truth data")
    input_dict = None
    metadata_dict = None
    label_dict = None
    if input_json is not None:
        try:
            input_dict = json.loads(input_json)
        except:
            print("Couldn't load input json of ground truth")
            exit()
    if metadata is not None:
        try:
            metadata_dict = json.loads(metadata)
        except:
            print("Couldn't load metadata json of ground truth")
            exit()
    if label is not None:
        try:
            label_dict = json.loads(label)
        except:
            print("Couldn't load label json of ground truth")
            exit()
    print(client.create_ground_truth(app_id, input_dict, label_dict, tag, metadata_dict))


@client.command(name="update_ground_truth")
@click.option("--ground_truth_data_id", "-g", help="Ground truth data id", required=True)
@click.option("--input_json", "-i", help="Input json of ground truth")
@click.option("--label", "-l", help="Label (or output) json of ground truth")
@click.option("--tag", "-t", help="Tag ground truth data")
@click.option("--metadata", "-m", help="Metadata json")
@click.pass_context
def update_ground_truth(
    ctx, ground_truth_data_id: str, input_json: str = None, label: str = None, tag: str = None, metadata: str = None
):
    """
    Update (patch) ground truth data
    """
    client = ctx.obj["client"]
    print(f"Updating ground truth data {ground_truth_data_id}")
    input_dict = None
    metadata_dict = None
    label_dict = None
    if input_json is not None:
        try:
            input_dict = json.loads(input_json)
        except:
            print("Couldn't load input json of ground truth")
            exit()
    if metadata is not None:
        try:
            metadata_dict = json.loads(metadata)
        except:
            print("Couldn't load metadata json of ground truth")
            exit()
    if label is not None:
        try:
            label_dict = json.loads(label)
        except:
            print("Couldn't load label json of ground truth")
            exit()
    print(client.update_ground_truth(ground_truth_data_id, input_dict, label_dict, tag, metadata_dict))


@client.command(name="list_ground_truth_data")
@click.option("--app_id", "-a", help="Application id", required=True)
@click.option("--page", "-p", help="Page number", type=int)
@click.option("--size", "-s", help="Size of page", type=int)
@click.pass_context
def list_ground_truth_data(ctx, app_id: str, page: int, size: int):
    """
    List all ground truth data for an application
    """
    client = ctx.obj["client"]
    print(f"Fetching ground truth data per application {app_id}")
    print(client.list_ground_truth_data(app_id, page, size))


@client.command(name="get_ground_truth_data")
@click.option("--ground_truth_data_id", "-g", help="Ground truth data id", required=True)
@click.pass_context
def get_ground_truth_data(ctx, ground_truth_data_id: str):
    """
    Fetch single ground truth data object
    """
    client = ctx.obj["client"]
    print(f"Fetching ground truth data {ground_truth_data_id}")
    print(client.get_ground_truth_data(ground_truth_data_id))


@client.command(name="delete_ground_truth_data")
@click.option("--ground_truth_data_id", "-g", help="Ground truth data id", required=True)
@click.pass_context
def delete_ground_truth_data(ctx, ground_truth_data_id: str):
    """
    Mark ground truth data as deleted
    """
    client = ctx.obj["client"]
    print(f"Deleting ground truth data {ground_truth_data_id}")
    print(client.delete_ground_truth_data(ground_truth_data_id))


@client.command(name="create_ground_truth_from_job")
@click.option("--app_id", "-a", help="Application id", required=True)
@click.option("-job_id", "-j", help="Job id", required=True)
@click.pass_context
def create_ground_truth_from_job(ctx, app_id: str, job_id: str):
    client = ctx.obj["client"]
    print(f"Converting job {job_id} to ground truth data")
    print(client.create_ground_truth_from_job(app_id, job_id))


@cli.command()
@click.option("--api-key", help="Your super.AI API KEY", required=True)
def config(api_key):
    """
    Set api key.
    """
    save_api_key(api_key)


@cli.command()
@click.option("--username", "-u", help="super.AI Username", required=True)
@click.option("--password", "-p", prompt=True, hide_input=True)
@click.option("--show-pip/--no-show-pip", "-pip", default=False, help="Shows how to set pip configuration manually")
def login(username, password, show_pip):
    """
    Use username and password to get super.AI api key.
    """
    user = Cognito(
        access_key="AKIAIOSFODNN7EXAMPLE",
        secret_key="wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY",
        user_pool_id=COGNITO_USERPOOL_ID,
        client_id=COGNITO_CLIENT_ID,
        user_pool_region=COGNITO_REGION,
        username=username,
    )
    try:
        user.authenticate(password)
    except ClientError as e:
        if (
            e.response["Error"]["Code"] == "UserNotFoundException"
            or e.response["Error"]["Code"] == "NotAuthorizedException"
        ):
            print("Incorrect username or password")
            return
        else:
            print(f"Unexpected error: {e}")
            return

    client = Client(auth_token=user.access_token, id_token=user.id_token)
    api_keys = client.get_apikeys()
    if len(api_keys) > 0:
        save_api_key(api_keys[0], username=username)
        save_cognito_user(user)
        print(f"Api key {api_keys[0]} was set")
    else:
        print(f"User {username} doesn't have any api keys")

    try:
        aws_credentials = client.get_awskeys()
        if aws_credentials:
            save_aws_credentials(aws_credentials)
            pip_configure(show_pip=show_pip)
    except SuperAIAuthorizationError as authorization_error:
        logger.debug(f"ERROR Authorization: {str(authorization_error)}")
        remove_aws_credentials()
    except Exception as exception:
        logger.debug(f"ERROR: {str(exception)}")
        remove_aws_credentials()


@cli.command()
def logout():
    """
    Remove stored api key
    """
    save_api_key("")
    print("Stored api key was removed")


@cli.group()
def ai():
    """Build and push your model docker images"""
    pass


@ai.group()
def docker():
    """Docker specific commands"""
    pass


@docker.command(name="build", help="Build a docker image for a sagemaker model.")
@click.option("--image-name", "-i", required=True, help="Name of the image to be built")
@click.option(
    "--entry-point",
    "-e",
    required=True,
    help="Path to file which will serve as entrypoint to the sagemaker model. Generally this is a method which calls "
    "the predict method",
)
@click.option("--dockerfile", "-d", help="Path to Dockerfile. Default: Dockerfile", default="Dockerfile")
@click.option(
    "--command", "-c", help="Command to run after the entrypoint in the image. Default: serve", default="serve"
)
@click.option("--worker-count", "-w", help="Number of workers to run. Default: 1", default=1)
@click.option(
    "--entry-point-method",
    "-em",
    help="Method to be called inside the entry point. Make sure this method accepts the input data and context. "
    "Default: handle",
    default="handle",
)
@click.option(
    "--use-shell", "-u", help="Use shell to run the build process, which is more verbose. Used by default", default=True
)
def build_docker_image(image_name, entry_point, dockerfile, command, worker_count, entry_point_method, use_shell):
    build_image(
        image_name=image_name,
        entry_point=entry_point,
        dockerfile=dockerfile,
        command=command,
        worker_count=worker_count,
        entry_point_method=entry_point_method,
        use_shell=use_shell,
    )


@docker.command(name="push", help="Push the docker image built by `superai model docker-build` to ECR. ")
@click.option(
    "--image-name", "-i", required=True, help="Name of the image to be pushed. You can get this from `docker image ls`"
)
@click.option("--region", "-r", help="AWS region.  Default: us-east-1", default="us-east-1")
def push_docker_image(image_name, region):
    push_image(image_name=image_name, region=region)


@docker.command(
    "run-local",
    help="Run a docker container built by `superai model docker-build` locally. "
    "We assume here that the ports 8080 & 8081 are available",
)
@click.option("--image-name", "-i", required=True, help="Name of the image to be run")
@click.option(
    "--model-path",
    "-m",
    required=True,
    help="Path to the folder containing weights file to be used for getting inference",
)
@click.option(
    "--gpu",
    "-g",
    default=False,
    help="Run docker with GPUs enabled. Make sure this is a GPU container with cuda enabled, "
    "and nvidia-container-runtime installed",
)
def docker_run_local(image_name, model_path, gpu):
    options = [f"-v {os.path.abspath(model_path)}:/opt/ml/model/", "-p 80:8080", "-p 8081:8081 "]
    if gpu:
        options.append("--rm --gpus all")
    options = " ".join(options)
    command = f"docker run {options} {image_name}"
    logger.info(f"Running command: {command}")
    os.system(command)


@docker.command(
    "invoke-local",
    help="Invoke the locally deployed container. The API description of the local container can be found at "
    "http://localhost/api-description",
)
@click.option(
    "--mime",
    "-mm",
    default="application/json",
    help="MIME type of the payload. `application/json` will be sent to the invocation directly. For other MIME types, "
    "you can pass the path to file with --body. If its a valid path, it will be loaded and sent to the request. "
    "Default: `application/json`",
)
@click.option(
    "--body", "-b", required=True, help="Body of payload to be sent to the invocation. Can be a path to a file as well."
)
def docker_invoke_local(mime, body):
    invoke_local(mime, body)


def main():
    signal.signal(signal.SIGINT, _signal_handler)
    sys.exit(cli())


if __name__ == "__main__":
    main()
