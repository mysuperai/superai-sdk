""" superAi library to send task to Human or AI """
from __future__ import absolute_import, division, print_function, unicode_literals

import functools
import json
import logging
import os
import time
import warnings
from concurrent.futures import ALL_COMPLETED, FIRST_COMPLETED, wait
from copy import deepcopy
from functools import wraps
from random import randint

import requests
import sentry_sdk
from superai_schema.universal_schema.data_types import (
    get_current_version_id,
    list_to_schema,
    validate,
)
from superai_schema.universal_schema.task_schema_functions import text

# from canotic.ai import sagemaker_runtime as sm # TODO: Remove dependency
from colorama import Fore, Style
from genson import SchemaBuilder
from superai_dataclient.data_helper import DataHelper

from superai.config import settings
from superai.data_program.experimental import memo
from superai.log import logger
from superai.utils import load_api_key, sentry_helper

# from canotic.little_piggy import runtime as lp # TODO: Remove dependency

logger = logger.get_logger(__name__)

sentry_helper.init()

CACHE_FOLDER = "tmp"

if settings.backend == "qumes":
    from canotic.qumes_transport import (
        future,
        schedule_task,
        schedule_workflow,
        resolve_job,
        run_model_predict,
        load_snapshot,
        load_snapshot_data,
        save_snapshot,
        send_report,
        subscribe_workflow,
        attach_bill,
        send_reward,
        decline_result,
        save_hero_qualification,
        remove_hero_qualification,
        get_job_priority as job_priority,
        get_context_id,
        get_context_app_id,
        get_context_project_id,
        get_context_is_child,
        schedule_mtask,
        get_context_metadata,
        get_context_job_type,
        get_context_simple_id,
    )
else:
    from .transport import (
        attach_bill,
        decline_result,
        future,
        get_context_app_id,
        get_context_id,
        get_context_is_child,
        get_context_job_type,
        get_context_metadata,
        get_context_project_id,
        get_job_id as get_context_simple_id,
        get_job_priority as job_priority,
        load_snapshot,
        load_snapshot_data,
        remove_hero_qualification,
        resolve_job,
        run_model_predict,
        save_hero_qualification,
        save_snapshot,
        schedule_mtask,
        schedule_task,
        schedule_workflow,
        send_report,
        send_reward,
        subscribe_workflow,
    )


