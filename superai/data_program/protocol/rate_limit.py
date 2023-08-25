import datetime
import os
import tempfile

import diskcache as dc

cache = dc.Cache(os.path.join(tempfile.gettempdir(), "rate"))


def compute_api_wait_time(entity: str, max_tpm: int, current_increase: int = 1):
    """Uses in memory cache to keep track of how many TPM were done to a given entity,
    returns the number of seconds that you need to wait in order to not exceed the
    TPM that you provide. It's used to throttle API requests across threads.

    Args:
        entity (str): A unique name for the API you're throttling.
        max_tpm (int): The max TMP.
        current_increase (int, optional): The amount of transactions that would
        increase with the current request. Defaults to 1.

    Returns:
        int: The number of seconds to wait in order to send the request successfully, 0
        if the request can be performed. The reccomanded use is to wait the time if != 0
        + a random additional time, and call this function again, since other services could
        be filling the max TPM for the following minute before you.
    """

    now = datetime.datetime.now()
    current_minute = now.minute
    time_until_next_minute = 60 - now.second
    current_key = f"{entity}:{str(current_minute)}"

    saved_tpm = cache.get(current_key)

    if not saved_tpm:
        cache.set(current_key, current_increase, time_until_next_minute)
        return 0

    tpm_when_requested = saved_tpm + current_increase

    if tpm_when_requested < max_tpm:
        cache.incr(current_key, current_increase)
        return 0

    return time_until_next_minute
