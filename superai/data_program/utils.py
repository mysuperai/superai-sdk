import os
from functools import wraps
from inspect import getframeinfo, stack
from typing import Callable

import requests

from superai import Client
from superai.data_program.protocol.task import _parse_args
from superai.log import logger
from superai.utils import load_api_key


def parse_dp_definition(dp_definition):
    input_schema = _parse_args(schema=dp_definition.get("input_schema")).get("schema")
    output_schema = _parse_args(schema=dp_definition.get("output_schema")).get("schema")
    parameter_schema = _parse_args(schema=dp_definition.get("parameter_schema")).get("schema")
    return input_schema, output_schema, parameter_schema


def sign_url(url: str, client: Client = None):
    """
    Get signed url for a dataset given the resource URL. If the path is not a proper data path returns an unsigned URL
    in the response object

    :param url: Request URL
    :param client: :class:`Client <superai.client.Client>`
    :return: Signed url
    """
    if url.startswith("data://"):
        client = client if client else Client(api_key=load_api_key())
        return client.get_signed_url(path=url).get("signedUrl")

    return url


def download_content(url: str, client: Client = None, timeout: int = 10):
    """
    Downloads data given a `"data://..."` or URL path.

    :param url: Dataset's path or URL. If the URL is a `data` path then a signed URL will be generated first. If a
                    standard URL is passed then the `requests` library is used to load the URL and return the content
                    using response.json()
    :param client: :class:`Client <superai.client.Client>`
    :param timeout: (optional) How many seconds to wait for the server to send data before giving up, as a float.
    :return: URL content
    """
    if url.startswith("data://"):
        client = client if client else Client(api_key=load_api_key())
        return client.download_data(url, timeout=timeout)

    res = requests.get(url, timeout=timeout)
    if res.status_code == 200:
        return res.json()
    else:
        raise Exception(res.reason)


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
