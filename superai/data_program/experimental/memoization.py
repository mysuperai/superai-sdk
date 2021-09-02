from __future__ import absolute_import, division, print_function, unicode_literals

import asyncio
import os
import shutil
from time import time

import boto3
import botocore
import joblib

from superai.config import settings
from superai.log import logger

log = logger.get_logger(__name__)

# TODO: This is an experimental implementation of memoization for api calls. This is mainly used to support recovery
def memo(method, filename, folder=None, refresh=False):
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

        def pull_from_s3(filename, client):
            dest_folder = os.path.dirname(filename)
            if not os.path.isdir(dest_folder):
                os.makedirs(dest_folder)
            bucket = client.Bucket(s3_bucket)
            bucket.download_file(filename, filename)

        def refresh_push_to_s3(method, filepath, client):
            result = method()
            joblib.dump(result, filepath)
            push_to_s3(filepath, client)
            return result

        # logic
        if refresh:  # if forced refresh, then redo the method
            log.info("Refresh True {0}".format(method.__name__))
            return refresh_push_to_s3(method, filepath, client)

        if os.path.isfile(filepath):  # if have local cache, great, then continue
            return joblib.load(filepath)
        else:  # if local cache does not exist,
            try:  # try checking s3 for cache first, if exist, then return the value
                pull_from_s3(filepath, client)
                return joblib.load(filepath)
            except botocore.exceptions.ClientError as e:
                if e.response["Error"]["Code"] == "404":  # no local/s3 cache, produce the task, cache in local and s3
                    log.warning("The S3 and local cache does not exist.")
                    return refresh_push_to_s3(method, filepath, client)
                else:
                    raise  # other s3 errors
    finally:
        log.info("Memo elapsed time: {} secs".format(time() - start_time))


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
        if os.path.isfile(filepath):
            log.info(f"Removing local memo for {folder}/{filename}")
            os.remove(filepath)
        else:
            log.info(f"No local memo found for {folder}/{filename}")

        try:
            log.info(f"Removing s3 memo for {s3_bucket}/{folder}/{filename}")
            session = boto3.session.Session()
            client = session.resource("s3")
            client.Object(s3_bucket, filepath).delete()
        except botocore.exceptions.ClientError as e:
            log.warning("S3 Error: {}".format(e))

    if prefix:
        try:
            dirpath = os.path.join(folder, prefix)
            if os.path.isdir(dirpath):
                log.info(f"Removing local memo for {dirpath}")
                shutil.rmtree(dirpath)
            else:
                log.info(f"No local memo found for {folder}/{filename}")
        except Exception as e:
            log.warning(f"Exception while deleting memo {e}")

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
        pass
        try:
            objects = []
            delete_markers = version_list["DeleteMarkers"]
            for d in delete_markers:
                objects.append({"VersionId": d["VersionId"], "Key": d["Key"]})
                response = client.delete_objects(Bucket=Bucket, Delete={"Objects": objects})
                log.info(response)

            log.info(f"Deleted Memo Bucket={Bucket}, Delete='Objects': {objects}")
        except:
            pass
            IsTruncated = version_list["IsTruncated"]
            KeyMarker = version_list["NextKeyMarker"]
