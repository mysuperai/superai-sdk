from concurrent.futures import Future
from random import randint
from time import sleep, time
from typing import Dict, List, Optional

from superai.data_program.Exceptions import TaskExpiredMaxRetries, UnknownTaskStatus
from superai.data_program.protocol.task import (
    task_future,
    wait_tasks_AND,
    wait_tasks_OR,
)
from superai.data_program.task.workers import IdempotentWorker
from superai.log import logger
from superai.utils.opentelemetry import tracer

from .basic import Task
from .types import BaseRouter, Input, Output, SuperTaskConfig, TaskStrategy
from .workers import Worker

log = logger.get_logger(__name__)


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
            log.info(f"Task {task_template.name} submitted for worker {self.worker}.")
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


class TaskRouter(BaseRouter):
    """Wrapper class around creating, mapping and aggregating tasks according to the Worker Parameters in SuperTask."""

    def __init__(
        self,
        task_config: SuperTaskConfig,
        allowed_strategies: List[str] = [TaskStrategy.PRIORITY, TaskStrategy.FIRST_COMPLETED],
    ):
        self.task_config = task_config
        if self.task_config.params.strategy not in allowed_strategies:
            raise ValueError(f"Unknown task strategy {self.task_config.params.strategy}")

    @tracer.start_as_current_span("supertask_map")
    def map(self, task_input, task_output) -> Optional[Dict[int, TaskHandler]]:
        tasks = {}
        for index, worker in enumerate(self.task_config.workers):
            if not worker.active:
                continue
            task_handler = TaskHandler(task_input, task_output, worker, index)
            task_handler.submit_task()
            tasks[index] = task_handler

        if not tasks:
            # We mimic one idempotent worker, since we still want the input as the output of the SuperTask
            active_mocked_worker = IdempotentWorker(name="Idempotent", active=True)
            task_handler = TaskHandler(task_input, task_output, active_mocked_worker, 0)
            task_handler.submit_task()
            tasks[0] = task_handler

        # Semantically the function would be better suited for the reduce, however
        # due to the fact that the router is extended, we don't want child classes
        # being responsable to handle the retrials.
        return self._handle_retrial(tasks)

    @tracer.start_as_current_span("supertask_reduce")
    def reduce(self, task_futures: Dict[int, TaskHandler]) -> dict:
        """Handles retrial and aggregation of results"""
        # Sort futures based on initial index in `workers` list
        sorted_futures = sorted(task_futures.done, key=lambda f: f._index)

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
