import contextlib
import functools
import json
import os
import pathlib
import shutil
import signal
import sys
import time
from datetime import datetime
from typing import List, Optional, Union
from urllib.parse import urlparse

import click
import yaml
from pycognito import Cognito
from pycognito.exceptions import SoftwareTokenMFAChallengeException
from requests import ReadTimeout
from rich import print

from superai import __version__
from superai.apis.meta_ai.model import PredictionError
from superai.client import Client
from superai.config import (
    get_config_dir,
    get_current_env,
    list_env_configs,
    set_env_config,
    settings,
)
from superai.exceptions import SuperAIAuthorizationError, SuperAIStorageError
from superai.log import logger
from superai.utils import (
    load_api_key,
    remove_aws_credentials,
    save_api_key,
    save_aws_credentials,
    save_cognito_user,
)
from superai.utils.files import download_file_to_directory
from superai.utils.pip_config import pip_configure
from superai.utils.sso_login import sso_login

BASE_FOLDER = get_config_dir()
COGNITO_USERPOOL_ID = settings.get("cognito", {}).get("userpool_id")
COGNITO_CLIENT_ID = settings.get("cognito", {}).get("client_id")
COGNITO_REGION = settings.get("cognito", {}).get("region")

log = logger.get_logger(__name__)

save_file = ".AISave"


def _signal_handler(s, f):
    sys.exit(1)


@click.group()
def cli():
    pass


def common_params(func):
    @click.option("--verbose", "-v", is_flag=True, help="Verbose output")
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper


@cli.command()
@click.option("--verbose/--no-verbose", "-vvv", help="Verbose output", default=False)
def info(verbose):
    """Prints CLI configuration."""
    click.echo("=================")
    click.echo("Super.AI CLI Info:")
    click.echo("=================")
    load_api_key()
    click.echo(f"VERSION: {__version__}")
    click.echo(f"ENVIRONMENT: {get_current_env()}")
    click.echo(f"USER: {settings.get('user', {}).get('username')}")
    if verbose:
        click.echo(yaml.dump(settings.as_dict(env=get_current_env()), default_flow_style=False))


@cli.group()
@click.pass_context
def env(ctx):
    """Super.AI config operations"""


@env.command(name="list")
@click.pass_context
def env_list(ctx):
    """Args:
    ctx:
    """
    list_env_configs(verbose=True)


@env.command(name="set")
@click.option("--api-key", help="Your super.AI API KEY", required=False)
@click.option("--environment", "-e", help="Set environment", required=False)
@click.pass_context
def env_set(ctx, api_key, environment):
    """Sets configuration."""
    if environment:
        set_env_config(name=environment)
    if api_key:
        save_api_key(api_key)


@cli.group()
@click.pass_context
def client(ctx):
    """Super.AI API operations."""
    api_key = ""
    with contextlib.suppress(Exception):
        api_key = load_api_key()
    if len(api_key) == 0:
        print("User needs to login or set api key")
        exit()
    ctx.obj = {
        "client": Client(api_key=api_key, auth_token=settings.get("user", {}).get("cognito", {}).get("access_token"))
    }


# Create decorator to pass client object when needed
pass_client = click.make_pass_decorator(Client, ensure=True)


@client.command(name="create_jobs")
@click.option("--app_id", "-a", help="Application id", required=True)
@click.option("--callback_url", "-c", help="Callback URL for post when jobs finish")
@click.option("--inputs", "-i", help="Json list with inputs")
@click.option("--inputs_file", "-if", help="URL pointing to JSON file")
@click.pass_context
def create_jobs(ctx, app_id: str, callback_url: str, inputs: str, inputs_file: str):
    """Submits jobs"""
    client = ctx.obj["client"]
    print("Submitting jobs")
    json_inputs = None
    if inputs is not None:
        try:
            json_inputs = json.loads(inputs)
        except Exception:
            print("Couldn't read json inputs")
            exit()
    print(client.create_jobs(app_id, callback_url, json_inputs, inputs_file))


@client.command(name="fetch_job")
@click.option("--job_id", "-j", help="Job id", required=True)
@click.pass_context
def fetch_job(ctx, job_id: str):
    """Gets job given job ID."""
    client = ctx.obj["client"]
    print(f"Fetching job {job_id}")
    print(client.fetch_job(job_id))


@client.command(name="fetch_batches_job")
@click.option("--app_id", "-a", help="App id", required=True)
@click.pass_context
def fetch_batches_job(ctx, app_id: str):
    """Gets unprocessed batches given app ID"""
    client = ctx.obj["client"]
    print(f"Fetching batches {app_id}")
    print(client.fetch_batches_job(app_id))


@client.command(name="fetch_batch_job")
@click.option("--app_id", "-a", help="App id", required=True)
@click.option("--batch_id", "-b", help="Batch id", required=True)
@click.pass_context
def fetch_batch_job(ctx, app_id: str, batch_id: str):
    """Gets batch given app ID and batch ID."""
    client = ctx.obj["client"]
    print(f"Fetching batch {app_id} {batch_id}")
    print(client.fetch_batch_job(app_id, batch_id))


@client.command(name="get_job_response")
@click.option("--job_id", "-j", help="Job id", required=True)
@click.pass_context
def get_job_response(ctx, job_id: str):
    """Gets job response given job ID."""
    client = ctx.obj["client"]
    print(f"Getting job response {job_id}")
    print(client.get_job_response(job_id))


@client.command(name="cancel_job")
@click.option("--job_id", "-j", help="Job id", required=True)
@click.pass_context
def cancel_job(ctx, job_id: str):
    """Cancels a job given job ID. Only for jobs in SCHEDULED, IN_PROGRESS, or SUSPENDED state."""
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
    """Gets a paginated list of jobs (without response) given an application ID."""
    client = ctx.obj["client"]
    print(f"Fetching jobs per application {app_id}")
    if not status_in:
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
    "--send_email/--not_send_email",
    "-se/-nse",
    help="Choose if email is sent at the end",
    default=True,
)
@click.option(
    "--status_in",
    "-s_in",
    help="Status of jobs",
    multiple=True,
    type=click.Choice(["SCHEDULED", "IN_PROGRESS", "FAILED", "SUSPENDED", "CANCELED", "EXPIRED", "COMPLETED"]),
)
@click.option(
    "--with_history/--not_with_history",
    "-wh/-nwh",
    help="Choose if add job history to downloaded data",
    default=False,
)
@click.pass_context
def download_jobs(
    ctx,
    app_id: str,
    created_start_date: datetime,
    created_end_date: datetime,
    completed_start_date: datetime,
    completed_end_date: datetime,
    send_email: bool = None,
    status_in: List[str] = None,
    with_history: bool = None,
):
    """Triggers processing of job responses that is sent to customer email (default) once is finished."""
    client = ctx.obj["client"]
    print(f"Triggering job responses processing per application {app_id}")
    if not status_in:
        status_in = None
    print(
        client.download_jobs(
            app_id,
            created_start_date,
            created_end_date,
            completed_start_date,
            completed_end_date,
            status_in,
            send_email,
            with_history,
        )
    )


