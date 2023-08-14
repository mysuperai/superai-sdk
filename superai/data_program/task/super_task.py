from concurrent.futures import Future
from random import randint
from time import sleep, time
from typing import Dict, Generic, List, Optional, Union

from pydantic.generics import GenericModel

from superai.data_program.Exceptions import (
    ChildJobExpired,
    ChildJobFailed,
    ChildJobInternalError,
    TaskExpiredMaxRetries,
    UnknownTaskStatus,
)
from superai.data_program.protocol.task import (
    WorkflowType,
    execute,
    task_future,
    wait_tasks_AND,
    wait_tasks_OR,
)
from superai.log import logger
from superai.utils.opentelemetry import tracer

from ..workflow import Workflow
from .basic import Task, model_to_task_io_payload
from .types import (
    Input,
    Output,
    SuperTaskConfig,
    SuperTaskModel,
    TaskResponse,
    TaskStrategy,
)
from .workers import Worker

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
        if status == "EXPIRED":
            raise ChildJobExpired(failure_message)
        if status != "COMPLETED":
            raise ChildJobInternalError(failure_message)

        response = job.result().response()
        return response

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

        router = TaskRouter(task_config=task_configs)
        tasks = router.map(task_input, task_output)
        raw_result = router.reduce(tasks)

        return raw_result["formData"]


class TaskHandler:
    def __init__(self, task_input: Input, task_output: Output, worker: Worker, index: int):
        self.task_input = task_input
        self.task_output = task_output
        self.worker = worker
        self.retrial_policy = worker.on_timeout.action
        self.max_retries = worker.on_timeout.max_retries or 0
        self.constraints = self._map_worker_constraints(worker)
        self.index = index
        self.retries_done = 0

    def submit_task(self):
        """Create an actual task"""
        task_template = Task(name=self.worker.name)

        if self.worker.type == "idempotent":
            task_future = Future()
            task_future.set_result({"values": self.task_output, "timestamp": time(), "status": "COMPLETED"})
        else:
            task_future = task_template.submit(
                task_inputs=self.task_input,
                task_outputs=self.task_output,
                worker_type=self.worker.type,
                **self.constraints,
            )
            logger.info(f"Task {task_template.name} submitted for worker {self.worker}.")
        self.task_future = task_future
        self.task_future._index = self.index

    def is_future_done(self):
        return self.task_future.done()

    def is_result_ready(self):
        if self.worker.type == "idempotent":
            return True

        # check if future needs to be retried
        result = self.task_future.result()

        if result.status() in ["EXPIRED", "REJECTED"]:
            return False
        if result.status() != "COMPLETED":
            raise UnknownTaskStatus(str(result.status()))

        log.info("Task succeeded, checking results")
        getter = getattr(result.response(), "get", None)
        if callable(getter) and len(getter("values", [])) > 0:
            return True
        log.warning("Completed task, but empty task response.")
        return False

    def retry_future(self):
        if self.retries_done >= self.max_retries or self.retrial_policy != "RETRY":
            raise TaskExpiredMaxRetries(f"Exhausted the retries after {str(self.retries_done)} were done.")
        self.retries_done = self.retries_done + 1

        backoff_time = randint(5, 20) * self.retries_done
        log.info(f"Resending task after {backoff_time}s backoff period, trial no. {self.retries_done}")
        sleep(backoff_time)

        self.submit_task()

    @staticmethod
    def _map_worker_constraints(w: Worker) -> dict:
        """Map constraints from the worker model to the task constraints understandable by the backend."""
        constraints = {}
        if w.worker_constraints:
            constraint_dict = w.worker_constraints.dict()
            if "workerId" in constraint_dict:
                constraints["included_ids"] = w.worker_constraints.worker_id
            if "email" in constraint_dict:
                constraints["emails"] = w.worker_constraints.email
            if "groups" in constraint_dict:
                constraints["groups"] = w.worker_constraints.groups
            if "excludedGroups" in constraint_dict:
                constraints["excluded_groups"] = w.worker_constraints.excluded_groups
            if "trainings" in constraint_dict:
                constraints["qualifications"] = w.worker_constraints.trainings.get_metrics_list()
            if "trainingId" in constraint_dict and constraint_dict["trainingId"] is not None:
                constraints["qualifier_test_id"] = w.worker_constraints.training_id
        if w.timeout:
            constraints["time_to_expire_secs"] = w.timeout
        if "pay" in w.__fields__:
            constraints["cost"] = w.pay
        return constraints


class TaskRouter:
    """Wrapper class around creating, mapping and aggregating tasks according to the Worker Parameters in SuperTask."""

    def __init__(
        self,
        task_config: SuperTaskConfig,
        allowed_strategies: List[str] = [TaskStrategy.PRIORITY, TaskStrategy.FIRST_COMPLETED],
    ):
        self.task_config = task_config
        if self.task_config.params.strategy not in allowed_strategies:
            raise ValueError("Unknown task strategy.")

    @tracer.start_as_current_span("supertask_map")
    def map(self, task_input, task_output) -> Optional[Dict[int, TaskHandler]]:
        tasks = {}
        for index, worker in enumerate(self.task_config.workers):
            if not worker.active:
                continue
            task_handler = TaskHandler(task_input, task_output, worker, index)
            task_handler.submit_task()
            tasks[index] = task_handler
        return tasks

    @tracer.start_as_current_span("supertask_reduce")
    def reduce(self, task_futures: Dict[int, TaskHandler]) -> dict:
        """Handles retrial and aggregation of results"""
        results = self._handle_retrial(task_futures)
        # Sort futures based on initial index in `workers` list
        sorted_futures = sorted(results.done, key=lambda f: f._index)

        # Return first completed or highest priority task
        # In case of 'FirstCompleted', we should only have one task anyway
        selected = sorted_futures[0]

        # In case of more complex reduction we don't have a single future to return
        # for example in the case of combination of tasks. So we return the result.
        return selected.result()["values"]

    @tracer.start_as_current_span("handle_retrial")
    def _handle_retrial(self, task_futures: Dict[int, TaskHandler]) -> List[task_future]:
        while True:
            futures = wait_tasks_OR([handler.task_future for handler in task_futures.values()])

            for current_handler in task_futures.values():
                # since we waited with OR the first done is all we need.
                if current_handler.is_future_done():
                    break

            # is result ready is BLOCKING, that's why we check it only for the one future that's done
            if not current_handler.is_result_ready():
                # Future needs to be retried
                current_handler.retry_future()
                continue
            if self.task_config.params.strategy == TaskStrategy.FIRST_COMPLETED:
                return futures

            futures = wait_tasks_AND([handler.task_future for handler in task_futures.values()])

            result_ready = True
            for current_handler in task_futures.values():
                # if any of them doesn't have the result ready we need to retry
                if not current_handler.is_result_ready():
                    current_handler.retry_future()
                    result_ready = False

            if result_ready:
                return futures
