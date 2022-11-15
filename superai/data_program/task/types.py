import enum
from typing import Callable, Dict, Generic, List, Optional, Type, TypeVar, Union

from pydantic import Extra, Field, validator
from pydantic.generics import GenericModel
from superai_schema.types import BaseModel
from typing_extensions import Protocol, TypedDict

Input = TypeVar("Input", bound=BaseModel)
Output = TypeVar("Output", bound=BaseModel)


class MetricCalculateValueResponse(BaseModel):
    value: float


class MetricHandler(Protocol[Output]):
    # signature of the metric function
    def __call__(self, *, truths: List[Output], preds: List[Output]) -> Dict[str, MetricCalculateValueResponse]:
        pass


class Metric(BaseModel):
    name: str
    metric_fn: Callable

    def __init__(self, name: str, metric_fn: MetricHandler) -> None:
        """Use custom init method to allow backwards compatiblity with old signature with positional argument based init."""
        name = name
        metric_fn = metric_fn

        super().__init__(name=name, metric_fn=metric_fn)


class TaskTemplate(GenericModel, Generic[Input, Output]):
    """TaskTemplate is a generic class that can be used to define the input and output models for a task."""

    name: str
    input: Type[Input]
    output: Type[Output]
    metrics: Optional[List[str]] = Field(min_items=1)

    def __init__(self, metrics: Optional[List[Metric]] = None, **kwargs) -> None:
        if metrics is not None:
            metrics = [metric.name for metric in metrics]
        super().__init__(metrics=metrics, **kwargs)


class TaskResponse(GenericModel, Generic[Output]):
    """TaskResponse is a generic class to model the task response interface coming from the send_task functions."""

    task_output: Output
    hero_id: Optional[int]


class SendTask(Protocol[Output]):
    """Signature of the method to send a task within job context"""

    def __call__(
        self,
        name: str,
        *,
        task_template: TaskTemplate,
        task_input: BaseModel,
        task_output: Output,
        max_attempts: int,
        excluded_ids: List[int],
    ) -> TaskResponse[Output]:
        pass


class TaskIOPayload(TypedDict):
    schema: dict
    uiSchema: dict
    formData: dict


class WorkerType(str, enum.Enum):
    """The type of worker that is allowed to complete a task."""

    bots = "bots"
    me = "owner"
    ai = "ai"
    crowd = "crowd"
    collaborators = "collaborators"


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
        default=OnTimeoutAction.retry.value, description="Action to take when a task does not get completed in time."
    )
    max_retries: Optional[int] = Field(
        None, ge=1, description="If action is set to retry or reassign, specifies the number of attempts."
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
        LogicalOperator.AND, description="Logical operator to chain multiple training constraints."
    )
    training_constraints: List[TrainingConstraint] = Field(description="List of training constraints.")

    def get_metrics_list(self) -> List[str]:
        """Exports this model as a list of metrics backend can understand"""
        dict = self.dict(include={"training_constraints": True}, by_alias=False)
        return dict["training_constraints"]


class WorkerConstraint(BaseModel):
    """This models the selection criteria for a worker.
    We can either include or exclude workers by IDs or email addresses or group membership.
    Or we define constraints based on training qualifications.
    """

    worker_id: Optional[List[int]] = Field(
        None, min_items=1, description="Filter workers by their IDs.", title="Worker IDs"
    )
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


class Worker(BaseModel):
    """The main model for a task worker.
    It contains fields to select a worker and how to react on a response from a previously sent task.
    Additionally, it contains fields to shown in the UI for management (name, description).
    """

    name: str = Field("TaskWorker", min_length=1, description="Name of the worker.")
    description: Optional[str] = Field(
        None, description="Description of this worker entry. Used for organization and documentation."
    )
    type: WorkerType
    num_tasks: int = Field(
        1,
        ge=1,
        description="Number of tasks to send to this worker entry. In conjunction with `distinct` allows to send multiple tasks to the same/different worker.",
        title="Number of tasks",
    )
    timeout: int = Field(600, ge=1, description="Time in seconds for the worker to complete the task.")
    on_timeout: Optional[OnTimeout] = Field(
        OnTimeout(action=OnTimeoutAction.retry, max_retries=3), title="Timeout action"
    )
    distinct: Optional[bool] = Field(
        None, description="Ensures that the same worker does not receive the same task twice in case of recreation."
    )
    worker_constraints: Optional[WorkerConstraint] = Field(None, title="Worker Constraints")
    active: Optional[bool] = Field(True, description="If set to false, the worker entry is ignored.")
    confidence_threshold: Optional[float] = Field(
        0.0, ge=0.0, le=1.0, description="Allows rejecting task results with a confidence score below the threshold."
    )
    field_mappings: Optional[Dict[str, str]] = Field(
        None, description="Allows mapping the task output to a specific field in the job input."
    )

    class Config:
        extra = Extra.forbid


class TaskStrategy(str, enum.Enum):
    """A list of supported task combination strategies."""

    # TODO: add custom strategy

    FIRST_COMPLETED = "FIRST_COMPLETED"
    # BEST = "BEST"
    PRIORITY = "PRIORITY"


class SuperTaskParameters(BaseModel):
    """Parameter model for one super task.
    Contains additional paramaters to control the SuperTask execution, excluding worker parameters.
    E.g. the task combination strategy.
    The parameters here are supposed to be editable by the app owner.
    """

    strategy: Optional[TaskStrategy] = Field(TaskStrategy.FIRST_COMPLETED)