@client.command(name="get_jobs_operation")
@click.option("--app_id", "-a", help="Application id", required=True)
@click.option("--operation_id", "-o", help="Operation id", required=True)
@click.pass_context
def get_jobs_operation(
    ctx,
    app_id: str,
    operation_id: str,
):
    """Fetch jobs operation given application id and operation id"""
    client = ctx.obj["client"]
    print(f"Fetching jobs operation per application {app_id} operation {operation_id}")
    print(client.get_jobs_operation(app_id, operation_id))


@client.command(name="downloaded_jobs_url")
@click.option("--app_id", "-a", help="Application id", required=True)
@click.option("--operation_id", "-o", help="Operation id", required=True)
@click.option("--seconds_ttl", "-sttl", help="Seconds ttl for url", default=60, type=click.INT, show_default=True)
@click.pass_context
def downloaded_jobs_url(
    ctx,
    app_id: str,
    operation_id: str,
    seconds_ttl: int,
):
    """Generates downloaded jobs url given application id and operation id"""
    client = ctx.obj["client"]
    print(f"Generating downloaded jobs url per application {app_id} operation {operation_id}")
    print(client.generates_downloaded_jobs_url(app_id, operation_id, seconds_ttl))


@client.command(name="download_tasks")
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
    help="Status of tasks",
    multiple=True,
    type=click.Choice(["SCHEDULED", "IN_PROGRESS", "FAILED", "CANCELED", "PENDING", "EXPIRED", "COMPLETED"]),
)
@click.pass_context
def download_tasks(
    ctx,
    app_id: str,
    created_start_date: datetime,
    created_end_date: datetime,
    completed_start_date: datetime,
    completed_end_date: datetime,
    status_in: List[str] = None,
):
    """Trigger download of tasks data that can be retrieved using task operation id."""
    client = ctx.obj["client"]
    print(f"Triggering task download processing per application {app_id}")
    if not status_in:
        status_in = None
    print(
        client.download_tasks(
            app_id,
            created_start_date,
            created_end_date,
            completed_start_date,
            completed_end_date,
            status_in,
        )
    )


@client.command(name="get_tasks_operation")
@click.option("--app_id", "-a", help="Application id", required=True)
@click.option("--operation_id", "-o", help="Operation id", required=True)
@click.pass_context
def get_tasks_operation(
    ctx,
    app_id: str,
    operation_id: str,
):
    """Fetch tasks operation given application id and operation id"""
    client = ctx.obj["client"]
    print(f"Fetching tasks operation per application {app_id} operation {operation_id}")
    print(client.get_tasks_operation(app_id, operation_id))


@client.command(name="downloaded_tasks_url")
@click.option("--app_id", "-a", help="Application id", required=True)
@click.option("--operation_id", "-o", help="Operation id", required=True)
@click.option("--seconds_ttl", "-sttl", help="Seconds ttl for url", default=60, type=click.INT, show_default=True)
@click.pass_context
def downloaded_tasks_url(
    ctx,
    app_id: str,
    operation_id: str,
    seconds_ttl: int,
):
    """Generates downloaded tasks url given application id and operation id"""
    client = ctx.obj["client"]
    print(f"Generating downloaded tasks url per application {app_id} operation {operation_id}")
    print(client.generates_downloaded_tasks_url(app_id, operation_id, seconds_ttl))


@client.command(name="download_data")
@click.argument("data_url", type=str)
@click.option(
    "--path",
    required=False,
    help="Path to download artifact. Default is current working directory.",
    type=click.Path(exists=True, writable=True, dir_okay=True),
    default=os.getcwd(),
)
@click.pass_context
def download_data(ctx, data_url: str, path: str):
    """Downloads from Super.AI Data Storage to a local file."""
    client = ctx.obj["client"]
    response = client.get_signed_url(data_url)
    signed_url = response["signedUrl"]

    parsed = urlparse(data_url)
    url_path = pathlib.Path(parsed.path)
    filename = url_path.name

    logger.info(f"Downloading {filename} to {path}")
    try:
        download_file_to_directory(url=signed_url, filename=filename, path=path)
    except RuntimeError as e:
        raise SuperAIStorageError(str(e)) from e


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
    """Submits fresh ground truth data."""
    client = ctx.obj["client"]
    print("Submitting fresh ground truth data")
    input_dict = None
    metadata_dict = None
    label_dict = None
    if input_json is not None:
        try:
            input_dict = json.loads(input_json)
        except Exception:
            print("Couldn't load input json of ground truth")
            exit()
    if metadata is not None:
        try:
            metadata_dict = json.loads(metadata)
        except Exception:
            print("Couldn't load metadata json of ground truth")
            exit()
    if label is not None:
        try:
            label_dict = json.loads(label)
        except Exception:
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
    """Updates (PATCH) ground truth data."""
    client = ctx.obj["client"]
    print(f"Updating ground truth data {ground_truth_data_id}")
    input_dict = None
    metadata_dict = None
    label_dict = None
    if input_json is not None:
        try:
            input_dict = json.loads(input_json)
        except Exception:
            print("Couldn't load input json of ground truth")
            exit()
    if metadata is not None:
        try:
            metadata_dict = json.loads(metadata)
        except Exception:
            print("Couldn't load metadata json of ground truth")
            exit()
    if label is not None:
        try:
            label_dict = json.loads(label)
        except Exception:
            print("Couldn't load label json of ground truth")
            exit()
    print(client.update_ground_truth(ground_truth_data_id, input_dict, label_dict, tag, metadata_dict))


@client.command(name="list_ground_truth_data")
@click.option("--app_id", "-a", help="Application id", required=True)
@click.option("--page", "-p", help="Page number", type=int)
@click.option("--size", "-s", help="Size of page", type=int)
@click.pass_context
def list_ground_truth_data(ctx, app_id: str, page: int, size: int):
    """Lists all ground truth data for an application."""
    client = ctx.obj["client"]
    print(f"Fetching ground truth data per application {app_id}")
    print(client.list_ground_truth_data(app_id, page, size))


@client.command(name="get_ground_truth_data")
@click.option("--ground_truth_data_id", "-g", help="Ground truth data id", required=True)
@click.pass_context
def get_ground_truth_data(ctx, ground_truth_data_id: str):
    """Fetches single ground truth data object."""
    client = ctx.obj["client"]
    print(f"Fetching ground truth data {ground_truth_data_id}")
    print(client.get_ground_truth_data(ground_truth_data_id))