def task(
    input,
    output,
    humans=None,
    ai=None,
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
):
    """Routing task for annotations to one or more supervision sources
    :param input: a list of input semantic items
    :param output: a list of output semantic items
    :param humans: a list of crowd heroes email addresses
    :param ai: a canotic.ai object that exposes predict(ai_input) interface
    :param ai_input: input to the ai
    :param qualifications: list of required hero qualifications
    :param name: task type
    :param price: price tag to be associated with the task
    :param title: task title
    :param description: task description
    :param paragraphs: task details
    :param completed_tasks: a metadata placeholder to indicate the number of completed tasks
    :param total_tasks: a metadata placeholder to indicate the number of total tasks
    :param included_ids: a list of crowd hero ids to be included
    :param excluded_ids: a list of crowd hero ids to be excluded
    :param explicit_id: direct the task to specific hero id
    :param groups: a list of groups
    :param excluded_groups: a list of excluded groups
    :param time_to_resolve_secs: time in secs before the task is resolved (default: 0)
    :param time_to_update_secs: time in secs before the task is updated (default: 0)
    :param time_to_expire_secs: time in secs before the task will be expired (default: 0)
    :param show_reject: show reject button
    :param amount: price to pay crowd heroes
    :return:
    """
    # TODO(veselin): the number of parameters passed to this function is getting too long, we should organize it into class or dictionary
    if ai is not None:
        ai_output = ai.predict(ai_input)
        if ai_output is not None:
            f = future()
            # Flag to differentiate a machine vs human response.
            ai_output.update({"_ai_response": True})
            f.set_result(ai_output)
            print("Task was completed by Canotic meta-AI.")
            return f

    if "CANOTIC_AGENT" in os.environ:
        return schedule_task(
            name,
            humans,
            price,
            input,
            ai_input,
            output,
            title,
            description,
            paragraphs,
            completed_tasks,
            total_tasks,
            included_ids,
            excluded_ids,
            explicit_id,
            time_to_resolve_secs,
            time_to_update_secs,
            time_to_expire_secs,
            qualifications,
            show_reject,
            groups,
            excluded_groups,
            amount,
            get_current_version_id(),
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
):
    """
    Create an instance of a workflow
    :param name: name of the workflow to create the instance
    :param params: parameters as dictionary to the workflow instance
    :param constraints: a set of execution constraints such as a list of emails, ids, or groups to send task to
    :param data_folder: a data folder to be uploaded and accessed from the instance through canotic.request.data()
    :param tag: workflow auxiliary tag
    :param time_to_expire_secs: an expiration time in secs
    :return:
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
        )

    return None


def get_job_id():
    """
    :return: job id of current job, for little piggy, it always returns little piggy
    """
    if "CANOTIC_AGENT" in os.environ:
        return get_context_id()
    else:
        return "LITTLE_PIGGY"


def get_job_priority(api_key=None):
    """
    return job priority
    """
    if "CANOTIC_AGENT" in os.environ:
        priority = job_priority()
        if priority:
            return priority
        else:
            logger.info("Failed to query job priority `{}`.".format(get_job_id()))
            raise RuntimeError("Failed to query job priority id `{}`.".format(get_job_id()))
    else:
        return "LITTLE_PIGGY"


def get_job_app():
    """
    :return: app id of current job, for little piggy, it always returns little piggy
    """
    if "CANOTIC_AGENT" in os.environ:
        return get_context_app_id()
    else:
        return "LITTLE_PIGGY"


def get_job_project():
    """
    :return: project id of current job, for little piggy, it always returns little piggy
    """
    if "CANOTIC_AGENT" in os.environ:
        return get_context_project_id()
    else:
        return "LITTLE_PIGGY"


def retry(exceptions, tries=5, delay=1, backoff=2, logger=logging):
    """
    Retry calling the decorated function using an exponential backoff.

    Args:
        exceptions: The exception to check. may be a tuple of
            exceptions to check.
        tries: Number of times to try (not retry) before giving up.
        delay: Initial delay between retries in seconds.
        backoff: Backoff multiplier (e.g. value of 2 will double the delay
            each retry).
        logger: Logger to use. If None, print.
    """

    def deco_retry(f):
        @wraps(f)
        def f_retry(*args, **kwargs):
            logger.warning(Fore.LIGHTRED_EX + "DEPRECATED: Plase use superai.utils.retry" + Style.RESET_ALL)
            mtries, mdelay = tries, delay
            while mtries > 1:
                try:
                    return f(*args, **kwargs)
                except exceptions as e:
                    msg = "{}, Retrying {} in {} seconds... {} tries left".format(e, f, mdelay, mtries)
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
    """
    Get the unique project name given the project id
    :param ID: project id
    :return: project name
    """
    url_format = "{}/admin/projects/{}"
    headers = {"x-api-key": endpoint_api_key}
    res = requests.get(url_format.format(endpoint, ID), headers=headers)
    if res.status_code == 200:
        records = res.json()
        return records["name"]
    else:
        logging.error("Failed to query project `{}`. Error: {}".format(ID, res.json()))
        return None


@retry(Exception)
def get_job_by_id(id, active=True, api_key=None, use_memo=False, endpoint_api_key=None, endpoint=None):
    """
    Get job by id
    :param id:
    :param active: default is True # TODO: need to revisit @purnawirman
    :param api_key: default is root api key # TODO: need to revisit @purnawirman
    :return:
    """
    logger.warning(Fore.LIGHTRED_EX + "DEPRECATED: Will be removed in next version" + Style.RESET_ALL)

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
            logging.error("Failed to query job `{}`. Error: {}".format(id, res.json()))
            raise Exception(res.reason)

    if use_memo:
        return memo(
            lambda: func,
            "{}/{}/{}_{}".format(get_job_id(), "get_job_by_id", id, active),
        )
    return func()


def get_job_project_name():
    """
    :return: project id of current job, for little piggy, it always returns little piggy
    """
    if "CANOTIC_AGENT" in os.environ:
        pid = get_context_project_id()
        return get_project_name(pid)
    else:
        return "LITTLE_PIGGY"


def get_job_tag(api_key: str = None):
    """

    :return: current job tag #
    """
    api_key = api_key or load_api_key()
    raise NotImplementedError("Fetching job tag is not supported")


def get_job_simple_id(api_key=None):
    """

    :return: current job id #
    """
    if "CANOTIC_AGENT" in os.environ:
        job_id = get_context_simple_id()
        if job_id:
            return job_id
        else:
            logger.info("Failed to query job simple id `{}`.".format(get_job_id()))
            raise RuntimeError("Failed to query job simple id `{}`.".format(get_job_id()))
    else:
        return "LITTLE_PIGGY"


def get_metadata():
    """
    :return: Job Metadata
    """
    if "CANOTIC_AGENT" in os.environ:
        return get_context_metadata()


def get_job_type():
    """
    :return: Job Type
    """
    if "CANOTIC_AGENT" in os.environ:
        return get_context_job_type()


def is_job_child():
    """
    :return: if current job is child, for little piggy, it always returns False
    """
    if "CANOTIC_AGENT" in os.environ:
        return get_context_is_child()
    else:
        return False


def get_workflow_prefix():
    """
    :return: project id of current job, for little piggy, it always returns little piggy
    """
    if "WF_PREFIX" in os.environ:
        return os.environ["WF_PREFIX"]
    else:
        return "lp"


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
        if snap is not None:
            if "snapshot" in snap:
                return snap["snapshot"]

    return None


def restore_snapshot_data():
    """TODO(veselin): add description"""
    if "CANOTIC_AGENT" in os.environ:
        return load_snapshot_data()

    return None


def report(status):
    """TODO(veselin): add description"""
    if "CANOTIC_AGENT" in os.environ:
        return send_report(status)


def update_performance_database(performance):
    """TODO(purnawirman): too trivial to be in DS-SDK"""
    print("the model performance is {}".format(performance))


def is_task_skipped(wf_task):
    """
    Check if the task is rejected/skipped by labellers.
    :param wf_task: task, class Future
    :return:
    """
    return "values" not in wf_task.result()


def get_task_value(resp, idx=0):
    """
    Get value of a responded task
    :param resp: response of a task
    :param idx: index of the response value
    :return: response value of a task
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
    """
    Get type of a responded task
    :param resp: response of a task
    :param idx: index of the response value
    :return: response type of a task
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


def wait_tasks_OR(tasks, timeout=None):
    """
    Wait for list of tasks until one of the tasks is completed, idempotency safe.
    :param tasks: list of tasks to be wait
    :param timeout: maximum wait time
    :return: results contain done and not done tasks
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


