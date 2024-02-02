import json
import os
import pathlib
import shutil
from typing import Optional, Union
from urllib.parse import urlparse

import click
from rich import print

from superai.cli.ai_instance import ai_instance_group
from superai.cli.ai_methods import ai_method_group
from superai.cli.ai_training import ai_training_group
from superai.cli.helper import pass_client
from superai.client import Client
from superai.config import settings
from superai.log import logger
from superai.utils.files import download_file_to_directory

PREDICTOR_CONFIG_JSON = ".predictor_config.json"

log = logger.get_logger(__name__)

save_file = ".AISave"


@click.group(name="ai")
@click.option("--organization", "-o", help="Organization name", required=False, default=None)
@click.pass_context
def ai_group(ctx, organization: str):
    """View, list and control models and their deployments."""
    ctx.obj = {"client": Client.from_credentials(organization_name=organization)}


ai_group.add_command(ai_method_group)
ai_group.add_command(ai_training_group)
ai_group.add_command(ai_instance_group)


# Create a CLI validate command that loads the .yaml from the current directory and then instantiates a AI object with it
@ai_group.command("validate-config")
@click.option("--file", "-f", default="config.yml")
def validate_ai_config(file: pathlib.Path):
    """Validate model definition file"""
    from superai.meta_ai import AI

    ai = AI.from_yaml(file)
    print(ai)


@ai_group.command("export-local")
@click.option("--file", "-f", default="config.yml")
@click.option("--output-dir", "-o", default=".AISave", help="Output directory to save the AI config file.")
@click.option("--overwrite", "-w", is_flag=True, default=False, help="Overwrite existing file.")
def export_ai(file: pathlib.Path, output_dir: pathlib.Path, overwrite: bool):
    """Exports all the files necessary to deploy the AI locally."""
    from superai.meta_ai import AI

    ai = AI.from_yaml(file)
    ai._save_local(path=output_dir, overwrite=overwrite)


@ai_group.command("migrate-config")
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


@ai_group.command("list")
@click.option("--name", required=False, help="Filter by AI name.")
@click.option("--version", required=False, help="Filter by AI version.")
@click.option("--organization", required=False, type=str, help="Filter by Organization.")
@click.option("--owned-by-me", is_flag=True, help="Filter by AI owned by me.")
@click.option(
    "--fuzzy/--strict", is_flag=True, help="Fuzzy search by AI name or version.", default=True, show_default=True
)
@pass_client
def list_ai(client, name: Union[click.UUID, str], version: str, organization: str, fuzzy: bool, owned_by_me: bool):
    """List available AI (templates)"""
    if organization:
        organization = client._get_organization_id(organization)
    owner_id = client._get_user_id() if owned_by_me else None
    print(
        client.list_ai(
            name=str(name) if name else None,
            version=str(version) if version else None,
            organization_id=organization,
            owner_id=owner_id,
            fuzzy=fuzzy,
        )
    )


@ai_group.command("view")
@click.argument("id", type=click.UUID)
@pass_client
def get_ai(client, id: Union[click.UUID, str]):
    """View model parameters"""
    print(client.get_ai(str(id)))


@ai_group.command("update")
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


@ai_group.command("download")
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

    log.info(f"Downloading {filename} to {path}")
    download_file_to_directory(url=url, filename=filename, path=path)


@ai_group.group(help="Deployed models running in our infrastructure")
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
        print(f"[b][u]Model: {deployment.modelv2s.name}[/b][/u]")
        print(f"{deployment}\n")


@deployment.command("view")
@click.argument("id", type=click.UUID)
@pass_client
def view_deployment(client, id: Union[str, click.UUID]):
    """View deployment parameters"""
    print(client.get_deployment(str(id)))


@ai_group.group()
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


@ai_group.group()
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
    log.info(f"Running command: {command}")
    os.system(command)


@ai_group.command("deploy", help="Deploy an AI from its config file")
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
    log.info(f"Loaded AI: {ai_object}")

    ai_object.save(weights_path=ai_object.weights_path, overwrite=True, create_checkpoint=update_weights)
    log.info(f"Pushed AI: {ai_object}")
    ai_object.build()
    log.info(f"Built AI: {ai_object}")
    ai_object.push_image()
    log.info(f"Pushed AI: {ai_object}")


