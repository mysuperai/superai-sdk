from __future__ import annotations

import datetime
import enum
import hashlib
import json
import os
import re
import shlex
import shutil
import subprocess
import tarfile
import time
import traceback
from pathlib import Path
from typing import TYPE_CHECKING, Dict, List, Optional, Union
from urllib.parse import urlparse

import boto3  # type: ignore
import requests
import yaml
from docker import DockerClient
from docker.errors import ImageNotFound
from rich.prompt import Confirm

from superai import Client, settings
from superai.exceptions import ModelDeploymentError, ModelNotFoundError
from superai.log import logger
from superai.meta_ai.ai_helper import (
    create_model_entrypoint,
    create_model_handler,
    find_root_model,
    get_ecr_image_name,
    get_user_model_class,
    list_models,
    upload_dir,
)
from superai.meta_ai.deployed_predictors import (
    DeployedPredictor,
    LocalPredictor,
    RemotePredictor,
)
from superai.meta_ai.dockerizer import get_docker_client, push_image
from superai.meta_ai.environment_file import EnvironmentFileProcessor
from superai.meta_ai.parameters import (
    Config,
    HyperParameterSpec,
    ModelParameters,
    TrainingParameters,
)
from superai.meta_ai.schema import EasyPredictions, Schema, SchemaParameters
from superai.utils import load_api_key, load_auth_token, load_id_token, retry

# Prefix path for the model directory on storage backend
MODEL_ARTIFACT_PREFIX_S3 = "meta_ai_models"
# extended path to model weights
MODEL_WEIGHT_INFIX_S3 = "saved_models"

if TYPE_CHECKING:
    from superai.meta_ai import BaseModel

log = logger.get_logger(__name__)


class Stage(str, enum.Enum):
    DEV = "DEV"
    PROD = "PROD"
    STAGING = "STAGING"
    LATEST = "LATEST"
    SANDBOX = "SANDBOX"


class Orchestrator(str, enum.Enum):
    LOCAL_DOCKER = "LOCAL_DOCKER"
    LOCAL_DOCKER_LAMBDA = "LOCAL_DOCKER_LAMBDA"
    LOCAL_DOCKER_K8S = "LOCAL_DOCKER_K8S"
    MINIKUBE = "MINIKUBE"
    AWS_SAGEMAKER = "AWS_SAGEMAKER"
    AWS_SAGEMAKER_ASYNC = "AWS_SAGEMAKER_ASYNC"
    AWS_LAMBDA = "AWS_LAMBDA"
    AWS_EKS = "AWS_EKS"
    GCP_KS = "GCP_KS"


class TrainingOrchestrator(str, enum.Enum):
    LOCAL_DOCKER_K8S = "LOCAL_DOCKER_K8S"
    AWS_EKS = "AWS_EKS"


class PredictorFactory(object):
    __predictor_classes = {
        "LOCAL_DOCKER": LocalPredictor,
        "LOCAL_DOCKER_LAMBDA": LocalPredictor,
        "LOCAL_DOCKER_K8S": LocalPredictor,
        "AWS_SAGEMAKER": RemotePredictor,
        "AWS_SAGEMAKER_ASYNC": RemotePredictor,
        "AWS_LAMBDA": RemotePredictor,
        "AWS_EKS": RemotePredictor,
    }

    @staticmethod
    def get_predictor_obj(orchestrator: Orchestrator, *args, **kwargs) -> "DeployedPredictor.Type":
        """Factory method to get a predictor"""
        predictor_class = PredictorFactory.__predictor_classes.get(orchestrator)

        if predictor_class:
            return predictor_class(*args, **kwargs)
        raise NotImplementedError(f"The predictor of orchestrator:`{orchestrator}` is not implemented yet.")


