import json
from typing import Callable, Dict, Generic, List, Optional, Tuple, Type, TypeVar

from attr import define
from pydantic import Extra, Field, root_validator
from superai_schema.types import BaseModel
from typing_extensions import Protocol

from superai.data_program.task.types import (
    DPSuperTaskConfigs,
    DPSuperTasks,
    Input,
    Metric,
    Output,
    SendSuperTask,
    SendTask,
    SuperTaskSchemaResponse,
    TaskTemplate,
)
from superai.data_program.workflow import WorkflowConfig

Parameters = TypeVar("Parameters", bound=BaseModel)


@define
class PostProcessContext:
    job_uuid: Optional[str] = None
    job_cache: Optional[dict] = None
    app_uuid: Optional[str] = None


class PostProcessRequestModel(BaseModel):
    job_uuid: str
    response: dict
    app_uuid: Optional[str]
    app_params: Optional[dict]


class SuperTaskGraphRequestModel(BaseModel):
    app_params: dict
    super_task_params: dict


class MethodResponse(BaseModel):
    method_name: str
    role: str


class JobContext(Generic[Output]):
    workflow: WorkflowConfig
    send_task: SendTask[Output]
    job_cache: Optional[dict]
    is_training: bool
    send_supertask: SendSuperTask[Output]

    def __init__(
        self,
        workflow: WorkflowConfig,
        send_task: SendTask[Output],
        use_job_cache: bool = False,
        is_training: bool = False,
        send_supertask: Optional[SendSuperTask[Output]] = None,
    ):
        self.workflow = workflow
        self.send_task = send_task
        self.job_cache = {} if use_job_cache else None
        self.is_training = is_training
        self.send_supertask = send_supertask


class HandlerOutput(BaseModel):
    input_model: Type[Input]
    output_model: Type[Output]
    process_fn: Callable[[Input, JobContext], Output]
    post_process_fn: Optional[Callable[[Output, PostProcessContext], str]]
    templates: Optional[List[TaskTemplate]] = Field([])
    metrics: Optional[List[Metric]] = Field([], min_items=1)
    super_tasks: Optional[DPSuperTasks] = Field([])
    post_processing: Optional[bool]
    super_tasks_graph_fn: Optional[Callable[[DPSuperTaskConfigs, Output], Dict[str, list]]]

    class Config:
        arbitrary_types_allowed = True

    @root_validator
    def validate_templates(cls, values):
        """Automatically add the super task templates to the templates list and validate uniqueness"""
        templates = values.get("templates", [])
        if "super_tasks" in values and values["super_tasks"]:
            for st in values.get("super_tasks", []):
                templates.append(st.template)

        # Ensure that task names are unique
        names = [t.name for t in templates]
        if len(names) != len(set(names)):
            raise ValueError("Task names must be unique. Make sure you don't add templates from SuperTasks twice.")

        return values


class Handler(Protocol[Parameters]):
    """Signature of the data program's main logic"""

    def __call__(self, params: Parameters, super_tasks: Optional[Parameters] = None) -> HandlerOutput:
        pass


class SchemaServerResponse(BaseModel):
    input_schema: dict
    input_ui_schema: dict
    output_schema: dict
    output_ui_schema: dict
    super_tasks: Optional[List[SuperTaskSchemaResponse]] = None
    post_processing: Optional[bool]

    class Config:
        extra = Extra.forbid


@define
class DataProgramDefinition:
    input_schema: dict
    output_schema: dict
    input_ui_schema: Optional[dict] = {}
    output_ui_schema: Optional[dict] = {}
    parameter_schema: Optional[dict] = {}
    parameter_ui_schema: Optional[dict] = {}
    default_parameter: Optional[dict] = None
    supertask_models: Optional[DPSuperTasks] = []

    def parse_args(self, uses_new_schema=None) -> Tuple:
        from superai.data_program.protocol.task import _parse_args

        input_schema = _parse_args(schema=self.input_schema, uses_new_schema=uses_new_schema).get("schema")
        output_schema = _parse_args(schema=self.output_schema, uses_new_schema=uses_new_schema).get("schema")
        parameter_schema = _parse_args(schema=self.parameter_schema, uses_new_schema=uses_new_schema).get("schema")
        default_parameter = self.default_parameter
        return (
            input_schema,
            output_schema,
            parameter_schema,
            default_parameter,
        )

    @classmethod
    def from_handler(
        cls, params: Parameters, handler: Handler[Parameters], default_super_task_configs: Parameters = None
    ) -> "DataProgramDefinition":
        param_schema = params.schema()
        from superai.data_program.utils import _call_handler

        handler_output = _call_handler(handler, params, super_task_configs=default_super_task_configs)
        input_model, output_model = (
            handler_output.input_model,
            handler_output.output_model,
        )
        from superai_schema.types import UiWidget

        return DataProgramDefinition(
            parameter_schema=param_schema,
            parameter_ui_schema=params.ui_schema() if isinstance(params, UiWidget) else {},
            input_schema=input_model.schema(),
            input_ui_schema=input_model.ui_schema() if issubclass(input_model, UiWidget) else {},
            output_schema=output_model.schema(),
            output_ui_schema=output_model.ui_schema() if issubclass(output_model, UiWidget) else {},
            default_parameter=json.loads(params.json(exclude_none=True)),
            supertask_models=handler_output.super_tasks,
        )