@ai_group.command("local-deploy", help="Deploy an AI from its config file")
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
@click.option(
    "--log/--no-log", "-l/-nl", "log_predictor", help="Log the deployment, this blocks the executor", default=False
)
@click.option("--skip-build/--no-skip-build", "-sb/-nsb", help="Skip building the docker image", default=False)
@click.option(
    "--update-weights/--no-update-weights",
    "-uw/-nuw",
    help="Force updating the weights. Only respected if weights were uploaded before.",
    default=False,
)
def local_deploy_ai(
    config_file, clean=True, redeploy=True, log_predictor=False, skip_build=False, update_weights=False
):
    """Local Deploy an AI model for integration testing"""
    from superai.meta_ai import Orchestrator
    from superai.meta_ai.ai import AI
    from superai.meta_ai.deployed_predictors import LocalPredictor

    if clean and os.path.exists(save_file):
        shutil.rmtree(save_file)

    ai_object = AI.from_yaml(config_file)
    log.info(f"Loaded AI: {ai_object}")

    ai_object.build(skip_build=skip_build)
    log.info(f"Built AI: {ai_object}")

    ai_object.save(overwrite=True, create_checkpoint=update_weights)
    log.info(f"Saved AI: {ai_object}")

    predictor_obj: LocalPredictor = LocalPredictor(
        orchestrator=Orchestrator.LOCAL_DOCKER_K8S,
        deploy_properties=ai_object.default_deployment_parameters,
        local_image_name=ai_object.local_image,
        weights_path=ai_object.weights_path,
    )
    predictor_obj.deploy(redeploy=redeploy)
    predictor_dict = {predictor_obj.__class__.__name__: predictor_obj.to_dict()}
    with open(ai_object.cache_path() / PREDICTOR_CONFIG_JSON, "w") as f:
        click.echo(f"Storing predictor config in cache path {ai_object.cache_path() /PREDICTOR_CONFIG_JSON}")
        json.dump(predictor_dict, f)

    if log_predictor:
        predictor_obj.log()


@ai_group.command("local-undeploy", help="Undeploy an AI from its config file")
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

    config_path = ai_object.cache_path() / PREDICTOR_CONFIG_JSON
    if not config_path.exists():
        raise click.ClickException(f"Predictor config does not exist at {config_path}")
    with open(config_path, "r") as predictor_config:
        predictor_dictionary = json.load(predictor_config)
        log.info(f"Loading predictor config: {predictor_dictionary}")
    client = ai_object._client
    predictor_obj: DeployedPredictor = DeployedPredictor.from_dict(predictor_dictionary, client)
    predictor_obj.terminate()
    # Remove the cache path folder
    if config_path.exists():
        shutil.rmtree(config_path.parent)


@ai_group.command("create-instance", help="Create an AI instance from a local AI config file")
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
    """Push and deploy an AI and its artifacts (docker image, default checkpoint)
    Is used in CI/CD flow for AIs. Requires a local AI config file.
    """
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
            from superai.meta_ai.exceptions import DockerImageNotFoundError

            try:
                instance.deploy(redeploy=True, orchestrator=orchestrator)
                print(f"Deployed AI instance: {instance}")
            except DockerImageNotFoundError:
                raise click.ClickException(
                    f"Missing docker image for AI instance {instance.id}. Try building the image first with `superai ai build`."
                )


@ai_group.command("build", help="Build an AI from its config file")
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
    # Return image name
    click.echo(ai_object.local_image)


@ai_group.command("predictor-test", help="Test the predictor created from the deploy command")
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
    from superai.meta_ai.deployed_predictors import DeployedPredictor, LocalPredictor

    ai_object = AI.from_yaml(config_file)
    ai_object.save(overwrite=True)
    print(ai_object.cache_path())
    config_path = ai_object.cache_path() / ".predictor_config.json"
    if not config_path.exists():
        raise click.ClickException(f"Predictor config does not exist at {config_path}")
    with open(config_path, "r") as predictor_config:
        predictor_dictionary = json.load(predictor_config)
        log.info(f"Loading predictor config: {predictor_dictionary}")
    predictor: LocalPredictor = DeployedPredictor.from_dict(predictor_dictionary, client)
    log.info(f"Waiting for predictor to be ready, {wait_seconds} seconds")
    is_ready = predictor.wait_until_ready(timeout=wait_seconds)
    if not is_ready:
        raise click.ClickException(f"Predictor was not ready after {wait_seconds} seconds")
    log.info("Predictor is ready")

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


@ai_group.command("predictor-ping", help="Ping the predictor in context")
@click.option(
    "--config-file",
    "-c",
    help="Points to the config file",
    type=click.Path(exists=True, readable=True, dir_okay=True, path_type=pathlib.Path),
)
@pass_client
def predictor_ping(client, config_file):
    """Ping the predictor in context"""
    from superai.meta_ai.ai import AI
    from superai.meta_ai.deployed_predictors import DeployedPredictor, LocalPredictor

    ai_object = AI.from_yaml(config_file)
    config_path = ai_object.cache_path() / PREDICTOR_CONFIG_JSON
    if os.path.exists(config_path):
        with open(config_path, "r") as predictor_config:
            predictor_dictionary = json.load(predictor_config)
        predictor: LocalPredictor = DeployedPredictor.from_dict(predictor_dictionary)
        is_alive = predictor.ping()
        # Return exit code 0 if ping is successful
        exit(0 if is_alive else 1)
    else:
        raise click.ClickException(f"Predictor config did not exist at {config_path}")


@ai_group.command("predictor-teardown", help="Teardown the predictor in context")
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
        log.info(f"Removing predictor config at {config_path}")
        os.remove(config_path)
    else:
        raise click.ClickException(f"Predictor config did not exist at {config_path}")
