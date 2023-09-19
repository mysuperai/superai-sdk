import json
from pathlib import Path
from typing import Optional, Union

import click
from requests import ReadTimeout
from rich import print

from superai.apis.meta_ai.model import PredictionError
from superai.cli.helper import common_params, pass_client
from superai.client import Client
from superai.log import logger

log = logger.get_logger(__name__)


@click.group(name="instance")
def ai_instance_group():
    """AI Instance commands.
    An AI instance is a specific version of an AI that is ready to be deployed.
    It is created from an AI template and usually namespaced to a specific user or organization.
    """


@ai_instance_group.command("list")
@click.option("--name", required=False, help="Filter by instance name.")
@click.option("--ai_name", required=False, help="Filter by AI name.")
@click.option("--ai_version", required=False, help="Filter by AI version.")
@click.option("--visibility", required=False, help="Filter by instance visibility.")
@click.option("--checkpoint_tag", required=False, help="Filter by instance checkpoint tag.")
@click.option(
    "--fuzzy/--strict", is_flag=True, help="Fuzzy search by AI name or version.", default=True, show_default=True
)
@click.option("--owned-by-me", is_flag=True, help="Filter by AI owned by me.")
@click.option("--organization", required=False, type=str, help="Filter by Organization name.")
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
    owned_by_me: bool = False,
    organization: str = None,
    fuzzy: bool = True,
):
    """List available AI instances."""
    if organization:
        organization = client._get_organization_id(organization)
    owner_id = client._get_user_id() if owned_by_me else None
    print(
        client.list_ai_instances(
            name=name,
            ai_name=ai_name,
            to_json=True,
            ai_version=ai_version,
            visibility=visibility,
            checkpoint_tag=checkpoint_tag,
            verbose=verbose,
            organization_id=organization,
            owner_id=owner_id,
            fuzzy=fuzzy,
        )
    )


@ai_instance_group.command("view")
@click.argument("instance_uuid", type=click.UUID)
@click.option("--detailed", "-d", is_flag=True, help="Show detailed information about the AI instance.")
@pass_client
def view_ai_instance(client: Client, instance_uuid: Union[str, click.UUID], detailed: bool = False):
    """View a single AI instance."""
    print(client.get_ai_instance(str(instance_uuid), to_json=True, view_checkpoint=detailed))


@ai_instance_group.command("instantiate")
@click.option(
    "--ai_uri",
    "-a",
    help="URI of the AI you want to instantiate. E.g. 'ai://superai/doc-processor'",
)
@click.option("--name", "-n", help="Name of the new instance.")
@click.option("--ai_uuid", "-u", help="UUID of the AI you want to instantiate.")
def instantiate(ai_uri: str = None, name: str = None, ai_uuid: str = None):
    """Instantiate a new AI instance from an existing AI."""
    if not ai_uri and not ai_uuid:
        log.warning("Please provide either an AI URI or an AI UUID.")
        return

    from superai.meta_ai.ai_helper import instantiate_superai

    if ai_uri:
        from superai.meta_ai.ai_uri import AiURI

        uri = AiURI.parse(ai_uri)
        if uri.owner_name != "superai":
            log.warning("Only superai models can be instantiated currently.")
            return
        instance = instantiate_superai(ai_name=uri.model_name, ai_version=uri.version, new_instance_name=name)
    else:
        instance = instantiate_superai(ai_uuid=ai_uuid, new_instance_name=name)
    log.info(f"Instantiated new AI instance: {instance}")


# Add two CLI functions to deploy and undeploy an AI instance
@ai_instance_group.command("deploy")
@click.option("--instance_uuid", "-i", help="UUID of the AI instance to deploy.", required=True)
@click.option("--redeploy", help="Will force redeploy of existing deployment.", required=False, default=True)
@click.option("--wait_time_seconds", "-w", help="Time to wait for deployment to complete.", required=False, default=10)
def deploy(instance_uuid: str, redeploy: bool = True, wait_time_seconds: int = 10):
    """Deploy an AI instance."""

    from superai.meta_ai import AIInstance

    i = AIInstance.load(instance_uuid)
    i.deploy(redeploy=redeploy, wait_time_seconds=wait_time_seconds)


@ai_instance_group.command("undeploy")
@click.option("--instance_uuid", "-i", help="UUID of the AI instance to undeploy.", required=True)
@click.option(
    "--wait_time_seconds", "-w", help="Time to wait for undeployment to complete.", required=False, default=10
)
def undeploy(instance_uuid: str, wait_time_seconds: int = 10):
    """Undeploy an AI instance."""

    from superai.meta_ai import AIInstance

    i = AIInstance.load(instance_uuid)
    i.undeploy(wait_time_seconds=wait_time_seconds)


@ai_instance_group.command("predict")
@click.argument("instance_uuid", type=click.UUID)
@click.option(
    "--data",
    "-d",
    help="Input to be used for prediction. Expected as JSON encoded dictionary.",
    type=str,
)
@click.option(
    "--data-file",
    "-f",
    help="Input file to be used for prediction. Expected as JSON encoded dictionary.",
    type=click.Path(exists=True),
)
@click.option(
    "--parameters",
    type=str,
    help="Parameters to be used for prediction. Expected as JSON encoded dictionary.",
    default=None,
)
@click.option(
    "--timeout",
    type=int,
    help="Time to wait for prediction to complete. Expect worst case timeouts of 900 seconds (15 minutes) for new "
    "deployment startups.",
    default=60,
    show_default=True,
)
@pass_client
def predict(
    client,
    instance_uuid: Union[str, click.UUID],
    data: Optional[str] = None,
    data_file: Optional[Path] = None,
    parameters: str = None,
    timeout: int = None,
):
    """Predict using a deployed AI instance."""
    if not data and not data_file:
        log.warning("Please provide either --data or --data-file.")
        return
    if data_file:
        with open(data_file, "r") as f:
            data = f.read()
    try:
        response = client.predict_from_endpoint(
            model_id=str(instance_uuid),
            input_data=json.loads(data),
            parameters=json.loads(parameters) if parameters else None,
            timeout=timeout,
        )
        print(response)
    except ReadTimeout:
        print("Timeout waiting for prediction to complete. Try increasing --timeout value.")
    except PredictionError as e:
        log.exception(f"Remote prediction failed. Error message from AI: {e.args[0]}", exc_info=False)
