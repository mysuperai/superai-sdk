import os
from functools import wraps
from inspect import getframeinfo, stack
from typing import Callable, Optional

import requests

from superai import Client
from superai.data_program.task.types import DPSuperTaskConfigs
from superai.data_program.types import HandlerOutput, Parameters
from superai.log import logger
from superai.utils import load_api_key


def sign_url(url: str, client: Client = None):
    """Gets signed URL for a dataset given the resource URL. If the path is not a proper data path, it returns an unsigned URL
    in the response object.

    Args:
        url: Request URL
        client: :class:`Client <superai.client.Client>`

    Returns:
        Signed URL.
    """
    if url.startswith("data://"):
        client = client or Client(api_key=load_api_key())
        return client.get_signed_url(path=url).get("signedUrl")

    return url


def download_content(url: str, client: Client = None, timeout: int = 10):
    """Downloads data given a `"data://..."` or URL path.

    Args:
        url: Dataset's path or URL. If the URL is a `data` path then a signed URL will be generated first. If a
                    standard URL is passed then the `requests` library is used to load the URL and return the content
                    using response.json().
        client: :class:`Client <superai.client.Client>`.
        timeout: Optional; how many seconds to wait for the server to send data before giving up, as a float.

    Returns:
        URL content.
    """
    if url.startswith("data://"):
        client = client or Client(api_key=load_api_key())
        return client.download_data(url, timeout=timeout).json()

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


def _call_handler(
    handler, params: Parameters, super_task_configs: Optional[DPSuperTaskConfigs] = None
) -> HandlerOutput:
    """Call the handler with the given parameters and super task parameters.
    Acts as a single point of entry for the handler call.
    Is used for backwards compatibility with the old handler signature.
    Args:
        params:
        super_task_configs:

    Returns:

    """
    if super_task_configs is None:
        return handler(params)
    else:
        return handler(params, super_task_configs)
