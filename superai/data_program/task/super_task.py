from typing import Generic, List, Union

from pydantic.generics import GenericModel

from superai.data_program.Exceptions import ChildJobFailed, ChildJobInternalError
from superai.data_program.protocol.task import (
    WorkflowType,
    execute,
    task_future,
    wait_tasks_AND,
    wait_tasks_OR,
)
from superai.log import logger

from ..workflow import Workflow
from .basic import Task, model_to_task_io_payload
from .types import (
    Input,
    Output,
    SuperTaskConfig,
    SuperTaskModel,
    TaskResponse,
    TaskStrategy,
    Worker,
)

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

    def schedule(
        self, task_input: Input, task_output: Output, super_task_params: SuperTaskConfig
    ) -> TaskResponse[Output]:
        """Function responsible for scheduling a new child job (which will run `execute`), waiting and returning the result.

        The parameters for the super tasks get passed down from the router job and tha used for the job creation.

        Args:
            task_input: The input for the task.
            task_output:    The output for the task.
            super_task_params: The parameters for the super task.

        Returns:

        """

        job = execute(
            name=self.qualified_name,
            params=self.job_input_model(input=task_input, output=task_output).dict(),
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
        if status != "COMPLETED":
            raise ChildJobInternalError(failure_message)

        response = job.result().response()
        return TaskResponse[self._template.output].parse_obj(response)

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
        job_input = self.job_input_model.parse_obj(job_input)
        task_input = job_input.input
        task_output = job_input.output

        router = TaskRouter(task_config=task_configs, task_input=task_input, task_output=task_output)
        tasks = router.map()
        selected = router.reduce(tasks)

        raw_result = selected.result()
        logger.debug(f"Task {selected} completed.")
        output = task_output.parse_obj(raw_result["values"]["formData"])

        return self.job_output_model(task_output=output).dict(exclude_unset=True, exclude_none=True)


class TaskRouter:
    """Wrapper class around creating, mapping and aggregating tasks according to the Worker Parameters in SuperTask."""

    def __init__(
        self,
        task_config: SuperTaskConfig,
        task_input: Input,
        task_output: Output,
    ):
        self.task_config = task_config
        self.task_input = task_input
        self.task_output = task_output

    def map(self) -> List[task_future]:
        tasks = []
        for index, w in enumerate(self.task_config.workers):
            if not w.active:
                continue
            task_future = self._create_worker_future(w, self.task_input, self.task_output)
            task_future._index = index

            tasks.append(task_future)
        return tasks

    def reduce(self, task_futures: List[task_future]) -> task_future:
        # Wait and aggregate results
        results = None
        if self.task_config.params.strategy == TaskStrategy.FIRST_COMPLETED:
            results = wait_tasks_OR(task_futures)
        elif self.task_config.params.strategy == TaskStrategy.BEST:
            # TODO: find way to have scores to sort by
            # results = wait_tasks_AND(tasks)
            raise NotImplementedError("TaskStrategy.BEST is not implemented yet.")
        elif self.task_config.params.strategy == TaskStrategy.PRIORITY:
            results = wait_tasks_AND(task_futures)
        else:
            raise ValueError("Unknown task strategy.")

        if not results or not results.done:
            raise Exception("No complete results returned from tasks.")

        # Sort futures based on initial index in `workers` list
        sorted_futures = sorted(results.done, key=lambda f: f._index)

        if (
            self.task_config.params.strategy == TaskStrategy.FIRST_COMPLETED
            or self.task_config.params.strategy == TaskStrategy.PRIORITY
        ):
            # Return first completed or highest priority task
            # In case of 'FirstCompleted', we should only have one task anyway
            selected = sorted_futures[0]
        else:
            raise Exception("Could not find completed and matching task future.")
        return selected

    def _create_worker_future(self, w: Worker, task_input, task_output):
        """Create an actual task and return the future."""
        task_template = Task(name=w.name)

        constraints = self._map_worker_constraints(w)

        task_future = task_template.submit(
            task_inputs=model_to_task_io_payload(task_input),
            task_outputs=model_to_task_io_payload(task_output),
            worker_type=w.type,
            **constraints,
        )
        logger.info(f"Task {task_template.name} submitted for worker {w}.")
        return task_future

    @staticmethod
    def _map_worker_constraints(w) -> dict:
        """Map constraints from the worker model to the task constraints understandable by the backend."""
        constraints = {}
        if w.worker_constraints:
            constraints["included_ids"] = w.worker_constraints.worker_id
            constraints["emails"] = w.worker_constraints.email
            constraints["groups"] = w.worker_constraints.groups
            constraints["excluded_groups"] = w.worker_constraints.excluded_groups
            if w.worker_constraints.trainings:
                constraints["qualifications"] = w.worker_constraints.trainings.get_metrics_list()
        return constraints
