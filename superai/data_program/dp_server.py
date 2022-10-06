import contextlib
import os
from typing import Callable, Dict, List, Optional, Union

import fastapi
import uvicorn
from fastapi import HTTPException, Response, status
from jsonschema import ValidationError, validate
from pydantic import BaseModel
from pyngrok import ngrok
from superai_schema.types import UiWidget
from typing_extensions import Literal

from superai.client import Client
from superai.data_program.types import (
    Handler,
    MethodResponse,
    Metric,
    MetricCalculateValueResponse,
    MetricRequestModel,
    Output,
    Parameters,
    PostProcessContext,
    PostProcessRequestModel,
    SchemaServerResponse,
    TaskTemplate,
    WorkflowConfig,
)
from superai.log import logger
from superai.utils import load_api_key, load_auth_token, load_id_token, retry

log = logger.get_logger(__name__)


class DPServer:
    name: str
    params: Parameters
    params_schema: dict
    generate: Handler[Parameters]
    log_level: Literal["critical", "error", "warning", "info", "debug", "trace"]
    post_process_fn: Optional[Callable[[Output, PostProcessContext], str]]
    task_templates_dict: Dict[str, TaskTemplate]
    workflows: List[MethodResponse]
    metrics_dict: Dict[str, Metric]

    def __init__(
        self,
        params: Parameters,
        generate: Handler[Parameters],
        name: str,
        workflows: List[WorkflowConfig],
        template_name: str,
        port: int,
        log_level: Literal["critical", "error", "warning", "info", "debug", "trace"] = "info",
    ):
        self.name = name
        self.params = params
        self.params_schema = params.schema()
        self.generate = generate
        self.log_level = log_level

        handler_output = generate(self.params)
        self.input_model = handler_output.input_model
        self.output_model = handler_output.output_model
        self.post_process_fn = handler_output.post_process_fn

        self.template_name = template_name

        self.workflows = []
        for method in workflows:
            method_name = f"{self.name}.{method.name}"
            if method.measure:
                self.workflows.append(MethodResponse(method_name=method_name, role="normal"))
            if method.is_gold:
                self.workflows.append(MethodResponse(method_name=method_name, role="gold"))

        assert len(handler_output.metrics) > 0, "At least one metric should be defined"
        self.metrics_dict = {metric.name: metric for metric in handler_output.metrics}

        for task_template in handler_output.templates:
            assert (
                task_template.metrics_dict.keys() == self.metrics_dict.keys()
            ), "The metric names in task template should be a same as in metrics"
        self.task_templates_dict = {task_template.name: task_template for task_template in handler_output.templates}
        self.dp_server_port = port
        self.client = Client(api_key=load_api_key(), auth_token=load_auth_token(), id_token=load_id_token())

    @retry(Exception, tries=5, delay=0.5, backoff=1)
    def get_reverse_proxy_endpoint(self) -> str:
        endpoint = self.client.get_workflow(self.template_name).get("endpoint", None)
        return endpoint

    @retry(Exception, tries=5, delay=0.5, backoff=1)
    def update_reverse_proxy_endpoint(self, public_url: str) -> None:
        self.client.update_workflow(self.template_name, body={"endpoint": public_url})

    @contextlib.contextmanager
    def ngrok_contextmanager(self, is_local=False):
        # Boot up ngrok reverse proxy only in case of local deploy
        if is_local and self.template_name:
            # ensure the connection gets closed properly
            try:
                original_reverse_proxy_endpoint = self.get_reverse_proxy_endpoint()
                ngrok_tunnel = ngrok.connect(self.dp_server_port)
                new_reverse_proxy_endpoint = ngrok_tunnel.public_url
                logger.info(f"Setting {new_reverse_proxy_endpoint} as public endpoint until shutdown of the DP server")
                self.update_reverse_proxy_endpoint(new_reverse_proxy_endpoint)
                yield
            finally:
                logger.info(f"Reverting endpoint back to {original_reverse_proxy_endpoint}")
                self.update_reverse_proxy_endpoint(original_reverse_proxy_endpoint)
                ngrok.disconnect(new_reverse_proxy_endpoint)
        else:
            yield

    def run(self):
        app = fastapi.FastAPI()
        cls = self.params.__class__

        class RequestModel(BaseModel):
            params: cls

        @app.post("/schema", response_model=SchemaServerResponse)
        def handle_post(app_params: RequestModel) -> SchemaServerResponse:
            handler_output = self.generate(app_params.params)
            input_model, output_model = handler_output.input_model, handler_output.output_model

            try:
                # FastAPI's request body parser seems to ignore some directives
                # in JSON schema (e.g. `uniqueItems`) so I need to validate again
                validate(app_params.params.dict(), self.params_schema)
            except ValidationError as e:
                log.exception(e)
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
                log.exception(e)
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
                log.exception(e)
                raise HTTPException(status_code=422, detail=str(e))

        @app.get("/methods", response_model=List[MethodResponse])
        def get_methods():
            return self.workflows

        @app.post("/post-process", response_model=Optional[str])
        def post_process(output: PostProcessRequestModel) -> Union[str, Response]:
            if self.post_process_fn is None:
                # this data program does not implement post-processing
                return Response(status_code=status.HTTP_204_NO_CONTENT)
            try:
                output_response = self.output_model.parse_obj(output.response)
                context = PostProcessContext(job_uuid=output.job_uuid, app_uuid=output.app_uuid)
                return self.post_process_fn(output_response, context)
            except Exception as e:
                log.exception(e)
                raise HTTPException(status_code=422, detail=str(e))

        is_local = not (os.environ.get("ECS") or os.environ.get("JENKINS_URL"))

        with self.ngrok_contextmanager(is_local=is_local):
            uvicorn.run(app, host="0.0.0.0", port=self.dp_server_port, log_level=self.log_level)