def wait_tasks_AND(tasks, timeout=None):
    """
    Wait for list of tasks until all of the tasks are completed, idempotency safe.
    :param tasks: list of tasks to be wait
    :param timeout: maximum wait time
    :return: results contain done and not done tasks
    """
    return wait(tasks, timeout=timeout, return_when=ALL_COMPLETED)


def join_futures_array(array):
    """
    Combine all futures into one future
    :param array: list of futures
    :return: combined future
    """
    f = array.pop()
    while array:
        f = array.pop().then(lambda x, next=f: next)

    return f


def join_futures(*args):
    """TODO(veselin): please add function description"""
    return join_futures_array(list(args))


def send_response(response=None, data_folder=None, bill=None):
    """Post response as a result of a job completion"""
    if "CANOTIC_AGENT" in os.environ:
        resolve_job(response, data_folder, bill)
    else:
        print(json.dumps(response))


def qualify(hero_item, metric, value=None):
    """Store hero metric"""
    if "CANOTIC_AGENT" in os.environ:
        save_hero_qualification(hero_item, metric, value)
    else:
        print('set metric["{}"]["{}"]={}'.format(hero_item, metric, value))


def qualify_canotic(hero_id, metric, value=None):
    """
    Create a qualification for canotic hero, of id `hero_id`, and metric name of `metric`. The value is float number.
    """
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
    """ """
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
            "{}/{}/{}_{}_{}_{}".format(get_job_id(), "qualify_mturk", mturkId, metric, value, sandbox),
        )
    return func()


