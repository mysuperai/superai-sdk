from concurrent.futures import Future
from typing import List

import pytest
from pydantic import ValidationError
from superai_schema.types import BaseModel

# import superai
from superai.data_program import Worker, WorkerType
from superai.data_program.task.super_task import (
    SuperTaskJobInput,
    SuperTaskWorkflow,
    TaskRouter,
)
from superai.data_program.task.types import (
    MetricOperator,
    OnTimeout,
    SuperTaskConfig,
    SuperTaskModel,
    TaskStrategy,
    TrainingConstraint,
    TrainingConstraintSet,
    WorkerConstraint,
)


def test_task_workers():
    class Workers(BaseModel):
        __root__: List[Worker]
        # overwrite __init__ to allow passing a list of workers

    with pytest.raises(ValidationError):
        # Ensure that wrong arguments like `count` raise error right away
        task_workers = Workers(__root__=[Worker(type=WorkerType.collaborators, count=1)])

    task_workers = Workers(__root__=[Worker(type=WorkerType.collaborators, num_tasks=1)])
    assert task_workers is not None

    task_workers = Workers(
        __root__=[
            Worker(
                type=WorkerType.crowd,
                num_tasks=3,
                timeout=100,
                on_timeout=OnTimeout(action="RETRY", max_retries=3),
            )
        ]
    )
    assert task_workers

    task_workers = Workers(
        __root__=[
            Worker(
                type=WorkerType.crowd,
                num_tasks=3,
                timeout=100,
                on_timeout=OnTimeout(action="RETRY", max_retries=3),
            ),
            Worker(type=WorkerType.collaborators, num_tasks=1, timeout=100),
        ]
    )
    assert task_workers
    schema = task_workers.schema()
    assert schema


def test_task_worker_schema():
    class Workers(BaseModel):
        __root__: List[Worker]
        # overwrite __init__ to allow passing a list of workers

    schema = Workers.schema_json(indent=2)
    assert schema


def test__map_worker_constraints():

    worker = Worker(
        type=WorkerType.collaborators, worker_constraints=WorkerConstraint(email=["test@test.com"], worker_id=[1])
    )
    constraints = TaskRouter._map_worker_constraints(worker)
    assert "emails" in constraints
    assert "included_ids" in constraints
    assert constraints["emails"][0] == "test@test.com"
    assert constraints["included_ids"][0] == 1

    worker = Worker(
        type=WorkerType.collaborators,
        worker_constraints=WorkerConstraint(
            trainings=TrainingConstraintSet(
                training_constraints=[TrainingConstraint(name="test", value=0.5, operator=MetricOperator.GREATER_THAN)]
            )
        ),
    )
    constraints = TaskRouter._map_worker_constraints(worker)
    assert "qualifications" in constraints
    assert "test" == constraints["qualifications"][0]["name"]
    assert 0.5 == constraints["qualifications"][0]["value"]
    assert "GREATER_THAN" == constraints["qualifications"][0]["operator"]


class mock_task_result:
    """Removes terminate guard from the original task result class"""

    def __init__(self, result):
        self._result = result

    def status(self):
        return self._result["status"] if "status" in self._result else None

    def timestamp(self):
        return self._result["timestamp"] if "timestamp" in self._result else None

    def __getitem__(self, key):
        return self._result[key]

    def get(self, key):
        return self._result.get(key)

    def response(self):
        return self._result


def test_task_router(monkeypatch):

    test_future = Future()
    monkeypatch.setattr("superai.data_program.task.basic.Task._create_task_future", lambda *args, **kwargs: test_future)

    params = SuperTaskConfig(workers=[Worker(type=WorkerType.collaborators)], strategy=TaskStrategy.FIRST_COMPLETED)

    class TestInput(BaseModel):
        url: str

    class TestOutput(BaseModel):
        annotation: str

    router = TaskRouter(
        task_config=params, task_input=TestInput(url="http://a.com"), task_output=TestOutput(annotation="")
    )
    assert router
    futures = router.map()
    assert futures

    result = mock_task_result({"status": "COMPLETED", "timestamp": 1234, "annotation": "test"})
    test_future.set_result(result)

    selected = router.reduce(futures)
    assert selected == test_future

    result = selected.result()
    assert result == result


def test_super_task_workflow(monkeypatch):
    class TestInput(BaseModel):
        url: str

    class TestOutput(BaseModel):
        annotation: str

    params = SuperTaskConfig(workers=[Worker(type=WorkerType.collaborators)], strategy=TaskStrategy.FIRST_COMPLETED)
    model = SuperTaskModel.create(name="test", config=params, input=TestInput, output=TestOutput)
    workflow = SuperTaskWorkflow(model, prefix="test_dp")

    # Create dummy future with result
    test_future = Future()
    result = mock_task_result(dict(values=dict(formData=dict(annotation="test"))))
    test_future.set_result(result)

    # Mock task router functions already tested above
    monkeypatch.setattr("superai.data_program.task.super_task.TaskRouter.map", lambda *args, **kwargs: [test_future])
    monkeypatch.setattr("superai.data_program.task.super_task.TaskRouter.reduce", lambda *args, **kwargs: test_future)

    input = SuperTaskJobInput(input=TestInput(url="http://a.com"), output=TestOutput(annotation=""))
    output = workflow.execute_workflow(job_input=input, configs=params.dict())
    assert output
    assert output["task_output"]["annotation"] == "test"
