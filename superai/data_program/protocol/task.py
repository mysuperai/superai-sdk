"""Super.AI library to send task to human or AI."""
from __future__ import absolute_import, division, print_function, unicode_literals

import functools
import json
import logging
import os
import time
from concurrent.futures import ALL_COMPLETED, FIRST_COMPLETED, wait
from copy import deepcopy
from enum import Enum
from functools import wraps
from random import randint
from typing import Optional

import requests
import sentry_sdk
from genson import SchemaBuilder
from superai_dataclient import DataHelper
from superai_schema.universal_schema.data_types import (
    get_current_version_id,
    list_to_schema,
    validate,
)

from superai.data_program.experimental import memo
from superai.log import logger
from superai.utils import load_api_key, sentry_helper
from superai.utils.opentelemetry import tracer

from .transport_factory import (  # noqa # isort:skip
    get_context_app_id,
    get_context_id,
    get_context_is_child,
    get_context_job_type,
    get_context_metadata,
    get_context_project_id,
    get_context_simple_id,
    load_snapshot,
    load_snapshot_data,
    remove_hero_qualification,
    resolve_job,
    save_hero_qualification,
    save_snapshot,
    schedule_task,
    schedule_workflow,
    send_report,
    start_threads,
    subscribe_workflow,
    task_future,
    task_result,
)

logger = logger.get_logger(__name__)

sentry_helper.init()

CACHE_FOLDER = "tmp"


@tracer.start_as_current_span("task")
def task(
    input,
    output,
    humans=None,
    ai=False,
    ai_input=None,
    qualifications=None,
    name=None,
    price="default",
    title=None,
    description=None,
    paragraphs=None,
    completed_tasks=None,
    total_tasks=None,
    included_ids=None,
    excluded_ids=None,
    explicit_id=None,
    groups=None,
    excluded_groups=None,
    time_to_resolve_secs=None,
    time_to_update_secs=None,
    time_to_expire_secs=None,
    show_reject=False,
    amount=None,
    worker_type: Optional[str] = None,
    qualifier_test_id=None,
) -> task_future:
    """Routes task for labeling to one or more supervision sources.

    Args:
        input: A list of input semantic items.
        output: A list of output semantic items.
        humans: a list of crowd heroes email addresses
        ai: If True, the task will be sent to an AI. (superseded by worker_type)
        qualifications: List of required hero qualifications.
        name: Task type
        price: Price tag to be associated with the task.
        title: Task title.
        description: Task description.
        paragraphs: Task details.
        completed_tasks: A metadata placeholder to indicate the number of completed tasks.
        total_tasks: A metadata placeholder to indicate the number of total tasks.
        included_ids: A list of crowd hero IDs to be included.
        excluded_ids: A list of crowd hero IDs to be excluded.
        explicit_id: Direct the task to a specific hero ID.
        groups: A list of groups.
        excluded_groups: A list of excluded groups.
        time_to_resolve_secs: Time in seconds before the task is resolved (default: 0).
        time_to_update_secs: Time in seconds before the task is updated (default: 0).
        time_to_expire_secs: Time in seconds before the task will be expired (default: 0).
        show_reject: Show reject button.
        amount: Price to pay crowd heroes.
        worker_type: worker type to be used for the task
        qualifier_test_id: Id of the qualifier that needs to be passed to receive the task
    """
    # TODO(veselin): the number of parameters passed to this function is getting too long, we should organize it into class or dictionary
    if "CANOTIC_AGENT" in os.environ:
        return schedule_task(
            name=name,
            humans=humans,
            price=price,
            input=input,
            output=output,
            title=title,
            description=description,
            paragraphs=paragraphs,
            completed_tasks=completed_tasks,
            total_tasks=total_tasks,
            includedIds=included_ids,
            excludedIds=excluded_ids,
            explicitId=explicit_id,
            timeToResolveSec=time_to_resolve_secs,
            timeToUpdateSec=time_to_update_secs,
            timeToExpireSec=time_to_expire_secs,
            qualifications=qualifications,
            show_reject=show_reject,
            groups=groups,
            excluded_groups=excluded_groups,
            amount=amount,
            schema_version=get_current_version_id(),
            is_ai=ai,
            worker_type=worker_type,
            qualifier_test_id=qualifier_test_id,
        )
    else:
        raise NotImplementedError("Little piggy not supported")
        # lp.try_initialize()
        #
        # # Post a task to LittlePiggy.
        # r = lp.post_task(input, output, ai_input=ai_input, name=name, price=price)
        # # Wait until the future is completed.
        # return r


