"""A transport layer for communicating with the Agent"""
from __future__ import absolute_import, division, print_function, unicode_literals

import concurrent
import enum
import functools
import io
import json
import os
import signal
import sys
from logging import FATAL, WARN
from threading import Lock, Thread, local
from typing import Optional

import jsonpickle
import sentry_sdk
from futures_then import ThenableFuture as Future
from jsonschema.exceptions import ValidationError

from superai.data_program.Exceptions import *
from superai.data_program.experimental import forget_memo
from superai.log import logger
from superai.utils import sentry_helper

sentry_helper.init()

logger = logger.get_logger(__name__)


class OperationStatus(str, enum.Enum):
    SUCCEEDED = "SUCCEEDED"
    FAILED = "FAILED"
    NO_SUITABLE_COMBINER = "NO_SUITABLE_COMBINER"
    TASK_EXPIRED = "TASK_EXPIRED"
    JOB_EXPIRED = "JOB_EXPIRED"


class WorkflowType(str, enum.Enum):
    WORKFLOW = "workflows"
    SUPER_TASK = "super-task-workflows"


# A message to the agent
# meta_info: contains the information about the attempted operation and other details on how to interpret the body.
# body: contains the actual output of the operation (e.g. job output)
class message:
    class metaInfo:
        def __init__(self, version, operation_status):
            self.version = version
            self.operation_status = operation_status.value

    def __init__(self, body=None, operation_status=OperationStatus.SUCCEEDED, version=0.1):
        self.meta_info = self.metaInfo(version, operation_status)
        self.body = body

    @property
    def to_json(self):
        return jsonpickle.encode(self, unpicklable=False)


class future(Future):
    def __init__(self):
        Future.__init__(self)
        self._cookie = None

    def set_cookie(self, cookie):
        self._cookie = cookie

    def cookie(self):
        return self._cookie


# Dictionary to store all local workflows
_workflow_functions = {}
_workflow_functions_lock = Lock()  # Lock to protect _workflow_callbacks logic

# Dictionary to store all futures
_task_futures = {}
_task_futures_lock = Lock()  # Lock to protect _task_dictionary logic

# Job input parameter
_job_input = {}
_job_input_data = {}
_job_input_lock = Lock()

# Job snapshot state
_snapshot = {}
_snapshot_data = {}
_snapshot_lock = Lock()

# Child job result
_child_job = {}
_child_job_lock = Lock()

_terminate_flag = {}
_terminate_flag_lock = Lock()

_pipe_lock = Lock()

# in-out fifo pipes for communication with Agent
_in_pipe = (
    io.open("/tmp/canotic.in." + os.environ["CANOTIC_AGENT"], "r", encoding="utf-8")
    if "CANOTIC_AGENT" in os.environ
    else None
)
_out_pipe = (
    io.open("/tmp/canotic.out." + os.environ["CANOTIC_AGENT"], "w", encoding="utf-8")
    if "CANOTIC_AGENT" in os.environ
    else None
)

_context = local()

if "CANOTIC_AGENT" in os.environ and "CANOTIC_SERVE" not in os.environ:
    _context.id = int(os.environ["CANOTIC_AGENT"])
    _context.uuid = os.environ["CANOTIC_AGENT"]
    _context.sequence = 0
    _context.bill = None
    _context.app_id = None
    _context.project_id = None
    _context.is_child = False
    _context.metadata = None
    _context.job_type = None

    with _task_futures_lock:
        _task_futures[_context.id] = {}
    with _job_input_lock:
        _job_input[_context.id] = future()
        _job_input_data[_context.id] = None
    with _snapshot_lock:
        _snapshot[_context.id] = None
        _snapshot_data[_context.id] = None
    with _child_job_lock:
        _child_job[_context.id] = None
    with _terminate_flag_lock:
        _terminate_flag[_context.id] = False


def terminate_guard(function):
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        with _terminate_flag_lock:
            if _terminate_flag[_context.id]:
                raise ValueError(f"Workflow instance {_context.id} terminated")
        return function(*args, **kwargs)

    return wrapper


