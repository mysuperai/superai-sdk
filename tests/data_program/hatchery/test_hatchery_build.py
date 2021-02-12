import shutil
from os import makedirs
from pathlib import Path

import pytest

from superai.config import settings
from superai.data_program.hatchery.utils.build import create_agent_run_command

TEST_AGENT_FILE = "test-agent.jar"


@pytest.fixture(scope="module")
def agent_file_path():
    build_folder = Path(settings.hatchery_build_folder)
    makedirs(build_folder, exist_ok=True)
    jar_file = Path(settings.hatchery_build_folder) / TEST_AGENT_FILE
    jar_file.touch()
    yield jar_file
    jar_file.unlink()
    shutil.rmtree(build_folder.absolute())
    assert not build_folder.exists()


# TODO: Inject configuration variables otherwise this test is going to fail when then endpoints change
def test_create_agent_run_command_defaults(agent_file_path):
    settings.agent.file = agent_file_path
    command: str = create_agent_run_command(template_name="image", version="1", script="my_dummy_script.py")
    assert (
        command.strip()
        == f"java -jar {settings.hatchery_build_folder}/test-agent.jar --host https://bapi-test.super.ai --websocket wss://bapi-test.super.ai/agent --api_key FAKE_API_KEY --concurrency 100   --serve image --version 1 python my_dummy_script.py"
    )


def test_create_agent_run_command_with_params(agent_file_path):
    settings.agent.file = agent_file_path
    command: str = create_agent_run_command(
        template_name="image",
        version="0.11",
        script=TEST_AGENT_FILE,
        host="https://bapi-dev.super.ai",
        websocket="wss://bapi-dev.super.ai/agent",
        api_key="abcapi_key",
        concurrency=5,
        serve=True,
        force_schema=True,
    )
    assert (
        command.strip()
        == f"java -jar {settings.hatchery_build_folder}/test-agent.jar --host https://bapi-dev.super.ai --websocket wss://bapi-dev.super.ai/agent --api_key abcapi_key --concurrency 5  --force-schema --serve image --version 0.11 python test-agent.jar"
    )
