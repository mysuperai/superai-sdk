import logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from superai.data_program import DataProgram

import superai_schema.universal_schema.data_types as dt

from superai import Client
from superai.data_program.Exceptions import (
    CancelledError,
    ChildJobExpired,
    ChildJobFailed,
    ChildJobInternalError,
    JobTypeNotImplemented,
)
from superai.data_program.protocol.task import (
    execute,
    get_job_app,
    get_job_type,
    input_schema,
    metric_schema,
    output_schema,
    param_schema,
    workflow,
)
from superai.data_program.router import Router
from superai.log import logger

log = logger.get_logger(__name__)


class BasicRouter(Router):
    def __init__(
        self,
        name: str = "router",  # Can't get overriden for now
        client: Client = None,
        dataprogram: "DataProgram" = None,
        **kwargs,
    ):
        super().__init__(
            name=name,
            client=client,
            dataprogram=dataprogram,
            **kwargs,
        )

        self.default_wf = dataprogram.default_workflow
        self.gold_wf = dataprogram.gold_workflow

        assert len(self.workflows) > 0, "Router must have at least one workflow"
        assert self.default_wf is not None, "No default method registered."
        assert self.gold_wf is not None, "No gold method registered."

        self.prefix = dataprogram._name

        self._uses_new_schema = self.dataprogram._uses_new_schema
        self.input_schema = self.workflows[0].input_schema
        self.parameter_schema = self.workflows[0].parameter_schema
        self.default_parameter = self.workflows[0].default_parameter
        self.output_schema = self.workflows[0].output_schema

        self.name = name
        self.qualified_name = f"{self.prefix}.{self.name}"

        self.validate()
        self.subscribe_wf()

    def subscribe_wf(self):
        @workflow(self.name, self.prefix, uses_new_schema=self._uses_new_schema)
        @input_schema(name="inp", schema=self.input_schema, uses_new_schema=self._uses_new_schema)
        @param_schema(
            name="params",
            schema=self.parameter_schema,
            default=self.default_parameter,
            uses_new_schema=self._uses_new_schema,
        )
        @metric_schema(name="metric", schema=dt.bundle(), default={}, uses_new_schema=self._uses_new_schema)
        @output_schema(schema=self.output_schema, uses_new_schema=self._uses_new_schema)
        def router(inp, metric, params, super_task_params=None):
            app_id = get_job_app()
            job_type = get_job_type()
            log.info(f"Routing {job_type} job")

            if job_type == "BOT_INIT":
                return send_workflow_job(
                    workflow=self.default_wf,
                    input=inp,
                    params=params,
                    job_type=job_type,
                    app_uuid=app_id,
                    super_task_params=super_task_params,
                )

            elif job_type in (
                "DEFAULT",
                "ONBOARDING",
                "COLLABORATOR",
                "MEASURER",
            ):
                # Get selected method workflow
                selected_workflow = self.client.get_project(uuid=app_id).get("selectedWorkflow")
                if selected_workflow:
                    # Send job
                    job_response = send_workflow_job(
                        workflow=selected_workflow,
                        input=inp,
                        params=params,
                        job_type=job_type,
                        app_uuid=app_id,
                        super_task_params=super_task_params,
                    )
                    return job_response

                else:
                    logging.warning(f"No selected workflow for app {app_id}. " "Falling back to dataprogram default.")
                    return send_workflow_job(
                        workflow=self.default_wf,
                        input=inp,
                        params=params,
                        job_type=job_type,
                        app_uuid=app_id,
                        super_task_params=super_task_params,
                    )

            elif job_type == "CALIBRATION":
                # Send job to gold method
                job_response = send_workflow_job(
                    workflow=self.gold_wf,
                    input=inp,
                    params=params,
                    job_type=job_type,
                    app_uuid=app_id,
                    super_task_params=super_task_params,
                )
                return job_response
            else:
                raise JobTypeNotImplemented(f"Router does not support the given job type: {job_type}")

        def send_workflow_job(workflow, input, params, job_type, app_uuid, super_task_params):
            job = execute(
                workflow, params=input, app_params={"params": params}, tag=app_uuid, super_task_params=super_task_params
            )
            result = job.result()
            status = result.status()

            failure_message = f"{workflow} method did not complete for {job_type} job. Result {result}. Status {status}"
            if not status:
                raise ChildJobInternalError(failure_message)

            if status == "FAILED":
                raise ChildJobFailed(failure_message)
            elif status == "EXPIRED":
                raise ChildJobExpired(failure_message)
            elif status == "CANCELED":
                raise CancelledError(failure_message)
            elif status == "COMPLETED":
                return job.result().response(), job.result().data(), None
            else:
                raise ChildJobInternalError(failure_message)
