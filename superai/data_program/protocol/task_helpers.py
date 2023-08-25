import superai_schema.universal_schema.task_schema_functions as df

from superai.data_program.combiner.agreement_scores import (
    agreement_basic,
    agreement_exclusive_choice,
    agreement_multiple_choice,
)
from superai.data_program.combiner.combiner_functions import (
    basic_majority,
    exclusive_choice_majority,
    multiple_choice_majority,
)
from superai.data_program.Exceptions import (
    TaskExpiredMaxRetries,
    UnexpectedDataType,
    UnknownTaskStatus,
)
from superai.data_program.protocol.task import (
    get_task_type,
    get_task_value,
    task,
    task_future,
    task_result,
)
from superai.log import logger

log = logger.get_logger(__name__)


def resend_task(
    task_inputs,
    task_outputs,
    task_expiry_time,
    n_resend,
    task_name,
    qualifications=None,
    groups=None,
    excluded_ids=None,
    show_reject=False,
    amount=None,
    task_price=None,
):
    for n_tries in range(n_resend):
        future = task(
            input=task_inputs,
            output=task_outputs,
            name=task_name,
            price=task_price,
            qualifications=qualifications,
            groups=groups,
            time_to_expire_secs=task_expiry_time,
            excluded_ids=excluded_ids,
            show_reject=show_reject,
            amount=amount,
        )
        if not isinstance(future, task_future):
            log.warning(f"Task_future object={future} is of type={type(future)}, expected='task_future'")
        result = future.result()
        if not isinstance(result, task_result):
            log.warning(f"Task_result object={result} is of type={type(result)}, expected='task_result'")
        if result.status() == "COMPLETED":
            log.info("task succeeded")
            getter = getattr(result.response(), "get", None)
            if callable(getter) and len(getter("values", [])) > 0:
                return result
            log.warning("completed task, but empty task response.")
            log.info(f"resending task, trial no. {n_tries + 1}")
        elif result.status() in ["EXPIRED", "REJECTED"]:
            log.info(f"resending task, trial no. {n_tries + 1}")
        else:
            raise UnknownTaskStatus(str(result.status()))
    raise TaskExpiredMaxRetries(f"No crowd hero responded to task after {str(n_resend)} retries.")


def multiple_hero_task(num_heroes=1, agreement_score=True, **resend_task_kwargs):
    sent_heroes = []
    responses = []
    for _ in range(num_heroes):
        result = resend_task(excluded_ids=sent_heroes, **resend_task_kwargs)
        responses.append(result.response())
        sent_heroes.append(result.hero())
    if agreement_score:
        return task_combiner(responses, agreement_score=True)
    else:
        return task_combiner(responses, agreement_score=False)


def task_combiner(responses, agreement_score=True):
    n_fields = len(responses[0]["values"])
    responses_out = []
    scores = []
    for nf in range(n_fields):
        field_type = get_task_type(responses[0], nf)
        if field_type == "structured":
            rebuild_structured = True
            field_values = [get_task_value(r, nf)["value"] for r in responses]
            field_type = get_task_value(responses[0], nf)["type"]
            field_name = get_task_value(responses[0], nf)["tag"]
        else:
            rebuild_structured = False
            field_values = [get_task_value(r, nf) for r in responses]
        if field_type in ("text", "number", "integer", "binary-choice"):
            majority_vote_result = basic_majority(field_values)
            if agreement_score:
                score = agreement_basic(majority_vote_result, field_values)

        elif field_type == "exclusive-choice":
            majority_vote_result = exclusive_choice_majority(field_values)
            if agreement_score:
                score = agreement_exclusive_choice(majority_vote_result, field_values)

        elif field_type == "multiple-choice":
            majority_vote_result = multiple_choice_majority(field_values)
            if agreement_score:
                score = agreement_multiple_choice(majority_vote_result, field_values)

        else:
            raise UnexpectedDataType(f"The data type {field_type} is not currently supported.")
        if rebuild_structured:
            majority_vote_result = df.structured(tag=field_name, type=field_type, value=majority_vote_result)[
                "schema_instance"
            ]
        responses_out.append(majority_vote_result)
        scores.append(score)
    return (responses_out, scores) if agreement_score else responses_out
