from unittest.mock import patch

from click.testing import CliRunner

from superai import Client
from superai.cli.ai_instance import list_ai_instances


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
