import enum

from superai.data_program.Exceptions import TaskExpired, UnknownTaskStatus
from superai.data_program.protocol.task import task as task
import uuid

# from superai.apis.task_template import TaskTemplate


class Worker(str, enum.Enum):
    bots = "bots"
    me = "owner"
    ai = "ai"
    crowd = "crowd"


class Task:
    def __init__(self, name: str = None, max_retries: int = 0, max_attempts: int = None):
        self.name = name or f"TaskName-{uuid.uuid5()}"
        self.max_attempts = max_retries + 1 if not max_attempts else max_attempts
        self._task_future = None
        self._task_future_result = None

    @property
    def output(self):
        return self._task_future_result.response()

    def __call__(self, task_inputs=None, task_outputs=None, quality=None, cost=None, latency=None, **kwargs):
        self.process(task_inputs, task_outputs, quality=None, cost=None, latency=None, **kwargs)

    def process(self, task_inputs=None, task_outputs=None, quality=None, cost=None, latency=None, **kwargs):
        for n_tries in range(self.max_attempts):
            self._task_future = task(
                input=task_inputs,
                output=task_outputs,
                name=self.name,
                price="EASY",
                qualifications=None,
                groups=None,
                time_to_expire_secs=1 * 60 * 10,
                excluded_ids=None,
                show_reject=False,
                amount=None,
            )
            self._task_future_result = self._task_future.result()
            print(
                f"task status {self._task_future_result.status()} with response: {self._task_future_result.response()}"
            )
            if self._task_future_result.status() == "COMPLETED":
                print("task succeeded")
                if len(self._task_future_result.response()) > 0:
                    return self._task_future_result
                else:
                    print("WARNING: completed task, but empty task response.")
                    print("resending task, trial no. ", n_tries + 1)
                    continue
            elif self._task_future_result.status() in ["EXPIRED", "REJECTED"]:
                print("resending task, trial no. ", n_tries + 1)
                continue
            else:
                raise UnknownTaskStatus(str(self._task_future_result.status()))
        raise TaskExpired("No crowd hero responded to task after " + str(self.max_attempts) + "retries.")