def writeln_to_pipe_and_flush(text_data):
    try:
        print("Called by " + sys._getframe(1).f_code.co_name + " to pipe :" + text_data)
        _out_pipe.write(text_data)
    except TypeError as e:
        print(e)
        _out_pipe.write(unicode(text_data))
        sentry_sdk.capture_exception(e)
    except Exception as e:
        print(e)
        logger.exception("Exception writing text_data to pipe")
        sentry_sdk.capture_exception(e)

    try:
        try:
            _out_pipe.write("\n")
        except Exception as e:
            print(e)
            logger.exception("Exception writing \\n to pipe")
            sentry_sdk.capture_exception(e)
        finally:
            _out_pipe.flush()
    except BrokenPipeError as bp:
        sentry_sdk.capture_exception(bp)
        logger.exception(
            f"[BrokenPipeError] {str(bp)} \nfilename {bp.filename if bp.filename else None} \nfilename2 {bp.filename2 if bp.filename2 else None} \nstrerror {bp.strerror if bp.strerror else None}"
        )


class child_result:
    def __init__(self, result):
        self._id = result["id"] if "id" in result else None
        self._status = result["status"] if "status" in result else None
        self._response = result["response"] if "response" in result else None
        self._data_ref = result["dataRef"] if "dataRef" in result else None
        self._timestamp = result["timestamp"] if "timestamp" in result else None
        self._data = None

    @terminate_guard
    def id(self):
        return self._id

    @terminate_guard
    def status(self):
        return self._status

    @terminate_guard
    def response(self):
        return self._response

    @terminate_guard
    def timestamp(self):
        return self._timestamp

    @terminate_guard
    def data(self):
        if self._data is not None:
            return self._data.result()

        if self._data_ref is None:
            return None

        global _child_job
        self._data = _child_job[_context.id] = future()

        params = {
            "type": "LOAD_CHILD_DATA",
            "id": _context.id,
            "sequence": -1,
            "data": self._data_ref,
        }

        message_for_agent = message(params)

        with _pipe_lock:
            writeln_to_pipe_and_flush(message_for_agent.to_json)

        return self._data.result()

    @terminate_guard
    def __getitem__(self, key):
        if key == "timestamp":
            return self._timestamp

        raise ValueError(f"Expected 'timestamp' key, got {key}")


class child_job_future(future):
    def __init__(self):
        future.__init__(self)

    def set_result(self, response):
        super(child_job_future, self).set_result(child_result(response))


class task_result:
    def __init__(self, result):
        self._result = result

    @terminate_guard
    def id(self):
        return self._result["id"] if "id" in self._result else None

    @terminate_guard
    def status(self):
        return self._result["status"] if "status" in self._result else None

    @terminate_guard
    def hero(self):
        return self._result["workerId"] if "workerId" in self._result else None

    @terminate_guard
    def mturk_id(self):
        return self._result.get("hero", {}).get("mturkId")

    @terminate_guard
    def values(self):
        return self._result["values"] if "values" in self._result else None

    @terminate_guard
    def sequence(self):
        return self._result["sequence"] if "sequence" in self._result else None

    def task(self):
        return self.sequence()

    @terminate_guard
    def timestamp(self):
        return self._result["timestamp"] if "timestamp" in self._result else None

    @terminate_guard
    def __getitem__(self, key):
        return self._result[key]

    @terminate_guard
    def get(self, key):
        return self._result.get(key)

    @terminate_guard
    def response(self):
        return self._result


class task_future(future):
    def __init__(self):
        future.__init__(self)

    def set_result(self, response):
        super(task_future, self).set_result(task_result(response))