@client.command(name="delete_ground_truth_data")
@click.option("--ground_truth_data_id", "-g", help="Ground truth data id", required=True)
@click.pass_context
def delete_ground_truth_data(ctx, ground_truth_data_id: str):
    """Marks ground truth data as deleted."""
    client = ctx.obj["client"]
    print(f"Deleting ground truth data {ground_truth_data_id}")
    print(client.delete_ground_truth_data(ground_truth_data_id))


@client.command(name="create_ground_truth_from_job")
@click.option("--app_id", "-a", help="Application id", required=True)
@click.option("-job_id", "-j", help="Job id", required=True)
@click.pass_context
def create_ground_truth_from_job(ctx, app_id: str, job_id: str):
    """Create ground truth from job"""
    client = ctx.obj["client"]
    print(f"Converting job {job_id} to ground truth data")
    print(client.create_ground_truth_from_job(app_id, job_id))


@client.command(name="workflow_delete")
@click.option(
    "dp_qualified_name", "-d", help="The name of the rounter, for example image_disambiguation.router", required=True
)
@click.option("workflow_name", "-w", help="The name of the workflow", required=True)
@click.pass_context
def delete_workflow(ctx, dp_qualified_name, workflow_name):
    """Delete an existing workflow"""
    client = ctx.obj["client"]
    new_workflows = client.delete_workflow(dp_qualified_name, workflow_name)
    logger.info(
        f"Workflow {workflow_name} deleted with success from {dp_qualified_name}, new workflow list -> {new_workflows}"
    )


@cli.command()
@click.option("--api-key", help="Your super.AI API KEY", required=True)
def config(api_key):
    """Sets API key."""
    save_api_key(api_key)


@cli.command()
@click.option("--account-name", "-a", help="A valid account name", default="superai", show_default=True)
@click.option("--role-name", "-r", help="A valid role name", default="SuperAIDeveloper", show_default=True)
@click.option("--start-url", help="SSO start URL", default="https://superai.awsapps.com/start", show_default=True)
@click.option("--region", help="AWS region", default=settings.region, show_default=True)
def login_sso(account_name, role_name, start_url, region):
    """Login to SSO and add temporary key to the AWS credentials file"""
    sso_login(account_name, role_name, start_url, region)


@cli.command()
@click.option("--username", "-u", help="super.AI Username", required=True)
@click.option("--password", "-p", prompt=True, hide_input=True)
@click.option(
    "--show-pip/--no-show-pip",
    "-pip",
    default=False,
    help="Shows how to set pip configuration manually",
    show_default=True,
)
def login(username, password, show_pip):
    """Uses username and password to get super.AI API key."""
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
    except Exception as e:
        if type(e) is SoftwareTokenMFAChallengeException:
            code = input("Enter the 6-digit code generated by the TOTP generator (such as Google Authenticator): ")
            try:
                user.respond_to_software_token_mfa_challenge(code)
            except Exception as e:
                print(f"Unexpected error: {e}")
                return
        else:
            if hasattr(e, "response") and e.response["Error"]["Code"] in [
                "UserNotFoundException",
                "NotAuthorizedException",
            ]:
                print("Incorrect username or password")
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
    """Removes stored API key."""
    save_api_key("")
    print("Stored api key was removed")


@cli.group()
def ai():
    """View, list and control models and their deployments."""


# Create a CLI validate command that loads the .yaml from the current directory and then instantiates a AI object with it
@ai.command("validate-config")
@click.option("--file", "-f", default="config.yml")
def validate_ai_config(file: pathlib.Path):
    """Validate model definition file"""
    from superai.meta_ai import AI

    ai = AI.from_yaml(file)
    print(ai)


@ai.command("migrate-config")
@click.option("--file", "-f", default="config.yml")
@click.option("--yes", "-y", is_flag=True, default=False)
@click.option("--not-null", "-n", is_flag=True, default=True)
def migrate_ai_config(file: pathlib.Path, yes: bool, not_null: bool):
    """Migrate AI config to new schema."""
    from superai.meta_ai import AI

    ai = AI.from_yaml(file)
    print(ai)
    print("Migrating to new schema...")
    if yes or click.confirm(f"This will overwrite the existing {file}. Do you want to continue?", abort=True):
        ai.to_yaml(file, not_null=not_null)


@ai.command("list")
@click.option("--name", required=False, help="Filter by AI name.")
@click.option("--version", required=False, help="Filter by AI version.")
@pass_client
def list_ai(client, name: Union[click.UUID, str], version: str):
    """List available AI (templates)"""
    if name is None:
        print(client.list_ai())
    elif version is None:
        print(client.list_ai_by_name(str(name)))
    else:
        print(client.list_ai_by_name_version(str(name), str(version)))


@ai.command("list-instances")
@click.option("--name", required=False, help="Filter by instance name.")
@click.option("--ai_name", required=False, help="Filter by AI name.")
@click.option("--ai_version", required=False, help="Filter by AI version.")
@click.option("--visibility", required=False, help="Filter by instance visibility.")
@click.option("--checkpoint_tag", required=False, help="Filter by instance checkpoint tag.")
@common_params
@pass_client
def list_ai_instances(
    client: Client,
    name: str = None,
    ai_name: str = None,
    ai_version: str = None,
    visibility: str = None,
    checkpoint_tag: str = None,
    verbose: bool = False,
):
    """List available AI instances."""
    print(
        client.list_ai_instances(
            name=name,
            ai_name=ai_name,
            to_json=True,
            ai_version=ai_version,
            visibility=visibility,
            checkpoint_tag=checkpoint_tag,
            verbose=verbose,
        )
    )


@ai.command("view")
@click.argument("id", type=click.UUID)
@pass_client
def get_ai(client, id: Union[click.UUID, str]):
    """View model parameters"""
    print(client.get_ai(str(id)))


@ai.command("update")
@click.argument("id", type=click.UUID)
@click.option("--name", required=False, help="AI name")
@click.option("--description", required=False, help="AI description")
@pass_client
def update_ai(client, id: Union[click.UUID, str], name: str, description: str, visibility: str):
    """Update model parameters"""
    params = {}
    if name is not None:
        params["name"] = name
    if description is not None:
        params["description"] = description
    print(client.update_ai(str(id), **params))


@ai.command("download")
@click.argument("artifact_type", type=click.Choice(["source", "weights"]))
@click.argument("id", type=click.UUID)
@click.option("--app-id", required=False, help="Application id, necessary for app trained models.")
@click.option(
    "--path",
    required=False,
    help="Path to download artifact. Default is current working directory.",
    type=click.Path(exists=True, writable=True),
    default=os.getcwd(),
)
@click.option("--timeout", required=False, help="Timeout in seconds", type=int, default=360)
@pass_client
def download_artifact(
    client, id: Union[str, click.UUID], artifact_type: str, app_id: Union[str, click.UUID], path: str, timeout: int
):
    """Download model artifact"""
    url = client.get_artifact_download_url(
        model_id=str(id),
        artifact_type=artifact_type,
        app_id=str(app_id),
        timeout=timeout,
    )

    parsed = urlparse(url)
    url_path = pathlib.Path(parsed.path)
    filename = url_path.name

    logger.info(f"Downloading {filename} to {path}")
    download_file_to_directory(url=url, filename=filename, path=path)


