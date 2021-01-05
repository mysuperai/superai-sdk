""" Log initializer """
from __future__ import absolute_import, division, print_function, unicode_literals

import itertools
import logging
import sys
from logging.handlers import RotatingFileHandler
from typing import List

DEBUG = logging.DEBUG
INFO = logging.INFO
ERROR = logging.ERROR
WARNING = logging.WARNING
DEFAULT_LOG_FILENAME = "superai.log"
_log_format = (
    "%(asctime)s - %(levelname)s - %(filename)s - %(threadName)s - [%(name)s:%(funcName)s:%(lineno)s] - %(message)s"
)
_date_format = "%Y-%m-%d %H:%M:%S"
_style = "{"

loggers: List[logging.Logger] = []


def create_file_handler(
    log_format=_log_format,
    log_filename=DEFAULT_LOG_FILENAME,
    max_bytes=5000000,
    backup_count=25,
):
    """ Create rotating file handler """
    formatter = CustomFormatter(fmt=log_format, datefmt=_date_format, style=_style)
    handler = RotatingFileHandler(log_filename, maxBytes=max_bytes, backupCount=backup_count)
    handler.setFormatter(formatter)
    return handler


def create_console_handler(log_format=_log_format, stream=sys.stdout):
    """ Create logging to stream """
    formatter = CustomFormatter(fmt=log_format, datefmt=_date_format)
    console_handler = logging.StreamHandler(stream)
    console_handler.setFormatter(formatter)
    return console_handler


def get_logger(name=None, propagate=True):
    """ Get logger object """
    logger = logging.getLogger(name)
    logger.propagate = propagate
    loggers.append(logger)
    return logger


def exception(line):
    """ Log exception """
    return logging.exception(line)


def debug(line):
    """ Log debug """
    return logging.debug(line)


def warn(line):
    """ Log warning """
    return logging.warn(line)


def error(line):
    """ Log error """
    return logging.error(line)


def info(line):
    """ Log info """
    return logging.info(line)


def init(filename=None, console=True, log_level=INFO, log_format=_log_format):
    """ Initialize logging setup """
    if not log_format:
        log_format = _log_format

    log_handlers: List[logging.Handler] = []
    if console:
        log_handlers.append(create_console_handler(log_format=log_format))
    if filename is not None:
        log_handlers.append(create_file_handler(log_format=log_format, log_filename=filename))

    for pair in itertools.product(loggers, log_handlers):
        pair[0].addHandler(pair[1])
        pair[0].setLevel(log_level)

    logging.basicConfig(format=_log_format, level=log_level, handlers=log_handlers)
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