@terminate_guard
def schedule_task(
    name=None,
    humans=None,
    price=None,
    input=None,
    output=None,
    title=None,
    description=None,
    paragraphs=None,
    completed_tasks=None,
    total_tasks=None,
    includedIds=None,
    excludedIds=None,
    explicitId=None,
    timeToResolveSec=None,
    timeToUpdateSec=None,
    timeToExpireSec=None,
    qualifications=None,
    show_reject=None,
    groups=None,
    excluded_groups=None,
    amount=None,
    schema_version=None,
    is_ai=None,
    qualifier_test_id=None,
) -> task_future:
    """Schedules a task for execution by inserting it into the future table."""
    seq = _context.sequence
    _context.sequence += 1

    constraints = {}

    if humans is not None:
        constraints["emails"] = humans

    if price is not None:
        constraints["priceTag"] = price

    if amount is not None:
        constraints["amount"] = amount

    if excludedIds is not None:
        constraints["excluded"] = excludedIds

    if includedIds is not None:
        constraints["included"] = includedIds

    if excluded_groups is not None:
        constraints["excludedGroups"] = excluded_groups

    if groups is not None:
        constraints["groups"] = groups

    if explicitId is not None:
        constraints["id"] = explicitId

    if timeToResolveSec is not None:
        constraints["timeToResolve"] = 1000 * timeToResolveSec

    if timeToUpdateSec is not None:
        constraints["timeToUpdate"] = 1000 * timeToUpdateSec

    if timeToExpireSec is not None:
        constraints["timeToExpire"] = 1000 * timeToExpireSec

    if qualifications is not None:
        constraints["metrics"] = qualifications

    if qualifier_test_id is not None:
        constraints["qualifierTestId"] = qualifier_test_id

    if (amount is None) and (price is None):
        constraints["priceTag"] = "EASY"

    if is_ai:
        constraints["type"] = "AI"

    params = {
        "type": "EVALUATE_TASK",
        "id": _context.id,
        "sequence": seq,
        "name": name,
        # 'platform': 'CANOTIC',
        "constraints": constraints,
        "payload": {},
    }

    params["payload"]["schemaVersion"] = schema_version

    params["payload"]["input"] = input
    params["payload"]["output"] = output

    params["payload"]["taskInfo"] = {}
    params["payload"]["actions"] = {}

    if completed_tasks is not None:
        params["payload"]["taskInfo"]["completedTasks"] = completed_tasks

    if total_tasks is not None:
        params["payload"]["taskInfo"]["totalTasks"] = total_tasks

    if title is not None:
        params["payload"]["taskInfo"]["title"] = title

    if description is not None:
        params["payload"]["taskInfo"]["description"] = description

    if paragraphs is not None:
        params["payload"]["taskInfo"]["paragraphs"] = paragraphs

    params["payload"]["actions"]["showReject"] = show_reject

    f = None
    with _task_futures_lock:
        if seq not in _task_futures[_context.id]:
            _task_futures[_context.id][seq] = task_future()

        f = _task_futures[_context.id][seq]

    message_for_agent = message(params)

    with _pipe_lock:
        writeln_to_pipe_and_flush(message_for_agent.to_json)

    return f


def schedule_workflow(
    name,
    param,
    constraints,
    data_folder,
    tag,
    timeToExpireSec,
    suffix,
    app_metrics,
    app_params,
    metadata,
    super_task_params: Optional[dict] = None,
):
    """Schedules a task for execution by inserting it into the future table."""
    seq = _context.sequence
    _context.sequence += 1

    params = {
        "type": "EXECUTE_JOB",
        "id": _context.id,
        "sequence": seq,
        "workflow": name,
    }

    if suffix is not None:
        params["suffix"] = suffix

    if timeToExpireSec is not None:
        params["timeToExpire"] = 1000 * timeToExpireSec

    if param is not None:
        params["subject"] = param

    if data_folder is not None:
        params["data"] = data_folder

    if constraints is not None:
        params["constraints"] = constraints

    if tag is not None:
        params["tag"] = tag

    if metadata is not None:
        params["metadata"] = metadata

    # Set context for the workflow
    context = {}
    if app_params is not None or app_metrics is not None:
        context = {}
    if app_metrics is not None:
        context["app_metrics"] = app_metrics
    if app_params is not None:
        context["app_params"] = app_params
    if super_task_params is not None:
        context["super_tasks"] = super_task_params
    if context:
        params["context"] = context

    f = None
    with _task_futures_lock:
        if seq not in _task_futures[_context.id]:
            _task_futures[_context.id][seq] = child_job_future()

        f = _task_futures[_context.id][seq]

    message_for_agent = message(params)

    with _pipe_lock:
        writeln_to_pipe_and_flush(message_for_agent.to_json)

    return f