@ai.group()
def method():
    """Directly call the AI methods to train and predict"""


@method.command("train", help="Start training of an AI object")
@click.option(
    "--path",
    "-p",
    default=".",
    help="Path to AI object save location. A new AI template and instance will be created from this path. Ensure this "
    "is the absolute path",
    required=True,
    type=click.Path(exists=True, readable=True, dir_okay=True),
)
@click.option(
    "--model-save-path",
    "-mp",
    help="Path to location where the weights will be saved.",
    required=True,
    show_default=True,
    type=click.Path(),
)
@click.option(
    "--training-data-path",
    "-tp",
    help="Path to location where the training data is stored in the local file system.",
    required=True,
    type=click.Path(exists=False, readable=False),
)
@click.option(
    "--test-data-path",
    "-tsp",
    help="Path to location where the test data is stored in the local file system.",
    type=click.Path(exists=False, readable=False),
)
@click.option(
    "--validation-data-path",
    "-vp",
    help="Path to location where the validation data is stored in the local file system.",
    type=click.Path(exists=False, readable=False),
)
@click.option(
    "--production-data-path",
    "-pp",
    help="Path to location where the production data is stored in the local file system.",
    type=click.Path(exists=False, readable=False),
)
@click.option(
    "--weights-path",
    "-wp",
    help="Path to location where the existing weights is stored local file system.",
    type=click.Path(exists=False, readable=False),
)
@click.option("--encoder-trainable/--no-encoder-trainable", default=False, show_default=True, type=bool)
@click.option("--decoder-trainable/--no-decoder-trainable", default=False, show_default=True, type=bool)
@click.option(
    "--hyperparameters",
    "-h",
    multiple=True,
    help="Hyperparameters to be passed. Please pass them as `-h train_split=0.2 -h cross_valid=False`",
)
@click.option(
    "--model-parameters",
    "-m",
    multiple=True,
    help="Model parameters to be passed. Please pass them as `-m some_parameter=0.2 -h other_parameter=False -h "
    "listed=['list','of','strings']`",
)
@click.option(
    "--callbacks",
    "-cl",
    help="Callbacks to be passed to training (yet to be implemented)",
)
@click.option(
    "--train-logger",
    "-tl",
    multiple=True,
    help="Train logger (yet to be implemented)",
)
def train(
    path,
    model_save_path,
    training_data_path,
    test_data_path,
    validation_data_path,
    production_data_path,
    weights_path,
    encoder_trainable,
    decoder_trainable,
    hyperparameters,
    model_parameters,
    callbacks,
    train_logger,
):
    """Start training locally"""
    from superai.meta_ai.ai import AI
    from superai.meta_ai.parameters import HyperParameterSpec, ModelParameters

    click.echo(
        f"Starting training from the path {path} with hyperparameters {hyperparameters} "
        f"and model parameters {model_parameters}"
    )
    processed_hyperparameters = HyperParameterSpec.load_from_list(hyperparameters)
    processed_model_parameters = ModelParameters.load_from_list(model_parameters)
    ai_object = AI.load(path, weights_path=weights_path)
    ai_object.train(
        model_save_path=model_save_path,
        training_data=training_data_path,
        test_data=test_data_path,
        production_data=production_data_path,
        validation_data=validation_data_path,
        weights_path=weights_path,
        encoder_trainable=encoder_trainable,
        decoder_trainable=decoder_trainable,
        hyperparameters=processed_hyperparameters,
        model_parameters=processed_model_parameters,
        callbacks=callbacks,
        train_logger=train_logger,
    )


@method.command("predict", help="Predict from AI")
@click.option(
    "--path",
    "-p",
    default=".",
    help="Path to AI object save location. A new AI template and instance will be created from this path",
    required=True,
    type=click.Path(exists=True, readable=True),
)
@click.option(
    "--data-path",
    "-dp",
    help="Path to file location where the input data is stored in the local file system.",
    type=click.Path(exists=True, readable=True, dir_okay=False),
    required=False,
)
@click.option("--json-input", "-i", required=False, type=str, help="Prediction input. Should be a valid JSON string")
@click.option(
    "--weights-path",
    "-wp",
    required=False,
    help="Path to weights to be loaded",
    type=click.Path(exists=True, readable=True),
)
@click.option(
    "--metrics-output-dir",
    required=False,
    help="If provided, metrics will be computed and saved to this directory.",
    type=click.Path(file_okay=False, path_type=pathlib.Path),
)
def predict(path, json_input=None, data_path: str = None, weights_path=None, metrics_output_dir=None):
    """Load a model and predict"""
    from superai.meta_ai.ai_helper import load_and_predict

    result = load_and_predict(
        model_path=path,
        weights_path=weights_path,
        data_path=data_path,
        json_input=json_input,
        metrics_output_dir=metrics_output_dir,
    )
    click.echo(f"Result : {result}")


@ai.group(help="Deployed models running in our infrastructure")
def deployment():
    """Deployment CLI group"""


@deployment.command("list")
@pass_client
@click.option(
    "--model_id",
    type=str,
    default=None,
    help="Filter deployments by model id. If provided, only deployments matching this model id will be listed",
)
@click.option(
    "--model_name",
    type=str,
    default=None,
    help="Filter deployments by model name. If provided, only deployments matching this model name will be listed",
)
@click.option(
    "--status",
    type=str,
    default=None,
    help="Filter deployments by status. "
    "If provided, only deployments matching this status will be listed. "
    "Must be one of the values "
    '"FAILED", "MAINTENANCE", "OFFLINE", "ONLINE", "PAUSED", "STARTING", "UNKNOWN"',
)
def list_deployments(
    client, model_id: Optional[str] = None, model_name: Optional[str] = None, status: Optional[str] = None
):
    """List all deployments"""
    d = client.list_deployments(model_id=model_id, model_name=model_name, status=status)
    for deployment in d:
        print(f"[b][u]Model: {deployment.model.name}[/b][/u]")
        print(f"{deployment}\n")


@deployment.command("view")
@click.argument("id", type=click.UUID)
@pass_client
def view_deployment(client, id: Union[str, click.UUID]):
    """View deployment parameters"""
    print(client.get_deployment(str(id)))


@deployment.command("start")
@click.argument("id", type=click.UUID)
@click.option(
    "--wait",
    type=click.INT,
    default=0,
    help="Allow command to block and wait for deployment to be ready. Returns when deployment is ONLINE.",
    show_default=True,
)
@pass_client
def start_deployment(client, id: Union[str, click.UUID], wait: int):
    """Create a deployment for the model."""
    print("Starting deployment...")
    if wait:
        print(f"Waiting for up to {wait} seconds. Note: Some deployments can take up to 15 minutes (900 seconds).")
    reached_state = client.set_deployment_status(str(id), target_status="ONLINE", timeout=wait)
    if reached_state:
        print("Deployment online.")
    else:
        print("Stopped waiting for ONLINE status. Process is still running in the backend.")


