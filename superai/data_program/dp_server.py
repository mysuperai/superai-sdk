from typing import List, Dict

import fastapi
import uvicorn
from fastapi import HTTPException
from jsonschema import validate, ValidationError
from pydantic import BaseModel
from superai_schema.types import UiWidget
from typing_extensions import Literal

from superai.data_program.types import (
    Handler,
    MethodResponse,
    Parameters,
    SchemaServerResponse,
    Output,
    Input,
    MetricRequestModel,
    MetricCalculateValueResponse,
    WorkflowConfig,
    TaskTemplate,
    Metric,
)


class DPServer:
    name: str
    params: Parameters
    params_schema: dict
    generate: Handler[Parameters, Input, Output]
    log_level: Literal["critical", "error", "warning", "info", "debug", "trace"]
    task_templates_dict: Dict[str, TaskTemplate]
    workflows: Dict[str, str]  # {qualified_name: role}
    metrics_dict: Dict[str, Metric]

    def __init__(
        self,
        params: Parameters,
        generate: Handler[Parameters, Input, Output],
        name: str,
        workflows: List[WorkflowConfig],
        log_level: Literal["critical", "error", "warning", "info", "debug", "trace"] = "info",
    ):
        self.name = name
        self.params = params
        self.params_schema = self.params.schema()
        self.generate = generate
        self.log_level = log_level
        (*_, task_templates, metrics) = generate(self.params)
        self.workflows = {f"{self.name}.{method.name}": "gold" if method.is_gold else "normal" for method in workflows}

        assert len(metrics) > 0, "At least one metric should be defined"
        self.metrics_dict = {metric.name: metric for metric in metrics}

        for task_template in task_templates:
            assert (
                task_template.metrics_dict.keys() == self.metrics_dict.keys()
            ), "The metric names in task template should be a same as in metrics"
        self.task_templates_dict = {task_template.name: task_template for task_template in task_templates}

    def run(self):
        app = fastapi.FastAPI()
        cls = self.params.__class__

        class RequestModel(BaseModel):
            params: cls

        @app.post("/schema", response_model=SchemaServerResponse)
        def handle_post(app_params: RequestModel) -> SchemaServerResponse:
            input_model, output_model, *_ = self.generate(app_params.params)

            try:
                # FastAPI's request body parser seems to ignore some directives
                # in JSON schema (e.g. `uniqueItems`) so I need to validate again
                validate(app_params.params.dict(), self.params_schema)
            except ValidationError as e:
                raise HTTPException(status_code=422, detail=f"{e.message}")

            return SchemaServerResponse(
                inputSchema=input_model.schema(),
                inputUiSchema=input_model.ui_schema() if issubclass(input_model, UiWidget) else {},
                outputSchema=output_model.schema(),
                outputUiSchema=output_model.ui_schema() if issubclass(output_model, UiWidget) else {},
            )

        @app.get("/metrics", response_model=List[str])
        def get_metrics() -> List[str]:
            return list(self.metrics_dict.keys())

        @app.post("/metrics/{metric_name}", response_model=Dict[str, MetricCalculateValueResponse])
        def calculate_metric(metric_name: str, payload: MetricRequestModel) -> Dict[str, MetricCalculateValueResponse]:
            metric = self.metrics_dict.get(metric_name, None)
            if metric is None:
                raise HTTPException(status_code=404, detail=f"{metric_name} not found.")
            try:
                return metric.metric_fn(payload.truths, payload.preds)
            except Exception as e:
                raise HTTPException(status_code=422, detail=str(e))

        @app.post("/metrics/task/{task_name}/{metric_name}", response_model=Dict[str, MetricCalculateValueResponse])
        def calculate_task_metric(
            task_name: str, metric_name: str, payload: MetricRequestModel
        ) -> Dict[str, MetricCalculateValueResponse]:
            task_template = self.task_templates_dict.get(task_name, None)
            if task_template is None:
                raise HTTPException(status_code=404, detail=f"{task_name} not found.")
            metric = task_template.metrics_dict.get(metric_name, None)
            if metric is None:
                raise HTTPException(status_code=404, detail=f"{metric_name} not found.")
            try:
                return metric.metric_fn(payload.truths, payload.preds)
            except Exception as e:
                raise HTTPException(status_code=422, detail=str(e))

        @app.get("/methods", response_model=List[MethodResponse])
        def get_methods():

            return list([MethodResponse(method_name=name, role=role) for name, role in self.workflows.items()])

        uvicorn.run(app, host="0.0.0.0", port=8001, log_level=self.log_level)
