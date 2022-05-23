import glob
import importlib
import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional, Union

import boto3
import pandas as pd
from jinja2 import Environment, PackageLoader, select_autoescape

from superai import Client
from superai.log import logger
from superai.utils import load_api_key, load_auth_token, load_id_token

log = logger.get_logger(__name__)


def list_models(
    ai_name: str,
    client: Client = Client(
        api_key=load_api_key(),
        auth_token=load_auth_token(),
        id_token=load_id_token(),
    ),
    raw: bool = False,
    verbose: bool = True,
) -> Union[List[Dict], pd.DataFrame]:
    """List existing models in the database, given the model name.

    Args:
        verbose: Print the output.
        raw: Return unformatted list of models.
        client: Instance of superai.client.
        ai_name: Name of the AI model.
    """
    model_entries: List[Dict] = client.get_model_by_name(ai_name, to_json=True)
    if raw:
        if verbose:
            log.info(json.dumps(model_entries, indent=1))
        return model_entries
    else:
        table = pd.DataFrame.from_dict(model_entries)
        if verbose:
            pd.set_option("display.max_colwidth", None)
            log.info(table)
        return table


def get_user_model_class(model_name, path: str = "."):
    """Obtain a class definition given the path to the class module"""
    cwd = os.getcwd()
    path_dir = os.path.abspath(path)
    if path != ".":
        os.chdir(path_dir)
        sys.path.append(path_dir)
    parts = model_name.rsplit(".", 1)
    if len(parts) == 1:
        logger.info(f"Importing {model_name} from {path} (Absolute path: {path_dir})")
        interface_file = importlib.import_module(model_name)
        user_class = getattr(interface_file, model_name)
    else:
        logger.info(f"Importing submodule {parts}")
        interface_file = importlib.import_module(parts[0])
        user_class = getattr(interface_file, parts[1])
    if path != ".":
        os.chdir(cwd)
        sys.path.remove(path_dir)
    return user_class


def get_ecr_image_name(name, version):
    """Get the ECR image name containing the account id and region."""
    boto_session = boto3.session.Session()
    region = boto_session.region_name
    account = boto_session.client("sts").get_caller_identity()["Account"]
    ecr_image_name = f"{account}.dkr.ecr.{region}.amazonaws.com/{name}:{version}"
    return ecr_image_name


def create_model_entrypoint(worker_count: int) -> str:
    """Creates model entrypoint python script for sagemaker deployments"""
    assert worker_count > 0, "Worker count must be greater than 0"
    jinja_env = Environment(
        loader=PackageLoader("superai.meta_ai", package_path="template_contents"), autoescape=select_autoescape()
    )
    template = jinja_env.get_template("server_script.py")
    args = dict(worker_count=worker_count)
    entry_point_file_content: str = template.render(args)
    return entry_point_file_content


def create_model_handler(model_name: str, ai_cache: int, lambda_mode: bool) -> str:
    """Creates a model handler python script called by sagemaker to wrap the AI class."""
    assert model_name, "Model name must be provided"
    jinja_env = Environment(
        loader=PackageLoader("superai.meta_ai", package_path="template_contents"), autoescape=select_autoescape()
    )
    if not lambda_mode:
        template = jinja_env.get_template("runner_script_s2i.py")
        args = dict(model_name=model_name)
    else:
        template = jinja_env.get_template("lambda_script.py")
        args = dict(ai_cache=ai_cache, model_name=model_name)
    scripts_content: str = template.render(args)
    return scripts_content


def find_root_model(name, client) -> Optional[str]:
    models = client.get_model_by_name(name)
    possible_root_models = [x for x in models if x.version == 1]
    if possible_root_models:
        if len(possible_root_models) == 1:
            log.warning("Found root model based on name. Its recommended to use an explicit root_id.")
            return possible_root_models[0].id
        else:
            log.error(
                "Found multiple possible root AIs based on name: {possible_root_models}. Please pass an explicit root_id."
            )


def upload_dir(localDir, awsInitDir, bucketName, prefix="/"):
    """
    from current working directory, upload a 'localDir' with all its subcontents (files and subdirectories...)
    to a aws bucket
    Parameters
    ----------
    localDir :   localDirectory to be uploaded, with respect to current working directory
    awsInitDir : prefix 'directory' in aws
    bucketName : bucket in aws
    prefix :     to remove initial '/' from file names

    https://stackoverflow.com/a/64445594/15820564
    Returns
    -------
    None
    """
    assert localDir, "localDir must be provided"
    log.info("Uploading directory: {} to bucket: {}".format(localDir, bucketName))
    s3 = boto3.resource("s3")
    cwd = str(Path.cwd())
    p = Path(os.path.join(Path.cwd(), localDir))
    mydirs = list(p.glob("**"))
    for mydir in mydirs:
        fileNames = glob.glob(os.path.join(mydir, "*"))
        fileNames = [f for f in fileNames if not Path(f).is_dir()]
        len(fileNames)
        for i, fileName in enumerate(fileNames):
            fileName = str(fileName).replace(os.path.join(cwd, localDir), "")
            if fileName.startswith(prefix):  # only modify the text if it starts with the prefix
                fileName = fileName.replace(prefix, "", 1)  # remove one instance of prefix
            log.info("Uploading file: {}".format(fileName))
            awsPath = os.path.join(awsInitDir, str(fileName))
            s3.meta.client.upload_file(os.path.join(localDir, fileName), bucketName, awsPath)