@deployment.command("stop")
@click.argument("id", type=click.UUID)
@click.option(
    "--wait",
    type=click.INT,
    default=0,
    help="Allow command to block and wait for deployment to be ready. Returns when deployment is ONLINE.",
    show_default=True,
)
@pass_client
def stop_deployment(client, id: Union[str, click.UUID], wait: int):
    """Stop and tear-down a model deployment."""
    print("Tearing down model deployment...")
    if wait:
        print(f"Waiting for up to {wait} seconds.")
    reached_state = client.set_deployment_status(str(id), target_status="OFFLINE", timeout=wait)
    if reached_state:
        print("Deployment offline.")
    else:
        print("Stopped waiting for OFFLINE status. Process is still running in the backend.")


@deployment.command("predict")
@click.argument("id", type=click.UUID)
@click.argument(
    "data",
    type=str,
)
@click.option(
    "--parameters",
    type=str,
    help="Parameters to be used for prediction. Expected as JSON encoded dictionary.",
)
@click.option(
    "--timeout",
    type=int,
    help="Time to wait for prediction to complete. Expect worst case timeouts of 900 seconds (15 minutes) for new "
    "deployment startups.",
    default=20,
    show_default=True,
)
@pass_client
def predict(client, id: Union[str, click.UUID], data: str, parameters: str, timeout: int):
    """Predict using a deployed model

    `DATA` is the input to be used for prediction. Expected as JSON encoded dictionary.

    """
    try:
        response = client.predict_from_endpoint(
            model_id=str(id),
            input_data=json.loads(data),
            parameters=json.loads(parameters) if parameters else None,
            timeout=timeout,
        )
        print(response)
    except ReadTimeout:
        print("Timeout waiting for prediction to complete. Try increasing --timeout value.")
    except PredictionError:
        # TODO: Print error message when available in object
        print("Prediction failed. Check the logs for more information.")


@ai.group()
def prediction():
    """View and list predictions"""


@prediction.command("view")
@click.argument("id", required=True, type=click.UUID)
@pass_client
def view_prediction(client, id: Union[str, click.UUID]):
    """View prediction object"""
    p = client.get_prediction_with_data(str(id))
    print(p.__json_data__)


@deployment.command(
    "scaling",
    help="Control scaling of deployed models. Currently only supports configuring the automatic scale-in of models "
    "after a period of no prediction activity.",
)
@click.argument("id", type=click.UUID)
@click.option(
    "--min_instances",
    type=click.INT,
    required=False,
    default=0,
    help="Minimum number of instances allowed.",
    show_default=True,
)
@click.option(
    "--scale_in_timeout",
    type=click.INT,
    required=False,
    default=None,
    help="Allow scale-in after this number of seconds without prediction. Should be higher than the time it takes to "
    "startup a model.",
    show_default=True,
)
@pass_client
def scaling(client, id: Union[str, click.UUID], min_instances: int, scale_in_timeout: int):
    """Control scaling of deployed models"""
    current = client.get_deployment(id)
    print(
        f"Current settings:"
        f"\n\tmin_instances: {current['min_instances']}"
        f"\n\tscale_in_timeout: {current['scale_in_timeout']}"
    )
    if min_instances is not None:
        print("Changing config: min_instances")
        print(client.set_min_instances(str(id), min_instances))
    if scale_in_timeout is not None:
        print("Changing config: scale_in_timeout")
        print(client.set_scale_in_timeout(str(id), scale_in_timeout))


@ai.group()
def docker():
    """Docker specific commands"""


@docker.command(name="push")
@click.argument("id", required=True, type=click.UUID)
@click.option(
    "--image-name", "-i", required=True, help="Name of the image to be pushed. You can get this from `docker image ls`"
)
@click.option("--region", "-r", help="AWS region", default=settings.region, show_default=True)
def push_docker_image(model_id: Union[str, click.UUID], image_name: str, region: str):
    """Push the docker image built by `superai model docker-build` to ECR.

    ID is the UUID of the AI model.
    Check `superai ai list` to see the list of models with their UUIDs.
    """
    from superai.meta_ai.ai_helper import push_image

    if ":" in image_name:
        image, version = image_name.split(":")
    else:
        image = image_name
        version = None
    push_image(image_name=image, model_id=str(model_id), version=version, region=region)


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
    type=click.Path(exists=True, readable=True),
)
@click.option(
    "--gpu",
    "-g",
    default=False,
    help="Run docker with GPUs enabled. Make sure this is a GPU container with cuda enabled, "
    "and nvidia-container-runtime installed",
    show_default=True,
)
def docker_run_local(image_name: str, model_path: str, gpu: bool):
    """Run model on local docker"""
    options = [f"-v {os.path.abspath(model_path)}:/opt/ml/model/", "-p 80:8080", "-p 8081:8081 "]
    if gpu:
        options.append("--rm --gpus all")
    options = " ".join(options)
    command = f"docker run {options} {image_name}"
    logger.info(f"Running command: {command}")
    os.system(command)


@ai.group()
def training():
    """View and manage trainings"""


@training.command(name="list")
@click.option("--app_id", "-a", help="Application id", required=False)
@click.option("--model_id", "-m", help="Model id", required=False)
@click.option(
    "--state",
    "-s",
    help="Filter by state",
    required=False,
    default=None,
    show_default=True,
    type=click.Choice(["FINISHED", "IN_PROGRESS", "FAILED", "PAUSED", "UNKNOWN"]),
)
@click.option(
    "--limit", "-l", help="Limit the number of returned rows", required=False, default=10, show_default=True, type=int
)
@pass_client
def list_trainings(client, app_id: Union[str, click.UUID], model_id: Union[str, click.UUID], state: str, limit: int):
    """List trainings. Allows filtering by state and application id."""
    model_id_str = str(model_id) if model_id else None
    app_id_str = str(app_id) if app_id else None
    trainings = client.get_trainings(app_id_str, model_id_str, state=state, limit=limit)
    if trainings:
        print(trainings)


@training.command(name="start")
@click.option("--app_id", "-a", help="Application id", required=True)
@click.option("--model_id", "-m", help="Model id", required=True)
@click.option(
    "--properties",
    "-p",
    help="Custom properties, if not set default ones for the template will be used",
    required=True,
)
@pass_client
def start_training(client, app_id: Union[str, click.UUID], model_id: Union[str, click.UUID], properties: str):
    """Start a new training"""
    json_inputs = None
    if properties:
        try:
            json_inputs = json.loads(properties)
        except Exception:
            print("Couldn't read json inputs")
            exit()

    idx = client.create_training_entry(str(model_id), str(app_id), json_inputs)
    if idx:
        print(f"Started a new training with ID {idx}")


