from concurrent.futures import Future
from unittest.mock import Mock

import pytest
from pydantic import ValidationError
from superai_schema.types import BaseModel

from superai.data_program import CollaboratorWorker, CrowdWorker, IdempotentWorker
from superai.data_program.Exceptions import TaskExpiredMaxRetries

# import superai
from superai.data_program.task.super_task import SuperTaskWorkflow
from superai.data_program.task.task_router import TaskHandler, TaskRouter
from superai.data_program.task.types import (
    SuperTaskConfig,
    SuperTaskModel,
    TaskStrategy,
)
from superai.data_program.task.workers import (
    BotWorker,
    HumanWorkerConstraint,
    MetricOperator,
    OnTimeout,
    OnTimeoutAction,
    TrainingConstraint,
    TrainingConstraintSet,
    Worker,
    WorkerConstraint,
    WorkerType,
)


class TestInput(BaseModel):
    url: str


class TestOutput(BaseModel):
    annotation: str


sample_input = TestInput(url="https://a.com")
sample_output = TestOutput(annotation="")
completed_future = {"status": "COMPLETED", "timestamp": 1234, "values": {"annotation": "test"}}
expired_future = {"status": "EXPIRED", "timestamp": 1234, "values": {"annotation": "test"}}


def test_worker_schema():
    worker = CollaboratorWorker()
    assert worker
    assert worker.schema()
    assert worker.dict()


def test__map_worker_constraints():
    worker = CollaboratorWorker(worker_constraints=HumanWorkerConstraint(email=["test@test.com"], worker_id=[1]))
    print(worker.dict())
    constraints = TaskHandler._map_worker_constraints(worker)
    print(constraints)
    assert "emails" in constraints
    assert "included_ids" in constraints
    print(constraints)
    assert constraints["emails"][0] == "test@test.com"
    assert constraints["included_ids"][0] == 1


def test_worker_instance():
    """Worker should not be instantiated without type"""
    with pytest.raises(ValidationError):
        Worker()


def test_worker_type_in_worker():
    """Ensure that the `type` key is part of the dict when using pydantic's dict() method"""
    worker = CollaboratorWorker()
    worker_dict = worker.dict()
    assert str(worker_dict["type"]) == WorkerType.collaborators.value


def test_bot_worker():
    bot = BotWorker()
    assert str(bot.type) == "bots"
    dictionary = bot.dict()
    assert "workerConstraints" in dictionary
    assert "groups" in dictionary["workerConstraints"]
    assert dictionary["workerConstraints"]["groups"][0] == "BOTS"


def test_worker():
    """Test that the worker constraints are acting as expected"""
    # Unset worker_id sholud not trigger validation error
    worker_without_id = CrowdWorker(
        worker_constraints=WorkerConstraint(
            email=["test@test.com"],
        ),
    )
    assert worker_without_id


@pytest.mark.skip(reason="Disabled until UI can interpret training constraints")
def test_worker_training_constraint():
    worker = CrowdWorker(
        worker_constraints=WorkerConstraint(
            trainings=TrainingConstraintSet(
                training_constraints=[TrainingConstraint(name="test", value=0.5, operator=MetricOperator.GREATER_THAN)]
            )
        ),
    )
    constraints = TaskHandler._map_worker_constraints(worker)
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
    result = mock_task_result(completed_future)
    test_future.set_result(result)

    params = SuperTaskConfig(workers=[CollaboratorWorker(), BotWorker()], strategy=TaskStrategy.FIRST_COMPLETED)

    router = TaskRouter(task_config=params)
    assert router
    futures = router.map(task_input=sample_input, task_output=sample_output)
    assert futures

    selected = router.reduce(futures)
    assert selected == test_future.result()["values"]


def test_super_task_workflow(monkeypatch, mocker):
    # Disable transport calls
    mocker.patch("superai.data_program.protocol.task.start_threading")
    mocker.patch("superai.data_program.protocol.task.serve_workflow")
    mocker.patch("superai.data_program.protocol.transport.subscribe_workflow")

    params = SuperTaskConfig(workers=[CollaboratorWorker()], strategy=TaskStrategy.FIRST_COMPLETED)
    model = SuperTaskModel.create(name="test", config=params, input=TestInput, output=TestOutput)
    workflow = SuperTaskWorkflow(model, prefix="test_dp")

    # Create dummy future with result
    test_future = Future()
    result = mock_task_result(dict(formData=dict(annotation="test")))
    test_future.set_result(result)

    # Mock task router functions already tested above
    monkeypatch.setattr("superai.data_program.task.task_router.TaskRouter.map", lambda *args, **kwargs: [test_future])
    monkeypatch.setattr(
        "superai.data_program.task.task_router.TaskRouter.reduce",
        lambda *args, **kwargs: dict(formData=dict(annotation="test")),
    )

    inputs = dict(input=sample_input, output=sample_output)
    output = workflow.execute_workflow(job_input=inputs, configs=params.dict())
    assert output
    assert output["annotation"] == "test"


