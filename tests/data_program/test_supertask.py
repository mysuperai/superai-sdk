from concurrent.futures import Future

import pytest
from pydantic import ValidationError
from superai_schema.types import BaseModel

from superai.data_program import CollaboratorWorker, CrowdWorker

# import superai
from superai.data_program.task.super_task import SuperTaskWorkflow, TaskRouter
from superai.data_program.task.types import (
    SuperTaskConfig,
    SuperTaskModel,
    TaskStrategy,
)
from superai.data_program.task.workers import (
    BotWorker,
    HumanWorkerConstraint,
    MetricOperator,
    TrainingConstraint,
    TrainingConstraintSet,
    Worker,
    WorkerConstraint,
    WorkerType,
)


def test_worker_schema():
    worker = CollaboratorWorker()
    assert worker
    assert worker.schema()
    assert worker.dict()


def test__map_worker_constraints():
    worker = CollaboratorWorker(worker_constraints=HumanWorkerConstraint(email=["test@test.com"], worker_id=[1]))
    print(worker.dict())
    constraints = TaskRouter._map_worker_constraints(worker)
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

    params = SuperTaskConfig(workers=[CollaboratorWorker(), BotWorker()], strategy=TaskStrategy.FIRST_COMPLETED)

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

    result = mock_task_result({"status": "COMPLETED", "timestamp": 1234, "values": {"annotation": "test"}})
    test_future.set_result(result)

    selected = router.reduce(futures)
    assert selected == test_future.result()["values"]


def test_super_task_workflow(monkeypatch, mocker):
    class TestInput(BaseModel):
        url: str

    class TestOutput(BaseModel):
        annotation: str

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
    monkeypatch.setattr("superai.data_program.task.super_task.TaskRouter.map", lambda *args, **kwargs: [test_future])
    monkeypatch.setattr(
        "superai.data_program.task.super_task.TaskRouter.reduce",
        lambda *args, **kwargs: dict(formData=dict(annotation="test")),
    )

    inputs = dict(input=TestInput(url="http://a.com"), output=TestOutput(annotation=""))
    output = workflow.execute_workflow(job_input=inputs, configs=params.dict())
    assert output
    assert output["annotation"] == "test"
