from typing import Callable, Optional, Type, TypeVar, Tuple, Generic, List, Dict
from typing_extensions import Protocol, TypedDict

from superai_schema.types import BaseModel


Input = TypeVar("Input", bound=BaseModel)
Output = TypeVar("Output", bound=BaseModel)
Parameters = TypeVar("Parameters", bound=BaseModel)


class MetricCalculateValueResponse(BaseModel):
    value: float


class MetricHandler(Protocol[Output]):
    # signature of the metric function
    def __call__(self, *, truths: List[Output], preds: List[Output]) -> Dict[str, MetricCalculateValueResponse]:
        pass


class Metric:
    name: str
    metric_fn: MetricHandler

    def __init__(self, name: str, metric_fn: MetricHandler) -> None:
        self.name = name
        self.metric_fn = metric_fn


class TaskTemplate(Generic[Input, Output]):
    name: str
    input: Type[Input]
    output: Type[Output]
    metrics_dict: Dict[str, Metric]

    def __init__(self, name: str, input: Type[Input], output: Type[Output], metrics: List[Metric]) -> None:
        self.name = name
        self.input = input
        self.output = output
        assert len(metrics) > 0, "At least one task metric should be defined"
        self.metrics_dict = {metric.name: metric for metric in metrics}


class SendTask(Protocol[Output]):
    """
    Signature of the method to send a task within job context
    """

    def __call__(
        self, name: str, *, task_template: TaskTemplate, task_input: BaseModel, task_output: Output, max_attempts: int
    ) -> Output:
        pass


class WorkflowConfig:
    name: str
    is_default: bool
    is_gold: bool
    description: Optional[str]

    def __init__(self, name: str, *, is_default: bool = False, is_gold: bool = False, description: str = None):
        self.name = name
        self.is_gold = is_gold
        self.is_default = is_default
        self.description = description


class JobContext(Generic[Output]):
    workflow: WorkflowConfig
    send_task: SendTask[Output]

    def __init__(self, workflow: WorkflowConfig, send_task: SendTask[Output]):
        self.workflow = workflow
        self.send_task = send_task


class Handler(Protocol[Parameters, Input, Output]):
    """
    Signature of the data program's "main logic"
    """

    def __call__(
        self, params: Parameters
    ) -> Tuple[Type[Input], Type[Output], Callable[[Input, JobContext], Output], List[TaskTemplate], List[Metric]]:
        pass


class DataProgramDefinition(TypedDict):
    input_schema: dict
    input_ui_schema: Optional[dict]
    output_schema: dict
    output_ui_schema: Optional[dict]
    parameter_schema: Optional[dict]
    parameter_ui_schema: Optional[dict]
    default_parameter: Optional[dict]


class TaskIOPayload(TypedDict):
    schema: dict
    uiSchema: dict
    formData: dict


class SchemaServerResponse(BaseModel):
    inputSchema: dict
    inputUiSchema: dict
    outputSchema: dict
    outputUiSchema: dict


class MetricRequestModel(BaseModel):
    truths: List[dict]
    preds: List[dict]


class MethodResponse(BaseModel):
    method_name: str
    role: str
