import click
from rich import print

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


@ai_instance_group.command("instantiate")
@click.option(
    "--ai_uri",
    "-a",
    required=True,
    help="URI of the AI you want to instantiate. E.g. 'ai://superai/doc-processor'",
)
@click.option("--name", "-n", required=True, help="Name of the new instance.")
def instantiate(ai_uri: str, name: str):
    """Instantiate a new AI instance from an existing AI."""
    from superai.meta_ai.ai_uri import AiURI

    uri = AiURI.parse(ai_uri)
    if uri.owner_name != "superai":
        log.warning("Only superai models can be instantiated currently.")
        return

    from superai.meta_ai.ai_helper import instantiate_superai

    instance = instantiate_superai(ai_name=uri.model_name, ai_version=uri.version, new_instance_name=name)
    log.info(f"Instantiated new AI instance: {instance}")
