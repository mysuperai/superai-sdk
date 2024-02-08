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
from superai.data_program.task.types import (
    DPSuperTaskConfigs,
    Metric,
    MetricCalculateValueResponse,
    MetricRequestModel,
    SuperTaskSchemaResponse,
    TaskTemplate,
)
from superai.data_program.types import (
    Handler,
    MethodResponse,
    Output,
    Parameters,
    PostProcessContext,
    PostProcessRequestModel,
    SchemaServerResponse,
    SuperTaskGraphRequestModel,
)
from superai.data_program.utils import _call_handler
from superai.data_program.workflow import WorkflowConfig
from superai.log import logger
from superai.utils import load_api_key, load_auth_token, load_id_token, retry
from superai.utils.opentelemetry import instrumented_lifespan

log = logger.get_logger(__name__)


class DPServer:
    name: str
    params: Parameters
    super_task_configs: DPSuperTaskConfigs
    params_schema: dict
    handler_fn: Handler[Parameters]
    log_level: Literal["critical", "error", "warning", "info", "debug", "trace"]
    post_process_fn: Optional[Callable[[Output, PostProcessContext], str]]
    task_templates_dict: Dict[str, TaskTemplate]
    workflows: List[MethodResponse]
    metrics_dict: Dict[str, Metric]

    def __init__(
        self,
        params: Parameters,
        handler_fn: Handler[Parameters],
        name: str,
        workflows: List[WorkflowConfig],
        template_name: str,
        port: int,
        log_level: Literal["critical", "error", "warning", "info", "debug", "trace"] = "info",
        force_no_tunnel: bool = False,
        super_task_params: DPSuperTaskConfigs = None,
    ):
        """

        Args:
            params: DP Handler parameters
            handler_fn: Handler instantiated with params
            name: DP name (prefix)
            workflows: List of workflows to handle
            template_name: Full DP name (prefix + workflow suffix)
            port: Port to run the server on
            log_level: Log level
            force_no_tunnel: Disables ngrok tunneling, in case you only want to run the server locally for testing
            super_task_models: List of super task schemas
        """
        self.name = name
        self.params = params
        self.params_schema = params.schema()
        self.handler_fn = handler_fn
        self.template_name = template_name
        self.log_level = log_level
        self.force_no_tunnel = force_no_tunnel
        self.super_task_configs = super_task_params
        handler_output = _call_handler(self.handler_fn, self.params, self.super_task_configs)

        self.workflows = []
        for method in workflows:
            method_name = f"{self.name}.{method.name}"
            if method.measure:
                self.workflows.append(MethodResponse(method_name=method_name, role="normal"))
            if method.is_gold:
                self.workflows.append(MethodResponse(method_name=method_name, role="gold"))

        if not handler_output.metrics or len(handler_output.metrics) == 0:
            logger.warning("At least one metric should be defined")
        self.metrics_dict = {metric.name: metric for metric in handler_output.metrics}

        # FIXME: This assertion assumes that we only have one task template which has the same metrics as the global metrics list
        self.task_templates_dict = {task_template.name: task_template for task_template in handler_output.templates}
        self.dp_server_port = port
        self.client = Client(api_key=load_api_key(), auth_token=load_auth_token(), id_token=load_id_token())
        self.super_tasks_graph_fn = handler_output.super_tasks_graph_fn

    @retry(Exception, tries=5, delay=0.5, backoff=1)
    def get_reverse_proxy_endpoint(self) -> str:
        return self.client.get_workflow(self.template_name).get("endpoint", None)

    @retry(Exception, tries=5, delay=0.5, backoff=1)
    def update_reverse_proxy_endpoint(self, public_url: str) -> None:
        self.client.update_workflow(self.template_name, body={"endpoint": public_url})

    @contextlib.contextmanager
    def ngrok_contextmanager(self, needs_tunnel=False):
        # Boot up ngrok reverse proxy only in case of local deploy
        if needs_tunnel and self.template_name:
            # Ensure that the connection gets closed properly
            new_reverse_proxy_endpoint = None
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
                if new_reverse_proxy_endpoint:
                    ngrok.disconnect(new_reverse_proxy_endpoint)
        else:
            yield

    def define_app(self) -> fastapi.FastAPI:
        app = fastapi.FastAPI(lifespan=instrumented_lifespan)
        cls = self.params.__class__

        class RequestModel(BaseModel):
            params: cls
            # TODO: Turbine should pass those params
            # super_task_params: Optional[Dict[str, SuperTaskParams]] = None

        @app.post(
            "/schema",
            response_model=SchemaServerResponse,
            response_model_exclude_none=True,
            response_model_exclude_unset=False,
        )
        def handle_post(app_params: RequestModel) -> SchemaServerResponse:
            # TODO: Turbine should pass those params
            # super_task_params = app_params.super_task_params
            # handler_output = _call_handler(self.handler_fn, app_params.parms, super_task_params)
            handler_output = _call_handler(self.handler_fn, app_params.params, self.super_task_configs)
            input_model, output_model = handler_output.input_model, handler_output.output_model
            has_post_processing = handler_output.post_processing
            # super_task_models = handler_output.super_tasks

            try:
                # FastAPI's request body parser seems to ignore some directives
                # in JSON schema (e.g. `uniqueItems`) so I need to validate again
                validate(app_params.params.dict(), self.params_schema)
            except ValidationError as e:
                log.exception(e)
                raise HTTPException(status_code=422, detail=f"{e.message}")

            # TODO: Use passed and validated super_task_params for generating response
            # for st in super_task_models:
            super_task_responses = []
            if self.super_task_configs:
                for name, st_config in self.super_task_configs.items():
                    method_name = f"{self.name}.{name}"
                    super_task_responses.append(
                        SuperTaskSchemaResponse(
                            super_task_workflow=method_name,
                            parameters=st_config.params,
                            workers=st_config.workers,
                            workers_schema=st_config.get_workers_schema() or {},
                            parameters_schema=st_config.params.schema() or {},
                        )
                    )

            response = SchemaServerResponse(
                input_schema=input_model.schema(),
                input_ui_schema=input_model.ui_schema() if issubclass(input_model, UiWidget) else {},
                output_schema=output_model.schema(),
                output_ui_schema=output_model.ui_schema() if issubclass(output_model, UiWidget) else {},
                super_tasks=super_task_responses or None,  # This hides the key when it's empty
                post_processing=has_post_processing,
            )
            return response

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
            app_params = cls.parse_obj(output.app_params["params"])
            handler_output = _call_handler(self.handler_fn, app_params, self.super_task_configs)
            output_model, post_process_fn = handler_output.output_model, handler_output.post_process_fn
            if post_process_fn is None:
                # This data program does not implement post-processing
                return Response(status_code=status.HTTP_204_NO_CONTENT)
            try:
                output_response = output_model.parse_obj(output.response)
                context = PostProcessContext(job_uuid=output.job_uuid, app_uuid=output.app_uuid)
                return post_process_fn(output_response, context)
            except Exception as e:
                log.exception(e)
                raise HTTPException(status_code=422, detail=str(e))

        @app.post("/super_tasks-graph", response_model=Dict[str, List])
        def retrieve_graph(payload: SuperTaskGraphRequestModel) -> Union[Optional[Dict[str, List]], HTTPException]:
            print(payload)
            app_params = payload.app_params["params"]
            super_task_params = payload.super_task_params

            if not app_params or not super_task_params:
                # can't comput graph
                return HTTPException(status_code=422, detail="Missing app params or supertask params")

            return self.super_tasks_graph_fn(super_task_params, app_params)

        @app.get("/health")
        def health():
            return "OK"

        return app

    def run(self):
        app = self.define_app()
        needs_tunnel = not (os.environ.get("ECS") or self.force_no_tunnel)

        with self.ngrok_contextmanager(needs_tunnel=needs_tunnel):
            uvicorn.run(app, host="0.0.0.0", port=self.dp_server_port, log_level=self.log_level)
