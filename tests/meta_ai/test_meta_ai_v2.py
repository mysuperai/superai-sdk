import os
import shutil
from pathlib import Path
from unittest import mock

import boto3
import pytest
from moto import mock_aws
from superai_builder.docker import client

import superai
from superai import settings
from superai.meta_ai import AIInstance, AILoader
from superai.meta_ai.ai import AI
from superai.meta_ai.ai_checkpoint import AICheckpoint
from superai.meta_ai.ai_helper import get_public_superai_instance
from superai.meta_ai.ai_instance import AIInstanceConfig, AIInstanceConfigFile
from superai.meta_ai.ai_loader import TEMPLATE_SAVE_FILE_NAME
from superai.meta_ai.base.base_ai import BaseAI
from superai.meta_ai.exceptions import AIException
from superai.meta_ai.schema import TaskPredictionInstance

"""
Structure of V2 AI objects:

AI:
    - Is the object created by the AI developer
    - Contains all metadata about the AI
    - Has a semantic version (simplified to Major.Minor without patch)
    
AI Instance:
    - Is an instance of an AI
    - Contains copies of default values from ModelTemplate
    - Allows modification of default values (e.g. hyperparameters)
    - Stores reference to Checkpoint tag to decide which weights to use
    
Checkpoint:
    - Contains only the weights of a Model
    - References an AI and AIInstance
"""


@pytest.fixture(scope="module")
def vcr(vcr):
    """All local API requests to Meta-AI Api are recorded in a cassette.
    The main config lives in fixtures/ai_client_fixture.py.
    This just extends that config with some local overrides.

    To re-record the cassette, delete the cassette file and run the tests again.
    """
    # Add switch for debugging
    vcr.record_mode = "once"
    # Ignore AWS calls
    vcr.ignore_hosts = ["amazonaws.com"]
    return vcr


@pytest.fixture(scope="module", autouse=True)
def set_dev_env():
    with settings.using_env("dev"):
        yield


@pytest.fixture(scope="module")
def aws_credentials(monkeysession):
    """Mocked AWS Credentials for moto."""
    monkeysession.setenv("AWS_ACCESS_KEY_ID", "testing")
    monkeysession.setenv("AWS_SECRET_ACCESS_KEY", "testing")
    monkeysession.setenv("AWS_SECURITY_TOKEN", "testing")
    monkeysession.setenv("AWS_SESSION_TOKEN", "testing")
    monkeysession.setenv("AWS_DEFAULT_REGION", "us-east-1")


@pytest.fixture(scope="module", autouse=True)
def record_cassette(vcr, aws_credentials):
    """Record cassette for all API requests for tests in this module"""
    with vcr.use_cassette("test_ai_v2.yaml"):
        yield


@pytest.fixture(scope="module")
def tmp_path():
    """Create deterministic temp dir so we can use it in the cassette without matching issues caused by random names"""
    temp = Path("/tmp/ai_test")
    temp.mkdir(parents=True, exist_ok=True)
    yield temp
    # remove dir and contents
    for f in temp.glob("*"):
        if f.is_dir():
            shutil.rmtree(f)
        else:
            f.unlink()


@pytest.fixture(scope="module")
def s3(aws_credentials):
    """Mocked S3 client for moto."""
    with mock_aws():
        yield boto3.client("s3")


@pytest.fixture(scope="module")
def ecr(aws_credentials, module_mocker):
    """Mocked ECR client for moto, disabled ECR login."""
    with mock_aws():
        # Disable unused ecr login
        module_mocker.patch("superai.meta_ai.ai_helper.aws_ecr_login", return_value=0)
        yield boto3.client("ecr")


@pytest.fixture(scope="module")
def sts(aws_credentials):
    """Mocked STS client for moto, hooks into SSO token logic."""
    with mock_aws():
        yield boto3.client("sts")


@pytest.fixture(scope="module")
def bucket(s3: boto3.client):
    """Create a bucket for testing uploads"""
    s3.create_bucket(
        Bucket=settings["meta_ai_bucket"],
    )


@pytest.fixture(scope="module")
def ai_name():
    """Generate static name for AI

    Was random before, but this caused issues with the cassette.
    """
    return "test_ai"


@pytest.fixture(scope="module")
def local_ai(bucket, ai_name, tmp_path, ecr, sts) -> AI:
    """Define local AI object for testing.
    It should be enough to specify the model class and the path to the model."""
    model_path = Path(__file__).parent / "fixtures" / "model"
    ai = AI(
        name=ai_name,
        model_class="DummyAI",
        model_class_path=str(model_path.absolute()),
        weights_path=tmp_path,
    )
    yield ai