def execute(
    name,
    params=None,
    constraints=None,
    data_folder=None,
    tag=None,
    time_to_expire_secs=None,
    suffix=None,
    app_metrics=None,
    app_params=None,
    metadata=None,
    super_task_params: Optional[dict] = None,
):
    """Creates an instance of a workflow.

    Args:
        name: Name of the workflow from which to create the instance.
        params: Parameters as a dictionary to the workflow instance.
        constraints: A set of execution constraints to which you want to send the task, such as a list of emails, IDs, or groups
        data_folder: A data folder to be uploaded and accessed from the instance through canotic.request.data().
        tag: Workflow auxiliary tag.
        time_to_expire_secs: An expiration time in seconds.
    """
    if "CANOTIC_AGENT" in os.environ:
        return schedule_workflow(
            name,
            params,
            constraints,
            data_folder,
            tag,
            time_to_expire_secs,
            suffix,
            app_metrics,
            app_params,
            metadata,
            super_task_params=super_task_params,
        )

    return None


def get_job_id():
    """Returns:
    Job ID of current job. For little piggy, it always returns little piggy.
    """
    return get_context_id() if "CANOTIC_AGENT" in os.environ else "LITTLE_PIGGY"


def get_job_app():
    """Returns:
    The app ID of the current job. For little piggy, it always returns little piggy.
    """
    if "CANOTIC_AGENT" in os.environ:
        return get_context_app_id()
    else:
        return "LITTLE_PIGGY"


def get_job_project():
    """Returns:
    The project ID of current job. For little piggy, it always returns little piggy.
    """
    if "CANOTIC_AGENT" in os.environ:
        return get_context_project_id()
    else:
        return "LITTLE_PIGGY"


def retry(exceptions, tries=5, delay=1, backoff=2, logger=logging):
    """Retries calling the decorated function using an exponential backoff.

    Args:
        exceptions: The exception to check. may be a tuple of
            exceptions to check.
        tries: Number of times to try (not retry) before giving up.
        delay: Initial delay between retries in seconds.
        backoff: Backoff multiplier (e.g., value of 2 will double the delay
            each retry).
        logger: Logger to use. If None, print.
    """

    def deco_retry(f):
        @wraps(f)
        def f_retry(*args, **kwargs):
            logger.warning("DEPRECATED: Plase use superai.utils.retry")
            mtries, mdelay = tries, delay
            while mtries > 1:
                try:
                    return f(*args, **kwargs)
                except exceptions as e:
                    msg = f"{e}, Retrying {f} in {mdelay} seconds... {mtries} tries left"
                    if logger:
                        logger.warning(msg)
                    else:
                        print(msg)
                    time.sleep(mdelay)
                    mtries -= 1
                    mdelay *= backoff
            return f(*args, **kwargs)

        return f_retry  # true decorator

    return deco_retry


@retry(Exception)
def get_project_name(ID, endpoint_api_key=None, endpoint=None):
    """Gets the unique project name given the project ID.

    Args:
        ID: The project ID

    Returns:
        The project name.
    """
    url_format = "{}/admin/projects/{}"
    headers = {"x-api-key": endpoint_api_key}
    res = requests.get(url_format.format(endpoint, ID), headers=headers)
    if res.status_code == 200:
        records = res.json()
        return records["name"]
    else:
        logging.error(f"Failed to query project `{ID}`. Error: {res.json()}")
        return None


