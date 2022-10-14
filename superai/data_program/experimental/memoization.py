from __future__ import absolute_import, division, print_function, unicode_literals

import asyncio
import os
import tempfile
import threading
from io import BytesIO
from time import time

import boto3
import botocore
import joblib
from diskcache import Cache

from superai.config import settings
from superai.log import logger

MAX_BOTO_POOL_CONNECTIONS = 30

log = logger.get_logger(__name__)

cache = None
_cache_dir = os.path.join(tempfile.gettempdir(), "memo", settings.name)
# least-recently-stored is a read-only cache policy and faster than least-recently-used
cache_settings = dict(
    directory=_cache_dir, size_limit=settings.cache_size_in_bytes, eviction_policy="least-recently-stored"
)
_cache_lock = threading.Lock()


def _init_cache():
    global cache, _cache_lock
    # add lock
    with _cache_lock:
        if not cache:
            log.debug("Initializing cache...")
            cache = Cache(**cache_settings)


_init_cache()

_s3_client_lock = threading.Lock()
_s3_client = None


def _init_s3_client():
    # Init s3 client in a thread-safe way
    # using the _s3_client is thread safe and does not require a lock
    global _s3_client, _s3_client_lock
    with _s3_client_lock:
        if not _s3_client:
            log.debug("Initializing s3 client...")
            _s3_client = boto3.client(
                "s3", config=botocore.config.Config(max_pool_connections=MAX_BOTO_POOL_CONNECTIONS)
            )


_init_s3_client()

# TODO removing push function
def _push_to_s3(filename, object, s3_bucket):
    _s3_client.upload_fileobj(
        Fileobj=object, Key=filename, Bucket=s3_bucket, Config=boto3.s3.transfer.TransferConfig(use_threads=False)
    )


def _pull_from_s3(object, filename, s3_bucket) -> object:
    return _s3_client.download_fileobj(
        Bucket=s3_bucket, Key=filename, Fileobj=object, Config=boto3.s3.transfer.TransferConfig(use_threads=False)
    )


def _refresh_push_to_s3(method, filepath, s3_bucket) -> object:
    result = method()
    cache[filepath] = result
    with BytesIO() as tmpfile:
        joblib.dump(result, tmpfile)
        _push_to_s3(filepath, tmpfile, s3_bucket)
    return result


# TODO: This is an experimental implementation of memoization for api calls. This is mainly used to support recovery
def memo(method, filename, folder=None, refresh=False):
    start_time = time()
    try:
        if folder is None:
            folder = "memo/{}".format(settings.name)
        log.debug("Executing memo of {}/{}...".format(settings.name, filename))

        s3_bucket = settings.memo_bucket
        filepath = os.path.join(folder, filename)

        # logic
        if refresh:  # if forced refresh, then redo the method
            log.info("Refresh True {0}".format(method.__name__))
            return _refresh_push_to_s3(method, filepath, s3_bucket)
        if filepath in cache:  # if have local cache, great, then continue
            log.info("Cache hit for {}".format(filepath))
            result = cache.get(filepath)
            return result
        else:  # if local cache does not exist,
            try:  # try checking s3 for cache first, if exist, then return the value
                with BytesIO() as tmpfile:
                    _pull_from_s3(tmpfile, filename, s3_bucket)
                    result = joblib.load(tmpfile)
                log.info("Write to local cache for {}".format(filepath))
                cache[filepath] = result
                return result
            except botocore.exceptions.ClientError as e:
                if e.response["Error"]["Code"] == "404":  # no local/s3 cache, produce the task, cache in local and s3
                    log.debug("The S3 and local cache does not exist.")
                    return _refresh_push_to_s3(method, filepath, s3_bucket)
                else:
                    raise  # other s3 errors
    finally:
        log.debug("Memo elapsed time: {} secs".format(time() - start_time))


