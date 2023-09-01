import json
from typing import Union

import click
from rich import print

from superai.cli.helper import pass_client

JSON_ERROR_MESSAGE = "Couldn't read json inputs"


@click.group(name="training")
def ai_training_group():
    """View and manage trainings"""


@ai_training_group.command(name="list")
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


@ai_training_group.command(name="start")
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
            print(JSON_ERROR_MESSAGE)
            exit()

    idx = client.create_training_entry(str(model_id), str(app_id), json_inputs)
    if idx:
        print(f"Started a new training with ID {idx}")


@ai_training_group.command(name="trigger-template")
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


@ai_training_group.group()
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
            print(JSON_ERROR_MESSAGE)
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
            print(JSON_ERROR_MESSAGE)
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