def disqualify(hero_id, metric):
    """Delete hero metric"""
    if "CANOTIC_AGENT" in os.environ:
        remove_hero_qualification(hero_id, metric)
    else:
        print('delete metric["{}"]["{}"]'.format(hero_id, metric))


def serve_predict(predict_func, port=8080, context=None, use_sagemaker=True):
    """Register the predict_func as the prediction handler and start prediction service by listening to the port

    If use_sagemaker flag is set, create prediction endpoint on sagemaker fabric.
    """
    if use_sagemaker:
        # sm.serve_predict(predict_func, context, port=port)
        raise NotImplementedError("Sagemaker deploy is not implemented")
    else:
        run_model_predict(predict_func, port=port, context=context)


def tasks_parallel(records, task_fn, concurrency=1, task_callback=None):
    """Execute tasks in parallel from the given input `records`.

    Input `records` format is unknown to this executor, and the executor main responsibility is limited to scheduling
    the records by executing the `task_fn` callback defined as follows:

        task_fn(record, completed, total_tasks, price_tag='default', task_name=None, time_to_update_secs=None)

    where,
      `record`             : a record that contains information needed to execute a task
      `completed`          : the number of tasks completed so far
      `total_tasks`        : total number of tasks to be completed
      `price_tag`          : price tag
      `task_name`          : name of the task
      `time_to_update_secs`: number of seconds the tasks in PENDING state before it gets RESOLVED.
    """
    tasks = []
    total_tasks = len(records)
    outstanding_task_count = 0
    completed = 0
    while completed < total_tasks:
        remaining_tasks = total_tasks - completed - outstanding_task_count
        logger.info(
            "Completed: {}. Remaining Tasks: {}. Total Tasks: {}".format(completed, remaining_tasks, total_tasks)
        )
        for i in range(0, min(remaining_tasks, concurrency - outstanding_task_count)):
            index = completed + i + outstanding_task_count
            logger.info("INDEX: {}".format(index))
            record = records[index]
            fn = task_fn(record, index, total_tasks)
            fn.set_cookie({"seq": index})
            tasks.append(fn)
        wait_result = wait_tasks_OR(tasks)
        outstanding_task_count = len(wait_result.not_done)
        tasks = []
        for t in wait_result.not_done:
            tasks.append(t)
        completed += len(wait_result.done)

        if task_callback:
            for t in wait_result.done:
                task_callback(t.cookie()["seq"], t.result())


def execute_parallel(records, method_fn, concurrency=10, callback=None):
    """Execute a method that return future in parallel

    Input `records` format is unknown to this executor, and the executor main responsibility is limited to scheduling
    the records by executing the `method_fn` callback defined as follows:

        method_fn(record) -> return future

    The execution is concurrent with size 'concurrency'

    After execution, `callback` is invoked with the signature as follow:
        callback(sequence, t.result())
    where sequence is the sequence of the task being created,
    and t.result() is the result of the future invoked by method_fn
    """
    import time

    tasks = []
    total_tasks = len(records)
    outstanding_task_count = 0
    completed = 0
    while completed < total_tasks:
        remaining_tasks = total_tasks - completed - outstanding_task_count
        logger.info(
            "Completed: {}. Remaining Tasks: {}. Total Tasks: {}".format(completed, remaining_tasks, total_tasks)
        )
        print("Completed: {}. Remaining Tasks: {}. Total Tasks: {}".format(completed, remaining_tasks, total_tasks))
        for i in range(0, min(remaining_tasks, concurrency - outstanding_task_count)):
            sTime = randint(1, 8)
            logger.debug("SLEEPING: {} SECONDS".format(sTime))
            time.sleep(sTime)
            index = completed + i + outstanding_task_count
            logger.info("INDEX: {}".format(index))
            record = records[index]
            fn = method_fn(record)
            fn.set_cookie({"seq": index})
            tasks.append(fn)
        wait_result = wait_tasks_OR(tasks)
        outstanding_task_count = len(wait_result.not_done)
        tasks = []
        for t in wait_result.not_done:
            tasks.append(t)
        completed += len(wait_result.done)

        if callback:
            for t in wait_result.done:
                callback(t.cookie()["seq"], t.result())


