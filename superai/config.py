import os
import pathlib
import warnings
from logging import Logger
from typing import Dict

import yaml
from dynaconf import Dynaconf, Validator
from jsonmerge import merge

from superai.exceptions import SuperAIConfigurationError
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
    """Gets config root directory"""
    return __superai_root_dir


def list_env_configs(printInConsole=True, log: Logger = None) -> Dict:
    """List all available environments"""
    log = log or logger.get_logger(__name__)

    import yaml

    __config_path__ = _get_config_path()

    if printInConsole:
        print("Available envs:")

    with open(os.path.expanduser(f"{__config_path__}"), "r") as f:
        envs = yaml.safe_load(f)
        envs.pop("default") if envs.get("default") else None
        if printInConsole:
            for config in list(envs):
                # Default and testing environments are not relevant thus hidden from the output
                if config not in ["testing"]:
                    print("- {}".format(config))

    return envs


def set_env_config(name, root_dir: str = __superai_root_dir, log: Logger = None):
    """Set the active cluster name"""
    # settings.setenv("other", silent=False)
    log = log or logger.get_logger(__name__)

    env_config = list_env_configs(printInConsole=False)
    if name not in env_config:
        warnings.warn(f"Error loading env {name} choose one of {list(env_config.keys())}")
        raise ValueError(f"Env {name} doesn't exists")

    log.info(f"Setting config : {name}")
    with open(os.path.expanduser(f"{root_dir}/.env"), "w") as f:
        f.write(f"ENV_FOR_SUPERAI={name}")


def ensure_path_exists(f_path: str, only_dir=False):
    """
    Give some path, this function makes sure that the file exists. It will also take care of creating all necessary
    folders. If `only_dir` is set to True then the file won't be created but all folders leading to the path will.

    :param f_path: File path
    :param only_dir: Only create directories leading to the path
    :return: Created path
    """
    f_path = os.path.expanduser(f_path)
    in_folder = os.path.dirname(f_path)

    _log.debug(f"Ensure path exists {os.path.dirname(f_path)}")
    if not os.path.exists(in_folder):
        _log.debug(f"Creating path {os.path.dirname(in_folder)}")
        os.makedirs(in_folder, exist_ok=True)

    if not os.path.exists(f_path) and not only_dir:
        _log.debug(f"Creating file {f_path}")
        pathlib.Path(f_path).touch()

    return in_folder if only_dir else f_path


def add_secret_settings(content: dict = None):
    """
    Add content to the secrets file. The content can be any arbitrary dictionary and will be merged to the original
    file contents. If the secrets file doesn't exist, this method will create the necessary folders and path.

    :param content: Content to merge
    :return: None
    """
    content = content or {}
    secrets_path = os.path.expanduser(__secrets_path)
    secrets_folder = os.path.dirname(__secrets_path)
    _log.debug(f"Secrets path {os.path.dirname(secrets_path)}")
    ensure_path_exists(secrets_path)

    _log.debug(f"Loading secrets file: {secrets_path}")
    with open(secrets_path, "r") as f:
        secrets = dict(yaml.load(f, yaml.SafeLoader) or {})

    final_secrets = merge(secrets, content)

    with open(secrets_path, "w") as f:
        yaml.dump(final_secrets, f, allow_unicode=True, default_flow_style=False)
    _log.debug(f"Final secrets {final_secrets}")


def remove_secret_settings(path_in_settings: str):
    """
    Given a path in the form <key>__<nested_key>.. this function sets the value of the path to "". Each __ is parsed
    as a level traversing thought dict keys.

    :param path_in_settings: Path with __ operator to traverse the nested structure
    :return: None
    """
    secrets_path = os.path.expanduser(__secrets_path)
    secrets_folder = os.path.dirname(__secrets_path)
    _log.debug(f"Secrets path {os.path.dirname(secrets_path)}")
    if not os.path.exists(secrets_folder):
        _log.debug(f".secrets.yaml file not found in {os.path.dirname(secrets_path)}")
        return

    if not os.path.exists(secrets_path):
        _log.debug(f"Secrets file not found {secrets_path}")
        return

    _log.debug(f"Loading secrets file: {secrets_path}")
    with open(secrets_path, "r") as f:
        secrets = dict(yaml.load(f, yaml.SafeLoader) or {})

    # Removing key
    keys = path_in_settings.split("__")
    nkeys = len(keys)
    s = secrets
    for ki in range(len(keys)):
        if ki + 1 >= nkeys and s.get(keys[ki]):
            del s[keys[ki]]
        else:
            s = s.get(keys[ki])
            if not s:
                logger.debug(f"Nothing to remove, key not found {keys[ki]}")
                return

    final_secrets = secrets
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
        env_in_order = ["prod", "sandbox", "stg", "dev", "testing"]
        envs = list_env_configs()
        for e in env_in_order:
            if e in envs:
                set_env_config(name=e)
                return
        warnings.warn(f"Defaults not found, available envs are: {envs.keys()}")


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
