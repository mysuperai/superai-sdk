import os
import pathlib
import warnings
from logging import Logger
from typing import Dict, Optional

import boto3
import yaml
from dynaconf import Dynaconf, Validator  # type: ignore
from jsonmerge import merge  # type: ignore

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


def _get_config_path(log: Logger = None) -> str:
    log = log or logger.get_logger(__name__)
    config_path = None
    for p in reversed(dynaconf_setting_files):
        if "secrets" in p:
            continue
        if os.path.exists(p):
            print(f"Reading configs from {p}")
            config_path = p
            break
        else:
            log.debug(f"{p} does not exist")

    if not config_path:
        print("Error: No setting.yaml file found")

    return config_path


def get_config_dir() -> str:
    """Gets config root directory."""
    return __superai_root_dir


def list_env_configs(verbose: bool = True, log: Logger = None) -> Dict:
    """Lists all available environments.s"""
    log = log or logger.get_logger(__name__)

    __config_path__ = _get_config_path()

    if verbose:
        print("Available envs:")

    with open(os.path.expanduser(f"{__config_path__}"), "r") as f:
        envs = yaml.safe_load(f)
        envs.pop("default") if envs.get("default") else None
        if verbose:
            for config in list(envs):
                # Default and testing environments are not relevant thus hidden from the output
                if config not in ["testing"]:
                    print(f"- {config}")

    return envs


def set_env_config(name: str, root_dir: str = __superai_root_dir, log: Logger = None):
    """Sets the active cluster name."""
    # settings.setenv("other", silent=False)
    log = log or logger.get_logger(__name__)

    env_config = list_env_configs(verbose=False)
    if name not in env_config:
        warnings.warn(f"Error loading env {name} choose one of {list(env_config.keys())}")
        raise ValueError(f"Env {name} doesn't exists")

    log.info(f"Setting config : {name}")
    with open(os.path.expanduser(f"{root_dir}/.env"), "w") as f:
        try:
            f.write(f"{__env_switcher}={name}")
        except Exception:
            os.environ[__env_switcher] = name


def ensure_path_exists(f_path: str, only_dir=False) -> str:
    """Given a path, this function makes sure that the file exists. It will also take care of creating all necessary
    folders. If `only_dir` is set to True then the file won't be created but all folders leading to the path will.

    Args:
        f_path: File path
        only_dir: Only create directories leading to the path

    Returns:
        The created path.
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
    """Adds content to the secrets file. The content can be any arbitrary dictionary and will be merged to the original
    file contents. If the secrets file doesn't exist, this method creates the necessary folders and path.

    Args:
        content: Content to merge

    Returns:
        None.
    """
    content = content or {}
    secrets_path = os.path.expanduser(__secrets_path)
    os.path.dirname(__secrets_path)
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
    """Given a path in the form <key>__<nested_key>.., this function sets the value of the path to "". Each __ is parsed
    as a level traversing thought dict keys.

    Args:
        path_in_settings: Path with __ operator to traverse the nested structure.

    Returns:
        None.
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
    path = pathlib.Path(root_dir)
    if not path.exists():
        try:
            path.mkdir(exist_ok=True, parents=True)
        except Exception as e:
            print(f"Exception creating dir {path.absolute()}: {e}")

    dot_env_file = os.path.join(root_dir, ".env")
    if not os.path.exists(dot_env_file) and not os.getenv(__env_switcher):
        env_in_order = ["prod", "dev", "testing"]
        envs = list_env_configs()
        for e in env_in_order:
            if e in envs:
                set_env_config(name=e)
                return
        warnings.warn(f"Defaults not found, available envs are: {envs.keys()}")


def get_current_env() -> str:
    """Gets the current configured environment"""
    return settings.current_env.lower()


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
        "DUMMY_APP",
        "CACHE_SIZE_IN_BYTES",
        must_exist=True,
    ),
    Validator("SCHEMA_PORT", gt=0, lt=65535, is_type_of=int, default=8002),
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
    loaders=["superai.utils.dp_env_loader", "dynaconf.loaders.env_loader"],
)

_log = logger.init(
    filename=settings.get("log", {}).get("filename"),
    console=settings.get("log", {}).get("console"),
    log_level=settings.get("log", {}).get("level"),
    log_format=settings.get("log", {}).get("format"),
)

# Convenience method for dynamically switching envs
using_env = settings.using_env


def get_ai_bucket():
    """Gets the bucket name from the account prefix in the settings."""
    bucket_name_prefix = settings["meta_ai_bucket"]
    complete_bucket_name = _get_bucket_name_from_prefix(bucket_name_prefix)
    return complete_bucket_name


def _get_bucket_name_from_prefix(bucket_prefix) -> Optional[str]:
    """boto3 bucket name from a list of buckets starting with a prefix"""
    s3 = boto3.client("s3", region_name=settings.region)
    try:
        bucket_list = s3.list_buckets()
        return next(
            (bucket["Name"] for bucket in bucket_list["Buckets"] if bucket["Name"].startswith(bucket_prefix)),
            None,
        )
    except Exception:
        # When debug is enabled, this will print the full stack trace
        _log.warning(f"Could not get bucket name via AWS API. Try to setup your AWS credentials or login to SSO.")
        raise