@terminate_guard
def resolve_job(response, data_folder, bill):
    """Resolves a job and persist the response."""
    seq = _context.sequence
    _context.sequence += 1

    params = {
        "type": "RESOLVE_JOB",
        "id": _context.id,
        "sequence": seq,
        "annotation": response,
    }

    if data_folder is not None:
        params["data"] = data_folder

    if bill is None:
        bill = _context.bill

    if bill is not None:
        params["bill"] = bill

    message_for_agent = message(params)

    with _pipe_lock:
        writeln_to_pipe_and_flush(message_for_agent.to_json)

    f = None
    with _task_futures_lock:
        if seq not in _task_futures[_context.id]:
            _task_futures[_context.id][seq] = future()

        f = _task_futures[_context.id][seq]

    f.result()


@terminate_guard
def suspend_job_for_no_combiner():
    """Suspends a job."""
    seq = _context.sequence
    _context.sequence += 1

    params = {"type": "SUSPEND_JOB", "id": _context.id, "sequence": seq}

    message_for_agent = message(params, OperationStatus.NO_SUITABLE_COMBINER)

    with _pipe_lock:
        writeln_to_pipe_and_flush(message_for_agent.to_json)

    f = None
    with _task_futures_lock:
        if seq not in _task_futures[_context.id]:
            _task_futures[_context.id][seq] = future()

        f = _task_futures[_context.id][seq]

    f.result()


@terminate_guard
def fail_job(error):
    """Fails a job."""
    print(error)
    seq = _context.sequence
    _context.sequence += 1

    params = {
        "type": "FAIL_JOB",
        "id": _context.id,
        "sequence": seq,
        "error": error,
    }

    message_for_agent = message(params)

    with _pipe_lock:
        writeln_to_pipe_and_flush(message_for_agent.to_json)

    f = None
    with _task_futures_lock:
        if seq not in _task_futures[_context.id]:
            _task_futures[_context.id][seq] = future()

        f = _task_futures[_context.id][seq]

    f.result()


@terminate_guard
def internal_error(error):
    """Fails a job."""
    print(error)
    seq = _context.sequence
    _context.sequence += 1

    params = {
        "type": "INTERNAL_ERROR",
        "id": _context.id,
        "sequence": seq,
        "error": error,
    }

    message_for_agent = message(params)

    with _pipe_lock:
        writeln_to_pipe_and_flush(message_for_agent.to_json)

    f = None
    with _task_futures_lock:
        if seq not in _task_futures[_context.id]:
            _task_futures[_context.id][seq] = future()

        f = _task_futures[_context.id][seq]

    f.result()


@terminate_guard
def expire_job(error):
    """Expires a job."""
    print(error)
    seq = _context.sequence
    _context.sequence += 1

    params = {
        "type": "EXPIRE_JOB",
        "id": _context.id,
        "sequence": seq,
        "error": error,
    }

    message_for_agent = message(params)

    with _pipe_lock:
        writeln_to_pipe_and_flush(message_for_agent.to_json)

    f = None
    with _task_futures_lock:
        if seq not in _task_futures[_context.id]:
            _task_futures[_context.id][seq] = future()

        f = _task_futures[_context.id][seq]

    f.result()