@pytest.fixture(scope="module")
def saved_ai(local_ai: AI):
    """Save the local AI object to the backend and return the registered uuid"""
    ai_uuid = local_ai.save(overwrite=True)
    assert ai_uuid
    yield local_ai
    deleted = local_ai._client.delete_ai(local_ai.id)
    assert deleted


@pytest.fixture(scope="module")
def pushed_ai(module_mocker, saved_ai: AI):
    """Push the saved AI object to the backend and return the registered uuid"""
    module_mocker.patch("superai.meta_ai.ai.push_image", return_value="registry/image:tag")
    ai_uuid = saved_ai.push_image(local_image="registry/image:tag")
    assert ai_uuid
    yield saved_ai


def test_ai_init(local_ai: AI):
    """Test that we can create an AI object"""
    assert local_ai
    # Testing the attr class
    assert local_ai.name
    assert local_ai.model_class
    assert local_ai.model_class_path
    assert local_ai._client


def test_ai_to_dict(local_ai: AI):
    """Test that we can use the to_dict and from_dict functions correctly."""
    ai_dict = local_ai.to_dict()
    assert ai_dict
    assert isinstance(ai_dict, dict)
    ai = AI.from_dict(ai_dict)
    assert ai
    assert ai.name == local_ai.name
    assert ai.model_class == local_ai.model_class
    assert ai.model_class_path == local_ai.model_class_path
    assert ai.metadata["base_ai_version"] == BaseAI.VERSION


def test_ai_to_yaml(local_ai: AI, tmp_path):
    """Test that we can use the to_yaml and from_yaml functions correctly."""
    tmp_path = tmp_path / "ai.yaml"
    local_ai.to_yaml(tmp_path)
    ai = AI.from_yaml(tmp_path)
    assert ai
    assert ai.name == local_ai.name
    assert ai.model_class == local_ai.model_class
    assert ai.model_class_path == local_ai.model_class_path


def test_ai_name_override(local_ai: AI, tmp_path):
    """In CI pipeline we want to add a prefix to the name of the AI for isolation."""
    tmp_path = tmp_path / "ai.yaml"
    local_ai.to_yaml(tmp_path)
    # set AI_NAME_PREFIX env variable to 'test'
    os.environ["AI_NAME_PREFIX"] = "test"
    try:
        ai = AI.from_yaml(tmp_path)
        assert ai.name == "test-" + local_ai.name
    except:
        raise
    finally:
        os.environ.pop("AI_NAME_PREFIX")

    # set AI_NAME_PREFIX env variable to ''
    os.environ["AI_NAME_PREFIX"] = ""
    try:
        ai = AI.from_yaml(tmp_path)
        assert ai.name == local_ai.name
    except:
        raise
    finally:
        os.environ.pop("AI_NAME_PREFIX")

    ai = AI.from_yaml(tmp_path, add_name_prefix="test2")
    assert ai.name == "test2-" + local_ai.name

    # Check that we don't add the prefix twice, since we load the ai from the yaml file multiple times internally
    ai.to_yaml(tmp_path)
    ai = AI.from_yaml(tmp_path, add_name_prefix="test2")
    assert ai.name == "test2-" + local_ai.name


def test_ai_predict(local_ai: AI):
    """Test that we can predict using the ai"""
    prediction = local_ai.predict({"input": "test"})
    assert prediction


def test_ai_export(local_ai: AI, tmp_path):
    """Test that we can export an AI object to a file."""
    AILoader.save_local(local_ai, tmp_path)
    # assert that the model config file is in the tmp_path
    assert os.path.exists(tmp_path / TEMPLATE_SAVE_FILE_NAME)
    # Test that we can load the exported file
    ai = AI.load(tmp_path)
    assert ai
    assert ai.name == local_ai.name
    assert ai.model_class == local_ai.model_class
    assert ai.version == local_ai.version

    prediction = ai.predict({"input": "test"})
    assert prediction


def test_save_model(local_ai: AI, tmp_path):
    """Only registered models can be pushed to the backend"""

    returned_ai = local_ai.save(weights_path=tmp_path, overwrite=True)
    assert returned_ai == local_ai  # returned_ai is the same object as local_ai
    ai_uuid = local_ai.id
    assert ai_uuid

    # Change visibility
    returned_ai.visibility = "PUBLIC"
    returned_ai.save(overwrite=True)
    assert returned_ai.visibility == "PUBLIC"

    # Test update method
    returned_ai.update(visibility="PRIVATE")
    assert returned_ai.visibility == "PRIVATE"