@retry(Exception)
def get_job_by_id(id, active=True, api_key=None, use_memo=False, endpoint_api_key=None, endpoint=None):
    """Gets a job by ID.

    Args:
        id:
        active: Default is True. # TODO: need to revisit @purnawirman
        api_key: Default is root API key # TODO: need to revisit @purnawirman
    """
    logger.warning("DEPRECATED: Will be removed in next version")

    def func():
        url_format = "{}/jobqueue/jobs/{}?apiKey={}"
        headers = {"x-api-key": endpoint_api_key}
        res = requests.get(
            url_format.format(endpoint, id, api_key),
            headers=headers,
        )
        if res.status_code == 200:
            records = res.json()
            return records
        else:
            logging.error(f"Failed to query job `{id}`. Error: {res.json()}")
            raise Exception(res.reason)

    if use_memo:
        return memo(
            lambda: func,
            f"{get_job_id()}/get_job_by_id/{id}_{active}",
        )
    return func()


def get_job_project_name():
    """Returns:
    The project ID of the current job. For little piggy, it always returns little piggy.
    """
    if "CANOTIC_AGENT" not in os.environ:
        return "LITTLE_PIGGY"
    pid = get_context_project_id()
    return get_project_name(pid)


def get_job_tag(api_key: str = None):
    """Returns:
    The current job tag number.
    """
    api_key = api_key or load_api_key()
    raise NotImplementedError("Fetching job tag is not supported")


def get_job_simple_id(api_key=None):
    """Returns:
    The current job ID.
    """
    if "CANOTIC_AGENT" in os.environ:
        job_id = get_context_simple_id()
        if job_id:
            return job_id
        else:
            logger.info(f"Failed to query job simple id `{get_job_id()}`.")
            raise RuntimeError(f"Failed to query job simple id `{get_job_id()}`.")
    else:
        return "LITTLE_PIGGY"


def get_metadata():
    """Returns:
    The job metadata.
    """
    if "CANOTIC_AGENT" in os.environ:
        return get_context_metadata()


def get_job_type():
    """Returns:
    The job type.
    """
    if "CANOTIC_AGENT" in os.environ:
        return get_context_job_type()


def is_job_child():
    """Returns:
    Whether the current job is a child job. For little piggy, it always returns False.
    """
    return get_context_is_child() if "CANOTIC_AGENT" in os.environ else False


def get_workflow_prefix():
    """Returns:
    The project ID of the current job. For little piggy, it always returns little piggy.
    """
    return os.environ["WF_PREFIX"] if "WF_PREFIX" in os.environ else "lp"


def store_snapshot(snapshot, data_folder=None):
    """TODO(veselin): add description"""
    if "CANOTIC_AGENT" in os.environ:
        return save_snapshot(snapshot, data_folder)

    return None


def auto_store_snapshot(var=None):
    if var is None:
        var = locals()
    if "CANOTIC_AGENT" in os.environ:
        new_var = {}
        for k, v in globals().items():
            try:
                json.dumps(k)
                json.dumps(v)
                new_var[k] = v
            except Exception as e:
                logger.error(e)
        return save_snapshot(new_var, None)
    return None


def auto_restore_snapshot():
    if "CANOTIC_AGENT" in os.environ:
        return (load_snapshot() or {}).get("snapshot", {})
    return None


def restore_snapshot():
    """TODO(veselin): add description"""
    if "CANOTIC_AGENT" in os.environ:
        snap = load_snapshot()
        if snap is not None and "snapshot" in snap:
            return snap["snapshot"]

    return None


def restore_snapshot_data():
    """TODO(veselin): add description"""
    return load_snapshot_data() if "CANOTIC_AGENT" in os.environ else None


def report(status):
    """TODO(veselin): add description"""
    if "CANOTIC_AGENT" in os.environ:
        return send_report(status)


def update_performance_database(performance):
    """TODO(purnawirman): too trivial to be in DS-SDK"""
    print(f"the model performance is {performance}")


def is_task_skipped(wf_task):
    """Checks if the task is rejected or skipped by labellers.

    Args:
        wf_task: Task, class Future.
    """
    return "values" not in wf_task.result()