def test_supertask_timeout_task_fail(monkeypatch):
    test_future = Future()
    monkeypatch.setattr("superai.data_program.task.basic.Task._create_task_future", lambda *args, **kwargs: test_future)
    result = mock_task_result(expired_future)
    test_future.set_result(result)

    params = SuperTaskConfig(
        workers=[
            CollaboratorWorker(on_timeout=OnTimeout(action=OnTimeoutAction.fail)),
            BotWorker(on_timeout=OnTimeout(action=OnTimeoutAction.fail)),
        ],
        strategy=TaskStrategy.FIRST_COMPLETED,
    )

    router = TaskRouter(task_config=params)

    with pytest.raises(TaskExpiredMaxRetries):
        router.map(task_input=sample_input, task_output=sample_output)


def test_supertask_timeout_task_expire(monkeypatch):
    test_future = Future()
    monkeypatch.setattr("superai.data_program.task.basic.Task._create_task_future", lambda *args, **kwargs: test_future)
    result = mock_task_result(expired_future)
    test_future.set_result(result)

    # Patch the backoff to speed up testing
    monkeypatch.setattr("superai.data_program.task.task_router.randint", Mock(side_effect=[1, 1]))

    params = SuperTaskConfig(
        workers=[
            CollaboratorWorker(on_timeout=OnTimeout(action=OnTimeoutAction.retry, max_retries=1)),
            BotWorker(on_timeout=OnTimeout(action=OnTimeoutAction.retry, max_retries=1)),
        ],
        strategy=TaskStrategy.FIRST_COMPLETED,
    )

    router = TaskRouter(task_config=params)

    # Should raise at the second retry since the result is always mocked as EXPIRED
    with pytest.raises(TaskExpiredMaxRetries):
        router.map(task_input=sample_input, task_output=sample_output)


def test_supertask_timeout_task_successful(monkeypatch):
    timeout_test_future = Future()
    successful_future = Future()
    return_data = [timeout_test_future, timeout_test_future, successful_future]
    timeout_result = mock_task_result(expired_future)
    working_result = mock_task_result(completed_future)
    timeout_test_future.set_result(timeout_result)
    successful_future.set_result(working_result)
    test_mock = Mock(side_effect=return_data)
    monkeypatch.setattr(
        "superai.data_program.task.basic.Task._create_task_future",
        test_mock,
    )
    # Patch the backoff to speed up testing
    monkeypatch.setattr("superai.data_program.task.task_router.randint", Mock(side_effect=[1, 1, 1]))

    params = SuperTaskConfig(
        workers=[
            CollaboratorWorker(on_timeout=OnTimeout(action=OnTimeoutAction.retry, max_retries=2)),
        ],
        strategy=TaskStrategy.FIRST_COMPLETED,
    )

    router = TaskRouter(task_config=params)
    # Should not raise since the third call has a completed future
    futures = router.map(task_input=sample_input, task_output=sample_output)
    router.reduce(futures)
    assert test_mock.call_count == len(return_data)


def test_supertask_timeout_task_successful_idempotent():
    params = SuperTaskConfig(
        workers=[IdempotentWorker()],
        strategy=TaskStrategy.FIRST_COMPLETED,
    )

    router = TaskRouter(task_config=params)
    futures = router.map(task_input=sample_input, task_output=sample_output)
    results = router.reduce(futures)
    assert results == sample_output


def test_supertask_editable():
    params = SuperTaskConfig(
        workers=[IdempotentWorker()],
        strategy=TaskStrategy.FIRST_COMPLETED,
        editable=False,
    )
    assert params.editable is False


def test_one_task_on_all_workers_inactive():
    params = SuperTaskConfig(
        workers=[
            IdempotentWorker(active=False),
            CollaboratorWorker(active=False, on_timeout=OnTimeout(action=OnTimeoutAction.retry, max_retries=2)),
        ],
        strategy=TaskStrategy.FIRST_COMPLETED,
    )

    router = TaskRouter(task_config=params)
    futures = router.map(task_input=sample_input, task_output=sample_output)
    assert futures
    assert len(futures.done) == 1
    assert len(futures.not_done) == 0
