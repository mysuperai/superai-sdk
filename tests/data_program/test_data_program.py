import os
import pathlib
from typing import List

import pytest
from superai_schema.types import BaseModel, Field

from superai.config import get_current_env, settings
from superai.data_program import (
    BotWorker,
    CollaboratorWorker,
    DataProgram,
    HandlerOutput,
    JobContext,
    Metric,
)
from superai.data_program.task.types import (
    DPSuperTaskConfigs,
    SuperTaskConfig,
    SuperTaskModel,
    SuperTaskParameters,
    TaskStrategy,
)
from superai.data_program.workflow import WorkflowConfig

TEST_TASK_NAME = "test_task"


class ParameterModel(BaseModel):
    instructions: str = Field(example="This is a test")


class JobInput(BaseModel):
    url: str = Field(title="Original Document", example="https://www.super.ai")


class JobOutput(BaseModel):
    url: str = Field(title="Document URL", example="https://www.super.ai")


def metric_func(truths: List[JobOutput], preds: List[JobOutput]):
    return {"f1_score": {"value": 0.0}}


metric = Metric("IMAGE_POLYGON:F1:BOUNDING_BOXES", metric_fn=metric_func)


def process_job(job_input: JobInput, context: JobContext[JobOutput]) -> JobOutput:
    return JobOutput(url=job_input.url)


def _dummy_handler(params: ParameterModel):
    """Dummy handler function used in the tests below"""

    return HandlerOutput(
        input_model=JobInput,
        output_model=JobOutput,
        process_fn=process_job,
        templates=[],
        metrics=[metric],
    )


def _dummy_handler_supertask(params: ParameterModel, super_task_params: DPSuperTaskConfigs = None):
    """Dummy handler function used in the tests below"""
    supertask = SuperTaskModel.create(name=TEST_TASK_NAME, input=JobInput, output=JobOutput, config=super_task_params)

    return HandlerOutput(
        input_model=JobInput,
        output_model=JobOutput,
        process_fn=process_job,
        super_task_params=[supertask],
        metrics=[metric],
    )


DP_NAME = "dp_test"


def test_schema_port(monkeypatch):
    """
    Test that the schema port is set correctly using Dynaconf and ENV variable

    Returns:

    """
    from superai.config import settings

    previous_port = settings.SCHEMA_PORT
    monkeypatch.setenv("SUPERAI_SCHEMA_PORT", "5000")
    settings.reload()
    assert settings.schema_port == 5000

    settings.SCHEMA_PORT = previous_port
    assert settings.schema_port == previous_port


@pytest.fixture(scope="module")
def vcr(vcr):
    vcr.serializer = "yaml"
    vcr.cassette_library_dir = f"{pathlib.Path(__file__).resolve().parent}/cassettes"
    vcr.record_mode = "once"
    vcr.match_on = ["method"]
    vcr.filter_headers = [
        "x-api-key",
        "x-app-id",
        "Content-Length",
        "User-Agent",
        "API-KEY",
        "AUTH-TOKEN",
        "ID-TOKEN",
        "Authorization",
        "Accept-Encoding",
    ]
    vcr.decode_compressed_response = True
    return vcr


@pytest.fixture
def use_dev_env_for_vcr(vcr):
    previous_env = get_current_env()
    assert previous_env == "testing"

    # Uncomment this for recording new cassettes in dev
    # settings.configure(FORCE_ENV_FOR_DYNACONF="dev")
    # settings.env_for_superai = "dev"
    # print(settings.as_dict())
    # assert settings.user.api_key is not None

    with vcr.use_cassette("dp_test.yaml"):
        yield
    # Restore previous env
    # settings.configure(FORCE_ENV_FOR_DYNACONF=previous_env)
    # settings.env_for_superai = previous_env


@pytest.fixture(scope="function", autouse=True)
def reset_agent_env():
    """Some of the tests have side effects in the OS environment variables. This fixture resets the environment"""
    # Clear before
    os.unsetenv("IN_AGENT")
    os.unsetenv("CANOTIC_AGENT")
    yield
    # Clear after
    os.unsetenv("IN_AGENT")
    os.unsetenv("CANOTIC_AGENT")


@pytest.fixture
def set_qumes_active(use_dev_env_for_vcr):
    previous_backend = settings.backend
    settings.backend = "qumes"
    assert settings.backend == "qumes"
    yield
    settings.backend = previous_backend


@pytest.mark.parametrize("handler", [_dummy_handler, _dummy_handler_supertask])
def test_data_program_creation(mocker, set_qumes_active, use_dev_env_for_vcr, handler):
    # Mock function create_template in apis/data_program.py
    default_params = ParameterModel(instructions="These are the DP default instructions.")

    if handler == _dummy_handler_supertask:
        default_super_task_configs = {
            "test_task": SuperTaskConfig(
                workers=[CollaboratorWorker(), BotWorker()],
                params=SuperTaskParameters(strategy=TaskStrategy.FIRST_COMPLETED),
            ),
        }
    else:
        default_super_task_configs = None

    dp = DataProgram.create(
        default_params=default_params,
        handler=handler,
        name=DP_NAME,
        default_super_task_configs=default_super_task_configs,
    )
    assert dp._name == DP_NAME
    assert dp._default_params == default_params
    assert dp._handler == handler

    # Test starting a service (DP Server in this case)
    # Patch out uvicorn.run, since its blocking normally
    mocked_run = mocker.patch("uvicorn.run")

    dp.start_service(
        workflows=[
            WorkflowConfig("parse", is_default=True, is_gold=True),
        ],
        service=DataProgram.ServiceType.SCHEMA,
        force_no_tunnel=True,
    )
    # We need to test if the function reached the final uvicorn run
    assert mocked_run.called

    # Test that the service check is rejecting wrong input
    with pytest.raises(ValueError):
        dp.start_service(
            workflows=[
                WorkflowConfig("parse", is_default=True, is_gold=True),
            ],
            service="NOT_A_SERVICE",
        )

    # Disable transport parts
    mocker.patch("superai.data_program.protocol.task.start_threading")
    mocker.patch("superai.data_program.protocol.task.serve_workflow")
    mocker.patch("superai.data_program.protocol.transport.subscribe_workflow")
    dp.start_service(
        workflows=[
            WorkflowConfig("parse", is_default=True, is_gold=True),
        ],
        service=DataProgram.ServiceType.DATAPROGRAM,
    )
    assert dp.workflows
