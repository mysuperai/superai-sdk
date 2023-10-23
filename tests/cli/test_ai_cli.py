import uuid
from unittest.mock import Mock, patch

from click.testing import CliRunner

from superai import Client
from superai.cli.ai import local_deploy_ai
from superai.cli.ai_instance import (
    deploy,
    list_ai_instances,
    predict,
    undeploy,
    view_ai_instance,
)
from superai.cli.ai_training import list_training_templates, view_training_template


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


@patch("superai.client.Client.get_ai_instance")
def test_view_ai_instance(get_ai_instance_api):
    # Arrange
    runner = CliRunner()
    client = Client(api_key="test_key", auth_token="test_token")
    instance_uuid = "a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11"
    detailed = True

    # Act
    result = runner.invoke(
        view_ai_instance,
        [str(instance_uuid), "--detailed"],
        obj={"client": client},
    )

    # Assert
    assert result.exit_code == 0
    get_ai_instance_api.assert_called_once_with(str(instance_uuid), to_json=True, view_checkpoint=detailed)


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


# Test for list_training_templates
@patch("superai.client.Client.list_training_templates")
def test_list_training_templates(list_training_templates_api):
    # Arrange
    runner = CliRunner()
    client = Client(api_key="test_key", auth_token="test_token")
    app_id = "app_123"
    model_id = "model_123"

    # Act
    result = runner.invoke(
        list_training_templates,
        ["--app_id", app_id, "--model_id", model_id],
        obj={"client": client},
    )

    # Assert
    assert result.exit_code == 0
    list_training_templates_api.assert_called_once_with(str(model_id), app_id)


# Test for view_training_template
@patch("superai.client.Client.get_training_template")
def test_view_training_template(get_training_template_api):
    # Arrange
    runner = CliRunner()
    client = Client(api_key="test_key", auth_token="test_token")
    app_id = "app_123"
    template_id = "template_123"

    # Act
    result = runner.invoke(
        view_training_template,
        ["--app_id", app_id, "--template_id", template_id],
        obj={"client": client},
    )

    # Assert
    assert result.exit_code == 0
    get_training_template_api.assert_called_once_with(str(template_id), app_id)


@patch("os.path.exists", return_value=True)
@patch("shutil.rmtree")
@patch("superai.meta_ai.ai.AI.from_yaml")
@patch("json.dump")
# @patch('open', mock_open())
def test_local_deploy_ai(mock_dump, mock_from_yaml, mock_rmtree, mock_exists, tmp_path):
    # Arrange
    runner = CliRunner()
    config_file = "some_config_file.yml"
    # Create a config file at tmp_path
    config_path = tmp_path / config_file
    config_path.touch()
    ai_object = Mock()
    predictor_obj = Mock()

    mock_from_yaml.return_value = ai_object
    ai_object.local_image = "some_local_image"
    ai_object.weights_path = "some_weights_path"
    ai_object.cache_path.return_value = tmp_path / "cache"
    # create directory for cache
    ai_object.cache_path.return_value.mkdir()
    ai_object.default_deployment_parameters = "some_deployment_parameters"

    mock_predictor_class = "superai.meta_ai.deployed_predictors.LocalPredictor"
    with patch(mock_predictor_class, return_value=predictor_obj) as mock_predictor:
        # Act
        result = runner.invoke(local_deploy_ai, ["--config-file", config_path])
        print(result.exc_info)
        print(result.output)
        # Assert
        assert result.exit_code == 0
        mock_rmtree.assert_called_once()
        mock_from_yaml.assert_called_once_with(config_path)
        ai_object.build.assert_called_once_with(skip_build=False)
        ai_object.save.assert_called_once_with(overwrite=True, create_checkpoint=False)
        mock_predictor.assert_called_once_with(
            orchestrator="LOCAL_DOCKER_K8S",
            deploy_properties="some_deployment_parameters",
            local_image_name="some_local_image",
            weights_path="some_weights_path",
        )
        predictor_obj.deploy.assert_called_once_with(redeploy=True)
        mock_dump.assert_called_once()
