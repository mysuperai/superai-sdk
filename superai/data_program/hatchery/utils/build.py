""" Common utility for building image """
from __future__ import absolute_import, division, print_function, unicode_literals

import logging
import shutil
from os import makedirs
from pathlib import Path
from shutil import copyfile
from sys import exit
from typing import List

from rich.progress import DownloadColumn, Progress, TransferSpeedColumn
from yaml import safe_load

from superai.config import settings
from superai.log import logdecorator, logger
from superai.utils import load_api_key

log = logger.get_logger()


def get_build_manifest(name: str = "default"):
    if name == "default":
        return f"""
---
agent:
  s3: piggy/Agent-{settings.dependency_version}.jar
"""

    raise ValueError(f"Manifest {name} not found.")


def build_path(path, asPath=False):
    """Wrap the file path with the build path"""
    path = Path(settings.hatchery_build_folder) / path

    return path if asPath else str(path)


@logdecorator.log_on_start(
    logging.INFO,
    "Initializing build path {path:s}. Forcing clean build {clean_build}",
)
@logdecorator.log_exception(
    logging.ERROR,
    "Exception creating build path: {e!r}",
    reraise=True,
)
def init_build_path(path: str = settings.hatchery_build_folder, clean_build: bool = False):
    if clean_build:
        clean_build_files(path=path)

    if not build_path_exists():
        log.info("Creating build folder")
        create_build_folder(path=path)


def create_build_folder(path=settings.hatchery_build_folder):
    """Create build folder to store all build related files"""
    path = Path(path)
    if not path.exists():
        makedirs(path, exist_ok=True)


@logdecorator.log_on_start(logging.DEBUG, "Deleting {path:s}")
def clean_build_files(path: str = settings.hatchery_build_folder):
    """Clean build folder"""
    path = Path()
    log.debug(f"Deleting {path}")
    try:
        shutil.rmtree(path)
    except Exception:
        pass


def build_path_exists():
    return Path(settings.hatchery_build_folder).exists()


def get_binaries(base_path=settings.s3_bucket, manifest=settings.build_manifest, force_download: bool = True):
    # TODO: Get rid of s3_bucket as parameters and encode this information in the build_manifest
    manifestPath = Path(manifest)
    if manifestPath and manifestPath.exists():
        should_copy = True
        try:
            if manifestPath.samefile(build_path(manifestPath.name)):
                should_copy = False
        except FileNotFoundError:
            pass

        if should_copy:
            copyfile(manifest, build_path(manifestPath.name))
    else:
        # Writing default manifest to predetermined location
        with open(build_path(manifestPath.name), "w") as f:
            f.write(get_build_manifest(name="default"))
            f.close()

    with open(build_path(manifestPath.name), "r") as f:
        _config = safe_load(f)
        log.debug(f"BUILD_MANIFEST: {_config}")

        if not _config.get("agent"):
            raise ValueError("build_manifest.yml needs to have agent and pips")

        if _config.get("agent").get("local") and _config.get("agent").get("s3"):
            raise ValueError("Agent file can be either local or in s3 but not both")

        if _config.get("pips", {}).get("local"):
            for _file in _config["pips"]["local"]:
                copy_local(_file)

        if _config.get("pips", {}).get("s3"):
            for _file in _config["pips"]["s3"]:
                copy_from_s3(base_path, _file, force_copy=force_download)

        if _config.get("agent", {}).get("local"):
            agent_location = copy_local(_config["agent"]["local"])

        if _config.get("agent", {}).get("s3"):
            agent_location = copy_from_s3(base_path, _config["agent"]["s3"], force_copy=force_download)

    log.info(f"Agent location set to {agent_location}")
    settings.agent.file = agent_location