@training.command(name="trigger-template")
@click.option("--app_id", "-a", help="Application id", required=True)
@click.option("--model_id", "-m", help="Model id", required=True)
@click.option("--training_template_id", "-tt", help="Training Template id", required=True)
@click.option("--task-name", "-tn", help="Task name to prepare dataset", required=True, type=str)
@click.option("--properties", "-p", help="Custom properties", required=False, type=dict)
@click.option("--metadata", "-md", help="Metadata", required=False, type=dict)
@pass_client
def trigger_template_training(
    client,
    app_id: Union[str, click.UUID],
    model_id: Union[str, click.UUID],
    training_template_id: Union[str, click.UUID],
    task_name: str,
    properties: dict,
    metadata: dict,
):
    """Start a new training from template"""
    try:
        if properties:
            properties = json.loads(properties)
        if metadata:
            metadata = json.loads(metadata)
    except Exception:
        print("Could process JSON properties or metadata")
        exit()

    idx = client.start_training_from_app_model_template(
        app_id=str(app_id),
        ai_instance_id=str(model_id),
        task_name=task_name,
        training_template_id=str(training_template_id),
        current_properties=properties,
        metadata=metadata,
    )
    if idx:
        print(f"Started new training with ID {idx}")


# @training.command("deploy", help="Deploy a AI from its config file")
# @click.option(
#     "--config-file",
#     "-c",
#     help="Config YAML file containing AI properties and training deployment definition",
#     type=click.Path(exists=True, readable=True, dir_okay=True, path_type=pathlib.Path),
# )
# @click.option("--push/--no-push", "-p/-np", help="Push the model before training", default=True)
# @click.option(
#     "--clean/--no-clean", "-cl/-ncl", help="Remove the local .AISave folder to perform a fresh deployment", default=True
# )
# def training_deploy(config_file, push=True, clean=True):
#     """Deploy a training from config"""
#     from superai.meta_ai.ai import AI
#
#     if clean and os.path.exists(save_file):
#         shutil.rmtree(save_file)
#     ai_object = AI.from_yaml(config_file)
#     ai_object.training_deployment_parameters
#     # TODO: remove all this wrapper code with parameter loading of the AITrainer class
#
#     if config_data.training_deploy is not None:
#         if push:
#             ai_object.save(overwrite=config_data.training_deploy.overwrite)
#         ai_object.training_deploy(
#             training_data_dir=config_data.training_deploy.training_data_dir,
#             skip_build=config_data.training_deploy.skip_build,
#             properties=config_data.training_deploy.properties,
#             training_parameters=config_data.training_deploy.default_training_parameters,
#             enable_cuda=config_data.training_deploy.enable_cuda,
#             build_all_layers=config_data.training_deploy.build_all_layers,
#             envs=config_data.training_deploy.envs,
#             download_base=config_data.training_deploy.download_base,
#         )
#     elif config_data.training_deploy_from_app is not None:
#         if push:
#             ai_object.save(overwrite=config_data.training_deploy_from_app.overwrite)
#         ai_object.start_training_from_app(
#             app_id=config_data.training_deploy_from_app.app_id,
#             task_name=config_data.training_deploy_from_app.task_name,
#             current_properties=config_data.training_deploy_from_app.current_properties,
#             metadata=config_data.training_deploy_from_app.metadata,
#             skip_build=config_data.training_deploy_from_app.skip_build,
#             enable_cuda=config_data.training_deploy_from_app.enable_cuda,
#             build_all_layers=config_data.training_deploy_from_app.build_all_layers,
#             envs=config_data.training_deploy_from_app.envs,
#             download_base=config_data.training_deploy_from_app.download_base,
#         )
#     else:
#         raise ValueError("configuration should contain 'training_deploy' or 'training_deploy_from_app' section")


@training.group()
def template():
    """View and manage training templates"""


@template.command(name="create")
@click.option("--app_id", "-a", help="Application id", required=False, default=None)
@click.option("--model_id", "-m", help="Root Model id or Model id", required=True)
@click.option(
    "--properties",
    "-p",
    help="Training parameters passed to the model when starting training.",
    required=True,
)
@pass_client
def create_template(client, app_id: Union[str, click.UUID], model_id: Union[str, click.UUID], properties: str):
    """Create a template for trainings.
    The template is used to instantiate new training instances.
    """
    json_inputs = None
    if properties:
        try:
            json_inputs = json.loads(properties)
        except Exception:
            print("Couldn't read json inputs")
            exit()

    idx = client.create_training_template_entry(
        ai_instance_id=str(model_id), properties=json_inputs, app_id=str(app_id)
    )
    if idx:
        print(f"Created new training with ID {idx}")


@template.command(name="update")
@click.option("--app_id", "-a", help="Application id", required=False, default=None)
@click.option("--model_id", "-m", help="Model id", required=True)
@click.option(
    "--properties",
    "-p",
    help="Training parameters passed to the model when starting training.",
    required=False,
)
@click.option(
    "--description",
    "-d",
    help="Description of the template",
    required=False,
)
@pass_client
def update_template(
    client, app_id: Union[str, click.UUID], model_id: Union[str, click.UUID], properties: str, description: str
):
    """Update an exising template for trainings.
    The template is used to instantiate new training instances.
    """
    if properties:
        try:
            json_inputs = json.loads(properties)
        except Exception:
            print("Couldn't read json inputs")
            exit()
    else:
        json_inputs = None
    idx = client.update_training_template(
        ai_instance_id=str(model_id), app_id=str(app_id), properties=json_inputs, description=description
    )
    if idx:
        print(f"Updated training template with id={idx}")


@template.command(name="list")
@click.option("--app_id", "-a", help="Application id", required=False, default=None)
@click.option("--model_id", "-m", help="Model id", required=True)
@pass_client
def list_training_templates(client, app_id: Union[str, click.UUID], model_id: Union[str, click.UUID]):
    """List existing training templates."""
    templates = client.get_training_templates(str(model_id), str(app_id))
    if templates:
        print(templates)


@template.command(name="view")
@click.option("--app_id", "-a", help="Application id", required=False, default=None)
@click.option("--template_id", "-t", help="Template id", required=True)
@pass_client
def view_training_template(client, app_id: Union[str, click.UUID], template_id: Union[str, click.UUID]):
    """List existing training templates."""
    template = client.get_training_template(str(template_id), str(app_id))
    if template:
        print(template)


