from os import environ
from pathlib import Path
from typing import List

from colorama import Fore, Style

from superai.data_program.hatchery.utils import (
    build_path,
    create_agent_run_command,
    execute_verbose,
    get_binaries,
    init_build_path,
)
from superai.log import logger
from superai.utils import load_api_key, stopwatch

log = logger.get_logger(__name__)

START_SH = "start.sh"


@stopwatch
def run(build_cfg: dict, runtime_cfg: dict, filepath=None):
    """Run user program in a container with several modes:

    local, container, remote:
    ----------------
    local: program runs in local
    container: program runs in a docker container
    remote: program runs in remote docker container

    concurrency:
    ------------
    Number of concurrent jobs can be run by the same agent. For GPU machine, default set to 1 due to default exclusive
    usage of GPU device by a data program.

    cpu:
    ----
    Specify the CPU unit reservation. 1024 cpu unit ~ 1 core. Default: 1024.

    memory:
    -------
    Specify the amount of memory in megabytes to be reserved. 1024 ~ 1Gb. The system may kill
    the container if it uses memory greater than the amount it requested. Default: 1024.

    build:
    ---------
    If whether to build docker images or not.
    """
    if filepath:
        filepath = Path(filepath)
        if not filepath.exists():
            raise ValueError(f"File {filepath.absolute()} does not exist")

    template_name = runtime_cfg.get("name")

    if not template_name:
        log.warn(
            Fore.LIGHTRED_EX + f"template_name not defined in build_config. Using python script name as template name. "
            f"This might throw some errors." + Style.RESET_ALL
        )

    if runtime_cfg["simulation"]:
        return

    init_build_path(clean_build=build_cfg.get("clean_build"))
    get_binaries(force_download=False)
    # Setting environment variables
    environment = runtime_cfg.get("environment", [])
    if runtime_cfg["local"]:
        start_sh = create_agent_run_command(
            template_name=template_name,
            version=build_cfg.get("version", "0.1"),
            script=filepath,
            args=build_cfg.get("args", []),
            serve=runtime_cfg.get("serve"),
            concurrency=runtime_cfg.get("concurrency"),
            force_schema=runtime_cfg.get("force_schema"),
            host=build_cfg.get("agent", {}).get("host"),
            websocket=build_cfg.get("agent", {}).get("websocket"),
            api_key=load_api_key(),
        )

        _run_task_local(
            start_sh,
            environment=environment,
        )


def _run_task_local(start_sh: str, environment: List[dict] = []):
    start_sh_path = Path(build_path(START_SH))
    with open(start_sh_path, "w") as f:
        f.write(start_sh)
    _run_local_start_command(environment=environment)


def _run_local_start_command(environment: List[dict] = []):
    for kv in environment:
        name = kv["name"]
        value = kv["value"]
        print('Setting ENV["{}"]:"{}"'.format(name, value))
        environ[name] = value
    execute_verbose('/bin/bash -c ". {}"'.format(build_path(START_SH)))