def get_task_value(resp, idx=0):
    """Gets the value of a responded task.

    Args:
        resp: Response of a task.
        idx: Index of the response value.

    Returns:
        Response value of a task.
    """
    if "values" in resp:
        try:
            return deepcopy(resp["values"][idx].get("schema_instance"))
        except Exception as e:
            with sentry_sdk.push_scope() as scope:
                scope.set_tag("task_id", resp.get("id", None))
                sentry_sdk.capture_exception(e)
            print(e)
    return []


def get_task_type(resp, idx=0):
    """Gets type of a responded task.

    Args:
        resp: response of a task
        idx: index of the response value.

    Returns:
        The response type of a task.
    """
    if "values" in resp:
        try:
            return deepcopy(resp["values"][idx].get("type"))
        except Exception as e:
            with sentry_sdk.push_scope() as scope:
                scope.set_tag("task_id", resp.get("id", None))
                sentry_sdk.capture_exception(e)
            print(e)
    return []


@tracer.start_as_current_span("wait_tasks_OR")
def wait_tasks_OR(tasks, timeout=None):
    """Waits for a list of tasks until one of the tasks is completed. Idempotency safe.

    Args:
        tasks: A list of tasks to be waited for.
        timeout: The maximum wait time.

    Returns:
        Results contain done and not done tasks.
    """
    results = wait(tasks, timeout=timeout, return_when=FIRST_COMPLETED)

    # serialize by order of completion

    if not results.done:
        return results

    first = next(iter(results.done))
    for f in results.done:
        if f.result()["timestamp"] < first.result()["timestamp"]:
            first = f

    results.done.discard(first)
    results.not_done.update(results.done)
    results.done.clear()
    results.done.add(first)

    return results


@tracer.start_as_current_span("wait_tasks_AND")
def wait_tasks_AND(tasks, timeout=None):
    """Waits for list of tasks until all of the tasks are completed. Idempotency safe.

    Args:
        tasks: A list of tasks to be waited for.
        timeout: The maximum wait time.

    Returns:
        Results contain done and not done tasks.
    """
    return wait(tasks, timeout=timeout, return_when=ALL_COMPLETED)


def join_futures_array(array):
    """Combines all futures into one future.

    Args:
        array: A list of futures.

    Returns:
        The combined future.
    """
    f = array.pop()
    while array:
        f = array.pop().then(lambda x, next=f: next)

    return f


def join_futures(*args):
    """TODO(veselin): please add function description"""
    return join_futures_array(list(args))


def send_response(response=None, data_folder=None, bill=None):
    """Posts the response as a result of a job completion."""
    if "CANOTIC_AGENT" in os.environ:
        resolve_job(response, data_folder, bill)
    else:
        print(json.dumps(response))


def qualify(hero_item, metric, value=None):
    """Stores hero metric."""
    if "CANOTIC_AGENT" in os.environ:
        save_hero_qualification(hero_item, metric, value)
    else:
        print(f'set metric["{hero_item}"]["{metric}"]={value}')


def qualify_canotic(hero_id, metric, value=None):
    """Creates a qualification for canotic hero, of id `hero_id`, and metric name of `metric`. The value is float number."""
    qualify({"platform": "CANOTIC", "workerId": hero_id}, metric, value)