@ai.command("deploy", help="Deploy an AI from its config file")
@click.option(
    "--config-file",
    "-c",
    help="Config YAML file containing AI properties and deployment definition",
    type=click.Path(exists=True, readable=True, dir_okay=True, path_type=pathlib.Path),
    default="config.yml",
)
@click.option(
    "--clean/--no-clean", "-cl/-ncl", help="Remove the local .AISave folder to perform a fresh deployment", default=True
)
@click.option(
    "--update-weights/--no-update-weights",
    "-uw/-nuw",
    help="Force updating the weights. Only respected if weights were uploaded before.",
    default=False,
)
def deploy_ai(config_file, clean=True, update_weights=False):
    """Push and deploy an AI and its artifacts (docker image, default checkpoint)."""
    from superai.meta_ai.ai import AI

    if clean and os.path.exists(save_file):
        shutil.rmtree(save_file)

    ai_object = AI.from_yaml(config_file)
    logger.info(f"Loaded AI: {ai_object}")

    ai_object.save(weights_path=ai_object.weights_path, overwrite=True, create_checkpoint=update_weights)
    logger.info(f"Pushed AI: {ai_object}")
    ai_object.build()
    logger.info(f"Built AI: {ai_object}")
    ai_object.push_image()
    logger.info(f"Pushed AI: {ai_object}")


@ai.command("local-deploy", help="Deploy an AI from its config file")
@click.option(
    "--config-file",
    "-c",
    help="Config YAML file containing AI properties and deployment definition",
    type=click.Path(exists=True, readable=True, dir_okay=True, path_type=pathlib.Path),
    default="config.yml",
)
@click.option(
    "--clean/--no-clean", "-cl/-ncl", help="Remove the local .AISave folder to perform a fresh deployment", default=True
)
@click.option("--redeploy/--no-clean", "-r/-nr", help="Redeploy the existing deployment", default=True)
@click.option("--log/--no-log", "-l/-nl", help="Log the deployment, this blocks the executor", default=False)
@click.option("--skip-build/--no-skip-build", "-sb/-nsb", help="Skip building the docker image", default=False)
@click.option(
    "--update-weights/--no-update-weights",
    "-uw/-nuw",
    help="Force updating the weights. Only respected if weights were uploaded before.",
    default=False,
)
def local_deploy_ai(config_file, clean=True, redeploy=True, log=False, skip_build=False, update_weights=False):
    """Local Deploy an AI model for integration testing"""
    from superai.meta_ai import Orchestrator
    from superai.meta_ai.ai import AI
    from superai.meta_ai.deployed_predictors import LocalPredictor

    if clean and os.path.exists(save_file):
        shutil.rmtree(save_file)

    ai_object = AI.from_yaml(config_file)
    logger.info(f"Loaded AI: {ai_object}")

    ai_object.build(skip_build=skip_build)
    logger.info(f"Built AI: {ai_object}")

    ai_object.save(overwrite=True, create_checkpoint=update_weights)
    logger.info(f"Saved AI: {ai_object}")

    predictor_obj: LocalPredictor = LocalPredictor(
        orchestrator=Orchestrator.LOCAL_DOCKER_K8S,
        deploy_properties=ai_object.default_deployment_parameters,
        local_image_name=ai_object.local_image,
        weights_path=ai_object.weights_path,
    )
    predictor_obj.deploy(redeploy=redeploy)
    predictor_dict = {predictor_obj.__class__.__name__: predictor_obj.to_dict()}
    with open(ai_object.cache_path() / ".predictor_config.json", "w") as f:
        click.echo(f"Storing predictor config in cache path {ai_object.cache_path() / '.predictor_config.json'}")
        json.dump(predictor_dict, f)

    if log:
        predictor_obj.log()


@ai.command("local-undeploy", help="Undeploy an AI from its config file")
@click.option(
    "--config-file",
    "-c",
    help="Config YAML file containing AI properties and deployment definition",
    type=click.Path(exists=True, readable=True, dir_okay=True, path_type=pathlib.Path),
    default="config.yml",
)
@click.option(
    "--clean/--no-clean", "-cl/-ncl", help="Remove the local .AISave folder to perform a fresh deployment", default=True
)
def local_undeploy_ai(config_file, clean=True):
    """Local Un-Deploy an AI model for integration testing"""
    from superai.meta_ai.ai import AI
    from superai.meta_ai.deployed_predictors import DeployedPredictor

    if clean and os.path.exists(save_file):
        shutil.rmtree(save_file)

    ai_object = AI.from_yaml(config_file)
    print(f"Loaded AI: {ai_object}")

    config_path = ai_object.cache_path() / ".predictor_config.json"
    if not config_path.exists():
        raise click.ClickException(f"Predictor config does not exist at {config_path}")
    with open(config_path, "r") as predictor_config:
        predictor_dictionary = json.load(predictor_config)
        log.info(f"Loading predictor config: {predictor_dictionary}")

    predictor_obj: DeployedPredictor = DeployedPredictor.from_dict(predictor_dictionary, client)
    predictor_obj.terminate()
    # Remove the cache path folder
    if config_path.exists():
        shutil.rmtree(config_path.parent)


@ai.command("create-instance", help="Create an AI instance from an AI config file")
@click.option(
    "--config-file",
    "-c",
    help="Config YAML file containing AI properties and deployment definition",
    type=click.Path(exists=True, readable=True, dir_okay=True, path_type=pathlib.Path),
    default="config.yml",
)
@click.option(
    "--clean/--no-clean", "-cl/-ncl", help="Remove the local .AISave folder to perform a fresh deployment", default=True
)
@click.option(
    "--visibility",
    "-V",
    help="Visibility of the AI instance",
    type=click.Choice(["PUBLIC", "PRIVATE"]),
    default="PRIVATE",
)
@click.option(
    "--deploy",
    "-d",
    help="Deploy the AI instance after creation",
    type=click.Choice(["True", "False"]),
    default="True",
)
# add name and weights path options
@click.option("--name", "-n", help="Name of the AI instance", type=str, default=None)
@click.option(
    "--weights-path",
    "-wp",
    help="Path to the weights file to be used for the AI instance. Can be a local path or a URI",
    type=str,
    default=None,
)
@click.option(
    "--instance-config",
    "-ic",
    help="Instance config file",
    type=click.Path(exists=False, readable=False, dir_okay=False, path_type=pathlib.Path),
    default="instance_config.yml",
)
@click.option(
    "--force-clone-checkpoint",
    "-fcc",
    help="Force cloning the checkpoint from the AI to the AI instance",
    type=click.Choice(["True", "False"]),
    default="False",
)
@click.option(
    "--orchestrator",
    "-o",
    help="Orchestrator to use for deployment",
    default="AWS_EKS_ASYNC",
    type=click.Choice(["AWS_EKS", "AWS_EKS_ASYNC"]),
)
def create_ai_instance(
    config_file,
    clean=True,
    visibility="PRIVATE",
    deploy=True,
    name=None,
    weights_path=None,
    instance_config=None,
    force_clone_checkpoint=False,
    orchestrator="AWS_EKS_ASYNC",
):
    """Push and deploy an AI and its artifacts (docker image, default checkpoint)."""
    from superai.meta_ai.ai import AI

    if clean and os.path.exists(save_file):
        shutil.rmtree(save_file)

    ai_object = AI.from_yaml(config_file, pull_db_data=True)
    if visibility != ai_object.visibility:
        ai_object.visibility = visibility
        log.warning(f"Setting visibility of AI to {visibility}.")

    print(f"Loaded AI: {ai_object}")
    ai_object.save(overwrite=True)
    print(f"Saved AI: {ai_object}")
    if name or weights_path:
        # Override config when name or weights_path is provided
        instances = [
            ai_object.create_instance(
                visibility=visibility,
                name=name,
                weights_path=weights_path,
                force_clone_checkpoint=force_clone_checkpoint,
            )
        ]
    elif instance_config.exists():
        from superai.meta_ai.ai_instance import instantiate_instances_from_config

        print(f"Loading instance config from {instance_config}")
        instances = instantiate_instances_from_config(
            instance_config, ai_object, visibility=visibility, force_clone_checkpoint=force_clone_checkpoint
        )
    else:
        instances = [ai_object.create_instance(visibility=visibility, force_clone_checkpoint=force_clone_checkpoint)]

    print(f"Created AI instances: {instances}")

    if deploy:
        for instance in instances:
            instance.deploy(redeploy=True, orchestrator=orchestrator)
            print(f"Deployed AI instance: {instance}")


