import logging

from superai import settings

logger = logging.getLogger(__name__)

try:
    if settings.backend == "qumes":
        # isort: off
        from superai_transport.transport.transport import (
            schedule_task,
            schedule_workflow,
            resolve_job,
            load_snapshot,
            load_snapshot_data,
            save_snapshot,
            send_report,
            subscribe_workflow,
            save_hero_qualification,
            remove_hero_qualification,
            get_context_id,
            get_context_app_id,
            get_context_project_id,
            get_context_is_child,
            get_context_metadata,
            get_context_job_type,
            get_context_simple_id,
            task_future,
            task_result,
            start_threads,
        )  # noqa # isort:skip
        from superai_transport.transport.rate_limit import compute_api_wait_time  # noqa # isort:skip
    else:
        from .transport import (
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
            save_hero_qualification,
            save_snapshot,
            schedule_task,
            schedule_workflow,
            send_report,
            subscribe_workflow,
            task_future,
            task_result,
            start_threads,
        )  # noqa # isort:skip

except ImportError as e:
    logger.exception(e)
