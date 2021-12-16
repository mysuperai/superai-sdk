from typing import Callable, Optional, Type, TypeVar, Tuple, Generic
from typing_extensions import Protocol, TypedDict

from superai_schema.types import BaseModel

Input = TypeVar("Input", bound=BaseModel)
Output = TypeVar("Output", bound=BaseModel)
Parameters = TypeVar("Parameters", bound=BaseModel)


class SendTask(Protocol[Output]):
    """
    Signature of the method to send a task within job context
    """

    def __call__(self, name: str, *, task_input: BaseModel, task_output: Output, max_attempts: int) -> Output:
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

    def __call__(self, params: Parameters) -> Tuple[Type[Input], Type[Output], Callable[[Input, JobContext], Output]]:
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