@retry(Exception, tries=10, delay=2)
def qualify_mturk(
    mturkId,
    metric,
    value=0,
    sandbox=False,
    owner_id=1,
    use_memo=False,
    endpoint_api_key: str = None,
    endpoint: str = None,
):
    # qualify({"platform": "MTURK", "workerId": hero_id}, metric, value)
    """"""
    assert isinstance(value, int), "Qualify MTURK only accept integer values"

    def func():
        url_format = "{}/admin/mturk/metricvalue?isSandbox={}&metricName={}&mturkId={}&ownerId={}&value={}"
        headers = {"x-api-key": endpoint_api_key}
        print(
            url_format.format(
                endpoint,
                sandbox,
                metric,
                mturkId,
                owner_id,
                value,
            )
        )
        res = requests.post(
            url_format.format(
                endpoint,
                sandbox,
                metric,
                mturkId,
                owner_id,
                value,
            ),
            headers=headers,
        )
        if res.status_code == 200:
            records = res.json()
            return records
        else:
            logging.error(
                "Failed to create qualification {} for mturk id {} in sandbox {} of value {}. "
                "Error: {}".format(metric, mturkId, sandbox, value, res.json())
            )
            raise Exception(res.reason)

    if use_memo:
        return memo(
            func,
            f"{get_job_id()}/qualify_mturk/{mturkId}_{metric}_{value}_{sandbox}",
        )
    return func()


def disqualify(hero_id, metric):
    """Deletes a hero metric."""
    if "CANOTIC_AGENT" in os.environ:
        remove_hero_qualification(hero_id, metric)
    else:
        print(f'delete metric["{hero_id}"]["{metric}"]')


@tracer.start_as_current_span("tasks_parallel")
def tasks_parallel(records, task_fn, concurrency=1, task_callback=None):
    """Executes tasks in parallel from the given input `records`.

    Input `records` format is unknown to this executor, and the executor's main responsibility is limited to scheduling
    the records by executing the `task_fn` callback defined as follows:

        task_fn(record, completed, total_tasks, price_tag='default', task_name=None, time_to_update_secs=None)

    where:

      `record`             : A record that contains information needed to execute a task.
      `completed`          : The number of tasks completed so far.
      `total_tasks`        : The total number of tasks to be completed.
      `price_tag`          : The price tag.
      `task_name`          : The name of the task.
      `time_to_update_secs`: The number of seconds the task is in the PENDING state before it gets RESOLVED.
    """
    tasks = []
    total_tasks = len(records)
    outstanding_task_count = 0
    completed = 0
    while completed < total_tasks:
        remaining_tasks = total_tasks - completed - outstanding_task_count
        logger.info(f"Completed: {completed}. Remaining Tasks: {remaining_tasks}. Total Tasks: {total_tasks}")
        for i in range(min(remaining_tasks, concurrency - outstanding_task_count)):
            index = completed + i + outstanding_task_count
            logger.info(f"INDEX: {index}")
            record = records[index]
            fn = task_fn(record, index, total_tasks)
            fn.set_cookie({"seq": index})
            tasks.append(fn)
        wait_result = wait_tasks_OR(tasks)
        outstanding_task_count = len(wait_result.not_done)
        tasks = list(wait_result.not_done)
        completed += len(wait_result.done)

        if task_callback:
            for t in wait_result.done:
                task_callback(t.cookie()["seq"], t.result())


@tracer.start_as_current_span("execute_parallel")
def execute_parallel(records, method_fn, concurrency=10, callback=None):
    """Executes a method that return future in parallel.

    Input `records` format is unknown to this executor, and the executor's main responsibility is limited to scheduling
    the records by executing the `method_fn` callback, which is defined as follows:

        method_fn(record) -> return future

    The execution is concurrent with size 'concurrency'.

    After execution, `callback` is invoked with the signature as follows:
        callback(sequence, t.result())
    where sequence is the sequence of the task being created,
    and t.result() is the result of the future invoked by method_fn.
    """
    import time

    tasks = []
    total_tasks = len(records)
    outstanding_task_count = 0
    completed = 0
    while completed < total_tasks:
        remaining_tasks = total_tasks - completed - outstanding_task_count
        logger.info(f"Completed: {completed}. Remaining Tasks: {remaining_tasks}. Total Tasks: {total_tasks}")
        print(f"Completed: {completed}. Remaining Tasks: {remaining_tasks}. Total Tasks: {total_tasks}")
        for i in range(min(remaining_tasks, concurrency - outstanding_task_count)):
            sTime = randint(1, 8)
            logger.debug(f"SLEEPING: {sTime} SECONDS")
            time.sleep(sTime)
            index = completed + i + outstanding_task_count
            logger.info(f"INDEX: {index}")
            record = records[index]
            fn = method_fn(record)
            fn.set_cookie({"seq": index})
            tasks.append(fn)
        wait_result = wait_tasks_OR(tasks)
        outstanding_task_count = len(wait_result.not_done)
        tasks = list(wait_result.not_done)
        completed += len(wait_result.done)

        if callback:
            for t in wait_result.done:
                callback(t.cookie()["seq"], t.result())