class AITemplate:
    def __init__(
        self,
        input_schema: Schema,
        output_schema: Schema,
        configuration: Config,
        name: str,
        description: str,
        model_class: str,
        model_class_path: str = ".",
        requirements: Optional[Union[str, List[str]]] = None,
        code_path: Union[str, List[str]] = None,
        conda_env: Union[str, Dict] = None,
        artifacts: Optional[Dict] = None,
        client: Client = None,
        bucket_name: str = None,
        parameters=None,
    ):
        """Create an AI template for subsequently creating instances of AI objects

        Args:
            input_schema: Input Schema of the AI Template
            output_schema: Output Schema of the AI Template
            configuration: Configuration of the AI Template
            model_class: Name of instance of a subclass of :class:`~BaseModel`. This file will be moved to the container
                         Any dependencies of the class should be included in one of the following locations:

                            - The SuperAI library.
                            - Package(s) listed in the model's Conda environment, specified by
                              the ``conda_env`` parameter.
                            - One or more of the files specified by the ``code_path`` parameter.

                         Note: If the class is imported from another module, as opposed to being defined in the
                         ``__main__`` scope, the defining module should also be included in code_path parameter.
                         If the name of the instance (Eg. ModelName) is not same as file name of imported module
                         (Eg. some_file.py), please change the passed argument to reflect the correct module path as
                         'some_file.ModelName'
            model_class_path: Path to the location where :param model_class is present
            name: Name of the AI template
            description: Description of the AI template
            requirements: A list of PyPi requirements or the path to a requirements.txt file. If both this
                             parameter and the :param: conda_env is specified an ValueError is raised.
            code_path: A list of local filesystem paths to Python file dependencies (or directories containing file
                          dependencies). These files are *prepended* to the system path before the ai is loaded.
            conda_env: Either a dictionary representation of a Conda environment or the path to a Conda environment
                      yaml file. This describes the environment this AI should be run in. If ``ai_class`` is not
                      ``None``, the Conda environment must at least specify the dependencies contained in
                      :func:`get_default_conda_env()`. If `None`, the default :func:`get_default_conda_env()`
                      environment is added to the AI. The following is an *example* dictionary representation of a
                      Conda environment::

                        {
                            'name': 'superai-env',
                            'channels': ['defaults'],
                            'dependencies': [
                                'python=3.7.2',
                            ]
                        }
            artifacts: A dictionary containing ``<name, artifact_uri>`` entries. Remote artifact URIs are resolved
                      to absolute filesystem paths, producing a dictionary of ``<name, absolute_path>`` entries.
                      ``ai_class`` can reference these resolved entries as the ``artifacts`` property of the
                      ``context`` parameter in
                            - :func:`BaseModel.load_context() <superai.meta_ai.base.BaseModel.load_context>`, and
                            - :func:`BaseModel.predict() <superai.meta_ai.base.BaseModel.predict>`.

                      For example, consider the following ``artifacts`` dictionary::

                        {
                            "my_file": "s3://my-bucket/path/to/my/file"
                        }

                      In this case, the ``"my_file"`` artifact is downloaded from S3. The
                      ``ai_class`` can then refer to ``"my_file"`` as an absolute filesystem
                      path via ``context.artifacts["my_file"]``.

                      If ``None``, no artifacts are added to the model.
            client:
            bucket_name:
            parameters: Optional; Parameters to be passed to the model, could be the model architecture parameters,
                           or training parameters.
                           For example: parameters=MyModel.params_schema.parameters(conv_layers=None,
                                                                    num_conv_layers=None,
                                                                    filter_size=3,
                                                                    num_filters=32,
                                                                    strides=(1, 1),
                                                                    padding='valid',
                                                                    dilation_rate=(1, 1),
                                                                    conv_use_bias=True)
        """
        self.input_schema = input_schema
        self.output_schema = output_schema
        self.configuration = configuration
        self.requirements = requirements
        self.name = name
        self.description = description
        self.code_path = code_path
        self.conda_env = conda_env
        self.artifacts = artifacts
        self.client = (
            client
            if client
            else Client(
                api_key=load_api_key(),
                auth_token=load_auth_token(),
                id_token=load_id_token(),
            )
        )
        self.bucket_name = bucket_name or settings["meta_ai_bucket"]
        self.parameters = parameters
        if model_class is None:
            raise NotImplementedError(
                "Ludwig like implicit model creation is not implemented yet, please provide a model_class"
            )
        self.model_class = model_class
        self.model_class_path = model_class_path
        self.environs: Optional[EnvironmentFileProcessor] = None

    @classmethod
    def load_local(cls, load_path: str) -> "AITemplate":
        with open(os.path.join(load_path, "AITemplateSaveFile.json"), "r") as json_file:
            details = json.load(json_file)
        requirements = os.path.join(load_path, "requirements.txt") if details.get("requirements") is not None else None
        conda_env = os.path.join(load_path, "conda.yml") if details.get("conda_env") is not None else None
        code_path = details.get("code_path")
        artifacts = details.get("artifacts")
        model_class = details["model_class"]
        name = details["name"]
        description = details["description"]
        input_schema = Schema.from_json(details["input_schema"])
        output_schema = Schema.from_json(details["output_schema"])
        configuration = Config.from_json(details["configuration"])
        template = AITemplate(
            input_schema=input_schema,
            output_schema=output_schema,
            configuration=configuration,
            name=name,
            description=description,
            model_class=model_class,
            model_class_path=load_path,
            requirements=requirements,
            code_path=code_path,
            conda_env=conda_env,
            artifacts=artifacts,
        )
        environs = EnvironmentFileProcessor(os.path.abspath(load_path))
        environs.from_dict(details["environs"])
        template.environs = environs
        return template

    def save(self, version_save_path):
        if os.path.exists(f"{self.model_class}.py"):
            shutil.copy(f"{self.model_class}.py", os.path.join(version_save_path, f"{self.model_class}.py"))
        # copy requirements file and conda_env
        if self.conda_env is not None:
            if type(self.conda_env) == dict:
                with open(os.path.join(version_save_path, "environment.yml"), "w") as conda_file:
                    yaml.dump(self.conda_env, conda_file, default_flow_style=False)
            elif (
                type(self.conda_env) == str
                and os.path.exists(os.path.abspath(self.conda_env))
                and (self.conda_env.endswith(".yml") or self.conda_env.endswith(".yaml"))
            ):
                shutil.copy(os.path.abspath(self.conda_env), os.path.join(version_save_path, "environment.yml"))
            else:
                raise ValueError("Make sure conda_env is a valid path to a .yml file or a dictionary.")
        log.info("Copying all code_path content")
        if self.code_path is not None:
            assert (
                type(self.code_path) == list and type(self.code_path) != str
            ), "Types don't match for code_path, please pass a list of strings."
        if self.model_class_path != ".":
            self.code_path = (
                [self.model_class_path] + self.code_path if self.code_path is not None else [self.model_class_path]
            )
        if self.code_path is not None:
            for path in self.code_path:
                shutil.copytree(path, os.path.join(version_save_path, os.path.basename(path)))
        if self.requirements is not None:
            if type(self.requirements) == str and os.path.exists(os.path.abspath(self.requirements)):
                shutil.copy(os.path.abspath(self.requirements), os.path.join(version_save_path, "requirements.txt"))
            elif type(self.requirements) == list:
                with open(os.path.join(version_save_path, "requirements.txt"), "w") as requirements_file:
                    requirements_file.write("\n".join(self.requirements))
            else:
                raise ValueError(
                    "Make sure requirements is a list of requirements or valid path to requirements.txt file"
                )
        if self.artifacts is not None and "run" in self.artifacts:
            shutil.copy(os.path.abspath(self.artifacts["run"]), os.path.join(version_save_path, "setup.sh"))
        # create the environment file
        self.environs = EnvironmentFileProcessor(os.path.abspath(version_save_path), filename="environment")
        self.environs.add_or_update("MODEL_NAME", self.model_class)
        if os.path.exists(os.path.join(version_save_path, "environment.yml")):
            with open(os.path.join(version_save_path, "environment.yml"), "r") as env_yaml:
                try:
                    conda_env_yaml = yaml.safe_load(env_yaml)
                    self.environs.add_or_update("CONDA_ENV_NAME", conda_env_yaml.get("name", "env"))
                except yaml.YAMLError as exc:
                    log.error(exc)
        with open(os.path.join(version_save_path, "AITemplateSaveFile.json"), "w") as ai_template_writer:
            content = {
                "description": self.description,
                "input_schema": self.input_schema.to_json,
                "output_schema": self.output_schema.to_json,
                "configuration": self.configuration.to_json,
                "name": self.name,
                "requirements": os.path.join(version_save_path, "requirements.txt")
                if self.requirements is not None
                else None,
                "code_path": self.code_path,
                "conda_env": os.path.join(version_save_path, "conda.yml") if self.conda_env is not None else None,
                "model_class": self.model_class,
                "model_class_path": self.model_class_path,
                "artifacts": self.artifacts,
                "environs": self.environs.to_dict(),
            }
            json.dump(content, ai_template_writer, indent=1)

    def get_or_create_training_entry(self, app_id: str, model_id: str, properties: dict = {}):
        existing_template_id = self.client.get_training_templates(app_id, model_id)
        if len(existing_template_id):
            log.info(f"Found existing template {existing_template_id}")
            self.template_id = existing_template_id[0].id
        else:
            template_id = self.client.create_training_template_entry(app_id, model_id, properties)
            log.info(f"Created template : {template_id}")
            self.template_id = template_id
        return self.template_id