def _worklow_thread(id, suffix, response):
    _context.id = id
    _context.uuid = response["uuid"]
    _context.app_id = response.get("appId")
    _context.root_app_uuid = response.get("rootAppUuid")
    _context.project_id = response["projectId"]
    _context.is_child = response["child"]
    _context.sequence = 0
    _context.bill = None
    _context.metadata = response.get("metadata")
    _context.job_type = response.get("jobType") or None
    _context.priority = response.get("priority")

    with _task_futures_lock:
        _task_futures[_context.id] = {}
    with _job_input_lock:
        _job_input[_context.id] = future()
        _job_input[_context.id].set_result(response)
        _job_input_data[_context.id] = None
    with _snapshot_lock:
        _snapshot[_context.id] = None
        _snapshot_data[_context.id] = None
    with _child_job_lock:
        _child_job[_context.id] = None
    with _terminate_flag_lock:
        _terminate_flag[_context.id] = False

    try:
        subject = response["subject"] if "subject" in response else None
        context = response["context"] if "context" in response else None
        function = None
        with _workflow_functions_lock:
            if suffix not in _workflow_functions:
                raise ValueError(f"Unexpected suffix: {suffix}")
            function = _workflow_functions[suffix]
        result = function(subject, context)
        resolve_job(*result) if type(result) == tuple else resolve_job(result, None, None)
    except ValidationError as error:
        internal_error(f"\nSchema validation error: {error}")
        with sentry_sdk.push_scope() as scope:
            sentry_capture_fatal_exception(scope, id, response, error)
        logger.exception("ValidationError encountered in _workflow_thread")
    except concurrent.futures._base.CancelledError as error:
        logger.info(
            f"Job #{_context.uuid} of type {_context.job_type} cancelled or expired for app_id {_context.app_id}. error {str(error)}"
        )
    except CancelledError as error:
        logger.info(
            f"Job #{_context.uuid} of type {_context.job_type} cancelled or expired for app_id {_context.app_id}. error {str(error)}"
        )
    except ChildJobFailed as error:
        fail_job(f"FAIL_JOB: Job {_context.uuid} child failed")
        with sentry_sdk.push_scope() as scope:
            sentry_capture_fatal_exception(scope, id, response, error)
        logger.exception(
            f"Job #{_context.uuid} of type {_context.job_type} throw child job failed {_context.app_id}. error {str(error)}"
        )
    except QualifierTaskExpired as error:
        fail_job(f"FAIL_JOB :: {type(error)}: {error}")
        logger.info(f"Qualifier task expired for Job #{_context.uuid} of type {_context.job_type}. error {str(error)}")
    except TaskExpiredMaxRetries as error:
        logger.info(
            f"Task expired after maximum number of retries for Job #{_context.uuid} of type {_context.job_type}. error {str(error)}"
        )
        if (_context.job_type and _context.job_type == "COLLABORATOR") or response.get("jobType") == "COLLABORATOR":
            expire_job(f"\nEXPIRE_JOB :: {type(error)}: {error}")
            scope_level = WARN
        else:
            internal_error(f"\nINTERNAL_ERROR :: {type(error)}: {error}")
            scope_level = FATAL
        with sentry_sdk.push_scope() as scope:
            scope.set_tag("job_id", id)
            scope.set_tag("job_uuid", _context.uuid)
            scope.set_tag("app_id", _context.app_id)
            scope.set_tag("is_child", _context.is_child)
            scope.set_tag("job_type", _context.job_type or response.get("jobType"))
            scope.set_level(scope_level)
            sentry_sdk.capture_exception(error)
    except ChildJobInternalError as error:
        internal_error(f"INTERNAL_ERROR: Job {_context.uuid} child threw internal error")
        with sentry_sdk.push_scope() as scope:
            sentry_capture_fatal_exception(scope, id, response, error)
        logger.exception(
            f"Job #{_context.uuid} of type {_context.job_type} throw child job internal error {_context.app_id}. error {str(error)}"
        )
    except EmptyPerformanceError as error:
        internal_error(f"\n INTERNAL_ERROR :: {type(error)}: {error}")
        with sentry_sdk.push_scope() as scope:
            sentry_capture_fatal_exception(scope, id, response, error)
        logger.error("Performance not found exception")
    except UnsatisfiedMetricsError as error:
        suspend_job_for_no_combiner()
        with sentry_sdk.push_scope() as scope:
            scope.set_tag("job_id", id)
            scope.set_tag("job_uuid", _context.uuid)
            scope.set_tag("app_id", _context.app_id)
            scope.set_tag("is_child", _context.is_child)
            scope.set_tag("job_type", _context.job_type or response.get("jobType"))
            scope.set_level(WARN)
            sentry_sdk.capture_exception(error)
        logger.error(f"Unsatisfied metrics for job: #{_context.id}")
    except Exception as ex:
        internal_error(f"\nINTERNAL_ERROR :: {type(ex)}: {ex}")
        with sentry_sdk.push_scope() as scope:
            scope.set_tag("job_id", id)
            scope.set_tag("job_uuid", _context.uuid)
            scope.set_tag("app_id", _context.app_id)
            scope.set_tag("is_child", _context.is_child)
            scope.set_tag("job_type", _context.job_type or response.get("jobType"))
            scope.set_level(FATAL)
            sentry_sdk.capture_exception(ex)
        logger.exception("Exception encountered in _workflow_thread")
    finally:
        with _task_futures_lock:
            del _task_futures[_context.id]
        with _job_input_lock:
            del _job_input[_context.id]
            del _job_input_data[_context.id]
        with _snapshot_lock:
            del _snapshot[_context.id]
            del _snapshot_data[_context.id]
        with _child_job_lock:
            del _child_job[_context.id]
        with _terminate_flag_lock:
            del _terminate_flag[_context.id]

        del _context.id
        del _context.sequence
        del _context.bill


