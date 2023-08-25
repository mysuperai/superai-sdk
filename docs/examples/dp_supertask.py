"""An example DataProgram that uses a SuperTask to process a single job.
SuperTasks are an abstraction of a single atomic task that can be used to create dynamically parameterized tasks based on App settings.
A SuperTask can contain multiple tasks with different Workers.
Additionally, a SuperTask has a strategy to aggregate the results of the tasks. (Still WIP)

"""
import logging
import time
from typing import Optional

from superai_schema.types import BaseModel, Field

from superai.data_program import (
    BotWorker,
    CollaboratorWorker,
    DataProgram,
    HandlerOutput,
    JobContext,
    Project,
)
from superai.data_program.task.types import (
    DPSuperTaskConfigs,
    SuperTaskConfig,
    SuperTaskModel,
    SuperTaskParameters,
    TaskStrategy,
)
from superai.data_program.workflow import WorkflowConfig

SUPER_TASK_NAME = "test_task"


class ParameterModel(BaseModel):
    """
    Select which fields to extract from your documents.
    """

    instructions: str

    class Config:
        title = "Test DP Instructions"


def handler(params: ParameterModel, super_task_params: Optional[DPSuperTaskConfigs] = None) -> HandlerOutput:
    instructions = params.instructions

    class JobInput(BaseModel):
        class Config:
            schema_extra = {"examples": [{"url": "https://cdn.super.ai/invoice-example.pdf"}]}

        url: str = Field(title="Original Document")

    class JobOutput(BaseModel):
        """Also acts as the output model for our super task."""

        message: str = Field("", title="Message")
        url: str = Field("", title="URL")

        class Config:
            title = "Processed Document"
            schema_extra = {"examples": [{"message": "test"}]}

    class TaskInput(BaseModel):
        instructions: str

        class Config:
            title = "Instructions"

    # Create a super task model
    # The params are passed in the `super_task_params` in the `handler()` and are coming from the App settings defined by the app owner.
    # When the DP initializes without an app context, the default super task parameters are passed.
    # The `super_task_params` contain the parameters for all supertasks. Single parameters can also be accessed by name.
    # E.g. `super_task_params[SUPER_TASK_NAME]` for the test_task.
    test_task = SuperTaskModel.create(name=SUPER_TASK_NAME, input=TaskInput, output=JobOutput, config=super_task_params)

    def process_job(job_input: JobInput, context: JobContext[JobOutput]) -> JobOutput:
        """Minimal job handler that just returns the output of a single SuperTask."""
        task_input = TaskInput(instructions=instructions)
        task_output = JobOutput(url=job_input.url)

        super_task_output = context.send_supertask(test_task, task_input, task_output)

        return super_task_output.task_output

    return HandlerOutput(
        input_model=JobInput,
        output_model=JobOutput,
        process_fn=process_job,
        super_tasks=[test_task],
    )


if __name__ == "__main__":
    dp_name = "dp_test_supertask"
    # Create a Dataprogram with default Super Task Params
    dp = DataProgram.create(
        default_params=ParameterModel(instructions="These are the DP default instructions."),
        # Create a SuperTaskParams object to pass to the DataProgram
        # This is mandatory if you want to use SuperTasks in your DataProgram
        default_super_task_configs={
            "test_task": SuperTaskConfig(
                workers=[CollaboratorWorker(), BotWorker()],
                params=SuperTaskParameters(strategy=TaskStrategy.FIRST_COMPLETED),
            ),
        },
        name=dp_name,
        handler=handler,
    )

    dp.start_all_services(
        workflows=[
            WorkflowConfig("parse", is_default=True, is_gold=True),
        ]
    )
    start = time.time()
    startup_timeout_secs = 30
    while not dp.schema_server_reachable() and time.time() - start < startup_timeout_secs:
        logging.info("Waiting for schema server to be reachable")
        time.sleep(1)

    project = Project(
        dataprogram=dp,
        name="My SuperTask Test project",
        params={"instructions": "These are my app instructions"},
        run_dataprogram=False,  # We already started the services
        # uuid="662b73b7-b1f7-4fef-8f82-cbf74f9ab510", # Use a specific UUID to reuse existing projects for testing
    )
