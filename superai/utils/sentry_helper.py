import logging
import os

import sentry_sdk
from sentry_sdk.integrations.logging import LoggingIntegration, ignore_logger

from superai import __version__
from superai.config import settings

sentry_logging = LoggingIntegration(
    level=logging.WARN,  # Capture info and above as breadcrumbs
    # event_level=logging.ERROR  # Send all events with level error
)


def before_send(event, hint):
    """Filters unnecessary events using the event info and hint.

    Args:
        event:
        hint:
    """
    return event


def init(sentry_dsn: str = None):
    ignore_logger("sentry_ignore")

    try:
        sentry_dsn = sentry_dsn or os.getenv("SENTRY_DSN")
        env = os.getenv("ENV_FOR_SUPERAI", settings.name)
        if sentry_dsn:
            sentry_sdk.init(
                dsn=sentry_dsn,
                environment=env,
                release=f"superai-sdk@{__version__}",
                before_send=before_send,
                integrations=[sentry_logging],
            )
    except Exception as error:
        logging.error(f"Sentry wasn't initialized because: {error}")