# TODO: this is hacky way of implementing memoization of random task
async def async_memo(method, filename, folder=None, refresh=False):
    """TODO(veselin/purnawirman): is this something we want to support and use going forward vs snapshot?"""
    start_time = time()
    try:
        if folder is None:
            folder = "memo/{}".format(settings.name)
        log.info("Executing memo of {}/{}...".format(settings.name, filename))
        session = boto3.session.Session()
        client = session.resource("s3")
        s3_bucket = settings.memo_bucket

        filepath = os.path.join(folder, filename)
        if not os.path.isdir(os.path.dirname(filepath)):
            os.makedirs(os.path.dirname(filepath))

        # TODO removing push function
        def push_to_s3(filename, client):
            # client.upload_file
            client.meta.client.upload_file(filename, s3_bucket, filename)

        async def pull_from_s3(filename, client):
            dest_folder = os.path.dirname(filename)
            if not os.path.isdir(dest_folder):
                os.makedirs(dest_folder)
            bucket = client.Bucket(s3_bucket)
            await asyncio.get_event_loop().run_in_executor(None, bucket.download_file, filename, filename)

        async def refresh_push_to_s3(method, filepath, client):
            result = await method()
            joblib.dump(result, filepath)
            await asyncio.get_event_loop().run_in_executor(None, push_to_s3, filepath, client)
            return result

        # logic
        if refresh:  # if forced refresh, then redo the method
            log.info("Refresh True {0}".format(method.__name__))
            return await refresh_push_to_s3(method, filepath, client)

        if os.path.isfile(filepath):  # if have local cache, great, then continue
            return joblib.load(filepath)
        else:  # if local cache does not exist,
            try:  # try checking s3 for cache first, if exist, then return the value
                await pull_from_s3(filepath, client)
                return joblib.load(filepath)
            except botocore.exceptions.ClientError as e:
                if e.response["Error"]["Code"] == "404":  # no local/s3 cache, produce the task, cache in local and s3
                    log.warning("The S3 and local cache does not exist.")
                    return await refresh_push_to_s3(method, filepath, client)
                else:
                    raise  # other s3 errors
    finally:
        log.info("Memo elapsed time: {} secs".format(time() - start_time))


def forget_memo(filename, folder=None, prefix: str = None):
    s3_bucket = settings.memo_bucket
    if folder is None:
        folder = "memo/{}".format(settings.name)

    if filename:
        filepath = os.path.join(folder, filename)
        if filepath in cache:  # if have local cache, great, then continue
            cache.pop(filepath)
        try:
            log.info(f"Removing s3 memo for {s3_bucket}/{folder}/{filename}")
            session = boto3.session.Session()
            client = session.resource("s3")
            client.Object(s3_bucket, filepath).delete()
        except botocore.exceptions.ClientError as e:
            log.warning("S3 Error: {}".format(e))

    if prefix:
        try:
            s3_prefix = f"{folder}/{prefix}" if prefix.endswith("/") else f"{folder}/{prefix}/"
            log.info(f"Removing s3 memo for Bucket={s3_bucket} Prefix={s3_prefix}")
            delete_all_objects(Bucket=s3_bucket, Prefix=s3_prefix)
        except botocore.exceptions.ClientError as e:
            log.info("S3 Error: {}".format(e))


def delete_all_objects(Bucket, Prefix, MaxKeys=50, KeyMarker=None):
    """
    TODO: Doesn't support pagination in case that a lot of keys need to be removed.

    :param Bucket: Bucket name
    :param Prefix: Key prefix
    :param MaxKeys: Max number of keys to return
    :param KeyMarker:AWS KeyMarker
    :return:
    """
    client = boto3.client("s3")

    if not KeyMarker:
        version_list = client.list_object_versions(Bucket=Bucket, MaxKeys=MaxKeys, Prefix=Prefix)
    else:
        version_list = client.list_object_versions(Bucket=Bucket, MaxKeys=MaxKeys, KeyMarker=KeyMarker, Prefix=Prefix)

    try:
        objects = []
        versions = version_list.get("Versions", [])
        for v in versions:
            objects.append({"VersionId": v["VersionId"], "Key": v["Key"]})
            response = client.delete_objects(Bucket=Bucket, Delete={"Objects": objects})
            log.info(response)

        log.info(f"Deleted Memo Bucket={Bucket}, Delete='Objects': {objects}")

    except:
        try:
            objects = []
            delete_markers = version_list["DeleteMarkers"]
            for d in delete_markers:
                objects.append({"VersionId": d["VersionId"], "Key": d["Key"]})
                response = client.delete_objects(Bucket=Bucket, Delete={"Objects": objects})
                log.info(response)

            log.info(f"Deleted Memo Bucket={Bucket}, Delete='Objects': {objects}")
        except:
            IsTruncated = version_list["IsTruncated"]  # noqa
            KeyMarker = version_list["NextKeyMarker"]
