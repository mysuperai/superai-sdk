import uuid
from unittest.mock import Mock, patch

from click.testing import CliRunner

from superai import Client
from superai.cli.ai_instance import deploy, list_ai_instances, predict, undeploy


@patch("superai.client.Client.list_ai_instances")
def test_list_ai_instances(list_instances_api):
    # Arrange
    runner = CliRunner()
    client = Client(api_key="test_key", auth_token="test_token")
    name = "test_name"
    ai_name = "test_ai_name"
    ai_version = "test_version"
    visibility = "test_visibility"
    checkpoint_tag = "test_tag"
    verbose = False

    # Act
    result = runner.invoke(
        list_ai_instances,
        [
            "--name",
            name,
            "--ai_name",
            ai_name,
            "--ai_version",
            ai_version,
            "--visibility",
            visibility,
            "--checkpoint_tag",
            checkpoint_tag,
        ],
        obj={"client": client},
    )

    # Assert
    assert result.exit_code == 0
    list_instances_api.assert_called_once_with(
        name=name,
        ai_name=ai_name,
        ai_version=ai_version,
        visibility=visibility,
        checkpoint_tag=checkpoint_tag,
        verbose=verbose,
        to_json=True,
        organization_id=None,
        owner_id=None,
        fuzzy=True,
    )


# Deploy function test
@patch("superai.meta_ai.ai_instance.AIInstance.load")
def test_deploy(mock_load):
    runner = CliRunner()
    mock_instance = mock_load.return_value

    result = runner.invoke(deploy, ["-i", "some-uuid"])

    mock_instance.deploy.assert_called_once()
    assert result.exit_code == 0


# Undeploy function test
@patch("superai.meta_ai.ai_instance.AIInstance.load")
def test_undeploy(mock_load):
    runner = CliRunner()
    mock_instance = mock_load.return_value

    result = runner.invoke(undeploy, ["-i", "some-uuid"])

    mock_instance.undeploy.assert_called_once()
    assert result.exit_code == 0


# Predict function test with data flag
@patch("superai.client.Client.predict_from_endpoint")
def test_predict_with_data(mock_predict_from_endpoint):
    runner = CliRunner()
    mock_client = Mock()

    context_obj = {"client": mock_client}
    runner.invoke(predict, [str(uuid.uuid4()), "-d", '{"key": "value"}'], obj=context_obj)

    mock_client.predict_from_endpoint.assert_called_once()


# Predict function test with data-file flag
@patch("superai.client.Client.predict_from_endpoint")
def test_predict_with_data_file(mock_predict_from_endpoint, tmp_path):
    runner = CliRunner()
    mock_client = Mock()

    context_obj = {"client": mock_client}
    file_path = tmp_path / "some-file-path.json"
    file_path.write_text('{"key": "value"}')

    result = runner.invoke(predict, [str(uuid.uuid4()), "-f", file_path], obj=context_obj)

    mock_client.predict_from_endpoint.assert_called_once()
    assert result.exit_code == 0
