import os
import subprocess

import boto3

from colorama import Fore, Style
from superai.exceptions import SuperAIConfigurationError
from superai.log import logger

log = logger.get_logger(__name__)


def _execute(cmd: str, env: dict = {}):
    env = env or {}
    FNULL = open(os.devnull, "w")
    for key, value in env.items():
        os.environ[key] = value
    res = subprocess.run(cmd.split(), stdout=subprocess.PIPE, stderr=FNULL)
    if res.returncode == 0 and res.stdout:
        stdout = res.stdout.decode("utf-8")
    else:
        raise ChildProcessError(f"Error running command {cmd} stderr={FNULL}")

    log.debug(
        f"Exit code: {res.returncode}. Message: {res.stdout.decode('utf-8') if res.stdout else None}. Command: {cmd}"
    )
    return stdout


def get_codeartifact_token(domain="superai", aws_profile="superai"):
    """
    Retrieving aws codearficat token
    AWS_PROFILE=superai aws codeartifact get-authorization-token --domain {domain} --query authorizationToken --output text
    :param domain:
    :return:
    """
    boto3.setup_default_session(profile_name=aws_profile)
    client = boto3.client("codeartifact")
    response = client.get_authorization_token(domain=domain, durationSeconds=43200)
    token = response.get("authorizationToken") if response and isinstance(response, dict) else None
    log.debug(f"Codeartifact token: {token}")
    return token


def set_index_url(
    token: str,
    pip_config_level: str = "site",
    repo="pypi-superai",
    domain="superai",
    owner_id="185169359328",
    region="us-east-1",
):
    supported_leves = ["site", "user", "global"]
    if not pip_config_level in supported_leves:
        raise AttributeError(f"pip config level {pip_config_level} unsupported. Use one of {supported_leves}")
    cmd = f"pip config set --{pip_config_level} global.index-url https://aws:{token}@{domain}-{owner_id}.d.codeartifact.{region}.amazonaws.com/pypi/{repo}/simple/"
    stdout = _execute(cmd)
    log.debug(f"Configuring pip: {cmd}")
    log.info(f"pip configuration set: {stdout}")
    return cmd


def pip_configure(
    pip_config_level: str = "site",
    repo: str = "pypi-superai",
    domain: str = "superai",
    owner_id: str = "185169359328",
    region="us-east-1",
    show_pip: bool = False,
):
    try:
        token = get_codeartifact_token(domain=domain)
        pip_cmd = set_index_url(
            token, pip_config_level=pip_config_level, repo=repo, domain=domain, owner_id=owner_id, region=region
        )
        if show_pip:
            print(
                f"{Fore.BLUE}Copy/Paste the following command to configure pip manually:{Style.RESET_ALL}\n{Fore.CYAN}{pip_cmd}{Style.RESET_ALL}"
            )
    except Exception as e:
        raise SuperAIConfigurationError(str(e))
