import logging

from superai import settings

logger = logging.getLogger(__name__)

try:
    if settings.backend == "qumes":
        # isort: off
        try:
            from canotic.qumes_transport import (
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
                task_future,
                task_result,
                start_threads,
            )  # noqa # nosort
        except ImportError:
            from superai_transport.transport.transport import (
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
                task_future,
                task_result,
                start_threads,
            )  # noqa # nosort
    else:
        from .transport import (
            attach_bill,
            decline_result,
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
            task_future,
            task_result,
            start_threads,
        )  # noqa # nosort

        # isort: off
except ImportError as e:
    logger.exception(e)