def sentry_capture_fatal_exception(scope, id, response, error):
    """Capture a fatal exception in sentry"""
    scope.set_tag("job_id", id)
    scope.set_tag("job_uuid", _context.uuid)
    scope.set_tag("app_id", response.get("appId"))
    scope.set_tag("is_child", _context.is_child)
    scope.set_tag("job_type", _context.job_type or response.get("jobType"))
    scope.set_level(FATAL)
    sentry_sdk.capture_exception(error)


def _task_pump():
    """This method waits for incoming response and resolves the corresponding task future."""
    while True:
        line = _in_pipe.readline().rstrip("\n")
        response = json.loads(line)
        if "type" not in response:
            raise ValueError("`type` is missing in response")

        if "id" not in response:
            raise ValueError("`id` is missing in response")

        id = response["id"]

        if response["type"] == "ERROR":
            kill_missing_error(response)
        elif response["type"] == "JOB_PARAMS":
            if "sequence" in response:
                raise ValueError("JOB_PARAMS come out of bound and don't expect to contain 'sequence'")

            job_input = None
            with _job_input_lock:
                job_input = _job_input[id]

            job_input.set_result(response)

        elif response["type"] == "JOB_DATA":
            if "sequence" in response:
                raise ValueError("JOB_DATA come out of bound and don't expect to contain 'sequence'")

            job_input_data = None
            with _job_input_lock:
                job_input_data = _job_input_data[id]

            job_input_data.set_result(response["data"] if "data" in response else None)

        elif response["type"] == "SNAPSHOT":
            snapshot = None
            with _snapshot_lock:
                snapshot = _snapshot[id]

            snapshot.set_result(response)

            if "sequence" in response:
                _context.sequence = response["sequence"]

        elif response["type"] == "SNAPSHOT_DATA":
            if "sequence" in response:
                raise ValueError("SNAPSHOT_DATA come out of bound and don't expect to contain 'sequence'")

            with _snapshot_lock:
                _snapshot_data[id]

            snapshot.set_result(response["data"] if "data" in response else None)

        elif response["type"] == "CHILD_JOB_DATA":
            if "sequence" in response:
                raise ValueError("CHILD_JOB_DATA come out of bound and don't expect to contain 'sequence'")

            child_job = None
            with _child_job_lock:
                child_job = _child_job[id]

            child_job.set_result(response["data"] if "data" in response else None)

        elif response["type"] == "EXECUTE":
            if "suffix" not in response:
                raise ValueError("Response `type` `EXECUTE` expects `suffix` property")

            suffix = response["suffix"]

            thread = Thread(
                target=_worklow_thread,
                name=f"{suffix}-{id}",
                args=(id, suffix, response),
            )
            thread.daemon = True
            thread.start()

        elif response["type"] in ["CANCEL", "SUSPEND"]:
            with _terminate_flag_lock:
                _terminate_flag[id] = True
            with _task_futures_lock:
                if id in _task_futures:
                    for seq in _task_futures[id]:
                        _task_futures[id][seq].cancel()
            with _job_input_lock:
                if id in _job_input:
                    _job_input[id].cancel()
                    if _job_input_data[id] is not None:
                        _job_input_data[id].cancel()
            with _snapshot_lock:
                if id in _snapshot:
                    if _snapshot[id] is not None:
                        _snapshot[id].cancel()
                    if _snapshot_data[id] is not None:
                        _snapshot_data[id].cancel()
            with _child_job_lock:
                if id in _child_job and _child_job[id] is not None:
                    _child_job[id].cancel()
            if response["type"] == "SUSPEND":
                job_uuid = response["uuid"]
                forget_memo(None, prefix=f"{job_uuid}/")

        else:
            if "sequence" not in response:
                raise ValueError("'sequence' expected in inbound message")

            seq = response["sequence"]
            f = None
            with _task_futures_lock:
                if id in _task_futures:
                    if seq not in _task_futures[id]:
                        if response["type"] == "CHILD_RESPONSE":
                            logger.warning(f"CHILD_RESPONSE:missing_child_job_future id {id} seq {seq}")
                            _task_futures[id][seq] = child_job_future()
                        else:
                            _task_futures[id][seq] = future()

                    f = _task_futures[id][seq]

            if f is None:
                sys.stderr.write(f"Unexpected id/sequence (late response?): {id}/{seq}\n")
                sys.stderr.flush()
            else:
                f.set_result(response)