def task_from_semantic_ui(
    record,
    completed,
    total_tasks,
    price_tag="default",
    task_name=None,
    ai=None,
    ai_input=None,
    time_to_update_secs=None,
):
    """Dispatch a task from Semantic UI record
    {
        "name": [...],
        "input": [...],
        "output": [...]
        "response": [...]
    }
    """
    # Merge the response to output
    if record.get("response"):
        for i in range(0, len(record["output"])):
            record["output"][i]["value"] = record["response"][i]["value"]

    r = task(
        input=record["input"],
        output=record["output"],
        ai=ai,
        ai_input=ai_input,
        name=record["name"] if task_name is None else task_name,
        price=price_tag,
        completed_tasks=completed,
        total_tasks=total_tasks,
        time_to_update_secs=time_to_update_secs,
    )
    return r


def get_all_metrics(metric, owner="1"):
    """TODO(purna): this should be part of the canotic.metrics and implemented through a proper key value store API lookup"""
    warnings.warn("this is either a workaround or hack")
    url = (
        "https://prometheus-nlb-prod-internal-b5f0c5af90c09892.elb.us-east-1.amazonaws.com"
        + "/resource/workers/metrics/{}/{}".format(owner, metric)
    )
    HEADERS = {"accept": "*/*", "Content-Type": "application/json"}
    r = requests.get(url, headers=HEADERS)
    return r.content


def serve_workflow(function, suffix=None, schema=None, prefix=None):
    """Register func as workflow"""
    if "CANOTIC_AGENT" in os.environ:
        subscribe_workflow(function=function, prefix=prefix, suffix=suffix, schema=schema)


def schema_wrapper(subject, context, function):
    kwargs = {}
    if hasattr(function, "__input_param__"):
        (name, schema) = function.__input_param__
        if schema is not None:
            logger.debug("SCHEMA NAME: {}".format(name))
            logger.debug("VALIDATING SUBJECT: \n{} \nSCHEMA: \n{}".format(subject, schema))
            validate(subject, schema, validate_remote=True, client=DataHelper())
        kwargs[name] = subject

    app_params = context["app_params"] if context is not None and "app_params" in context else None
    logger.debug("APP_PARAMS\n{}".format(app_params))
    if hasattr(function, "__app_params__"):
        logger.debug("__APP_PARAMS__\n{}".format(function.__app_params__))
        for name in function.__app_params__:
            param = app_params[name] if app_params is not None and name in app_params else None
            schema = function.__app_params__[name]
            if schema is not None:
                logger.debug("VALIDATING {}: PARAMS\n{} \nSCHEMA\n{}".format(name, param, schema))
                validate(param, schema, validate_remote=True, client=DataHelper())
            kwargs[name] = param

    app_metrics = context["app_metrics"] if context is not None and "app_metrics" in context else None
    logger.debug("APP_METRICS\n{}".format(app_metrics))
    if hasattr(function, "__app_metrics__"):
        logger.debug("__APP_METRICS__\n{}".format(function.__app_metrics__))
        for name in function.__app_metrics__:
            metric = app_metrics[name] if app_metrics is not None and name in app_metrics else None
            schema = function.__app_metrics__[name]
            if schema is not None:
                logger.debug("VALIDATING {}: METRIC\n{} \nSCHEMA\n{}".format(name, metric, schema))
                validate(metric, schema, validate_remote=True, client=DataHelper())
            kwargs[name] = metric

    logger.debug("FUNCTION KWARGS = {}".format(kwargs))
    f_output = function(subject) if 0 == len(kwargs) and subject is not None else function(**kwargs)

    if hasattr(function, "__output_param__"):
        schema = function.__output_param__
        if type(f_output) == tuple:
            logger.debug("VALIDATING OUTPUT_VALS: \n{} \nSCHEMA: \n{}".format(f_output[0], schema))
            validate(f_output[0], schema, validate_remote=True, client=DataHelper())
        else:
            validate(f_output, schema, validate_remote=True, client=DataHelper())
            logger.debug("VALIDATING OUTPUT_VALS: \n{} \nSCHEMA: \n{}".format(f_output, schema))

    return f_output