class WorkflowType(str, Enum):
    WORKFLOW = "workflows"
    SUPER_TASK = "super-task-workflows"


def serve_workflow(
    function, suffix=None, schema=None, prefix=None, workflow_type: Optional[WorkflowType] = WorkflowType.WORKFLOW
):
    """Register func as workflow."""
    if "CANOTIC_AGENT" in os.environ:
        if workflow_type is None:
            workflow_type = WorkflowType.WORKFLOW
        subscribe_workflow(
            function=function,
            prefix=prefix,
            suffix=suffix,
            schema=schema,
            workflow_type=workflow_type,
            api_key=load_api_key(),
        )


def schema_wrapper(subject, context, function, uses_new_schema: Optional[bool] = None):
    kwargs = {}

    # Validation needs to be skipped if schema without version is being in use
    # because input/output schema depends on app params.
    # In this case, DataProgram class is responsible for ensuring validity
    can_validate_input_output = _is_using_versioned_schema(uses_new_schema=uses_new_schema)

    if hasattr(function, "__input_param__"):
        (name, schema) = function.__input_param__
        if schema is not None and can_validate_input_output:
            logger.debug(f"SCHEMA NAME: {name}")
            logger.debug(f"VALIDATING SUBJECT: \n{subject} \nSCHEMA: \n{schema}")
            validate(subject, schema, validate_remote=True, client=DataHelper())
        kwargs[name] = subject

    app_params = context["app_params"] if context is not None and "app_params" in context else None
    logger.debug(f"APP_PARAMS\n{app_params}")
    if hasattr(function, "__app_params__"):
        logger.debug(f"__APP_PARAMS__\n{function.__app_params__}")
        for name in function.__app_params__:
            param = app_params[name] if app_params is not None and name in app_params else None
            schema = function.__app_params__[name]
            if schema is not None:
                logger.debug(f"VALIDATING {name}: PARAMS\n{param} \nSCHEMA\n{schema}")
                validate(param, schema, validate_remote=True, client=DataHelper())
            kwargs[name] = param

    # Passing down the super task params coming from the router job
    # The params are not validated until the super task is scheduled
    # The params will then be used as App Params and validated that way
    super_task_params = context["super_tasks"] if context is not None and "super_tasks" in context else None
    if super_task_params:
        logger.debug(f"SUPER_TASK_PARAMS\n{super_task_params}")
        kwargs["super_task_params"] = super_task_params

    app_metrics = context["app_metrics"] if context is not None and "app_metrics" in context else None
    logger.debug(f"APP_METRICS\n{app_metrics}")
    if hasattr(function, "__app_metrics__"):
        logger.debug(f"__APP_METRICS__\n{function.__app_metrics__}")
        for name in function.__app_metrics__:
            metric = app_metrics[name] if app_metrics is not None and name in app_metrics else None
            schema = function.__app_metrics__[name]
            if schema is not None:
                logger.debug(f"VALIDATING {name}: METRIC\n{metric} \nSCHEMA\n{schema}")
                validate(metric, schema, validate_remote=True, client=DataHelper())
            kwargs[name] = metric

    logger.debug(f"FUNCTION KWARGS = {kwargs}")
    f_output = function(subject) if not kwargs and subject is not None else function(**kwargs)

    if hasattr(function, "__output_param__") and can_validate_input_output:
        schema = function.__output_param__
        if type(f_output) == tuple:
            logger.debug(f"VALIDATING OUTPUT_VALS: \n{f_output[0]} \nSCHEMA: \n{schema}")
            validate(f_output[0], schema, validate_remote=True, client=DataHelper())
        else:
            validate(f_output, schema, validate_remote=True, client=DataHelper())
            logger.debug(f"VALIDATING OUTPUT_VALS: \n{f_output} \nSCHEMA: \n{schema}")

    return f_output


