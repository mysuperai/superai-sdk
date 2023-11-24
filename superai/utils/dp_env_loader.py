import json
import os
import time
from functools import lru_cache

import boto3
from dynaconf import LazySettings

from superai.log import logger

CACHE_TIMEOUT = 60 * 60 * 24  # 1 day


@lru_cache
def _retrieve_secret(env, setting_root_dir, secret_name_prefix="dataprograms-env-"):
    """Cached secret retrieval function.

    Args:
        env (str): Environment name
            Only used for invalidation of cache
        setting_root_dir (str): Root directory for settings
            Used to cache the secret in a file
        secret_name_prefix (str): Prefix for the secret name

    """
    logger.debug(f"Retrieving DP env secrets, {env}, {setting_root_dir}, {secret_name_prefix}")
    cache_file = os.path.join(setting_root_dir, f"dp_env_{env}.json")

    if os.path.exists(cache_file) and os.path.getmtime(cache_file) > time.time() - CACHE_TIMEOUT:
        logger.debug(f"Loading DP env secrets from cache file {cache_file}")
        with open(cache_file, "r") as f:
            return json.load(f)
    else:
        # Get secret name
        secrets_client = boto3.client("secretsmanager")
        secret_name = _get_secret_name(env, secret_name_prefix, secrets_client)

        # Get secret values
        logger.debug(f"Loading DP env secrets {secret_name}")
        secret_response = secrets_client.get_secret_value(SecretId=secret_name)
        secret_dict = json.loads(secret_response["SecretString"])

        with open(cache_file, "w") as f:
            logger.debug(f"Writing DP env secrets to cache file {cache_file}")

            json.dump(secret_dict, f)

        return secret_dict


def _get_secret_name(env: str, secret_name_prefix: str, client) -> str:
    """Searches for a secret with the given prefix and returns the first one that matches the environment.
    Checks if it matches the environment to prevent accidentally loading the wrong secret.

    """
    response = client.list_secrets(Filters=[{"Key": "name", "Values": [secret_name_prefix]}])
    secret_list = response["SecretList"]
    logger.debug(f"Found {len(secret_list)} secrets with prefix {secret_name_prefix}")
    if not secret_list:
        raise Exception(f"No secrets found with prefix {secret_name_prefix}")
    if len(secret_list) > 1:
        logger.warning(f"Found multiple secrets with prefix {secret_name_prefix}. Using first one.")

        # Choose the first secret that matches the prefix
    secret_name = secret_list[0]["Name"]
    if env.lower() not in secret_name:
        raise Exception(f"Secret name {secret_name} does not match environment {env}")
    return secret_name


def transform_key(key):
    """Transforms a key from the dynaconf ENV var injection format to the normal python nested property format.

    Example: SUPERAI_SUPERAI_TRANSPORT__core_endpoint -> superai_transport.core_endpoint
    """
    # Override root settings with prefixless keys
    key = key.replace("SUPERAI_", "")
    # Replace double underscore with dot
    key = key.replace("__", ".")
    # Make all lowercase
    key = key.lower()
    return key


def load(
    obj: LazySettings,
    env: str = "dev",
    silent: bool = True,
    key: str = None,
    filename: str = None,
) -> None:
    """Load DP environment secrets/config from AWS Secrets Manager.
    These values are unique to each environment and are used to connect to endpoints.
    """
    try:
        secret = _retrieve_secret(env, setting_root_dir=obj._root_path)
        # Update SDK settings with the secrets
        for secret_key, value in secret.items():
            obj[secret_key] = value

        try:
            # Try loading super_transport settings and setting the corresponding properties
            # This is necessary to inject the correct values into the transport layer
            try:
                from superai_transport.hatchery import hatchery_config as hc
            except ImportError:
                logger.debug("superai_transport not installed")
                return

            for secret_key, value in secret.items():
                secret_key = transform_key(secret_key)
                hc.settings[secret_key] = value
        except Exception as e:
            logger.warning(f"Error setting super_transport settings: {e}")
    except Exception as e:
        logger.debug(f"Error loading DP env secrets: {e}")
        if not silent:
            raise e
