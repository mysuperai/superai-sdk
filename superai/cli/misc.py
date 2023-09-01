import contextlib
import json
import os
import pathlib
from datetime import datetime
from typing import List
from urllib.parse import urlparse

import click
from rich import print

from superai.client import Client
from superai.config import settings
from superai.exceptions import SuperAIStorageError
from superai.log import logger
from superai.utils import load_api_key
from superai.utils.files import download_file_to_directory

log = logger.get_logger(__name__)


@click.group(name="client")
@click.pass_context
def api_client(ctx):
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


@api_client.command(name="create_jobs")
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


@api_client.command(name="fetch_job")
@click.option("--job_id", "-j", help="Job id", required=True)
@click.pass_context
def fetch_job(ctx, job_id: str):
    """Gets job given job ID."""
    client = ctx.obj["client"]
    print(f"Fetching job {job_id}")
    print(client.fetch_job(job_id))


@api_client.command(name="fetch_batches_job")
@click.option("--app_id", "-a", help="App id", required=True)
@click.pass_context
def fetch_batches_job(ctx, app_id: str):
    """Gets unprocessed batches given app ID"""
    client = ctx.obj["client"]
    print(f"Fetching batches {app_id}")
    print(client.fetch_batches_job(app_id))


@api_client.command(name="fetch_batch_job")
@click.option("--app_id", "-a", help="App id", required=True)
@click.option("--batch_id", "-b", help="Batch id", required=True)
@click.pass_context
def fetch_batch_job(ctx, app_id: str, batch_id: str):
    """Gets batch given app ID and batch ID."""
    client = ctx.obj["client"]
    print(f"Fetching batch {app_id} {batch_id}")
    print(client.fetch_batch_job(app_id, batch_id))


@api_client.command(name="get_job_response")
@click.option("--job_id", "-j", help="Job id", required=True)
@click.pass_context
def get_job_response(ctx, job_id: str):
    """Gets job response given job ID."""
    client = ctx.obj["client"]
    print(f"Getting job response {job_id}")
    print(client.get_job_response(job_id))


@api_client.command(name="cancel_job")
@click.option("--job_id", "-j", help="Job id", required=True)
@click.pass_context
def cancel_job(ctx, job_id: str):
    """Cancels a job given job ID. Only for jobs in SCHEDULED, IN_PROGRESS, or SUSPENDED state."""
    client = ctx.obj["client"]
    print(f"Cancelling job {job_id}")
    print(client.cancel_job(job_id))


@api_client.command(name="list_jobs")
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


@api_client.command(name="download_jobs")
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


@api_client.command(name="get_jobs_operation")
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


@api_client.command(name="downloaded_jobs_url")
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


@api_client.command(name="download_tasks")
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


@api_client.command(name="get_tasks_operation")
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


@api_client.command(name="downloaded_tasks_url")
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


@api_client.command(name="download_data")
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


@api_client.command(name="create_ground_truth")
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


@api_client.command(name="update_ground_truth")
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


@api_client.command(name="list_ground_truth_data")
@click.option("--app_id", "-a", help="Application id", required=True)
@click.option("--page", "-p", help="Page number", type=int)
@click.option("--size", "-s", help="Size of page", type=int)
@click.pass_context
def list_ground_truth_data(ctx, app_id: str, page: int, size: int):
    """Lists all ground truth data for an application."""
    client = ctx.obj["client"]
    print(f"Fetching ground truth data per application {app_id}")
    print(client.list_ground_truth_data(app_id, page, size))


@api_client.command(name="get_ground_truth_data")
@click.option("--ground_truth_data_id", "-g", help="Ground truth data id", required=True)
@click.pass_context
def get_ground_truth_data(ctx, ground_truth_data_id: str):
    """Fetches single ground truth data object."""
    client = ctx.obj["client"]
    print(f"Fetching ground truth data {ground_truth_data_id}")
    print(client.get_ground_truth_data(ground_truth_data_id))


@api_client.command(name="delete_ground_truth_data")
@click.option("--ground_truth_data_id", "-g", help="Ground truth data id", required=True)
@click.pass_context
def delete_ground_truth_data(ctx, ground_truth_data_id: str):
    """Marks ground truth data as deleted."""
    client = ctx.obj["client"]
    print(f"Deleting ground truth data {ground_truth_data_id}")
    print(client.delete_ground_truth_data(ground_truth_data_id))


@api_client.command(name="create_ground_truth_from_job")
@click.option("--app_id", "-a", help="Application id", required=True)
@click.option("-job_id", "-j", help="Job id", required=True)
@click.pass_context
def create_ground_truth_from_job(ctx, app_id: str, job_id: str):
    """Create ground truth from job"""
    client = ctx.obj["client"]
    print(f"Converting job {job_id} to ground truth data")
    print(client.create_ground_truth_from_job(app_id, job_id))


@api_client.command(name="workflow_delete")
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