@mock.patch("superai.meta_ai.image_builder.AiImageBuilder.build_image_superai_builder")
def test_build_model(mocked_builder, local_ai: AI, tmp_path):
    local_ai.build()
    assert mocked_builder.called
    assert local_ai._local_image


@pytest.fixture(scope="function")
def docker_client_mock(mocker):
    patched_docker_client = mocker.patch.object(client, "get_docker_client", autospec=True)

    mock_client = mocker.Mock()
    patched_docker_client.return_value = mock_client
    # Patch images.get() and images.push()
    mock_client.images.get.return_value = mocker.Mock()
    mock_client.images.push.return_value = ["Docker push dummy line"]

    yield patched_docker_client


def test_chaining_ai(mocker, local_ai: AI, docker_client_mock):
    """Test that we can chain together the main AI methods.
    This assumes that the return value is always the instance itself."""
    patched_s2i_build = mocker.patch.object(
        superai.meta_ai.image_builder.AiImageBuilder, "build_image_superai_builder", autospec=True
    )
    patched_s2i_build.return_value = "image:tag"

    # Used in pus_ image directly
    mocker.patch.object(superai.meta_ai.ai_helper, "get_docker_client", docker_client_mock)

    ai = local_ai.save(overwrite=True).build().push_image()
    assert patched_s2i_build.called
    assert docker_client_mock.called
    assert "image:tag" in ai.image


def test_duplicate(saved_ai):
    """Test that we cannot register the same model twice with the same name and version"""
    with pytest.raises(AIException):
        # We should not be able to register the same model twice with the same version
        saved_ai.save(weights_path="tests/meta_ai/v2/fixtures/model/weights.pth")


def test_get_ai_by_name(ai_name, saved_ai):
    """Test that we can get an AI object by name and version"""
    ai = AI.load(f"ai://{ai_name}")

    assert ai.id == saved_ai.id


def test_checkpoint_exists(ai_name, saved_ai):
    """When registering an AI model, its necessary to define a weights as a default.
    Internally we represent weights as checkpoints. Checkpoints are stored in the backend.
    """
    checkpoint = saved_ai.get_default_checkpoint()
    assert checkpoint
    # Checkpoint is a lean dataclass
    assert isinstance(checkpoint, AICheckpoint)
    assert checkpoint.template_id == saved_ai.id
    assert checkpoint.metadata == {}  # json
    assert checkpoint.description == ""  # str
    assert checkpoint.tag == "LATEST"  # str
    assert checkpoint.weights_path  # str

    checkpoint.change_description("new description")
    assert checkpoint.description == "new description"

    with pytest.raises(ValueError):
        checkpoint.change_tag("unknown tag")
    checkpoint.change_tag("STABLE")
    assert checkpoint.tag == "STABLE"


def test_create_checkpoint(saved_ai, tmp_path):
    # Create new checkpoint with local folder as weights
    local_checkpoint = AICheckpoint(template_id=saved_ai.id, weights_path=str(tmp_path))
    # Save checkpoint in database and upload weights
    remote_checkpoint = local_checkpoint.save()
    assert remote_checkpoint.id
    assert remote_checkpoint.weights_path
    # Check that the weights are in the right place
    assert "s3" in remote_checkpoint.weights_path
    assert tmp_path == remote_checkpoint._local_path

    # Test loading from database
    loaded = AICheckpoint.load(remote_checkpoint.id)
    assert loaded.id == remote_checkpoint.id
    assert loaded.template_id == remote_checkpoint.template_id
    assert loaded.tag == remote_checkpoint.tag
    assert loaded.description == remote_checkpoint.description
    assert loaded.metadata == remote_checkpoint.metadata
    assert loaded.weights_path == remote_checkpoint.weights_path


def test_create_ai_instance(ai_name, saved_ai):
    # ai = AI.load(f"ai://{ai_name}")

    # Create an instance without an associated app and checkpoint
    # this will pick the default checkpoint of the ai
    ai_instance = saved_ai.create_instance()

    AIInstance.load(ai_instance.id)
    assert ai_instance.id
    assert ai_instance.template_id == saved_ai.id
    assert ai_instance.save()

    ai_instance.description = "new description"
    ai_instance.save()
    assert ai_instance.description == "new description"

    # Reload from database and retest the fields
    ai_instance = AIInstance.load(ai_instance.id)
    assert ai_instance.id
    assert ai_instance.template_id == saved_ai.id
    assert ai_instance.description == "new description"

    # Make ai instance public
    ai_instance.update(visibility="PUBLIC")
    assert ai_instance.visibility == "PUBLIC"
    ai_instance.update(visibility="PRIVATE")
    assert ai_instance.visibility == "PRIVATE"


