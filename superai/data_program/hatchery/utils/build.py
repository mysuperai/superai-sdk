""" Common utility for building image """
from __future__ import absolute_import, division, print_function, unicode_literals

import logging
import shutil
from os import makedirs
from pathlib import Path
from shutil import copyfile
from sys import exit
from typing import List

from colorama import Fore, Style
from yaml import safe_load

from superai.utils import load_api_key
from superai.config import settings
from superai.log import logger, logdecorator

log = logger.get_logger()


def get_build_manifest(name: str = "default"):
    if name == "default":
        return """
---
agent:
  s3: piggy/Agent-{0}.jar
""".format(
            settings.dependency_version
        )

    raise ValueError(f"Manifest {name} not found.")


def build_path(path, asPath=False):
    """Wrap the file path with the build path"""
    path = Path(settings.hatchery_build_folder) / path

    return path if asPath else str(path)


@logdecorator.log_on_start(
    logging.INFO,
    Fore.LIGHTBLACK_EX + "Initializing build path {path:s}. Forcing clean build {clean_build}" + Style.RESET_ALL,
)
@logdecorator.log_exception(
    logging.ERROR,
    Fore.RED + "Exception creating build path: {e!r}" + Style.RESET_ALL,
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
    log.debug("Deleting {}".format(path))
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
        except FileNotFoundError as e:
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
        log.debug(Fore.BLUE + f"BUILD_MANIFEST: {_config}" + Style.RESET_ALL)

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

    log.info(Fore.LIGHTBLACK_EX + f"Agent location set to {agent_location}" + Style.RESET_ALL)
    settings.agent.file = agent_location


@logdecorator.log_on_start(
    logging.DEBUG,
    Fore.CYAN + "Started copying dependency {filename:s}" + Style.RESET_ALL,
)
@logdecorator.log_on_end(
    logging.DEBUG,
    Fore.CYAN + "Copying dependency {filename:s} finished successfully {result!s}" + Style.RESET_ALL,
)
@logdecorator.log_exception(
    logging.ERROR,
    Fore.RED + "Error on copying dependency {filename:s}: {e!r}" + Style.RESET_ALL,
    on_exceptions=Exception,
    reraise=True,
)
def copy_local(filename: str):
    filename = filename.strip()
    filePath = Path(filename)
    log.info("Copy dependency from {} to {}".format(filename, build_path(filePath.name)))
    copyfile(filename, build_path(filePath.name))
    return Path(build_path(filePath.name))


@logdecorator.log_on_start(
    logging.DEBUG,
    Fore.CYAN + "Started downloading from s3 bucket {bucket:s} file:{filename:s}" + Style.RESET_ALL,
)
@logdecorator.log_on_end(
    logging.DEBUG,
    Fore.CYAN
    + "Downloading from s3 bucket {bucket:s} file:{filename:s} finished successfully {result!s}"
    + Style.RESET_ALL,
)
@logdecorator.log_on_error(
    logging.ERROR,
    Fore.RED + "Error on downloading from s3 bucket {bucket:s} file:{filename:s}: {e!r}" + Style.RESET_ALL,
    on_exceptions=Exception,
    reraise=True,
)
def copy_from_s3(bucket: str, filename: str, force_copy: bool = True):
    import boto3
    import botocore

    session = boto3.session.Session(profile_name="superai")
    s3 = session.resource("s3")

    filename = filename.strip()
    filePath = Path(filename)
    destinationPath = build_path(filePath.name)

    if force_copy or not Path(destinationPath).exists():
        log.info(
            Fore.LIGHTBLACK_EX
            + 'Pulling "{}" from bucket "{}" to "{}"'.format(filename, bucket, build_path(filePath.name))
            + Style.RESET_ALL
        )
        try:
            s3.Bucket(bucket).download_file(filename, destinationPath)
        except botocore.exceptions.ClientError as e:
            if e.response["Error"]["Code"] == "404" or e.response["Error"]["Code"] == "403":
                log.error(
                    Fore.RED
                    + f"prefix {bucket} and filename {filename} does not exist or aws access is forbidden"
                    + Style.RESET_ALL
                )
            log.error(Fore.RED + str(e) + Style.RESET_ALL)
            exit(1)
    else:
        log.info(Fore.LIGHTBLACK_EX + f'{destinationPath} exists"' + Style.RESET_ALL)
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
        assert piggy_agent_path.is_file(), "Unable to find {} file".format(piggy_agent_path.absolute())
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