def _init_workflow_decorator(function, suffix, prefix):
    function.get_suffix = lambda: suffix
    function.get_prefix = lambda f=function: prefix
    function.get_input_param = lambda: function.__input_param__ if "__input_param__" in dir(function) else None
    function.get_output_param = lambda: function.__output_param__ if "__output_param__" in dir(function) else None
    function.get_app_params = lambda: function.__app_params__ if "__app_params__" in dir(function) else None
    function.get_app_metrics = lambda: function.__app_metrics__ if "__app_metrics__" in dir(function) else None
    function.get_example_data = lambda: function.__example_data__ if "__example_data__" in dir(function) else None


def workflow(suffix, prefix=None):
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
            logger.debug("SCHEMA INPUT\n{}".format(schema["input"]))

        if hasattr(function, "__output_param__"):
            schema["output"] = function.__output_param__
            logger.debug("SCHEMA OUTPUT\n{}".format(schema["output"]))

        if hasattr(function, "__app_params__"):
            schema["app_params"] = function.__app_params__
            logger.debug("APP PARAMS\n{}".format(schema["app_params"]))

        if hasattr(function, "__app_metrics__"):
            schema["app_metrics"] = function.__app_metrics__
            logger.debug("APP METRICS\n{}".format(schema["app_metrics"]))

        if hasattr(function, "__example_data__"):
            schema["example"] = function.__example_data__
            logger.debug("EXAMPLE DATA\n{}".format(schema["example"]))

        def function(subject, params, f=function):
            logger.debug("FUNCTION_SUBJECT: {}".format(subject))
            logger.debug("FUNCTION_PARAMS: {}".format(params))
            logger.debug("FUNCTION_F: {}".format(f))

            return schema_wrapper(subject, params, f)

        logger.debug("WORFLOW_function: {}".format(function))
        logger.debug("WORFLOW_suffix: {}".format(suffix))
        logger.debug("WORFLOW_schema: {}".format(schema))
        logger.debug("WORFLOW_prefix: {}".format(prefix))

        serve_workflow(function=function, suffix=suffix, schema=schema, prefix=prefix)
        return wrapper

    return decorator(suffix) if callable(suffix) else decorator


def _parse_args(*args, **kwargs):
    """
    f(name=asdfs)
    f(name=sdfs, schema=sdfs)
    """
    if len(args) > 1:
        raise ValueError("Decorator takes max 1 positional argument")

    if len(args) == len(kwargs) == 0:
        raise ValueError("At least one argument has to be passed to input decorator")

    f_args = dict()
    f_args["schema"] = None

    if len(args) == 1:
        f_args["name"] = args[0]

    f_args.update(kwargs)
    if f_args["schema"]:
        f_args["schema"] = list_to_schema(f_args["schema"])
        f_args["schema"]["$schema"] = get_current_version_id()

    return f_args


def input_schema(*args, **kwargs):
    """
    Supported inputs in the form of:
    @input_schema("param_name") -> func(param_name) with schema=None
    @input_schema(name="param_name") -> same as last example
    @input_schema(name="param_name", schema=bundle(product=data_type.STRING)) -> func(param_name) with schema=bundle(product=data_type.STRING))
    """

    def decorator(function):
        dargs = _parse_args(*args, **kwargs)

        if "name" in dargs and "schema" in dargs:
            function.__input_param__ = (dargs["name"], dargs["schema"])

        logger.debug("INPUT DECORATOR: {}".format(function.__input_param__))
        return function

    return decorator


