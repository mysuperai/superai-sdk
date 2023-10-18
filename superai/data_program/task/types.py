import enum
from abc import ABC, abstractmethod
from typing import Callable, Dict, Generic, List, Optional, Type, TypeVar, Union

from pydantic import Extra, Field, validator
from pydantic.generics import GenericModel
from superai_schema.types import BaseModel
from typing_extensions import Protocol, TypedDict

from .workers import (
    AIWorker,
    BotWorker,
    CollaboratorWorker,
    CrowdWorker,
    IdempotentWorker,
)

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


class TaskStrategy(str, enum.Enum):
    """A list of supported task combination strategies."""

    # TODO: add custom strategy

    FIRST_COMPLETED = "FIRST_COMPLETED"
    # BEST = "BEST"
    PRIORITY = "PRIORITY"


class BaseSuperTaskParameters(BaseModel):
    strategy: Optional[str] = Field(TaskStrategy.FIRST_COMPLETED)


class SuperTaskParameters(BaseSuperTaskParameters):
    """Parameter model for one super task.
    Contains additional paramaters to control the SuperTask execution, excluding worker parameters.
    E.g. the task combination strategy.
    The parameters here are supposed to be editable by the app owner.
    """

    strategy: Optional[TaskStrategy] = Field(TaskStrategy.FIRST_COMPLETED)


class SuperTaskWorkers(BaseModel):
    """Contains the model for the allowed workers for a SuperTask.
    Currently only contains a list of workers.
    It is necessary to create a correct JSONSchema.
    """

    __root__: List[Union[CrowdWorker, AIWorker, BotWorker, CollaboratorWorker, IdempotentWorker]]

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
    params: BaseSuperTaskParameters = Field(BaseSuperTaskParameters())
    editable: Optional[bool] = Field(default=None)

    def get_workers_schema(self) -> Optional[dict]:
        """Method to get the JSONSchema for the workers.
        Direct access to the workers is not possible, because the workers are wrapped in a list.
        """
        return self.__fields__["workers"].type_.schema()


class BaseRouter(ABC):
    @abstractmethod
    def map(self):
        pass

    @abstractmethod
    def reduce(self):
        pass


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
    router: Optional[type[BaseRouter]]

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
        router: Type[BaseRouter] = None,
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
        return SuperTaskModel(
            name=name,
            template=template,
            config=config,
            router=router,
        )


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

        super_task_params_dict = {}
        for super_task_param in response:
            response_stp = SuperTaskSchemaResponse.parse_obj(super_task_param)
            super_task_params_dict[response_stp.super_task_workflow.split(f"{dp_name}.")[1]] = SuperTaskConfig(
                workers=response_stp.workers, params=response_stp.parameters
            )
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

    def __len__(self):
        return len(self.__root__)

    def get_configs(self) -> DPSuperTaskConfigs:
        return DPSuperTaskConfigs.parse_obj({name: task.config for name, task in self.__root__.items()})


class SuperTaskSchemaResponse(BaseModel):
    """Expected payload schema for backend retrieved in the DP Server."""

    super_task_workflow: str
    workers: SuperTaskWorkers
    parameters: BaseSuperTaskParameters
    workers_schema: Optional[dict]
    parameters_schema: Optional[dict]


class MetricRequestModel(BaseModel):
    truths: List[dict]
    preds: List[dict]
