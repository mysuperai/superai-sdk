import glob
import importlib
import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional, Union

import boto3
import numpy as np
import pandas as pd
from jinja2 import Environment, PackageLoader, select_autoescape

from superai import Client
from superai.log import logger
from superai.meta_ai.dataset import Dataset
from superai.utils import load_api_key, load_auth_token, load_id_token

PREDICTION_METRICS_JSON = "metrics.json"

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


def get_user_model_class(model_name, save_location, path: Union[str, Path] = "."):
    """Obtain a class definition given the path to the class module

    Args:
        save_location: Location of the stored model (e.g. .AISave/...)
        path: Path to the class module relative to `save_location`
        model_name: Name of the model
    """
    location = Path(save_location)
    path_dir = location / path
    ai_module_path_str = str(path_dir.absolute())
    sys.path.append(ai_module_path_str)
    parts = model_name.rsplit(".", 1)
    if len(parts) == 1:
        logger.info(f"Importing {model_name} from {path} (Absolute path: {path_dir})")
        interface_file = importlib.import_module(model_name)
        user_class = getattr(interface_file, model_name)
    else:
        logger.info(f"Importing submodule {parts}")
        interface_file = importlib.import_module(parts[0])
        user_class = getattr(interface_file, parts[1])
    sys.path.remove(ai_module_path_str)
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


def create_model_handler(model_name: str, lambda_mode: bool, ai_cache: int = None) -> str:
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
                f"Found multiple possible root AIs based on name: {possible_root_models}. Please pass an explicit root_id."
            )


def upload_dir(local_dir: Union[Path, str], aws_root_dir: Union[Path, str], bucket_name: str, prefix: str = "/"):
    """
    from current working directory, upload a 'local_dir' with all its subcontents (files and subdirectories...)
    to a aws bucket
    Parameters
    ----------
    local_dir : local directory to be uploaded, with respect to current working directory
    aws_root_dir : prefix 'directory' in aws
    bucket_name : bucket in aws
    prefix : to remove initial '/' from file names

    https://stackoverflow.com/a/64445594/15820564
    Returns
    -------
    None
    """
    log.info(f"Uploading directory: {local_dir} to bucket: {bucket_name}")
    s3 = boto3.resource("s3")
    cwd = str(Path.cwd())
    p = Path(os.path.join(Path.cwd(), local_dir))
    subdirectories = list(p.glob("**"))
    for subdir in subdirectories:
        file_names = glob.glob(os.path.join(subdir, "*"))
        file_names = [f for f in file_names if not Path(f).is_dir()]
        for i, file_name in enumerate(file_names):
            file_name = str(file_name).replace(os.path.join(cwd, local_dir), "")
            if file_name.startswith(prefix):  # only modify the text if it starts with the prefix
                file_name = file_name.replace(prefix, "", 1)  # remove one instance of prefix
            log.info(f"Uploading file: {file_name}")
            aws_path = os.path.join(aws_root_dir, str(file_name))
            s3.meta.client.upload_file(os.path.join(local_dir, file_name), bucket_name, aws_path)


def load_and_predict(
    model_path: Union[Path, str],
    weights_path: Optional[Union[Path, str]] = None,
    data_path: Optional[Union[Path, str]] = None,
    json_input: Optional[str] = None,
    metrics_output_dir: Path = None,
):
    """
    Loads a model and makes a prediction on the data.
    Supports json string input or json file input.

    Parameters
    ----------
    model_path : str, Path
        Path to the model directory.
    weights_path : str, Path, optional
        Path to the weights file.
    data_path : str, Path, optional
        Path to the data file.
    json_input : str, optional
        JSON string input.
    metrics_output_dir : Path, optional
        Path to the directory where metrics will be saved.


    """
    if json_input is None and data_path is None:
        raise ValueError("No input data provided. Please provide either a JSON input or a data path")
    if data_path and json_input:
        raise ValueError("Please provide either a JSON input or a data path")

    from superai.meta_ai import AI

    if metrics_output_dir:
        try:
            from polyaxon import tracking

            tracking.init()
        except:
            log.debug("Polyaxon not installed. Tracking not enabled.")

    model_path = str(Path(model_path).absolute())
    log.info(f"Loading model files from: {model_path}")
    if weights_path:
        weights_path = str(Path(weights_path).absolute())
        log.info(f"Loading model weights from: {weights_path}")
    if data_path:
        data_path = Path(data_path).absolute()
        log.info(f"Loading data from: {data_path}")
        dataset = Dataset.from_file(data_path)
    else:
        dataset = Dataset.from_json(json_input=json_input)
    log.info(f"Dataset loaded: {dataset}")

    ai_object = AI.load_local(model_path, weights_path=weights_path)
    task_input = dataset.X_train
    if len(task_input) > 1:
        result = ai_object.predict_batch(task_input)
        scores = [instance["score"] for p in result for instance in p]
        predict_score = np.mean(scores)
    else:
        result = ai_object.predict(task_input[0])
        scores = [instance["score"] for instance in result]
        predict_score = np.mean(scores)
    log.info("Prediction score: {}".format(predict_score))
    if metrics_output_dir:
        store_prediction_metrics(metrics_output_dir, dict(score=predict_score))
    return result


def store_prediction_metrics(
    metrics_output_dir: Union[Path, str], metrics: dict, filename: str = PREDICTION_METRICS_JSON
) -> Path:
    """
    Method to store prediction metrics in a json file.
    Args:
        metrics_output_dir: Path to the directory where metrics will be saved.
        metrics: dict
            Dictionary of metrics.
            Keys should be the metric names and values should be the metric values.

    Returns:

    """
    metrics_output_dir = Path(metrics_output_dir)
    metrics_output_dir.mkdir(parents=True, exist_ok=True)
    metrics_output_path = metrics_output_dir / filename

    with open(metrics_output_path, "w") as f:
        json.dump(metrics, f)
    log.info("Metrics saved to: {}".format(metrics_output_path))
    return metrics_output_path