def _init_workflow_decorator(function, suffix, prefix):
    function.get_suffix = lambda: suffix
    function.get_prefix = lambda f=function: prefix
    function.get_input_param = lambda: function.__input_param__ if "__input_param__" in dir(function) else None
    function.get_output_param = lambda: function.__output_param__ if "__output_param__" in dir(function) else None
    function.get_app_params = lambda: function.__app_params__ if "__app_params__" in dir(function) else None
    function.get_app_metrics = lambda: function.__app_metrics__ if "__app_metrics__" in dir(function) else None
    function.get_example_data = lambda: function.__example_data__ if "__example_data__" in dir(function) else None


def workflow(suffix, prefix=None, workflow_type: Optional[WorkflowType] = None, uses_new_schema=None):
    def decorator(function):
        _init_workflow_decorator(function, suffix, prefix)

        @functools.wraps(function)
        def wrapper(
            params=None,
            constraints=None,
            data_folder=None,
            tag=None,
            time_to_expire_secs=None,
            app_params=None,
            app_metrics=None,
        ):
            return execute(
                name=None,
                params=params,
                constraints=constraints,
                data_folder=data_folder,
                tag=tag,
                time_to_expire_secs=time_to_expire_secs,
                suffix=suffix,
                app_params=app_params,
                app_metrics=app_metrics,
            )

        schema = {}
        if hasattr(function, "__input_param__"):
            (_, schema["input"]) = function.__input_param__
            logger.debug(f"SCHEMA INPUT\n{schema['input']}")

        if hasattr(function, "__output_param__"):
            schema["output"] = function.__output_param__
            logger.debug(f"SCHEMA OUTPUT\n{schema['output']}")

        if hasattr(function, "__app_params__"):
            schema["app_params"] = function.__app_params__
            logger.debug(f"APP PARAMS\n{schema['app_params']}")

            if hasattr(function, "__default_app_params__"):
                schema["default_app_params"] = function.__default_app_params__
                logger.debug(f"DEFAULT APP PARAMS\n{schema['default_app_params']}")

        if hasattr(function, "__app_metrics__"):
            schema["app_metrics"] = function.__app_metrics__
            logger.debug(f"APP METRICS\n{schema['app_metrics']}")

            if hasattr(function, "__default_app_metrics__"):
                schema["default_app_metrics"] = function.__default_app_metrics__
                logger.debug(f"DEFAULT APP METRICS\n{schema['default_app_metrics']}")

        if hasattr(function, "__example_data__"):
            schema["example"] = function.__example_data__
            logger.debug(f"EXAMPLE DATA\n{schema['example']}")

        def function(subject, params, f=function):
            logger.debug(f"FUNCTION_SUBJECT: {subject}")
            logger.debug(f"FUNCTION_PARAMS: {params}")
            logger.debug(f"FUNCTION_F: {f}")

            return schema_wrapper(subject, params, f, uses_new_schema=uses_new_schema)

        logger.debug(f"WORFLOW_function: {function}")
        logger.debug(f"WORFLOW_suffix: {suffix}")
        logger.debug(f"WORFLOW_schema: {schema}")
        logger.debug(f"WORFLOW_prefix: {prefix}")

        serve_workflow(function=function, suffix=suffix, schema=schema, prefix=prefix, workflow_type=workflow_type)
        return wrapper

    return decorator(suffix) if callable(suffix) else decorator


def _is_using_versioned_schema(uses_new_schema: Optional[bool] = None) -> bool:
    """The old schema is versioned. This function returns True if the new schema is not used."""
    return not uses_new_schema


