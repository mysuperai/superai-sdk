import logging
import time
from functools import wraps

from superai.log import logger


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


def stopwatch(f):
    @wraps(f)
    def _decorator_func(*args, **kwargs):
        start_time = int(round(time.time() * 1000))
        log = logging.getLogger(f.__module__)
        extra_args = {"func_name_override": f.__name__}
        return_val = f(*args, **kwargs)
        log.info(
            "{}() elapsed time: {} ms.".format(f.__name__, int(round(time.time() * 1000) - start_time)),
            extra=extra_args,
        )
        return return_val

    return _decorator_func


def experimental(func):
    """
    Decorator for marking APIs experimental in the docstring.

    :param func: A function to mark
    :returns Decorated function.
    """
    notice = (
        ".. Note:: Experimental: This method is subject to change or "
        + "removal in a future release without warning.\n"
    )
    func.__doc__ = notice + func.__doc__
    return func
