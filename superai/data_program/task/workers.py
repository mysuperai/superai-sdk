import enum
from abc import ABC
from typing import Dict, List, Optional

from pydantic import Extra, Field
from superai_schema.types import BaseModel
from typing_extensions import Literal


class WorkerType(str, enum.Enum):
    """The type of worker that is allowed to complete a task."""

    bots = "bots"
    me = "owner"
    ai = "ai"
    crowd = "crowd"
    collaborators = "collaborators"
    idempotent = "idempotent"


class OnTimeoutAction(str, enum.Enum):
    """Lists the action taken after the task of a worker times out.
    Is used in the router and combiner functions.
    """

    retry = "RETRY"
    reassign = "REASSIGN"
    fail = "FAIL"


class OnTimeout(BaseModel):
    """Defines the strategy taken when a task times out or is cancelled.
    Is used in the router and combiner functions.
    """

    action: OnTimeoutAction = Field(
        default=OnTimeoutAction.retry.value,
        description="Action to take when a task does not get completed in time.",
    )
    max_retries: Optional[int] = Field(
        None,
        ge=1,
        description="If action is set to retry or reassign, specifies the number of attempts.",
    )


class MetricOperator(str, enum.Enum):
    """Defines the operator used to compare the metric values.
    One example is to compare the confidence score of a task output with a predefined threshold.
    Or to compare the training score of a worker with a threshold.
    """

    LESS_THAN = "LESS_THAN"
    LESS_THAN_OR_EQUALS_TO = "LESS_THAN_OR_EQUALS_TO"
    EQUALS_TO = "EQUALS_TO"
    GREATER_THAN_OR_EQUALS_TO = "GREATER_THAN_OR_EQUALS_TO"
    GREATER_THAN = "GREATER_THAN"
    EXISTS = "EXISTS"
    NOT_EXISTS = "NOT_EXISTS"
    UNDEFINED = "UNDEFINED"


class TrainingConstraint(BaseModel):
    """Defines the training constraint for a worker.
    A worker is either qualified and fulfils the constraint or not.
    """

    name: str = Field(description="Name of the training constraint.")
    value: Optional[float] = Field(gt=0, le=1, description="The threshold value for the metric.")
    operator: MetricOperator = Field(MetricOperator.EXISTS)


class LogicalOperator(str, enum.Enum):
    """Enum to chain together multiple training constraints in a boolean expression."""

    AND = "_and"
    # TODO: Add OR operator in turbine
    # OR = "_or"


class TrainingConstraintSet(BaseModel):
    """Defines a set of training constraints.
    We expect only workers which fulfil all the constraints to be qualified.
    """

    # TODO: Add support in turbine for operator
    logical_operator: LogicalOperator = Field(
        LogicalOperator.AND,
        description="Logical operator to chain multiple training constraints.",
    )
    training_constraints: List[TrainingConstraint] = Field(description="List of training constraints.")

    def get_metrics_list(self) -> List[str]:
        """Exports this model as a list of metrics backend can understand"""
        dictionary = self.dict(include={"training_constraints": True}, by_alias=False)
        return dictionary["training_constraints"]


class WorkerConstraint(BaseModel):
    """This models the selection criteria for a general worker."""

    worker_id: Optional[List[int]] = Field(
        None,
        description="Filter workers by their IDs.",
        title="Worker IDs",
    )


class HumanWorkerConstraint(WorkerConstraint):
    """This models the selection criteria for a human worker.
    We can either include or exclude workers by IDs or email addresses or group membership.
    Or we define constraints based on training qualifications.
    """

    email: Optional[List[str]] = Field(None, description="Filter workers by their email addresses.", title="Emails")
    # TODO: Enable this once UI is ready in next Version
    # trainings: Optional[TrainingConstraintSet] = Field(
    #    None, description="Filter workers by their training qualifications."
    # )
    groups: Optional[List[str]] = Field(
        None,
        description="Filter workers by their group membership.",
    )
    excluded_groups: Optional[List[str]] = Field(None, description="Exclude workers by their group membership.")
    training_id: Optional[int] = Field(
        None, description="Send only to workers that have passed this training.", title="Training ID"
    )


class BotWorkerConstraint(WorkerConstraint):
    """Force a task to be completed by a bot worker. Identified by literal 'BOTS' group."""

    groups: List[Literal["BOTS"]] = Field(["BOTS"], description="Force a task to be completed by a bot worker.")


class Worker(BaseModel, ABC):
    """The main model for a task worker.
    It contains fields to select a worker and how to react on a response from a previously sent task.
    Additionally, it contains fields to shown in the UI for management (name, description).
    """

    name: str = Field("TaskWorker", min_length=1, description="Name of the worker.")
    description: Optional[str] = Field(
        None,
        description="Description of this worker entry. Used for organization and documentation.",
    )
    num_tasks: int = Field(
        1,
        ge=1,
        description="Number of tasks to send to this worker entry. In conjunction with `distinct` allows to send "
        "multiple tasks to the same/different worker.",
        title="Number of tasks",
    )
    timeout: int = Field(86400, ge=1, description="Time in seconds for the worker to complete the task.")
    on_timeout: Optional[OnTimeout] = Field(
        OnTimeout(action=OnTimeoutAction.retry, max_retries=3), title="Timeout action"
    )
    distinct: Optional[bool] = Field(
        None,
        description="Ensures that the same worker does not receive the same task twice in case of recreation.",
    )
    worker_constraints: Optional[WorkerConstraint] = Field(None, title="Worker Constraints")
    active: Optional[bool] = Field(True, description="If set to false, the worker entry is ignored.")
    confidence_threshold: Optional[float] = Field(
        0.0,
        ge=0.0,
        le=1.0,
        description="Allows rejecting task results with a confidence score below the threshold.",
    )
    type: Literal["crowd", "bots", "collaborators", "ai", "idempotent"] = Field(..., description="Type of the worker.")

    class Config:
        extra = Extra.forbid


class CrowdWorker(Worker):
    """Defines a human worker.
    It is a subclass of the Worker class and adds a field for the UI to show.
    """

    pay: float = Field(0.1, ge=0.005, description="How much does the hero get paid to solve the task.")
    worker_constraints: Optional[HumanWorkerConstraint] = Field(None, title="Worker Constraints")
    type: Literal["crowd"] = WorkerType.crowd.value


class CollaboratorWorker(Worker):
    """Defines a human worker.
    It is a subclass of the Worker class and adds a field for the UI to show.
    """

    worker_constraints: Optional[HumanWorkerConstraint] = Field(None, title="Worker Constraints")
    type: Literal["collaborators"] = WorkerType.collaborators.value


class AIWorker(Worker):
    """Defines an AI worker.
    It is a subclass of the Worker class and adds a field for the UI to show.
    """

    type: Literal["ai"] = WorkerType.ai.value
    field_mappings: Optional[Dict[str, str]] = Field(
        None,
        description="Allows mapping the task output to a specific field in the job input.",
    )


class BotWorker(Worker):
    """Defines a bot worker.
    It is a subclass of the Worker class and adds a field for the UI to show.
    """

    worker_constraints: BotWorkerConstraint = Field(BotWorkerConstraint(), title="Worker Constraints")
    type: Literal["bots"] = WorkerType.bots.value


class IdempotentWorker(Worker):
    """Defines an idempotent worker.
    This is a pass through worker, equivalent of providing the input of the SuperTask as output
    """

    type: Literal["idempotent"] = WorkerType.idempotent.value
