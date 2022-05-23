from typing import Callable, Dict, Generic, List, Optional, Type, TypeVar

from superai_schema.types import BaseModel
from typing_extensions import Protocol, TypedDict

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
        self,
        name: str,
        *,
        task_template: TaskTemplate,
        task_input: BaseModel,
        task_output: Output,
        max_attempts: int,
        excluded_ids: List[int],
    ) -> Output:
        pass


class WorkflowConfig:
    name: str
    is_default: bool
    is_gold: bool
    description: Optional[str]
    measure: bool

    def __init__(
        self,
        name: str,
        *,
        is_default: bool = False,
        is_gold: bool = False,
        description: str = None,
        measure: bool = True,
    ):
        self.name = name
        self.is_gold = is_gold
        self.is_default = is_default
        self.description = description
        self.measure = measure


class JobContext(Generic[Output]):
    workflow: WorkflowConfig
    send_task: SendTask[Output]
    job_cache: Optional[dict]
    is_training: bool

    def __init__(
        self,
        workflow: WorkflowConfig,
        send_task: SendTask[Output],
        use_job_cache: bool = False,
        is_training: bool = False,
    ):
        self.workflow = workflow
        self.send_task = send_task
        self.job_cache = {} if use_job_cache else None
        self.is_training = is_training


class PostProcessContext:
    job_uuid: Optional[str]
    job_cache: Optional[dict]

    def __init__(self, job_uuid: Optional[str] = None, job_cache: Optional[dict] = None):
        self.job_uuid = job_uuid
        self.job_cache = job_cache


class HandlerOutput(BaseModel):
    input_model: Type[Input]
    output_model: Type[Output]
    process_fn: Callable[[Input, JobContext], Output]
    post_process_fn: Optional[Callable[[Output, PostProcessContext], str]]
    templates: List[TaskTemplate]
    metrics: List[Metric]

    class Config:
        arbitrary_types_allowed = True


class Handler(Protocol[Parameters]):
    """
    Signature of the data program's "main logic"
    """

    def __call__(self, params: Parameters) -> HandlerOutput:
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


class PostProcessRequestModel(BaseModel):
    job_uuid: str
    response: dict


class MethodResponse(BaseModel):
    method_name: str
    role: str


class TaskResponse(Generic[Output]):
    task_output: Output
    hero_id: Optional[int]

    def __init__(
        self,
        task_output: Output,
        hero_id: Optional[int],
    ):
        self.task_output = task_output
        self.hero_id = hero_id
