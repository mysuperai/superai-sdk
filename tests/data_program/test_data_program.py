from typing import List

import pytest
from superai_schema.types import BaseModel, Field

from superai.data_program import DataProgram, HandlerOutput, JobContext, Metric
from superai.data_program.workflow import WorkflowConfig


class ParameterModel(BaseModel):
    instructions: str

    class Config:
        title = "Test DP Instructions"


def _dummy_handler(params: ParameterModel):
    """Dummy handler function used in the tests below"""
    params.instructions

    class JobInput(BaseModel):
        url: str = Field(title="Original Document")

    class JobOutput(BaseModel):
        url: str = Field(title="Document URL")

    def metric_func(truths: List[JobOutput], preds: List[JobOutput]):
        return {"f1_score": {"value": 0.0}}

    metric = Metric("IMAGE_POLYGON:F1:BOUNDING_BOXES", metric_fn=metric_func)

    def process_job(job_input: JobInput, context: JobContext[JobOutput]) -> JobOutput:
        job_output = JobOutput(url=job_input.url)
        return job_output

    return HandlerOutput(
        input_model=JobInput,
        output_model=JobOutput,
        process_fn=process_job,
        templates=[],
        metrics=[metric],
    )


DP_NAME = "dp_test"


@pytest.fixture
def mock_apis(monkeypatch):
    """Mock out the API call which registers the workflow normally"""

    def create_template(*args, **kwargs):
        return {"uuid": "123", "name": DP_NAME}

    monkeypatch.setattr("superai.apis.data_program.DataProgramApiMixin.create_template", create_template)


def test_schema_port(monkeypatch):
    """
    Test that the schema port is set correctly using Dynaconf and ENV variable

    Returns:

    """
    monkeypatch.setenv("SUPERAI_SCHEMA_PORT", "5000")
    from superai.config import settings

    settings.reload()
    assert settings.schema_port == 5000


def test_data_program_creation(mock_apis, mocker):
    # Mock function create_template in apis/data_program.py
    default_params = ParameterModel(instructions="These are the DP default instructions.")
    dp = DataProgram.create(default_params=default_params, handler=_dummy_handler, name=DP_NAME)
    assert dp._name == DP_NAME
    assert dp._default_params == default_params
    assert dp._handler == _dummy_handler

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