class AI:
    def __init__(
        self,
        ai_template: AITemplate,
        input_params: SchemaParameters,
        output_params: SchemaParameters,
        name,
        configuration: Optional[Config] = None,
        version: int = None,
        root_id: Optional[str] = None,
        description: Optional[str] = None,
        weights_path: str = None,
        overwrite=False,
        **kwargs,
    ):
        """Creates an AI with custom inference logic and optional data dependencies as a superai artifact.

        Args:
            input_params: Schema definition of the AI object input.
            output_params: Schema definition of the AI object output.
            name: Name of the AI. If the name already exists, an exception will be raised.
            version: AI integer version. If no version is specified the AI is set to version 1.
            root_id: Id of the root AI. Establishes the lineage of AIs.
                Is necessary when using `version` > 1.
            description: Optional; A free text description. Allows the user to describe the AI's intention.
            weights_path: Path to a file or directory containing model data. This is accessible in the
                          :func:`BaseModel.load_weights(weights_path) <superai.meta_ai.base.BaseModel.load_weights>
            **kwargs: Arbitrary keyword arguments
        """

        self.input_params = input_params
        self.output_params = output_params
        self.configuration = configuration
        self.ai_template = ai_template
        self.name = name
        self.version = version
        self.root_id = root_id
        self.bucket_name = self.ai_template.bucket_name
        self.description = description
        self.weights_path = weights_path
        self.code_path = self.ai_template.code_path
        self.conda_env = self.ai_template.conda_env
        self.requirements = self.ai_template.requirements
        self.artifacts = self.ai_template.artifacts
        self.parameters = self.ai_template.parameters
        self.client = self.ai_template.client

        self.overwrite = overwrite
        self.stage: Optional[str] = None  # stage is not set by default
        if "loaded" not in kwargs:
            # self.update_version_by_availability(kwargs.get("loaded", False))
            self._location = self.save(overwrite=self.overwrite)
        else:
            assert kwargs.get("location") is not None, "Location cannot be None while loading"
            self._location = kwargs.get("location")

        self.model_class_name = ai_template.model_class
        self.model_class_path = ai_template.model_class_path
        self.environs: "EnvironmentFileProcessor" = ai_template.environs
        self.is_weights_loaded = False

        self.container = None
        self._id = None
        self.model_class = None
        # ID of deployment serving predictions
        self.served_by: Optional[str] = None

    def _init_model_class(self):
        model_class_template = get_user_model_class(model_name=self.model_class_name, path=self.model_class_path)
        self.model_class: BaseModel = model_class_template(
            input_schema=self.ai_template.input_schema,
            output_schema=self.ai_template.output_schema,
            configuration=self.ai_template.configuration,
        )
        self.model_class.update_parameters(self.input_params, self.output_params)

    @property
    def id(self) -> Optional[str]:
        if not self._id:
            model = self.client.get_model_by_name_version(self.name, self.version)
            if model:
                self._id = model[0]["id"]
        return self._id

    @property
    def deployment_id(self) -> str:
        if self.served_by:
            return self.served_by
        else:
            # Legacy method to retrieve one deployment with matching model_id
            # Could lead to inconsistencies if multiple deployments are present
            deployment_list = self.client.list_deployments(self.id)
            if deployment_list:
                return deployment_list[0]["id"]

    @property
    def deployed(self) -> Optional[bool]:
        if self.id and self.deployment_id:
            deployment = self.client.get_deployment(self.served_by)
            if deployment:
                return True
        return False

    def __eq__(self, other):
        if not isinstance(other, AI):
            return False

        compare_keys = [
            "input_params",
            "output_params",
            "name",
            "version",
            "stage",
            "description",
            "artifacts",
            "parameters",
        ]
        comparisons = [self.__dict__[key] == other.__dict__[key] for key in compare_keys]
        return all(comparisons)

    def __str__(self):
        return (
            f"AI model : "
            f"\n\tName: {self.name} "
            f"\n\tVersion: {self.version}"
            f"\n\tDescription: {self.description}"
            f"\n\tStage: {self.stage}"
            f"\n\tId: {self.id}"
            f"\n\tDeployed: {self.deployed}"
        )

    def update_version_by_availability(self, loaded=False):
        existing_models = self.ai_template.client.get_model_by_name(self.name)
        if len(existing_models) and not loaded:
            if self.version in [x["version"] for x in existing_models]:
                latest_version: int = self.ai_template.client.get_latest_version_of_model_by_name(self.name)
                self.version = latest_version + 1
                log.info(
                    f"Found an existing model with name {self.name} in the database, "
                    f"incrementing version from the latest found version: {latest_version} -> {self.version}"
                )

    @classmethod
    def load_by_name_version(cls, name, version: int = None, stage: str = None) -> "AI":
        """
        Loads an AI by name. If the version or stage are specified that specific version will be loaded.

        Args:
            name: AI name.
            version: A version number.
            stage: The AI stage.

        Returns:
            AI object
        """
        raise NotImplementedError("Method not supported")

    @classmethod
    def load(cls, path: str, weights_path: str = None) -> "AI":
        """Loads an AI from a local or S3 path. If an S3 path is passed, the AI model will be downloaded from S3
        directly.

        Args:
            path
            weights_path
            if :param path is a valid path, the model will be loaded from the local path
            if :param path is a valid S3 path, i.e., s3://bucket/prefix/some_model_path, the model will be downloaded
            from S3. Manage S3 access using your AWS credentials.
            if :param path is a valid model path i.e., prefix is model://some_name/version, or model://some_name/stage
            then the database will be referenced to find the relevant model and loaded.

            A path can be considered valid only if there is an `AISaveFile.json` and `ai_model` file present.

        Returns:
            AI class of the loaded model
        """
        if path.startswith("s3://"):
            return cls.load_from_s3(path, weights_path)
        elif path.startswith("model://"):
            # get s3 path from db and load using cls.load_from_s3(path)
            name = path.split("model://")[-1].split("/")[0]
            log.info(f"Searching models with name `{name}` in database...")
            all_models: List[Dict] = list_models(name, raw=True, verbose=False)
            if len(all_models):
                match = re.search("(.*)/(.*)", path.split("model://" + name + "/")[-1])
                if match is not None:
                    stage, version = match.groups()
                    if stage and version:
                        selected = list(
                            filter(
                                lambda x: x["stage"] == stage and x["version"] == version,
                                all_models,
                            )
                        )
                        if len(selected):
                            s3_path = selected[0]["modelSavePath"]
                            weights_path = selected[0]["weightsPath"]
                            return cls.load_from_s3(s3_path, weights_path)
                        else:
                            raise ModelNotFoundError(
                                f"No model found for the given stage {stage} and version {version}"
                            )
                    log.info("Returning the latest version in models")
                    selected = all_models.sort(key=lambda x: x["version"], reverse=True)[0]
                    s3_path = selected["modelSavePath"]
                    weights_path = selected["weightsPath"]
                    return cls.load_from_s3(s3_path, weights_path)
                else:
                    # either stage or version is present
                    # check for version
                    ending = path.split(f"model://{name}/")[-1]
                    if cls.is_valid_version(ending):
                        s3_path = [entry for entry in all_models if int(entry["version"]) == int(ending)][0][
                            "modelSavePath"
                        ]
                    else:
                        stage = ending
                        selected_models: List[dict] = [entry for entry in all_models if entry["stage"] == stage]
                        model_entry = selected_models.sort(key=lambda x: x["version"], reverse=True)[0]
                        s3_path = model_entry["modelSavePath"]
                        weights_path = model_entry["weightsPath"]
                    return cls.load_from_s3(s3_path, weights_path)
            else:
                raise ModelNotFoundError(f"No models found for the given name : {name}")
        else:
            if os.path.exists(path):
                return cls.load_local(path, weights_path)
            else:
                raise ValueError("Invalid path, please ensure the path exists")

    @staticmethod
    def is_valid_version(version: str) -> bool:
        try:
            int(version)
            return True
        except ValueError:
            return False

    @classmethod
    def load_from_s3(cls, path: str, weights_path: Optional[str] = None) -> "AI":
        assert path.startswith("s3") and path.endswith(
            "AISavedModel.tar.gz"
        ), "Invalid path provided, should start with s3 and end with AISavedModel.tar.gz"
        log.info(f"Loading from '{path}' with weights in '{weights_path}'")
        s3 = boto3.client("s3")

        download_folder = os.path.join("/tmp", f"ai_contents_{int(time.time())}")
        if not os.path.exists(download_folder):
            os.makedirs(download_folder)
        log.info(f"Storing temporary files in {download_folder}")

        parsed_url = urlparse(path, allow_fragments=False)
        bucket_name = parsed_url.netloc
        path_to_object = parsed_url.path if not parsed_url.path.startswith("/") else parsed_url.path[1:]

        log.info(f"Downloading and unpacking AI object from bucket `{bucket_name}` and path `{path_to_object}`")
        s3.download_file(bucket_name, path_to_object, os.path.join(download_folder, "AISavedModel.tar.gz"))
        with tarfile.open(os.path.join(download_folder, "AISavedModel.tar.gz")) as tar:
            tar.extractall(path=os.path.join(download_folder, "AISavedModel"))
        return cls.load_local(
            load_path=os.path.join(download_folder, "AISavedModel", "ai"),
            weights_path=weights_path,
            download_folder=download_folder,
        )

    @classmethod
    def load_local(cls, load_path: str, weights_path: Optional[str] = None, **kwargs) -> "AI":
        """Loads AI model stored locally.

        Args:
            weights_path: Location of weights.
            load_path: The location of the AISave or any other matching folder.
            **kwargs: Arbitrary keyword arguments

        """
        log.info(f"Attempting to load model from {load_path}...")
        with open(os.path.join(load_path, "AISaveFile.json"), "r") as json_file:
            details = json.load(json_file)
        log.info("Verifying AISaveFile.json...")
        input_params = details["input_params"]
        output_params = details["output_params"]
        configuration = details["configuration"]
        name = details["name"]
        version = details.get("version")
        description = details.get("description")

        ai_template = AITemplate.load_local(load_path)

        if weights_path is not None:
            if weights_path.startswith("s3"):
                s3 = boto3.client("s3")
                download_folder = kwargs.get("download_folder", os.path.join("/tmp", f"ai_contents_{int(time.time())}"))
                if not os.path.exists(download_folder):
                    os.makedirs(download_folder)
                parsed_url = urlparse(weights_path, allow_fragments=False)
                bucket_name = parsed_url.netloc
                path_to_object = parsed_url.path if not parsed_url.path.startswith("/") else parsed_url.path[1:]
                log.info(f"Downloading and unpacking weights from bucket '{bucket_name}' and path '{path_to_object}'")
                s3.download_file(
                    bucket_name, path_to_object, os.path.join(download_folder, os.path.basename(weights_path))
                )
                if weights_path.endswith(".tar.gz"):
                    tar_weights = tarfile.open(os.path.join(download_folder, os.path.basename(weights_path)))
                    weights_folder_name = os.path.basename(weights_path).split(".tar.gz")[0]
                    weights_path = os.path.join(download_folder, weights_folder_name)
                    tar_weights.extractall(path=download_folder)
                    log.info(f"New weights path {weights_path}")
                    tar_weights.close()
                    shutil.rmtree(os.path.join(download_folder, os.path.basename(weights_path)))
            elif not os.path.exists(weights_path):
                raise ValueError(
                    f"Unexpected weights path provided {weights_path}. Please ensure its a s3 path or a local folder"
                )

        log.info(f"Loaded model from {load_path}")
        return AI(
            ai_template=ai_template,
            input_params=input_params,
            output_params=output_params,
            name=name,
            configuration=configuration,
            version=version,
            description=description,
            weights_path=weights_path,
            location=load_path,
            loaded=True,
        )

    def _create_database_entry(self, **kwargs):
        """Adds an entry in the meta AI database.

        Args:
            name: Name of the model.
            description: Description of model.
            version: Version of model.
            stage: Stage of model.
            metadata: Metadata associated with model.
            endpoint: Endpoint specified of the model.
            input_schema: Input schema followed by model.
            output_schema: Output schema followed by model.
            model_save_path: Location in S3 where the AISaveModel has to be placed.
            weights_path: Location of weights.
            visibility: Visibility of model. Default visibility: PRIVATE.
            root_id: Id of the root model. Establishes the lineage of the model.
            **kwargs: Arbitrary keyword arguments

        """
        log.info("Creating database entry...")
        if not self.id:
            self._id = self.client.add_model(**kwargs)
        else:
            # TODO: Add proper exception class
            raise Exception("Model is already registered in the Database.")
        return self.id

    def transition_ai_version_stage(
        self,
        stage: str,
        version: Optional[int] = None,
        archive_existing: bool = True,
    ):
        """Transitions an AI version number to the specified stage. [Mutable]

        Args:
            version: Optinal; AI version number. Can be defaulted to object version.
            stage: Transition AI version to new stage.
            archive_existing: When transitioning an AI version to a particular stage, this flag dictates whether
                                 all existing ai versions in that stage should be atomically moved to the “archived”
                                 stage. This ensures that at-most-one ai version exists in the target stage. This
                                 field is by default set to True.
        Returns:
             Updated AI version
        """
        # TODO: Archive existing
        sett_version = version if version is not None else self.version
        assert sett_version is not None, "Cannot transition ai version with None"
        try:
            # FIXME: handle empty version or stage to not overwrite entry in DB
            self.client.update_model(self.name, version=sett_version, stage=stage)
            log.info(f"Transitioned Model {self.name}:{sett_version} to stage:{stage}")
            self.stage = stage
            self.save(overwrite=True)
            self.push()
        except Exception as e:
            traceback.print_exc()
            log.info(f"Could not update model due to reason: {e}. \nMake sure you have pushed the model")
        return self

    def update_weights_path(self, weights_path: str):
        """Updates model weight file. Running this operation will increase the AI version.

        Args:
            weights_path: Path to a file or directory containing model data.
        """
        if self.version is not None:
            self.version += 1
        else:
            self.version = 1
        self.weights_path = weights_path
        self._location = self.save()
        # self.push()
        log.info(
            f"AI version updated to {self.version} after updating weights. New version created in {self._location}. "
            f"Make sure to AI.push to update in database"
        )
        # TODO Do we return a new AI object?

    def update_ai_class(self, model_class: str, model_class_path="."):
        """Updates the model_class. Running this operation will increase the AI version.

        Args:
            model_class: Name of a subclass of :class:`~BaseModel`.
            model_class_path: Path to :param model_class
        """
        if self.version is not None:
            self.version += 1
        else:
            self.version = 1
        self.model_class = None
        self.model_class_name = model_class
        self.model_class_path = model_class_path
        self._location = self.save(overwrite=True)
        # self.push()
        log.info(
            f"AI version updated to {self.version} after updating AI class. New version created in {self._location}. "
            f"Make sure to AI.push to update in database."
        )

    def update(
        self,
        version: Optional[int] = None,
        stage: Optional[str] = None,
        weights_path: Optional[str] = None,
        ai_class: Optional[str] = None,
        ai_class_path: str = ".",
    ):
        """
        Updates the AI.

        Args:
            version: New AI version number. If the version number already exists, this method will fail.
            stage: New AI stage.
            weights_path: New path to a file or directory containing model data.
            ai_class: Name of a subclass of :class:`~BaseModel`.
            ai_class_path: Path to :param ai_class_path
        """
        models = self.client.get_model_by_name(self.name)
        if version is None:
            log.info(f"Version not specified, checking version: {self.version}")
            version = self.version
        if len(models) == 0:
            raise Exception(
                f"No models found with the name: {self.name}:{self.version}. "
                f"Make sure you have 'AI.push'ed some models. "
            )
        elif version in [x["version"] for x in models]:
            raise Exception(
                f"Model name and version already exists. Try updating the version number. "
                f"Hint: Try version {self.client.get_latest_version_of_model_by_name(self.name) + 1}"
            )
        else:
            kwargs = {}
            if stage is not None:
                kwargs["stage"] = stage
            if weights_path is not None:
                kwargs["weights_path"] = weights_path
            if kwargs != {}:
                self.version = version
                self.weights_path = weights_path
                self._location = self.save()
                log.info(f"Updated model {self.name}:{self.version}. " f"Make sure to AI.push to update the database")
        if ai_class is not None:
            self.model_class = None
            self.model_class_name = ai_class
            self.model_class_path = ai_class_path
            self.save(overwrite=True)
        log.info("AI.update complete!")
        self.push()

    def predict(self, inputs):
        """Predicts from model_class and ensures that predict method adheres to schema in ai_definition.

        Args:
            inputs
        """
        if self.model_class is None:
            self._init_model_class()
        if not self.is_weights_loaded:
            if self.weights_path is not None:
                self.model_class.load_weights(self.weights_path)
            self.is_weights_loaded = True
        output = self.model_class.predict(inputs)
        result = EasyPredictions(output).value
        return result

    def save(self, path: str = ".AISave", overwrite: bool = False):
        """Saves the model locally.

        Args:
            path:
            overwrite:
        """
        save_path = os.path.join(path, self.name)
        if not os.path.exists(save_path):
            os.makedirs(save_path)

        if self.version is None:
            version = "0"
        else:
            version = str(self.version)
        version_save_path = os.path.join(save_path, version)
        if not os.path.exists(version_save_path):
            os.makedirs(version_save_path)
        elif overwrite:
            log.info(f"Removing existing content from path: {version_save_path}")
            shutil.rmtree(version_save_path)
            os.makedirs(version_save_path)

        self.ai_template.save(version_save_path)
        # save file information
        with open(os.path.join(version_save_path, "AISaveFile.json"), "w") as ai_file_writer:
            content = {
                "input_params": self.input_params.to_json,
                "output_params": self.output_params.to_json,
                "configuration": self.configuration,
                "name": self.name,
                "version": self.version,
                "stage": self.stage,
                "description": self.description,
                "weights_path": self.weights_path,
            }
            json.dump(content, ai_file_writer, indent=1)
        log.info(f"Saved model in {version_save_path}")
        return version_save_path

    @retry(Exception, tries=5, delay=0.5, backoff=1)
    def _upload_tarfile(self, upload_info, path):
        log.info(f"Uploading file at {path} to {upload_info}")
        with open(path, "rb") as f:
            files = {"file": (path, f)}
            upload_response = requests.post(upload_info["url"], data=upload_info["fields"], files=files)
        if upload_response.status_code == 204:
            log.info("Upload complete successfully")
        else:
            raise Exception(
                f"Could not upload file {upload_response.status_code}: {upload_response.reason}\n"
                f"{upload_response.text} "
            )

    @staticmethod
    def _compress_folder(path_to_tarfile: str, location: str):
        """Helper to compress a directory into a tarfile

        Args:
            path_to_tarfile: Path to file to be generated after compressing
            location: Path to folder to be compressed
        """

        assert path_to_tarfile.endswith(".tar.gz"), "Should be a valid tarfile path"
        with tarfile.open(path_to_tarfile, "w:gz") as tar:
            for ff in os.listdir(location):
                tar.add(os.path.join(location, ff), ff)
            # tar.list()
        assert os.path.exists(path_to_tarfile)

    def push(self, update_weights: bool = False, weights_path: Optional[str] = None, overwrite=False) -> str:
        """Pushes the saved model to S3, creates an entry and enters the S3 URI in the database.

        Args:
            update_weights: Update weights in s3 or not
            weights_path: Path to weights in s3
            overwrite: Overwrite existing entry
        """
        if self.id:
            if not overwrite:
                log.warning("Model already exists in the DB and overwrite is not set.")
                return self.id
            else:
                if settings.current_env == "prod":
                    confirmed = Confirm.ask(
                        "Do you [bold]really[/bold] want to push weights for a [red]production[/red] AI? This can negatively impact Data Programs relying on the existing AI."
                    )
                    if not confirmed:
                        log.warning("Aborting push")
                        raise ModelDeploymentError("Push aborted by User")
        else:
            if self.version > 1:
                self.root_id = self.root_id or find_root_model(self.name, self.client)
                if self.root_id is None:
                    raise ValueError(
                        "AIs with version > 1 must have a root_id. This should be the ID of the AI with version=1."
                    )
            self._id = self._create_database_entry(
                name=self.name,
                version=self.version,
                description=self.description,
                metadata=self.artifacts,
                input_schema=self.input_params.to_json,
                output_schema=self.output_params.to_json,
                root_id=self.root_id,
            )

        modelSavePath = self._upload_model_folder(self.id)
        weights = self._upload_weights(self.id, update_weights, weights_path)
        self.client.update_model(self.id, weights_path=weights, model_save_path=modelSavePath)
        return self.id

    def _upload_model_folder(self, idx: str) -> str:
        s3_client = boto3.client("s3")
        path_to_tarfile = os.path.join(self._location, "AISavedModel.tar.gz")
        log.info(f"Compressing AI folder at {self._location}")
        self._compress_folder(path_to_tarfile, self._location)
        object_name = os.path.join(MODEL_ARTIFACT_PREFIX_S3, idx, self.name, str(self.version), "AISavedModel.tar.gz")
        with open(path_to_tarfile, "rb") as f:
            s3_client.upload_fileobj(f, self.bucket_name, object_name)
        modelSavePath = os.path.join("s3://", self.bucket_name, object_name)
        log.info(f"Uploaded AI object to '{modelSavePath}'")
        return modelSavePath

    def _upload_training_data(self, local_directory: str, training_id: str) -> str:
        training_data_path = os.path.join("training/data", training_id)
        # TODO: replace s3 push with push via signed url or similar
        local_directory_path = Path(local_directory)
        upload_dir(local_directory_path, training_data_path, self.bucket_name, prefix="/")
        log.info(f"Uploaded Training data to {training_data_path}.")
        return training_data_path

    def _upload_weights(self, idx: str, update_weights: bool, weights_path: Optional[str]) -> Optional[str]:
        weights: Optional[str] = None
        if self.weights_path is not None and update_weights:
            if self.weights_path.startswith("s3"):
                weights = self.weights_path
            elif os.path.exists(self.weights_path):
                if os.path.isdir(self.weights_path):
                    upload_object_name = os.path.join(MODEL_ARTIFACT_PREFIX_S3, MODEL_WEIGHT_INFIX_S3, idx)
                else:
                    raise ValueError("weights_path must be a directory")
                log.info("Uploading weights...")
                upload_dir(self.weights_path, upload_object_name, self.bucket_name, prefix="/")
                weights = f"s3://{os.path.join(self.bucket_name, upload_object_name)}"
                log.info(f"Uploaded weights to '{weights}'")
            else:
                log.warn("Weights path provided were invalid, weights will not be uploaded")
        else:
            log.warn("No weights path given, weights will not be uploaded")
            if weights_path is not None:
                weights = weights_path
        return weights

    def deploy(
        self,
        orchestrator: "Orchestrator" = Orchestrator.LOCAL_DOCKER,
        skip_build: bool = False,
        properties: Optional[dict] = None,
        enable_cuda: bool = False,
        enable_eia: bool = False,
        redeploy: bool = False,
        **kwargs,
    ) -> "DeployedPredictor.Type":
        """Here we need to create a docker container with superai-sdk installed. Then we need to create a server
        script and prediction script, which basically calls ai.predict.
        We need to pass the ai model inside the image, install conda env or requirements.txt as required.
        Serve local: run the container locally using Cli (in a separate thread)
        Serve sagemaker: create endpoint after pushing container to ECR

        Args:
            orchestrator: Which orchestrator to be used to deploy.
            skip_build: Skip building
            enable_cuda: Create CUDA-Compatible image
            enable_eia: Create Elastic Inference compatible image
            properties: Optional dictionary with properties for instance creation.
                Possible values (with defaults) are:
                    "sagemaker_instance_type": "ml.m5.xlarge"
                    "sagemaker_initial_instance_count": 1
                    "sagemaker_accelerator_type": "ml.eia2.large" (None by default)
                    "lambda_memory": 256
                    "lambda_timeout": 30
            redeploy: Allow un-deploying existing deployment and replacing it.

            # Hidden kwargs
            worker_count: Number of workers to use for serving with Sagemaker.
            ai_cache: Cache of ai objects for a lambda, 5 by default considering the short life of a lambda function
            build_all_layers: Perform a fresh build of all layers
            envs: Pass custom environment variables to the deployment. Should be a dictionary like
                  {"LOG_LEVEL": "DEBUG", "OTHER": "VARIABLE"}
            download_base: Always download the base image to get the latest version from ECR
        """
        if redeploy and settings.current_env == "prod":
            confirmed = Confirm.ask(
                "Do you [bold]really[/bold] want to redeploy a [red]production[/red] AI? This can negatively impact Data Programs relying on the existing AI."
            )
            if not confirmed:
                log.warning("Aborting deployment")
                raise ModelDeploymentError("Deployment aborted by User")

        is_lambda_orchestrator = orchestrator in [Orchestrator.LOCAL_DOCKER_LAMBDA, Orchestrator.AWS_LAMBDA]
        # Updating environs before image builds
        for key, value in kwargs.get("envs", {}).items():
            self.environs.add_or_update(key, value)
        if orchestrator in [
            Orchestrator.LOCAL_DOCKER,
            Orchestrator.LOCAL_DOCKER_LAMBDA,
            Orchestrator.AWS_LAMBDA,
            Orchestrator.AWS_SAGEMAKER,
            Orchestrator.AWS_SAGEMAKER_ASYNC,
        ]:
            self._prepare_dependencies(
                worker_count=kwargs.get("worker_count", 1),
                lambda_mode=is_lambda_orchestrator,
                ai_cache=kwargs.get("ai_cache", 5),
            )
            if not skip_build:
                self.build_image_s2i(
                    self.name,
                    str(self.version),
                    enable_cuda=enable_cuda,
                    enable_eia=enable_eia,
                    lambda_mode=is_lambda_orchestrator,
                    from_scratch=kwargs.get("build_all_layers", False),
                    always_download=kwargs.get("download_base", False),
                )
        elif orchestrator in [Orchestrator.AWS_EKS, Orchestrator.LOCAL_DOCKER_K8S]:
            if properties is None:
                properties = {}
            k8s_config = self._prepare_k8s_dependencies(enable_cuda=enable_cuda, properties=properties, **kwargs)
            properties["kubernetes_config"] = k8s_config
            if not skip_build:
                self.build_image_s2i(
                    self.name,
                    str(self.version),
                    enable_cuda=enable_cuda,
                    enable_eia=enable_eia,
                    lambda_mode=is_lambda_orchestrator,
                    k8s_mode=True,
                    from_scratch=kwargs.get("build_all_layers", False),
                    always_download=kwargs.get("download_base", False),
                )
        elif orchestrator in [Orchestrator.GCP_KS]:
            raise NotImplementedError()
        else:
            raise ValueError(f"Invalid Orchestrator, should be one of {[e for e in Orchestrator]}")
        # build kwargs
        kwargs = {}
        if orchestrator in [Orchestrator.LOCAL_DOCKER, Orchestrator.LOCAL_DOCKER_LAMBDA, Orchestrator.LOCAL_DOCKER_K8S]:
            kwargs["image_name"] = f"{self.name}:{self.version}"
            kwargs["weights_path"] = self.weights_path
            kwargs["lambda_mode"] = is_lambda_orchestrator
            kwargs["k8s_mode"] = orchestrator == Orchestrator.LOCAL_DOCKER_K8S
        else:
            if not skip_build:
                ecr_image_name = self.push_model(self.name, str(self.version))
            else:
                ecr_image_name = get_ecr_image_name(self.name, self.version)
            kwargs = dict(client=self.client, name=self.name, version=str(self.version))
            if self.id is None:
                raise LookupError(
                    "Cannot establish id, please make sure you push the AI model to create a database entry"
                )

            self.served_by = self.served_by or self.client.get_model(self.id)["served_by"]
            existing_deployment = self.client.get_deployment(self.served_by) if self.served_by else None
            log.info(f"Existing deployments : {existing_deployment}")
            if existing_deployment is None or "status" not in existing_deployment:

                # check if weights are present in the database
                models = self.client.get_model_by_name_version(self.name, self.version, verbose=True)
                model = models[0]
                log.info(f"Model attributes: {model}")
                assert (
                    model["weights_path"] is not None
                ), "Weights Path cannot be None in the database for the deployment to finish"

                self.served_by = self.client.deploy(
                    self.id, ecr_image_name, deployment_type=orchestrator.value, properties=properties
                )
                self.client.update_model(self.id, served_by=self.served_by)
            else:
                if redeploy:
                    self.undeploy()
                else:
                    raise Exception(
                        "Deployment with this version already exists. Try undeploy first or set `redeploy=True`."
                    )
                self.client.set_image(deployment_id=self.deployment_id, ecr_image_name=ecr_image_name)
                if properties:
                    self.client.set_deployment_properties(deployment_id=self.deployment_id, properties=properties)
                self.client.set_deployment_status(deployment_id=self.deployment_id, target_status="ONLINE")

            kwargs["id"] = self.deployment_id
        # get predictor
        predictor_obj: DeployedPredictor.Type = PredictorFactory.get_predictor_obj(orchestrator=orchestrator, **kwargs)

        return predictor_obj

    def undeploy(self) -> Optional[bool]:
        if self.id:
            if self.deployed:
                passed = self.client.undeploy(self.deployment_id)
                if passed:
                    log.info("Endpoint deletion request succeeded.")
                # TODO: Add wait for deployment status to be OFFLINE
                return passed
            else:
                log.info("Deployment already offline.")
                return True
        else:
            log.info("No ID found. Is the model registered in the Database?")
            return None

    @classmethod
    def load_api(cls, model_path, orchestrator: Orchestrator) -> "DeployedPredictor.Type":
        ai_object: Optional["AI"] = cls.load(model_path)
        assert ai_object is not None, "Need an AI object associated with the class to load"
        # TODO: If we pass a model_path like `model://...`, check if there is an endpoint entry, and check
        #  if endpoint is serving.
        # if endpoint is not serving:
        return ai_object.deploy(orchestrator)

    def _prepare_dependencies(
        self,
        worker_count: int = 1,
        lambda_mode: bool = True,
        ai_cache: int = 32,
        dockerd_entrypoint: str = "dockerd-entrypoint.py",
    ) -> None:

        with open(os.path.join(self._location, "handler.py"), "w") as handler_file:
            scripts_content = create_model_handler(self.ai_template.model_class, ai_cache, lambda_mode)
            handler_file.write(scripts_content)
        if not lambda_mode:
            with open(os.path.join(self._location, dockerd_entrypoint), "w") as entry_point_file:
                entry_point_file_content = create_model_entrypoint(worker_count)
                entry_point_file.write(entry_point_file_content)

    @staticmethod
    def _get_base_name(
        enable_eia: bool = False,
        lambda_mode: bool = False,
        enable_cuda: bool = False,
        k8s_mode: bool = False,
        version: int = 1,
    ) -> str:
        """Get Base Image given the configuration. By default the sagemaker CPU image name will be returned.

        Args:
            enable_eia: Return Elastic Inference base image name
            lambda_mode: Return Lambda base image name
            enable_cuda: Return GPU image names
            k8s_mode: Return Kubernetes base image names

        Return:
            String image name
        """
        if enable_eia and (lambda_mode or enable_cuda or k8s_mode):
            raise ValueError("Cannot use EIA with other options")
        if enable_cuda and lambda_mode:
            raise ValueError("Cannot use CUDA with Lambda")

        base_image = "superai-model-s2i-python3711"

        if enable_cuda:
            base_image += "-gpu"
        elif enable_eia:
            base_image += "-eia"
        else:
            base_image += "-cpu"

        if settings.current_env == "dev":
            base_image += "-internal"

        if lambda_mode:
            base_image += "-lambda"
        elif k8s_mode:
            base_image += "-seldon"

        return f"{base_image}:{version}"

    def _track_changes(self):
        # check the hash, if it doesn't exist, create one
        files = []
        if self.requirements:
            files.append("requirements.txt")
        if self.conda_env:
            files.append("environment.yml")
        if self.artifacts:
            if "run" in self.artifacts:
                files.append("setup.sh")
        changes_in_build = False
        cache_folder = os.path.join(settings.path_for(), "cache", self.name, str(self.version))
        if not os.path.exists(cache_folder):
            log.info(f"Creating cache folder {cache_folder}")
            os.makedirs(cache_folder)
        hash_file = os.path.join(cache_folder, ".hash.json")
        if not os.path.exists(hash_file):
            with open(hash_file, "w") as f_hash:
                json.dump({}, f_hash)
        with open(hash_file, "r") as f_hash:
            hash_content = json.load(f_hash)
        new_hash = hash_content
        for file in files:
            file_hash = hashlib.sha256(open(os.path.abspath(file), "rb").read()).hexdigest()
            if file_hash != hash_content.get(file):
                changes_in_build = True
            new_hash[file] = file_hash
        with open(hash_file, "w") as f_hash:
            json.dump(new_hash, f_hash)
        return changes_in_build

    def build_image_s2i(
        self,
        image_name: str,
        version_tag: str = "latest",
        enable_cuda: bool = False,
        enable_eia: bool = False,
        lambda_mode: bool = False,
        k8s_mode: bool = False,
        from_scratch: bool = False,
        always_download=False,
    ) -> None:
        """
        Build the image using s2i

        Args:
            image_name: Name of the image to be built
            version_tag: Version tag of the image
            enable_cuda: Enable CUDA in the images
            enable_eia: Generate elastic inference compatible image
            lambda_mode: Generate AWS Lambda compatible image
            k8s_mode: Generate Kubernetes compatible image
            from_scratch: Generate all layers from the scratch
            always_download: Always download the base image
        """
        start = time.time()
        cwd = os.getcwd()
        os.chdir(self._location)
        changes_in_build = self._track_changes()

        client = get_docker_client()
        base_image = self._get_base_name(enable_eia, lambda_mode, enable_cuda, k8s_mode)
        if always_download:
            log.info(f"Downloading newest base image {base_image}...")
            self._download_base_image(base_image, client)
        try:
            _ = client.images.get(base_image)
            log.info(f"Base image '{base_image}' found locally.")
        except ImageNotFound:
            log.info(f"Base image '{base_image}' not found locally, downloading...")
            self._download_base_image(base_image, client)
        if shutil.which("s2i") is None:
            raise ModuleNotFoundError(
                "s2i is not installed. Please install the package using "
                "'brew install source-to-image' or read installation instructions at "
                "https://github.com/openshift/source-to-image#installation."
            )
        if changes_in_build:
            from_scratch = True
        else:
            try:
                image = client.images.get(f"{image_name}-pip-layer:{version_tag}")
                log.info(f"No change in pip layer. Reusing old layers from image {image.id}...")
            except ImageNotFound:
                log.info("Pip layer image not found, rebuilding")
                from_scratch = True
        if from_scratch:
            self.environs.delete("BUILD_PIP")
            self._create_prediction_image_s2i(
                base_image_tag=base_image,
                image_tag=f"{image_name}-pip-layer:{version_tag}",
                client=client,
                lambda_mode=lambda_mode,
                k8s_mode=k8s_mode,
            )
        # fallback if the above environment adding is not run
        self.environs.add_or_update("BUILD_PIP=false")
        self._create_prediction_image_s2i(
            base_image_tag=f"{image_name}-pip-layer:{version_tag}",
            image_tag=f"{image_name}:{version_tag}",
            client=client,
            lambda_mode=lambda_mode,
            k8s_mode=k8s_mode,
        )
        log.info(f"Built main container `{image_name}:{version_tag}`")
        log.info(f"Time taken to build: {time.time() - start:.2f}s")
        os.chdir(cwd)

    def _create_prediction_image_s2i(self, base_image_tag, image_tag, client, lambda_mode=False, k8s_mode=False):
        """
        Extracted method which creates the prediction image

        Args:
            base_image_tag: Identifier of the base image name for building image
            image_tag: Identifier of the image name to be built
            client: Docker client
            lambda_mode: Lambda mode
            k8s_mode: Kubernetes mode
        """
        self.environs.add_or_update("SUPERAI_CONFIG_ROOT", "/tmp/.superai")
        if lambda_mode:
            self.environs.add_or_update("LAMBDA_MODE=true")
        elif k8s_mode:
            self.environs.add_or_update("SERVICE_TYPE=MODEL")
            self.environs.add_or_update("PERSISTENCE=0")
            self.environs.add_or_update("API_TYPE=REST")
            self.environs.add_or_update("SELDON_MODE=true")
        command = (
            f"s2i build -E {self.environs.location} "
            f"-v {os.path.join(os.path.expanduser('~'), '.aws')}:/root/.aws "
            f"-v {os.path.join(os.path.expanduser('~'), '.superai')}:/root/.superai "
            f"-v {os.path.join(os.path.expanduser('~'), '.canotic')}:/root/.canotic "
            f"--incremental=True . "
            f"{base_image_tag} {image_tag}"
        )
        return self._system(command)

    @staticmethod
    def _download_base_image(base_image: str, client: DockerClient) -> None:
        """
        Download the base image from ECR
        Args:
            base_image: Name of the base image
            client: Docker client
        """
        region = boto3.Session().region_name
        account_id = boto3.client("sts").get_caller_identity()["Account"]
        ecr_image_name = f"{account_id}.dkr.ecr.{region}.amazonaws.com/{base_image}"
        log.info(f"Base image not found. Downloading from ECR '{ecr_image_name}'")
        log.info("Logging in to ECR...")
        os.system(f"$(aws ecr get-login --region {region} --no-include-email)")
        os.system(f"docker pull {ecr_image_name}")
        log.info(f"Re-tagging image to '{base_image}'")
        client.images.get(f"{ecr_image_name}").tag(base_image)

    @staticmethod
    def _system(command):
        log.info(f"Running '{command}'")
        process = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE)
        (out, _) = process.communicate()
        if process.returncode != 0:
            raise subprocess.CalledProcessError(process.returncode, command, output=out)
        return process.returncode

    def push_model(self, image_name: Optional[str] = None, version: Optional[str] = None) -> str:
        """Push model in ECR, involves tagging and pushing.
        Note that your default AWS credentials will be used for this.

        Args:
            image_name: of local build image
            version: Version tag

        Returns:
            New tag of container pushed to ECR
        """
        if image_name is None:
            image_name = self.name
        if version is None:
            version = str(self.version)
        id = self.id
        if id is None:
            raise Exception("No ID found. AI needs to be registered  via `push()` first.")
        return push_image(image_name=image_name, model_id=id, version=version)

    def train(
        self,
        model_save_path,
        training_data,
        test_data=None,
        production_data=None,
        weights_path=None,
        encoder_trainable: bool = True,
        decoder_trainable: bool = True,
        hyperparameters: Optional[HyperParameterSpec] = None,
        model_parameters: Optional[ModelParameters] = None,
        callbacks=None,
        validation_data=None,
        train_logger=None,
    ):
        """Please fill hyperparameters and model parameters accordingly.

        Args:
            model_save_path: Save location of model
            training_data: Path to training data
            validation_data: Path to validation data
            test_data: Path to test data
            production_data: Path to production data
            callbacks: List of callbacks to be used
            weights_path: Path to existing weights to be trained on
            encoder_trainable: Whether encoder is trainable or not
            decoder_trainable: Whether decoder is trainable or not
            hyperparameters: Hyperparameters for training
            model_parameters: Model parameters for training
            train_logger: Logger for training
        """
        if self.model_class is None:
            self._init_model_class()
        if train_logger is not None:
            self.model_class.update_logger_path(train_logger)
        else:
            self.model_class.update_logger_path(
                os.path.join(self._location, "logs/fit/" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")),
            )
        log.info(f"If tensorboard callback is present, logging in {self.model_class.logger_dir}")
        train_instance = self.model_class.train(
            model_save_path=model_save_path,
            training_data=training_data,
            validation_data=validation_data,
            test_data=test_data,
            production_data=production_data,
            weights_path=weights_path,
            encoder_trainable=encoder_trainable,
            decoder_trainable=decoder_trainable,
            hyperparameters=hyperparameters,
            model_parameters=model_parameters,
            callbacks=callbacks,
        )

    def _prepare_k8s_dependencies(self, enable_cuda=False, properties=None, **kwargs) -> dict:
        """
        Prepare dependencies like kubernetes CRD
        Args:
            enable_cuda: Use CUDA in the CRD or not
            num_workers: Number of workers to run inside the pod
            maxReplicas: Maximum number of allowed replicas
            targetAverageUtilization: Estimated utilization to trigger autoscaling
            gpuTargetAverageUtilization: Estimated utilization to trigger autoscaling for GPU
            volumeMountName: Name of the volume to be mounted
            mountPath: folder_name to be used for mounting. Please note that this should be the path
            gpuBaseUtilization: GPU Base utilization

        Return:
             Dictionary of the CRD. This is saved in the save location as well.
        """
        if properties is None:
            properties = {}
        kubernetes_config = properties.get("kubernetes_config", {})
        kubernetes_config.update(
            dict(
                maxReplicas=kwargs.get("maxReplicas", kubernetes_config.get("maxReplicas", 5)),
                targetAverageUtilization=kwargs.get(
                    "targetAverageUtilization", kubernetes_config.get("targetAverageUtilization", 0.5)
                ),
                gpuTargetAverageUtilization=kwargs.get(
                    "gpuTargetAverageUtilization", kubernetes_config.get("gpuTargetAverageUtilization", 60)
                ),
                volumeMountName=kwargs.get("volumeMountName", kubernetes_config.get("volumeMountName", "efs-vpc")),
                mountPath=kwargs.get("mountPath", kubernetes_config.get("mountPath", "/shared")),
                numThreads=kwargs.get("worker_count", kubernetes_config.get("worker_count", 1)),
                enableCuda=enable_cuda,
            )
        )
        with open(os.path.join(self._location, f"{self.name}_config.json"), "w") as wfp:
            json.dump(kubernetes_config, wfp, indent=2)
        return kubernetes_config

    def training_deploy(
        self,
        orchestrator: "TrainingOrchestrator" = TrainingOrchestrator.LOCAL_DOCKER_K8S,
        training_data_dir: Optional[Union[str, Path]] = None,
        skip_build: bool = False,
        properties: Optional[dict] = None,
        enable_cuda: bool = False,
        training_parameters: Optional[TrainingParameters] = None,
        **kwargs,
    ):
        """Here we need to create a docker container with superai-sdk installed. Then we will create a run script

        Args:
            orchestrator: Which training orchestrator to be used to deploy.
            skip_build: Skip building
            enable_cuda: Create CUDA-Compatible image
            properties: An optional dictionary with properties for instance creation.
            training_data_dir: Path to training data
            training_parameters: A TrainingParameters object used for all training parameters to be passed to
                                BaseModel train method

            # Hidden kwargs
            worker_count: Number of workers to use for serving with Sagemaker.
            ai_cache: Cache of ai objects for a lambda, 5 by default considering the short life of a lambda function
            build_all_layers: Perform a fresh build of all layers
            envs: Pass custom environment variables to the deployment. Should be a dictionary like
                  {"LOG_LEVEL": "DEBUG", "OTHER": "VARIABLE"}
            download_base: Always download the base image to get the latest version from ECR
        """
        for key, value in kwargs.get("envs", {}).items():
            self.environs.add_or_update(key, value)
        if orchestrator in [TrainingOrchestrator.AWS_EKS, TrainingOrchestrator.LOCAL_DOCKER_K8S]:
            if properties is None:
                properties = {}
            k8s_config = self._prepare_k8s_dependencies(enable_cuda=enable_cuda, properties=properties, **kwargs)
            properties["kubernetes_config"] = k8s_config
            if not skip_build:
                self.build_image_s2i(
                    self.name,
                    str(self.version),
                    enable_cuda=enable_cuda,
                    enable_eia=False,
                    lambda_mode=False,
                    k8s_mode=True,
                    from_scratch=kwargs.get("build_all_layers", False),
                    always_download=kwargs.get("download_base", False),
                )
        else:
            # TODO: Add support for local training
            raise ValueError(f"Invalid Orchestrator, should be one of {[e for e in TrainingOrchestrator]}")
        # build kwargs
        kwargs = {}
        if orchestrator in [TrainingOrchestrator.LOCAL_DOCKER_K8S]:
            kwargs["image_name"] = f"{self.name}:{self.version}"
            kwargs["weights_path"] = self.weights_path
            kwargs["k8s_mode"] = orchestrator == TrainingOrchestrator.LOCAL_DOCKER_K8S
        else:
            if not skip_build:
                image_name = self.push_model(self.name, str(self.version))
            else:
                image_name = get_ecr_image_name(self.name, self.version)
            self.client.update_model(self.id, image=image_name, trainable=True)
            if self.id is None:
                raise LookupError(
                    "Cannot establish id, please make sure you push the AI model to create a database entry"
                )
            if training_parameters:
                loaded_parameters = json.loads(training_parameters.to_json())
            else:
                # TODO: load default parameters from AI
                loaded_parameters = {}
            # check if we have a training data directory
            instance_id = self.client.create_training_entry(
                model_id=self.id, properties=loaded_parameters, starting_state="STOPPED"
            )
            if training_data_dir is not None:
                self._upload_training_data(training_data_dir, training_id=instance_id)
            else:
                # TODO: Add alternative logic to inject app data
                log.warning("No training data directory provided, skipping upload")

            self.client.update_training_instance(instance_id, state="STARTING")
            log.info(f"Create training instance : {instance_id}")
