import json
import uuid
from typing import Dict, List, Optional

from superai_schema.types import BaseModel, UiWidget

from superai.data_program.Exceptions import TaskExpired, UnknownTaskStatus
from superai.data_program.protocol.task import task
from superai.data_program.protocol.transport import task_future
from superai.log import logger

from .types import TaskIOPayload
from .workers import WorkerType

log = logger.get_logger(__name__)


class Task:
    def __init__(self, name: str = None, max_attempts: int = 1):
        self.name = name or f"TaskName-{uuid.uuid4()}"
        self.max_attempts = max_attempts or 1
        self._task_future = None
        self._task_future_result = None

    worker_type_mapping: Dict[WorkerType, str] = {
        WorkerType.bots: "CROWD",
        WorkerType.me: "USER",
        WorkerType.collaborators: "USER",
        WorkerType.ai: "AI",
        WorkerType.crowd: "CROWD",
        WorkerType.idempotent: "IDEMPOTENT",
    }

    @property
    def output(self):
        return self._task_future_result.response()

    def __call__(self, task_inputs=None, task_outputs=None, quality=None, cost=None, latency=None, **kwargs):
        """
        Submit a task

        Args:
            task_inputs: Inputs to the task
            task_outputs: Output expected from the task
            quality: Quality expected from the task
            cost: Cost expected from the task
            latency: Latency expected from the task
            worker_type: Type of worker to be used for the task
            price: Price of task to be sent Eg. "EASY"
            time_to_expire_secs: Time to expire of the task
            qualifications: Qualification
            groups: Groups
            excluded_ids: Excluded Ids of heroes
            show_reject: Show rejection
        """
        self.process(task_inputs, task_outputs, cost=None, **kwargs)

    def submit(
        self,
        task_inputs=None,
        task_outputs=None,
        cost=None,
        groups=None,
        price="EASY",
        time_to_expire_secs=1 * 60 * 10,
        qualifications: List[dict] = None,
        excluded_ids: List[str] = None,
        show_reject: bool = False,
        worker_type: Optional[WorkerType] = None,
        included_ids: List[str] = None,
        excluded_groups: List[str] = None,
        emails: List[str] = None,
        qualifier_test_id: int = None,
    ) -> task_future:
        """
        Submit a task and return a task_future, which can be used to get the task result async.
        Args:
            task_inputs:
            task_outputs:
            cost:
            groups:
            price:
            time_to_expire_secs:
            qualifications:
            excluded_ids:
            show_reject:
            worker_type:
            included_ids:
            excluded_groups:
            emails: Email addresses of the users to be assigned the task
            qualifier_test_id: Id of the qualifier that needs to be passed to receive the task

        Returns:

        """
        self._task_future = self._create_task_future(
            input=task_inputs,
            output=task_outputs,
            name=self.name,
            price=price,
            qualifications=qualifications,
            groups=groups,
            time_to_expire_secs=time_to_expire_secs,
            excluded_ids=excluded_ids,
            show_reject=show_reject,
            amount=cost,
            worker_type=worker_type,
            included_ids=included_ids,
            excluded_groups=excluded_groups,
            humans=emails,
            qualifier_test_id=qualifier_test_id,
        )
        return self._task_future

    def _create_task_future(self, worker_type=None, groups=None, included_ids=None, **kwargs) -> task_future:
        if worker_type == WorkerType.bots:
            groups = ["BOTS"]
        name = kwargs.pop("name", self.name)

        explicit_id = None
        if worker_type == WorkerType.ai:
            # Needs ID
            if not included_ids or len(included_ids) != 1:
                raise ValueError("Invalid configuration. AI worker requires one and only one model ID")
            explicit_id = included_ids[0]

        mapped_worker_type = self.worker_type_mapping[worker_type] if worker_type else None

        task_future = task(name=name, worker_type=mapped_worker_type, groups=groups, explicit_id=explicit_id, **kwargs)
        return task_future

    def process(
        self,
        task_inputs=None,
        task_outputs=None,
        cost=None,
        groups=None,
        price="EASY",
        time_to_expire_secs=1 * 60 * 10,
        qualifications=None,
        excluded_ids=None,
        show_reject=False,
        worker_type: Optional[WorkerType] = None,
    ):
        for n_tries in range(self.max_attempts):
            self._task_future = self._create_task_future(
                input=task_inputs,
                output=task_outputs,
                price=price,
                qualifications=qualifications,
                groups=groups,
                time_to_expire_secs=time_to_expire_secs,
                excluded_ids=excluded_ids,
                show_reject=show_reject,
                amount=cost,
                worker_type=worker_type,
            )
            self._task_future_result = self._task_future.result()
            log.info(
                f"task status {self._task_future_result.status()} with response: {self._task_future_result.response()}"
            )
            if self._task_future_result.status() == "COMPLETED":
                log.info("task succeeded")
                if len(self._task_future_result.response()) > 0:
                    return self._task_future_result
                log.warning("completed task, but empty task response.")
                log.info(f"resending task, trial no. {n_tries + 1}")
            elif self._task_future_result.status() in ["EXPIRED", "REJECTED"]:
                log.info(f"resending task, trial no. {n_tries + 1}")
                continue
            else:
                raise UnknownTaskStatus(str(self._task_future_result.status()))
        raise TaskExpired(f"No crowd hero responded to task after {str(self.max_attempts)} retries.")


def model_to_task_io_payload(m: BaseModel) -> TaskIOPayload:
    return {
        "schema": m.schema(),
        "uiSchema": m.ui_schema() if isinstance(m, UiWidget) else {},
        "formData": json.loads(m.json(exclude_unset=True)),
    }
