""" Log initializer """
from __future__ import absolute_import, division, print_function, unicode_literals

import itertools
import logging
import sys
import os
from logging.handlers import RotatingFileHandler
from rich.logging import RichHandler
from typing import List

DEBUG = logging.DEBUG
INFO = logging.INFO
ERROR = logging.ERROR
WARNING = logging.WARNING
DEFAULT_LOG_FILENAME = "superai.log"
_log_format = (
    "%(asctime)s - %(levelname)s - %(filename)s - %(threadName)s - [%(name)s:%(funcName)s:%(lineno)s] - %(message)s"
)
_rich_log_format = "%(message)s - %(threadName)s"
_date_format = "%Y-%m-%d %H:%M:%S"
_style = "{"

loggers: List[logging.Logger] = []


def create_file_handler(
    log_format=_log_format,
    log_filename=DEFAULT_LOG_FILENAME,
    max_bytes=5000000,
    backup_count=25,
):
    """Create rotating file handler"""
    formatter = CustomFormatter(fmt=log_format, datefmt=_date_format, style=_style)
    handler = RotatingFileHandler(log_filename, maxBytes=max_bytes, backupCount=backup_count)
    handler.setFormatter(formatter)
    return handler


def create_non_cli_handler(log_format=_log_format, stream=sys.stdout):
    """Create logging to non-CLI console (like ECS)"""
    formatter = CustomFormatter(fmt=log_format, datefmt=_date_format)
    console_handler = logging.StreamHandler(stream)
    console_handler.setFormatter(formatter)
    return console_handler


def create_cli_handler():
    """Create logging handler for CLI with rich structured output"""
    rich_handler = RichHandler(rich_tracebacks=True)
    return rich_handler


def get_logger(name=None, propagate=True):
    """Get logger object"""
    logger = logging.getLogger(name)
    logger.propagate = propagate
    loggers.append(logger)
    return logger


def exception(line):
    """Log exception"""
    return logging.exception(line)


def debug(line):
    """Log debug"""
    return logging.debug(line)


def warn(line):
    """Log warning"""
    return logging.warn(line)


def error(line):
    """Log error"""
    return logging.error(line)


def info(line):
    """Log info"""
    return logging.info(line)


def init(filename=None, console=True, log_level=INFO, log_format=_log_format):
    """Initialize logging setup"""
    if not log_format:
        log_format = _log_format

    log_handlers: List[logging.Handler] = []
    if console:
        if os.getenv("ECS", False) or os.getenv("JENKINS_URL", False):
            log_handlers.append(create_non_cli_handler(log_format=log_format))
        else:
            # Use Rich for CLI
            log_handlers.append(create_cli_handler())
            # Set Format to short type for Rich
            log_format = _rich_log_format

    if filename is not None:
        # Alwoys log to file with verbose format
        log_handlers.append(create_file_handler(log_format=_log_format, log_filename=filename))

    for pair in itertools.product(loggers, log_handlers):
        pair[0].addHandler(pair[1])
        pair[0].setLevel(log_level)

    # Set Logging config based on CLI/Non/CLI Format
    logging.basicConfig(format=log_format, level=log_level, handlers=log_handlers)
    log = get_logger(__name__)
    if log_level > logging.INFO:
        log.log(level=log_level, msg=f"super.Ai logger initialized with log_level={log_level}")
    return log


class CustomFormatter(logging.Formatter):
    """Custom Formatter does these 2 things:
    1. Overrides 'funcName' with the value of 'func_name_override', if it exists.
    2. Overrides 'filename' with the value of 'file_name_override', if it exists.
    """

    def format(self, record):
        if hasattr(record, "func_name_override"):
            record.funcName = record.func_name_override
        if hasattr(record, "file_name_override"):
            record.filename = record.file_name_override
        if hasattr(record, "lineno_override"):
            record.lineno = record.lineno_override
        return super(CustomFormatter, self).format(record)


init()
