import os
from functools import wraps
from inspect import getframeinfo, stack
from typing import Callable

from superai.data_program.protocol.task import _parse_args
from superai.log import logger


def parse_dp_definition(dp_definition):
    input_schema = _parse_args(schema=dp_definition.get("input_schema")).get("schema")
    output_schema = _parse_args(schema=dp_definition.get("output_schema")).get("schema")
    parameter_schema = _parse_args(schema=dp_definition.get("parameter_schema")).get("schema")
    return input_schema, output_schema, parameter_schema


def IgnoreInAgent(fn: Callable):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        log = logger.get_logger(fn.__qualname__)
        py_file_caller = getframeinfo(stack()[1][0])
        extra_args = {
            "func_name_override": fn.__name__,
            "file_name_override": os.path.basename(py_file_caller.filename),
            "lineno_override": py_file_caller.lineno,
        }
        log.debug(f"function {fn} is ignored inside agent", extra=extra_args)
        if not os.environ.get("IN_AGENT"):
            log.debug(f"Executing function {fn} because running in agent", extra=extra_args)
            return fn(*args, **kwargs)
        else:
            log.debug(
                f"Not execution function {fn} because running in agent",
                extra=extra_args,
            )
            return fn

    return wrapper