class SuperTaskWorkers(BaseModel):
    """Contains the model for the allowed workers for a SuperTask.
    Currently only contains a list of workers.
    Is necessary to create a correct JSONSchema.
    """

    __root__: List[Worker]

    def __getitem__(self, item):
        return self.__root__[item]

    def __iter__(self):
        return iter(self.__root__)

    def __len__(self):
        return len(self.__root__)


class SuperTaskConfig(BaseModel):
    """Configuration model for one super task.
    Contains the configuration how the task will get routed and to which workers.

    The parameters here are supposed to be editable by the app owner.
    """

    workers: SuperTaskWorkers
    params: SuperTaskParameters = Field(SuperTaskParameters())

    def get_workers_schema(self) -> dict:
        """Method to get the JSONSchema for the workers.
        Direct access to the workers is not possible, because the workers are wrapped in a list.
        """
        return self.__fields__["workers"].type_.schema()


class SuperTaskModel(BaseModel):
    """A super task is a task that is composed of multiple subtasks.

    The workers are the workers that are allowed to execute the subtasks.
    The subtasks are executed and aggregated determined by the strategy.
    Each task has a unique name (by workflow).
    The template contains the task template/schema for the subtasks and is stored in the super_task workflow.

    """

    name: str
    config: SuperTaskConfig
    template: TaskTemplate

    class Config:
        extra = Extra.forbid
        # arbitrary_types_allowed = True

    @classmethod
    def create(
        cls,
        name: str,
        input: Type[Input],
        output: Type[Output],
        config: Union[
            SuperTaskConfig,
            "DPSuperTaskConfigs",
        ],
    ) -> "SuperTaskModel":
        """Create a super task model from a name, input and output type and default params.
        Args:
            name: The name of the super task.
            input: Model of the input.
            output: Model of the output.
            config: (Default) parameter for the super task.
                Different to input/output, this is not a type but an instance of the params.
                Is supposed to be passed in the `super_task_params` in the `handler()`.
                Also allows passing the `DPSuperTaskConfigs` which contains all named parameters for a Data program.

        Returns:
            SuperTaskModel instance

        """
        if isinstance(config, DPSuperTaskConfigs):
            config = config[name]
        elif not isinstance(config, SuperTaskConfig):
            raise ValueError(f"Expected SuperTaskConfig or DPSuperTaskConfigs, got {type(config)}")

        template = TaskTemplate(
            name=name,
            input=input,
            output=output,
        )
        model = SuperTaskModel(
            name=name,
            template=template,
            config=config,
        )
        return model


class SendSuperTask(Protocol[Output]):
    """Signature of the method to send a super task within job context"""

    def __call__(
        self,
        name: Union[str, SuperTaskModel],
        task_input: BaseModel,
        task_output: Output,
    ) -> TaskResponse[Output]:
        pass


class DPSuperTaskConfigs(BaseModel):
    """Collects all the super task configs for a Dataprogram (as defaults) or concrete App
    Is extending a normal dict, where the keys are the unique super task names.
    Contains validation to make sure the super task names are the same as the keys.
    """

    __root__: Dict[str, SuperTaskConfig]

    def __iter__(self):
        return iter(self.__root__.values())

    def items(self):
        return self.__root__.items()

    def __getitem__(self, key):
        return self.__root__[key]

    def __init__(self, root_value: Optional[Dict[str, SuperTaskConfig]] = None, **kwargs):
        """Allow init with list or dict"""
        value = root_value or kwargs.pop("__root__", None) or kwargs
        super().__init__(__root__=value)

    @classmethod
    def from_schema_response(cls, response: List[dict], dp_name: str) -> "DPSuperTaskConfigs":
        """Create a `DPSuperTaskConfigs` from the schema response of a Data Program.
        Args:
            response: The schema SuperTaskSchemaResponse stored in the database.
            dp_name: The name of the Data Program.
        """
        """Turbines schema is a bit different from the SDK schema"""
        super_task_params_list = [SuperTaskSchemaResponse.parse_obj(stp) for stp in response]
        super_task_params_dict = {
            stp.super_task_workflow.split(dp_name + ".")[1]: SuperTaskConfig.parse_obj(stp)
            for stp in super_task_params_list
        }
        return cls.parse_obj(super_task_params_dict)


class DPSuperTasks(BaseModel):
    """Collects all the super tasks models for a data program.
    Is extending a normal dict, where the keys are the unique super task names.
    Contains validation to make sure the super task names are the same as the keys.
    """

    __root__: Dict[str, SuperTaskModel] = Field()

    def __iter__(self):
        return iter(self.__root__.values())

    @validator("__root__")
    def validate_unique(cls, v):
        for key, value in v.items():
            if key != value.name:
                raise ValueError("Super task name must match the key")
        return v

    def __init__(self, root_value: Optional[Union[List, dict]] = None, **kwargs):
        """Allow init with list or dict"""
        value = root_value or kwargs.pop("__root__", None) or kwargs
        if isinstance(value, list):
            value = {item.name: item for item in value}
        super().__init__(__root__=value)

    def get_configs(self) -> DPSuperTaskConfigs:
        return DPSuperTaskConfigs.parse_obj({name: task.config for name, task in self.__root__.items()})


class SuperTaskSchemaResponse(BaseModel):
    """Expected payload schema for backend retrieved in the DP Server."""

    super_task_workflow: str
    workers: SuperTaskWorkers
    parameters: SuperTaskParameters
    workers_schema: dict
    parameters_schema: dict


class MetricRequestModel(BaseModel):
    truths: List[dict]
    preds: List[dict]