def output_schema(*args, **kwargs):
    """
    TODO: Write appropriate docu

    :param kwargs:
    :return:
    """

    def decorator(function):
        dargs = _parse_args(*args, **kwargs)

        function.__output_param__ = dargs["schema"]
        logger.debug("OUTPUT DECORATOR: {}".format(function.__output_param__))

        return function

    return decorator


def example(data):
    def decorator(function):
        function.__example_data__ = data
        return function

    return decorator


def param_schema(*args, **kwargs):
    def decorator(function):
        dargs = _parse_args(*args, **kwargs)

        if "name" in dargs and "schema" in dargs:
            if not hasattr(function, "__app_params__"):
                function.__app_params__ = {}

            function.__app_params__[dargs["name"]] = dargs["schema"]

        logger.debug("APP_PARAMS DECORATOR: {}".format(function.__app_params__))

        return function

    return decorator


def metric_schema(*args, **kwargs):
    def decorator(function):
        dargs = _parse_args(*args, **kwargs)

        if "name" in dargs and "schema" in dargs:
            if not hasattr(function, "__app_metrics__"):
                function.__app_metrics__ = {}

            function.__app_metrics__[dargs["name"]] = dargs["schema"]

            logger.debug("APP_METRICS DECORATOR: {}".format(function.__app_metrics__))

        return function

    return decorator


def schema(sample):
    b = SchemaBuilder()
    b.add_object(sample)

    return b.to_schema()


def reward(task, amount, reason=None):
    if "CANOTIC_AGENT" in os.environ:
        send_reward(task, amount, reason)


def decline(task, reason):
    if "CANOTIC_AGENT" in os.environ:
        decline_result(task, reason)


def bill(amount):
    if "CANOTIC_AGENT" in os.environ:
        attach_bill(amount)


def export_data(json_output):
    os.makedirs(".canotic", exist_ok=True)
    folder = ".canotic/{}".format(get_job_id())
    filepath = "{}/{}.json".format(folder, get_job_id())
    os.makedirs(folder, exist_ok=True)
    json.dump(json_output, open(filepath, "w"))
    return folder


def mtask(
    input,
    output,
    name=None,
    qualifications=None,
    title=None,
    description=None,
    amount=None,
    paragraphs=None,
    show_reject=True,
    sandbox=None,
    timeToResolveSec=None,
    timeToExpireSec=None,
):
    """Routing task for annotations to one or more supervision sources
    :param input: a list of input semantic items
    :param output: a list of output semantic items
    :param name: task type
    :param price: price tag to be associated with the task
    :param title: task title
    :param description: task description
    :param paragraphs: task details
    :param show_reject: show reject button
    :param amount: price to pay crowd heroes
    :param sandbox: send to sandbox for debug
    :param timeToResolveSec: time in second for mturk to resolve the task once they accept it
    :param timeToExpireSec: time in second for the task to expire from its creation
    :return:
    """
    if "CANOTIC_AGENT" in os.environ:
        return schedule_mtask(
            name,
            input,
            output,
            title,
            description,
            paragraphs,
            show_reject,
            amount,
            sandbox,
            timeToResolveSec,
            timeToExpireSec,
            qualifications,
        )


def urgent_task(
    input,
    output,
    humans=None,
    ai=None,
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
):
    input = [text("**URGENT TASK**")] + input
    return task(
        input,
        output,
        humans=humans,
        ai=ai,
        ai_input=ai_input,
        qualifications=qualifications,
        name=name,
        price=price,
        title=title,
        description=description,
        paragraphs=paragraphs,
        completed_tasks=completed_tasks,
        total_tasks=total_tasks,
        included_ids=included_ids,
        excluded_ids=excluded_ids,
        explicit_id=explicit_id,
        groups=groups,
        excluded_groups=excluded_groups,
        time_to_resolve_secs=time_to_resolve_secs,
        time_to_update_secs=time_to_update_secs,
        time_to_expire_secs=time_to_expire_secs,
        show_reject=show_reject,
        amount=amount,
    )
