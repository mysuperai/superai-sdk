import pytest

from superai import config
from superai.meta_ai.ai_helper import (
    ECR_MODEL_ROOT_PREFIX,
    _ai_name_validator,
    _ai_version_validator,
    ecr_full_name,
    ecr_registry_suffix,
    push_image,
)
from superai.meta_ai.exceptions import AIException


@pytest.mark.parametrize(
    "name",
    [
        "AI-Name",
        "AI_Name",
        "AI123",
        "AI_name-123",
    ],
)
def test_ai_name_validator_valid(name):
    """Test that the AI name validator accepts valid AI names."""
    try:
        _ai_name_validator(None, None, name)
    except AIException as e:
        pytest.fail(f"Valid name '{name}' raised a ValueError: {e}")


@pytest.mark.parametrize(
    "name",
    [
        "AI Name",
        "AI@Name",
        "AI!name",
        "AI#name$123",
    ],
)
def test_ai_name_validator_invalid(name):
    """Test that the AI name validator rejects invalid AI names."""
    with pytest.raises(AIException, match="AI name can only contain alphanumeric characters"):
        _ai_name_validator(None, None, name)


@pytest.mark.parametrize(
    "version",
    [
        "1.0",
        "3.2",
        "0.9",
        "10.5",
    ],
)
def test_ai_version_validator_valid(version):
    """Test that the AI version validator accepts valid AI versions."""
    try:
        _ai_version_validator(None, None, version)
    except AIException as e:
        pytest.fail(f"Valid version '{version}' raised a ValueError: {e}")


@pytest.mark.parametrize(
    "version",
    [
        "1.0.0",
        "3.2.1",
        "1",
        "a.b",
    ],
)
def test_ai_version_validator_invalid(version):
    """Test that the AI version validator rejects invalid AI versions."""
    with pytest.raises(AIException, match="AI version can only be in the format {MAJOR}.{MINOR} e.g  1.0 or 3.2"):
        _ai_version_validator(None, None, version)


@pytest.fixture
def ecr_client_mock(mocker):
    client = mocker.Mock()
    client.describe_repositories.side_effect = Exception("Repository not found")
    client.create_repository.return_value = None
    return client


@pytest.fixture
def sts_client_mock(mocker):
    client = mocker.Mock()
    client.get_caller_identity.return_value = {"Account": "123456789012"}
    return client


@pytest.fixture
def boto_session_mock(mocker, sts_client_mock, ecr_client_mock):
    session = mocker.Mock()
    session.client.side_effect = lambda service: {
        "sts": sts_client_mock,
        "ecr": ecr_client_mock,
    }[service]
    return session


@pytest.fixture
def docker_client_mock(mocker):
    client = mocker.Mock()
    client.images.get.return_value.tag.return_value = None
    client.images.push.return_value = [{}]
    return client


def test_push_image(mocker, boto_session_mock, docker_client_mock):
    # Mock external functions
    mocker.patch("superai.meta_ai.ai_helper.get_boto_session", return_value=boto_session_mock)
    mocker.patch("superai.meta_ai.ai_helper.aws_ecr_login", return_value=None)
    mocker.patch("superai.meta_ai.ai_helper.get_docker_client", return_value=docker_client_mock)
    mocker.patch(
        "superai.meta_ai.ai_helper.ecr_full_name", return_value=("full_name", "registry_prefix", "repository_name")
    )

    # Call the function
    result = push_image("test_image", "test_model_id")

    # Assert the result
    assert result == "full_name"

    # Assert external function calls
    boto_session_mock.client.assert_has_calls([mocker.call("sts"), mocker.call("ecr")])
    docker_client_mock.images.get.assert_called_once_with("test_image:latest")
    docker_client_mock.images.get.return_value.tag.assert_called_once_with("full_name")
    docker_client_mock.images.push.assert_called_once_with(repository="full_name", stream=True, decode=True)


def test_ecr_full_name(mocker, boto_session_mock):
    # Mock external function
    mocker.patch("superai.meta_ai.ai_helper.get_boto_session", return_value=boto_session_mock)

    # Call the function
    full_name, registry_prefix, repository_name = ecr_full_name("test_image", "latest", "test_model_id")

    # Assert the result
    assert registry_prefix == "123456789012.dkr.ecr.us-east-1.amazonaws.com"
    assert repository_name == f"{ECR_MODEL_ROOT_PREFIX}/{config.settings.name}/test_model_id/test_image"
    assert full_name == f"{registry_prefix}/{repository_name}:latest"

    # Assert external function call
    boto_session_mock.client.assert_called_once_with("sts")


def test_ecr_registry_suffix():
    # Call the function
    full_suffix_with_version, full_suffix = ecr_registry_suffix("test_image", "test_model_id", "latest")

    # Assert the result
    assert full_suffix == f"{ECR_MODEL_ROOT_PREFIX}/{config.settings.name}/test_model_id/test_image"
    assert full_suffix_with_version == f"{ECR_MODEL_ROOT_PREFIX}/{config.settings.name}/test_model_id/test_image:latest"