def kill_missing_error(response):
    """Kill a thread which does not have error in response"""
    if "error" not in response:
        raise ValueError("Response `type` `ERROR` expects `error` property")

    sys.stderr.write("Traceback (most recent call last):\n")
    sys.stderr.write(response["error"])
    sys.stderr.write("\n")
    sys.stderr.flush()

    os.kill(os.getpid(), signal.SIGTERM)


if "CANOTIC_AGENT" in os.environ:
    _task_thread = Thread(target=_task_pump, name="pump")
    _task_thread.daemon = "CANOTIC_SERVE" not in os.environ
    _task_thread.start()


@terminate_guard
def get_job_data():
    """Get job data"""
    global _job_input_data
    global _job_input_lock

    job_input_data = None
    with _job_input_lock:
        if _job_input_data[_context.id] is not None:
            job_input_data = _job_input_data[_context.id]

    if job_input_data is not None:
        return job_input_data.result()

    with _job_input_lock:
        _job_input_data[_context.id] = job_input_data = future()

    params = {"type": "LOAD_JOB_DATA", "id": _context.id, "sequence": -1}

    message_for_agent = message(params)

    with _pipe_lock:
        writeln_to_pipe_and_flush(message_for_agent.to_json)

    return job_input_data.result()


@terminate_guard
def save_hero_qualification(hero, qualification, value):
    """Persists hero metric."""

    params = {
        "type": "STORE_METRIC",
        "id": _context.id,
        "sequence": -1,
        "hero": hero,
        "metric": qualification,
    }

    if value is not None:
        params["value"] = value

    message_for_agent = message(params)

    with _pipe_lock:
        writeln_to_pipe_and_flush(message_for_agent.to_json)


@terminate_guard
def remove_hero_qualification(hero, qualification):
    """Perist hero metric"""

    params = {
        "type": "REMOVE_METRIC",
        "id": _context.id,
        "hero": hero,
        "metric": qualification,
    }

    message_for_agent = message(params)

    with _pipe_lock:
        writeln_to_pipe_and_flush(message_for_agent.to_json)


@terminate_guard
def save_snapshot(snapshot, data_folder):
    seq = _context.sequence

    params = {
        "type": "SNAPSHOT",
        "id": _context.id,
        "sequence": seq,
        "snapshot": snapshot,
    }

    if data_folder is not None:
        params["data"] = data_folder

    message_for_agent = message(params)

    with _pipe_lock:
        writeln_to_pipe_and_flush(message_for_agent.to_json)


@terminate_guard
def load_snapshot():
    global _snapshot
    global _snapshot_lock

    snapshot = None
    with _snapshot_lock:
        if _snapshot[_context.id] is not None:
            snapshot = _snapshot[_context.id]

    if snapshot is not None:
        return snapshot.result()

    with _snapshot_lock:
        _snapshot[_context.id] = snapshot = future()

    params = {
        "type": "RESTORE_SNAPSHOT",
        "id": _context.id,
        "sequence": _context.sequence,
    }

    message_for_agent = message(params)

    with _pipe_lock:
        writeln_to_pipe_and_flush(message_for_agent.to_json)

    return snapshot.result()


@terminate_guard
def load_snapshot_data():
    global _snapshot_data
    global _snapshot_lock

    snapshot_data = None
    with _snapshot_lock:
        if _snapshot_data[_context.id] is not None:
            snapshot_data = _snapshot_data[_context.id]

    if snapshot_data is not None:
        return snapshot_data.result()

    with _snapshot_lock:
        _snapshot_data[_context.id] = snapshot_data = future()

    params = {"type": "LOAD_SNAPSHOT_DATA", "id": _context.id, "sequence": -1}

    message_for_agent = message(params)

    with _pipe_lock:
        writeln_to_pipe_and_flush(message_for_agent.to_json)

    return snapshot_data.result()