@logdecorator.log_on_start(
    logging.DEBUG,
    "Started copying dependency {filename:s}",
)
@logdecorator.log_on_end(
    logging.DEBUG,
    "Copying dependency {filename:s} finished successfully {result!s}",
)
@logdecorator.log_exception(
    logging.ERROR,
    "Error on copying dependency {filename:s}: {e!r}",
    on_exceptions=Exception,
    reraise=True,
)
def copy_local(filename: str):
    filename = filename.strip()
    filePath = Path(filename)
    log.info(f"Copy dependency from {filename} to {build_path(filePath.name)}")
    copyfile(filename, build_path(filePath.name))
    return Path(build_path(filePath.name))


@logdecorator.log_on_start(
    logging.DEBUG,
    "Started downloading from s3 bucket {bucket:s} file:{filename:s}",
)
@logdecorator.log_on_end(
    logging.DEBUG,
    "Downloading from s3 bucket {bucket:s} file:{filename:s} finished successfully {result!s}",
)
@logdecorator.log_on_error(
    logging.ERROR,
    "Error on downloading from s3 bucket {bucket:s} file:{filename:s}: {e!r}",
    on_exceptions=Exception,
    reraise=True,
)
def copy_from_s3(bucket: str, filename: str, force_copy: bool = True):
    import boto3
    import botocore
    from boto3.s3.transfer import TransferConfig

    session = boto3.session.Session(profile_name="superai")
    s3 = session.resource("s3")

    filename = filename.strip()
    filePath = Path(filename)
    destinationPath = build_path(filePath.name)
    s3_bucket = s3.Bucket(bucket)

    if force_copy or not Path(destinationPath).exists():
        log.info(f'Pulling "{filename}" from bucket "{bucket}" to "{destinationPath}"')
        try:
            # Use Rich progress bar to track download progress
            size_bytes = s3_bucket.Object(filename).content_length
            with Progress(*Progress.get_default_columns(), DownloadColumn(), TransferSpeedColumn()) as progress:
                download_task = progress.add_task("Downloading", total=size_bytes, unit="B")

                def work_done(chunk):
                    progress.update(download_task, advance=chunk)

                # Disable threading during transfer to mitigate Python 3.9 threading issues
                config = TransferConfig(use_threads=False)
                s3_bucket.download_file(filename, destinationPath, Config=config, Callback=work_done)
        except botocore.exceptions.ClientError as e:
            if e.response["Error"]["Code"] == "404" or e.response["Error"]["Code"] == "403":
                log.error(f"prefix {bucket} and filename {filename} does not exist or aws access is forbidden")
            if e.response["Error"]["Code"] == "400":
                log.error(
                    f"S3 Operation not possible. Is session token still valid? Try `superai login` again when in doubt."
                )
            log.error(str(e))
            exit(1)
    else:
        log.info(f"{destinationPath} exists")
    return Path(destinationPath)


def create_agent_run_command(
    template_name: str,
    version: str,
    script: str,
    args: List[str] = [],
    run_once: bool = False,
    serve: bool = True,
    concurrency: int = 100,
    force_schema: bool = False,
    host: str = settings.agent.host,
    websocket: str = settings.agent.websocket,
    api_key: str = None,
):
    """Generate piggy command line to execute target script"""
    api_key = api_key or load_api_key()
    piggy_agent_path = Path(settings.agent.file)
    if not piggy_agent_path.is_file():
        piggy_agent_path = Path(settings.hatchery_build_folder) / settings.agent.file
        assert piggy_agent_path.is_file(), f"Unable to find {piggy_agent_path.absolute()} file"
    return (
        "java -jar {path} {host} {websocket} {api_key} {concurrency} {runonce} {force_schema} {serve} "
        "{template_name} --version {version} python {script} {args}\n".format(
            path=piggy_agent_path,
            host="--host {}".format(host) if host else "",
            websocket="--websocket {}".format(websocket) if websocket else "",
            api_key="--api_key {}".format(api_key) if api_key else "",
            concurrency="--concurrency {}".format(concurrency) if concurrency else "",
            runonce="--runonce" if run_once else "",
            force_schema="--force-schema" if force_schema else "",
            serve="--serve" if serve else "--workflow",
            template_name=template_name,
            version=version,
            script=script,
            args=" ".join(args),
        )
    )