@ai.command("build", help="Build an AI from its config file")
@click.option(
    "--config-file",
    "-c",
    help="Config YAML file containing AI properties and deployment definition",
    type=click.Path(exists=True, readable=True, dir_okay=True, path_type=pathlib.Path),
    default="config.yml",
)
@click.option(
    "--clean/--no-clean", "-cl/-ncl", help="Remove the local .AISave folder to perform a fresh deployment", default=True
)
def build_ai(config_file, clean=True):
    """Build an AI image locally. Can be used for testing (in CI/CD)."""
    from superai.meta_ai.ai import AI

    if clean and os.path.exists(save_file):
        shutil.rmtree(save_file)

    ai_object = AI.from_yaml(config_file)
    print(f"Loaded AI: {ai_object}")

    ai_object.build()
    print(f"Built AI: {ai_object}")


@ai.command("predictor-test", help="Test the predictor created from the deploy command")
@click.option(
    "--config-file",
    "-c",
    help="Points to the config file",
    type=click.Path(exists=True, readable=True, dir_okay=True, path_type=pathlib.Path),
    default="config.yml",
)
@click.option("--predict-input", "-i", help="Prediction input", type=str, required=False)
@click.option("--predict-input-file", "-if", help="Prediction input file", type=click.Path(), required=False)
@click.option("--predict-input-folder", "-ifo", help="Prediction input folder", type=click.Path(), required=False)
@click.option(
    "--expected-output",
    "-o",
    help="Expected output (should only be used if your model is consistent)",
    type=str,
    required=False,
)
@click.option(
    "--expected-output-file",
    "-of",
    help="Expected output file (should only be used if your model is consistent",
    type=click.Path(),
)
@click.option("--wait-seconds", "-w", help="Seconds to wait for the predictor to be ready", type=int, default=1)
@pass_client
def predictor_test(
    client,
    config_file,
    predict_input=None,
    predict_input_file=None,
    predict_input_folder=None,
    expected_output=None,
    expected_output_file=None,
    wait_seconds=1,
):
    """Deploy and test a predictor from config file"""
    from superai.meta_ai.ai import AI
    from superai.meta_ai.deployed_predictors import DeployedPredictor

    log.info(f"Waiting for predictor to be ready, {wait_seconds} seconds")
    time.sleep(wait_seconds)

    ai_object = AI.from_yaml(config_file)
    ai_object.save(overwrite=True)
    print(ai_object.cache_path())
    config_path = ai_object.cache_path() / ".predictor_config.json"
    if not config_path.exists():
        raise click.ClickException(f"Predictor config does not exist at {config_path}")
    with open(config_path, "r") as predictor_config:
        predictor_dictionary = json.load(predictor_config)
        log.info(f"Loading predictor config: {predictor_dictionary}")
    predictor: DeployedPredictor = DeployedPredictor.from_dict(predictor_dictionary, client)
    if predict_input is not None:
        predict_input = json.loads(predict_input)
        predicted_output = predictor.predict(predict_input)
        click.echo(predicted_output)
        assert predicted_output is not None
    elif predict_input_file is not None:
        with open(predict_input_file, "r") as predict_file_stream:
            predict_input = json.load(predict_file_stream)
        predicted_output = predictor.predict(predict_input)
        click.echo(predicted_output)
        assert predicted_output is not None
    elif predict_input_folder is not None:
        folder = pathlib.Path(predict_input_folder)
        predicted_output = []
        for file in folder.iterdir():
            if not file.suffix == ".json":
                continue
            with open(file, "r") as predict_file_stream:
                predict_input = json.load(predict_file_stream)
                output = predictor.predict(predict_input)
                assert output is not None
                predicted_output.append(output)
    else:
        raise ValueError("One of --predict-input, --predict-input-file, --predict-input-folder should be passed")

    expected_message = "Expected output should be same as predicted output"
    if expected_output is not None:
        assert predicted_output == expected_output, expected_message
        expected_output = json.loads(expected_output)
        assert predicted_output.dict() == expected_output, expected_message
    if expected_output_file is not None:
        with open(expected_output_file, "r") as output_file_stream:
            expected_output = json.load(output_file_stream)
            assert predicted_output == expected_output, expected_message
            assert predicted_output.dict() == expected_output, expected_message


@ai.command("predictor-teardown", help="Teardown the predictor in context")
@click.option(
    "--config-file",
    "-c",
    help="Points to the config file",
    type=click.Path(exists=True, readable=True, dir_okay=True, path_type=pathlib.Path),
)
@pass_client
def predictor_teardown(client, config_file):
    """Remove a deployed predictor from config file"""
    from superai.meta_ai.ai import AI
    from superai.meta_ai.deployed_predictors import DeployedPredictor

    ai_object = AI.from_yaml(config_file)
    config_path = os.path.join(
        settings.path_for(), "cache", ai_object.name, str(ai_object.version), ".predictor_config.json"
    )
    if os.path.exists(config_path):
        with open(config_path, "r") as predictor_config:
            predictor_dictionary = json.load(predictor_config)
        predictor: DeployedPredictor = DeployedPredictor.from_dict(predictor_dictionary, client)
        predictor.terminate()
        logger.info(f"Removing predictor config at {config_path}")
        os.remove(config_path)
    else:
        raise click.ClickException(f"Predictor config did not exist at {config_path}")


def main():
    """Entrypoint"""
    signal.signal(signal.SIGINT, _signal_handler)
    sys.exit(cli())


if __name__ == "__main__":
    main()
