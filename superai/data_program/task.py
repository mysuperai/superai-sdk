import enum

from superai.data_program.Exceptions import TaskExpired, UnknownTaskStatus
from superai.data_program.protocol.task import task as task
import uuid
from superai.log import logger

log = logger.get_logger(__name__)

# from superai.apis.task_template import TaskTemplate


class Worker(str, enum.Enum):
    bots = "bots"
    me = "owner"
    ai = "ai"
    crowd = "crowd"


class Task:
    def __init__(self, name: str = None, max_attempts: int = 1):
        self.name = name or f"TaskName-{uuid.uuid4()}"
        self.max_attempts = 1 if not max_attempts else max_attempts
        self._task_future = None
        self._task_future_result = None

    @property
    def output(self):
        return self._task_future_result.response()

    def __call__(self, task_inputs=None, task_outputs=None, quality=None, cost=None, latency=None, **kwargs):
        """
        Submit a task
        :param task_inputs: Inputs to the task
        :param task_outputs: Output expected from the task
        :param quality: Quality expected from the task
        :param cost: Cost expected from the task
        :param latency: Latency expected from the task

        # Hidden kwargs: (To show autofill arguments in Pycharm)
        :param price: Price of task to be sent Eg. "EASY"
        :param time_to_expire_secs: Time to expire of the task
        :param qualifications: Qualification
        :param groups: Groups
        :param excluded_ids: Excluded Ids of heroes
        :param show_reject: Show rejection
        :return:
        """
        self.process(task_inputs, task_outputs, quality=None, cost=None, latency=None, **kwargs)

    def process(self, task_inputs=None, task_outputs=None, quality=None, cost=None, latency=None, **kwargs):
        # Process all possible kwargs
        price = kwargs.get("price", "EASY")
        time_to_expire_secs = kwargs.get("time_to_expire_secs", 1 * 60 * 10)
        qualifications = kwargs.get("qualifications")
        groups = kwargs.get("groups")
        excluded_ids = kwargs.get("excluded_ids")
        show_reject = kwargs.get("show_reject", False)

        for n_tries in range(self.max_attempts):
            self._task_future = task(
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
            )
            self._task_future_result = self._task_future.result()
            log.info(
                f"task status {self._task_future_result.status()} with response: {self._task_future_result.response()}"
            )
            if self._task_future_result.status() == "COMPLETED":
                log.info("task succeeded")
                if len(self._task_future_result.response()) > 0:
                    return self._task_future_result
                else:
                    log.warning("completed task, but empty task response.")
                    log.info("resending task, trial no. ", n_tries + 1)
                    continue
            elif self._task_future_result.status() in ["EXPIRED", "REJECTED"]:
                log.info("resending task, trial no. ", n_tries + 1)
                continue
            else:
                raise UnknownTaskStatus(str(self._task_future_result.status()))
        raise TaskExpired("No crowd hero responded to task after " + str(self.max_attempts) + "retries.")