@terminate_guard
def send_report(status):
    params = {
        "type": "STORE_REPORT",
        "id": _context.id,
        "sequence": -1,
        "status": status,
    }

    message_for_agent = message(params)

    with _pipe_lock:
        writeln_to_pipe_and_flush(message_for_agent.to_json)


def subscribe_workflow(function, prefix, suffix, schema=None, workflow_type: Optional[WorkflowType] = None, **kwargs):
    """Subscribes a workflow.
    TODO: Add workflow_type support for websocket
    """
    if suffix is None:
        raise ValueError("Suffix is missing")

    with _workflow_functions_lock:
        _workflow_functions[suffix] = function

    params = {"type": "SUBSCRIBE", "suffix": suffix}

    if schema is not None:
        params["schema"] = schema

    if prefix is not None:
        params["workflow"] = prefix

    message_for_agent = message(params)

    with _pipe_lock:
        writeln_to_pipe_and_flush(message_for_agent.to_json)


@terminate_guard
def send_reward(task, amount, reason):
    """Give hero a reward"""
    if task is None:
        raise ValueError("Reward task is missing")

    if amount is None:
        raise ValueError("Reward amount is missing")

    params = {
        "type": "REWARD_HERO",
        "id": _context.id,
        "sequence": task,
        "amount": amount,
        "reason": reason,
    }

    message_for_agent = message(params)

    with _pipe_lock:
        writeln_to_pipe_and_flush(message_for_agent.to_json)


@terminate_guard
def decline_result(task, reason):
    if reason is None:
        raise ValueError("Decline reason is missing")

    params = {"type": "DECLINE", "id": _context.id, "sequence": task, "reason": reason}

    message_for_agent = message(params)

    with _pipe_lock:
        writeln_to_pipe_and_flush(message_for_agent.to_json)


@terminate_guard
def get_context_id():
    return _context.uuid


@terminate_guard
def get_job_id():
    return _context.id


@terminate_guard
def get_root_app_uuid():
    return _context.root_app_uuid if hasattr(_context, "root_app_uuid") else None


@terminate_guard
def get_job_priority():
    return _context.priority if hasattr(_context, "priority") else None


@terminate_guard
def get_context_app_id():
    return _context.app_id


@terminate_guard
def get_context_project_id():
    return _context.project_id


@terminate_guard
def get_context_is_child():
    return _context.is_child


@terminate_guard
def get_context_metadata():
    return _context.metadata


@terminate_guard
def get_context_job_type():
    return _context.job_type


@terminate_guard
def schedule_mtask(
    name,
    input,
    output,
    title,
    description,
    paragraphs,
    show_reject,
    amount,
    sandbox,
    timeToResolveSec=None,
    timeToExpireSec=None,
    qualifications=None,
):
    """Schedules a task for execution by inserting it into the future table."""
    seq = _context.sequence
    _context.sequence += 1

    constraints = {}

    if amount is not None:
        constraints["amount"] = amount

    if sandbox is not None:
        constraints["sandBox"] = sandbox

    if timeToResolveSec is not None:
        constraints["timeToResolve"] = 1000 * timeToResolveSec

    if timeToExpireSec is not None:
        constraints["timeToExpire"] = 1000 * timeToExpireSec

    if qualifications is not None:
        constraints["metrics"] = qualifications

    params = {
        "type": "EVALUATE_TASK",
        "id": _context.id,
        "sequence": seq,
        "name": name,
        "platform": "MTURK",
        "constraints": constraints,
        "payload": {},
    }

    params["payload"]["input"] = input
    params["payload"]["output"] = output

    params["payload"]["taskInfo"] = {}
    params["payload"]["actions"] = {}

    if title is not None:
        params["payload"]["taskInfo"]["title"] = title

    if description is not None:
        params["payload"]["taskInfo"]["description"] = description

    if paragraphs is not None:
        params["payload"]["taskInfo"]["paragraphs"] = paragraphs

    params["payload"]["actions"]["showReject"] = show_reject

    f = None
    with _task_futures_lock:
        if seq not in _task_futures[_context.id]:
            _task_futures[_context.id][seq] = task_future()

        f = _task_futures[_context.id][seq]

    message_for_agent = message(params)

    with _pipe_lock:
        writeln_to_pipe_and_flush(message_for_agent.to_json)

    return f


def start_threads():
    pass
