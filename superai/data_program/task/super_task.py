from typing import Generic, Union

from pydantic.generics import GenericModel

from superai.data_program.Exceptions import (
    CancelledError,
    ChildJobExpired,
    ChildJobFailed,
    ChildJobInternalError,
)
from superai.data_program.protocol.task import WorkflowType, execute
from superai.data_program.task.task_router import TaskRouter
from superai.log import logger
from superai.utils.opentelemetry import tracer

from ..workflow import Workflow
from .basic import model_to_task_io_payload
from .types import Input, Output, SuperTaskConfig, SuperTaskModel, TaskResponse

log = logger.get_logger(__name__)


class SuperTaskJobInput(GenericModel, Generic[Input, Output]):
    input: Input
    output: Output


class SuperTaskWorkflow(Workflow):
    def __init__(self, schema: SuperTaskModel, prefix: str):
        """Initialize a SuperTaskWorkflow in the DP context.
        It contains the (meta) schema of the task, and the workers that will be used to execute the task.

        A SuperTaskWorkflow(-workflow) is a global object.
        Job specific parameters should not be stored in the SuperTaskWorkflow object.

        During dataprogram execution, a super task is instantiated through the normal schedule_workflow() call.
        The Dataprogram will pick up a new SuperTaskWorkflow-Job and execute its workflow, defined in _execute()..

        Args:
            schema: The schema of the super task.
            prefix: The prefix of the super task name, comes from the DataProgram context.
        """
        self._schema = schema
        self._template = schema.template
        self.job_input_model = SuperTaskJobInput[self._template.input, self._template.output]
        self.job_output_model = TaskResponse[self._template.output]
        from superai.data_program.types import DataProgramDefinition

        dp_definition = DataProgramDefinition(
            input_schema=self.job_input_model.schema(),
            output_schema=self.job_output_model.schema(),
            parameter_schema=self._schema.config.schema(),
            default_parameter=self._schema.config.dict(exclude_unset=True, exclude_none=True),
        )
        self._subscribed = False
        super().__init__(
            workflow_fn=self.execute_workflow,
            prefix=prefix,
            name=schema.name,
            dp_definition=dp_definition,
            on_init_put=False,
            workflow_type=WorkflowType.SUPER_TASK,
            use_new_schema=True,
        )
        if self.name != self._template.name:
            raise ValueError("SuperTaskWorkflow name and TaskTemplate name should be the same.")

    @property
    def schema(self) -> SuperTaskModel:
        return self._schema

    def _register(self):
        """# TODO
        Register Task schema in the backend (Schema service).
        """

    @tracer.start_as_current_span(name="super_task_schedule")
    def schedule(
        self, task_input: Input, task_output: Output, super_task_params: SuperTaskConfig
    ) -> TaskResponse[Output]:
        """Function responsible for scheduling a new child job (which will run `execute`), waiting and returning the result.

        The parameters for the super tasks get passed down from the router job and that's used for the job creation.

        Args:
            task_input: The input for the task.
            task_output: The output for the task.
            super_task_params: The parameters for the super task.

        Returns:

        """

        job = execute(
            name=self.qualified_name,
            params=dict(input=model_to_task_io_payload(task_input), output=model_to_task_io_payload(task_output)),
            app_params=dict(params=super_task_params.dict(exclude_unset=True, exclude_none=True)),
            super_task_params=super_task_params.dict(exclude_unset=True, exclude_none=True),
        )
        result = job.result()
        status = result.status()

        failure_message = (
            f"{self.qualified_name} method did not complete for SuperTaskWorkflow. Result {result}. Status {status}"
        )
        if not status:
            raise ChildJobInternalError(failure_message)

        if status == "FAILED":
            raise ChildJobFailed(failure_message)
        elif status == "EXPIRED":
            raise ChildJobExpired(failure_message)
        elif status == "CANCELED":
            raise CancelledError(failure_message)
        elif status == "COMPLETED":
            response = job.result().response()
            return response
        else:
            raise ChildJobInternalError(failure_message)

    @tracer.start_as_current_span(name="super_task_workflow")
    def execute_workflow(
        self,
        job_input: SuperTaskJobInput,
        configs: Union[dict, SuperTaskConfig],
        **kwargs,
    ) -> dict:
        """Main workflow function of the SuperTaskWorkflow.
        Runs inside the child job.
        Is containing the logic to create actual Tasks and aggregate the results based on the parameters.

        Args:
            job_input:
            configs:
            **kwargs:

        Returns:

        """
        # checks task input type
        task_configs = self._schema.config.parse_obj(configs)
        task_input = job_input["input"]
        task_output = job_input["output"]

        if self.schema.router:
            router = self.schema.router(task_config=task_configs)
        else:
            router = TaskRouter(task_config=task_configs)
        tasks = router.map(task_input, task_output)
        raw_result = router.reduce(tasks)

        return raw_result["formData"]
