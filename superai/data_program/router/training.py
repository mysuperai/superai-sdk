import os
from typing import TYPE_CHECKING

from superai.data_program.router import Router

if TYPE_CHECKING:
    from superai.data_program import DataProgram

from superai import Client
from superai.data_program.Exceptions import ChildJobFailed, JobTypeNotImplemented
from superai.data_program.protocol.task import (
    execute,
    get_job_app,
    get_job_type,
    input_schema,
    output_schema,
    param_schema,
    workflow,
)


class Training(Router):
    def __init__(
        self,
        training_dataprogram: "DataProgram" = None,
        dataprogram_name: str = os.getenv("TRAINING_DATAPROGRAM"),
        dataprogram_suffix: str = "router",
        name: str = "training",
        client: Client = None,
    ):
        super().__init__(
            name=name,
            client=client,
            dataprogram=training_dataprogram,
        )
        assert (
            dataprogram_name is not None and dataprogram_suffix is not None
        ), "Training should register with a dataprogram_name and dataprogram_suffix"

        self.parent_workflow = f"{dataprogram_name}.{dataprogram_suffix}"
        self.default_wf_name = training_dataprogram.default_workflow
        self.workflows = training_dataprogram.workflows

        assert self.default_wf_name is not None, "No default method registered."

        self.prefix = training_dataprogram.name

        self.input_schema = self.workflows[0].input_schema
        self.parameter_schema = self.workflows[0].parameter_schema
        self.default_parameter = self.workflows[0].default_parameter
        self.output_schema = self.workflows[0].output_schema

        self.name = name
        self.wf_name = f"{self.prefix}.{self.name}"

        self.validate()
        self.subscribe_wf()
        # self.update_wf(api_key=api_key)

    def subscribe_wf(self):
        @workflow(self.name + "", self.prefix)
        @input_schema(name="inp", schema=self.input_schema)
        @param_schema(name="params", schema=self.parameter_schema)
        @output_schema(schema=self.output_schema)
        def training(inp, params):
            app_id = get_job_app()
            job_type = get_job_type()
            print(f"ROUTING {job_type} JOB")

            if job_type == "TRAINING":
                # Send job
                selected_workflow = self.client.get_project(uuid=app_id).get("selectedWorkflow")
                return send_workflow_job(
                    workflow=selected_workflow,
                    input=inp,
                    params=params,
                    job_type=job_type,
                    app_uuid=app_id,
                )

            else:
                raise JobTypeNotImplemented(f"Training does not support the given job type: {job_type}")

        def send_workflow_job(workflow, input, params, job_type, app_uuid):
            job = execute(workflow, params=input, app_params={"params": params}, tag=app_uuid)
            result = job.result()
            status = result.status()
            if not status or status != "COMPLETED":
                raise ChildJobFailed(
                    f"{workflow} method did not complete for {job_type} job. Result {result}. Status {status}"
                )
            return job.result().response(), job.result().data(), None