def _parse_args(*args, uses_new_schema: Optional[bool] = None, **kwargs):
    """f(name=asdfs)
    f(name=sdfs, schema=sdfs)
    f(name=sdfs, schema=sdfs, default=sdfs)

    Args:
        uses_new_schema: Signals whether the new schema is used or not. Controls injection of schema version for legacy schema.
    """
    if len(args) > 1:
        raise ValueError("Decorator takes max 1 positional argument")

    if len(args) == len(kwargs) == 0:
        raise ValueError("At least one argument has to be passed to input decorator")

    f_args = {"schema": None, "default": None}
    if len(args) == 1:
        f_args["name"] = args[0]

    f_args.update(kwargs)

    if f_args["schema"] and _is_using_versioned_schema(uses_new_schema=uses_new_schema):
        f_args["schema"] = list_to_schema(f_args["schema"])
        f_args["schema"]["$schema"] = get_current_version_id()

    return f_args


def input_schema(*args, uses_new_schema: Optional[bool] = None, **kwargs):
    """Supported inputs in the form of:
    @input_schema("param_name") -> func(param_name) with schema=None
    @input_schema(name="param_name") -> same as last example
    @input_schema(name="param_name", schema=bundle(product=data_type.STRING)) -> func(param_name) with schema=bundle(product=data_type.STRING))
    """

    def decorator(function):
        dargs = _parse_args(*args, uses_new_schema=uses_new_schema, **kwargs)

        if "name" in dargs and "schema" in dargs:
            function.__input_param__ = (dargs["name"], dargs["schema"])

        logger.debug(f"INPUT DECORATOR: {function.__input_param__}")
        return function

    return decorator


def output_schema(*args, uses_new_schema: Optional[bool] = None, **kwargs):
    """TODO: Write appropriate docu

    Args:
        **kwargs

    Returns:

    """

    def decorator(function):
        dargs = _parse_args(*args, uses_new_schema=uses_new_schema, **kwargs)

        function.__output_param__ = dargs["schema"]
        logger.debug(f"OUTPUT DECORATOR: {function.__output_param__}")

        return function

    return decorator


def example(data):
    def decorator(function):
        function.__example_data__ = data
        return function

    return decorator


def param_schema(*args, uses_new_schema: Optional[bool] = None, **kwargs):
    def decorator(function):
        dargs = _parse_args(*args, uses_new_schema=uses_new_schema, **kwargs)

        if "name" in dargs and "schema" in dargs:
            if not hasattr(function, "__app_params__"):
                function.__app_params__ = {}

            function.__app_params__[dargs["name"]] = dargs["schema"]

            if "default" in dargs:
                if not hasattr(function, "__default_app_params__"):
                    function.__default_app_params__ = {}

                function.__default_app_params__[dargs["name"]] = dargs["default"]

        logger.debug(f"APP_PARAMS DECORATOR: {function.__app_params__} (default: {function.__default_app_params__})")

        return function

    return decorator


def metric_schema(*args, uses_new_schema: Optional[bool] = None, **kwargs):
    def decorator(function):
        dargs = _parse_args(*args, uses_new_schema=uses_new_schema, **kwargs)

        if "name" in dargs and "schema" in dargs:
            if not hasattr(function, "__app_metrics__"):
                function.__app_metrics__ = {}

            function.__app_metrics__[dargs["name"]] = dargs["schema"]

            if "default" in dargs:
                if not hasattr(function, "__default_app_metrics__"):
                    function.__default_app_metrics__ = {}

                function.__default_app_metrics__[dargs["name"]] = dargs["default"]

            logger.debug(f"APP_METRICS DECORATOR: {function.__app_metrics__}")

        return function

    return decorator


def schema(sample):
    b = SchemaBuilder()
    b.add_object(sample)

    return b.to_schema()


def export_data(json_output):
    os.makedirs(".canotic", exist_ok=True)
    folder = f".canotic/{get_job_id()}"
    filepath = f"{folder}/{get_job_id()}.json"
    os.makedirs(folder, exist_ok=True)
    json.dump(json_output, open(filepath, "w"))
    return folder


def start_threading(join=True):
    threads = start_threads()
    if threads and join:
        threads[0].join()