def test_delete_ai_instance(ai_name, saved_ai):
    ai_instance = saved_ai.create_instance()
    ai_instance.delete()
    with pytest.raises(AIException):
        AIInstance.load(ai_instance.id)


def test_create_ai_instance_with_app(saved_ai):
    # Create with an app, will be visible in the App Dash UI
    ai_instance = saved_ai.create_instance()
    assert ai_instance.id
    app_id = "9317e0f9-77ee-4c32-b935-cfbce8c442a3"
    ai_instance.assign_to_project(app_id)

    ai_instance.remove_from_project(app_id)

    with pytest.raises(AIException):
        # Removing second time should raise an exception
        ai_instance.remove_from_project(app_id)


def test_get_current_checkpoint(ai_name, saved_ai):
    instance = saved_ai.create_instance()
    checkpoint = instance.get_checkpoint()
    assert checkpoint
    # We create a new checkpoint for each instance
    assert checkpoint.id != saved_ai.get_default_checkpoint().id
    assert checkpoint.tag == "LATEST"


def test_create_checkpoint_descendant(saved_ai, tmp_path):
    instance = saved_ai.create_instance()
    checkpoint = instance.get_checkpoint()
    assert checkpoint.ai_instance_id == instance.id
    checkpoint.change_tag("LATEST")
    descendant = checkpoint.create_descendant(weights_path=str(tmp_path))
    assert descendant
    assert descendant.id != checkpoint.id
    assert descendant.ai_instance_id == instance.id
    assert descendant.template_id == checkpoint.template_id
    assert descendant.tag == "LATEST"

    descendant2 = descendant.create_descendant(weights_path=str(tmp_path))
    assert descendant2
    assert descendant2.id != descendant.id
    assert descendant2.ai_instance_id == instance.id
    assert descendant2.template_id == descendant.template_id
    assert descendant2.tag == "LATEST"

    descendant2.change_tag("STABLE")


def test_remote_deploy(pushed_ai):
    instance = pushed_ai.create_instance()
    instance.deploy()
    assert instance.served_by

    instance.undeploy()


def test_remote_predict(module_mocker, pushed_ai):
    instance = pushed_ai.create_instance()
    instance.deploy(redeploy=True)
    available_mock = module_mocker.patch(
        "superai.apis.meta_ai.model.DeploymentApiMixin.check_endpoint_is_available", return_value=True
    )

    preds = TaskPredictionInstance(prediction={"class": "cat"}, score=0.5)
    predict_action = module_mocker.patch(
        "superai.apis.meta_ai.model.DeploymentApiMixin.predict_from_endpoint", return_value=preds
    )

    response = instance.predict(input_data={"input": "test"})

    assert available_mock.called
    assert predict_action.called

    assert response
    assert response["prediction"]
    assert response["score"]


def test_train_on_app(ai_name, saved_ai, tmp_path):
    """Test that we can train an AI instance on an app"""
    # Create with an app, will be visible in the App Dash UI
    ai_instance = saved_ai.create_instance()

    training_instance = ai_instance.train(local_path=tmp_path, skip_build=True)
    assert training_instance


def test_ai_instance_config(tmp_path):
    instance1 = AIInstanceConfig(weights_path="s3://test", name="instance1")
    assert instance1

    config_file = AIInstanceConfigFile(instances=[instance1])
    assert config_file
    config_file.to_yaml(tmp_path / "instance_config.yaml")

    config_file2 = AIInstanceConfigFile.from_yaml(tmp_path / "instance_config.yaml")
    assert config_file2
    assert config_file2.instances[0].name == "instance1"
    assert config_file2.instances[0].weights_path == "s3://test"


def test_get_public_superai_instance(saved_ai, mocker):
    ai_instance = saved_ai.create_instance(visibility="PUBLIC")
    assert ai_instance.id

    # Imitate superai owner id with our own user id
    mocker.patch("superai.meta_ai.ai_helper.SUPERAI_OWNER_ID", ai_instance.owner_id)

    assert get_public_superai_instance(name=ai_instance.name, version=saved_ai.version)
    assert not get_public_superai_instance(name=ai_instance.name, version="0.0.0")

    # Private instance should not be returned, and not the one with different name
    ai_instance2 = saved_ai.create_instance(name="different_name", visibility="PRIVATE")
    assert ai_instance2.id
    assert not get_public_superai_instance(name=ai_instance2.name, version=saved_ai.version)

    # Make ai instance public and test again
    ai_instance2.update(visibility="PUBLIC")
    assert get_public_superai_instance(name=ai_instance2.name, version=saved_ai.version)
