import os
import pathlib
import warnings
from logging import Logger
from typing import Dict

import yaml
from dynaconf import Dynaconf, Validator
from jsonmerge import merge

from superai.log import logger

local = pathlib.Path(__file__).parent.absolute()

__env_switcher: str = "ENV_FOR_SUPERAI"
__superai_root_dir: str = os.getenv("SUPERAI_CONFIG_ROOT") or "~/.superai"
__settings_path: str = os.path.expanduser(f"{__superai_root_dir}/settings.yaml")
__secrets_path: str = os.path.expanduser(f"{__superai_root_dir}/.secrets.yaml")
__local_settings_path: str = os.path.expanduser(f"{local}/settings.yaml")  # Default settings file
__local_secrets_path: str = os.path.expanduser(f"{local}/.secrets.yaml")

dynaconf_setting_files = [
    __local_settings_path,
    __local_secrets_path,
    __settings_path,
    __secrets_path,
]


def _get_config_path(log: Logger = None):
    log = log or logger.get_logger(__name__)
    config_path = None
    for p in reversed(dynaconf_setting_files):
        if "secrets" in p:
            continue
        if os.path.exists(p):
            print("Reading configs from {}".format(p))
            config_path = p
            break
        else:
            log.debug(f"{p} does not exist")

    if not config_path:
        print("Error: No setting.yaml file found")

    return config_path


def get_config_dir():
    return __superai_root_dir


def list_env_configs(printInConsole=True, log: Logger = None) -> Dict:
    """ List all available clusters """
    log = log or logger.get_logger(__name__)

    import yaml

    __config_path__ = _get_config_path()

    if printInConsole:
        print("Available envs:")

    with open(os.path.expanduser(f"{__config_path__}"), "r") as f:
        envs = yaml.safe_load(f)
        envs.pop("default")
        if printInConsole:
            for config in list(envs):
                # Default and testing environments are not relevant thus hidden from the output
                if config not in ["testing"]:
                    print("- {}".format(config))

    return envs


def set_env_config(name, root_dir: str = __superai_root_dir, log: Logger = None):
    """ Set the active cluster name """
    # settings.setenv("other", silent=False)
    log = log or logger.get_logger(__name__)

    env_config = list_env_configs(printInConsole=False)
    if name not in env_config:
        warnings.warn(f"Error loading env {name} choose one of {list(env_config.keys())}")
        raise ValueError(f"Env {name} doesn't exists")

    log.info(f"Setting config : {name}")
    with open(os.path.expanduser(f"{root_dir}/.env"), "w") as f:
        f.write(f"ENV_FOR_SUPERAI={name}")


def add_secret_settings(content: dict = None):
    content = content or {}
    secrets_path = os.path.expanduser(__secrets_path)
    secrets_folder = os.path.dirname(__secrets_path)
    _log.debug(f"Secrets path {os.path.dirname(secrets_path)}")
    if not os.path.exists(secrets_folder):
        _log.debug(f"Creating secrets path {os.path.dirname(secrets_path)}")
        os.makedirs(secrets_folder, exist_ok=True)

    if not os.path.exists(secrets_path):
        _log.debug(f"Creating secrets file {secrets_path}")
        pathlib.Path(secrets_path).touch()

    _log.debug(f"Loading secrets file: {secrets_path}")
    with open(secrets_path, "r") as f:
        secrets = dict(yaml.load(f, yaml.SafeLoader) or {})

    final_secrets = merge(secrets, content)

    with open(secrets_path, "w") as f:
        yaml.dump(final_secrets, f, allow_unicode=True, default_flow_style=False)
    _log.debug(f"Final secrets {final_secrets}")


def init_config(
    root_dir: str = __superai_root_dir,
):
    # This is necessary so that the first time the user initializes the repository
    # dynaconf doesn't fail
    root_dir = os.path.expanduser(root_dir)
    if not os.path.exists(root_dir):
        os.mkdir(root_dir)

    dot_env_file = os.path.join(root_dir, ".env")
    if not os.path.exists(dot_env_file):
        set_env_config(name="prod")


init_config()

validators = [
    # Ensure some parameters exists (are required)
    Validator(
        "NAME",
        "AGENT",
        "AGENT.FILE",
        "AGENT.HOST",
        "AGENT.WEBSOCKET",
        "BACKEND",
        "BASE_FOLDER",
        "BASE_URL",
        "BUILD_MANIFEST",
        "COGNITO.CLIENT_ID",
        "COGNITO.REGION",
        "COGNITO.USERPOOL_ID",
        "DEPENDENCY_VERSION",
        "HATCHERY_BUILD_FOLDER",
        "MEMO_BUCKET",
        "PROJECT_ROOT",
        "S3_BUCKET",
        must_exist=True,
    ),
    # validate a value is eq in specific env
    Validator("NAME", eq="test", env="testing"),
    Validator("NAME", eq="dev", env="dev"),
    Validator("NAME", eq="local", env="local"),
    Validator("NAME", eq="sandbox", env="sandbox"),
    Validator("NAME", eq="prod", env="prod"),
]

settings = Dynaconf(
    envvar_prefix="SUPERAI",
    env_switcher=__env_switcher,
    settings_files=dynaconf_setting_files,
    environments=True,
    includes=[
        # If any .secrets.yaml exits, will have higher priority than the previously
        # loaded config files
    ],
    load_dotenv=True,
    root_path=os.path.expanduser(__superai_root_dir),
    validators=validators,
    merge_enabled=True,
)

_log = logger.init(
    filename=settings.get("log", {}).get("filename"),
    console=settings.get("log", {}).get("console"),
    log_level=settings.get("log", {}).get("level"),
    log_format=settings.get("log", {}).get("format"),
)
