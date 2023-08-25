"""Common utility for building image."""

from __future__ import absolute_import, division, print_function, unicode_literals

import contextlib
import logging
import shutil
from os import makedirs
from pathlib import Path
from shutil import copyfile
from typing import Optional

from yaml import safe_load

from superai.config import settings
from superai.log import logdecorator, logger
from superai.utils import load_api_key
from superai.utils.files import s3_download_file

log = logger.get_logger()


def get_build_manifest(name: str = "default"):
    if name == "default":
        return f"""
---
agent:
  s3: piggy/Agent-{settings.dependency_version}.jar
"""

    raise ValueError(f"Manifest {name} not found.")


def build_path(path, as_path=False):
    """Wrap the file path with the build path"""
    path = Path(settings.hatchery_build_folder) / path

    return path if as_path else str(path)


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
def clean_build_files(path: Optional[str] = None):
    """Clean build folder"""
    path = settings.hatchery_build_folder if path is None else Path()
    log.debug(f"Deleting {path}")
    with contextlib.suppress(Exception):
        shutil.rmtree(path)


def build_path_exists():
    return Path(settings.hatchery_build_folder).exists()


def get_binaries(base_path=settings.s3_bucket, manifest=settings.build_manifest, force_download: bool = True):
    # TODO: Get rid of s3_bucket as parameters and encode this information in the build_manifest
    manifest_path = Path(manifest)
    if manifest_path and manifest_path.exists():
        should_copy = True
        with contextlib.suppress(FileNotFoundError):
            if manifest_path.samefile(build_path(manifest_path.name)):
                should_copy = False
        if should_copy:
            copyfile(manifest, build_path(manifest_path.name))
    else:
        # Writing default manifest to predetermined location
        with open(build_path(manifest_path.name), "w") as f:
            f.write(get_build_manifest(name="default"))
            f.close()

    with open(build_path(manifest_path.name), "r") as f:
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
    file_path = Path(filename)
    log.info(f"Copy dependency from {filename} to {build_path(file_path.name)}")
    copyfile(filename, build_path(file_path.name))
    return Path(build_path(file_path.name))


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
    filename = filename.strip()
    file_path = Path(filename)
    destination_path = build_path(file_path.name)

    if force_copy or not Path(destination_path).exists():
        s3_download_file(filename, destination_path, bucket, session_profile_name="superai")
    else:
        log.info(f"{destination_path} exists")
    return Path(destination_path)


def create_agent_run_command(
    template_name: str,
    version: str,
    script: str,
    args=None,
    run_once: bool = False,
    serve: bool = True,
    concurrency: int = 100,
    force_schema: bool = False,
    host: str = settings.agent.host,
    websocket: str = settings.agent.websocket,
    api_key: str = None,
):
    """Generates piggy command line to execute target script."""
    if args is None:
        args = []
    api_key = api_key or load_api_key()
    piggy_agent_path = Path(settings.agent.file)
    if not piggy_agent_path.is_file():
        piggy_agent_path = Path(settings.hatchery_build_folder) / settings.agent.file
        assert piggy_agent_path.is_file(), f"Unable to find {piggy_agent_path.absolute()} file"
    return (
        "java -jar {path} {host} {websocket} {api_key} {concurrency} {runonce} {force_schema} {serve} "
        "{template_name} --version {version} python {script} {args}\n".format(
            path=piggy_agent_path,
            host=f"--host {host}" if host else "",
            websocket=f"--websocket {websocket}" if websocket else "",
            api_key=f"--api_key {api_key}" if api_key else "",
            concurrency=f"--concurrency {concurrency}" if concurrency else "",
            runonce="--runonce" if run_once else "",
            force_schema="--force-schema" if force_schema else "",
            serve="--serve" if serve else "--workflow",
            template_name=template_name,
            version=version,
            script=script,
            args=" ".join(args),
        )
    )
