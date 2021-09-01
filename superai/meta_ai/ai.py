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
import sys
import tarfile
import time
import traceback
from typing import Dict, List, TYPE_CHECKING, Union, Optional
from urllib.parse import urlparse

import boto3  # type: ignore
import docker
import requests
import yaml
from docker.errors import ImageNotFound
from jinja2 import Template

from superai import Client
from superai import settings
from superai.exceptions import ModelNotFoundError
from superai.log import logger
from superai.meta_ai.ai_helper import prepare_dockerfile_string, get_user_model_class, list_models
from superai.meta_ai.deployed_predictors import LocalPredictor, DeployedPredictor, AWSPredictor
from superai.meta_ai.dockerizer import push_image
from superai.meta_ai.parameters import HyperParameterSpec, ModelParameters, Config
from superai.meta_ai.schema import Schema, SchemaParameters, EasyPredictions
from superai.meta_ai.template_contents import (
    runner_script_s2i,
    server_script,
    lambda_script,
)
from superai.utils import retry, load_api_key, load_auth_token, load_id_token

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
    MINIKUBE = "MINIKUBE"
    AWS_SAGEMAKER = "AWS_SAGEMAKER"
    AWS_LAMBDA = "AWS_LAMBDA"
    AWS_EKS = "AWS_EKS"
    GCP_KS = "GCP_KS"


class PredictorFactory(object):
    __predictor_classes = {
        "LOCAL_DOCKER": LocalPredictor,
        "LOCAL_DOCKER_LAMBDA": LocalPredictor,
        "AWS_SAGEMAKER": AWSPredictor,
        "AWS_LAMBDA": AWSPredictor,
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
        folder_name: str = "meta_ai_models",
        bucket_name: str = "canotic-ai",
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
                                'cloudpickle==0.5.8'
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
            folder_name:
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
        self.folder_name = folder_name
        self.bucket_name = bucket_name
        self.parameters = parameters
        if model_class is None:
            raise NotImplementedError(
                "Ludwig like implicit model creation is not implemented yet, please provide a model_class"
            )
        self.model_class = model_class
        self.model_class_path = model_class_path

    @classmethod
    def load_local(cls, load_path: str) -> "AITemplate":
        with open(os.path.join(load_path, "AITemplateSaveFile.json"), "r") as json_file:
            details = json.load(json_file)
        requirements = os.path.join(load_path, "requirements.txt") if details.get("requirements") is not None else None
        conda_env = os.path.join(load_path, "conda.yml") if details.get("conda_env") is not None else None
        code_path = details.get("code_path")
        artifacts = details.get("artifacts")
        model_class = details.get("model_class")
        name = details["name"]
        description = details["description"]
        input_schema = Schema.from_json(details["input_schema"])
        output_schema = Schema.from_json(details["output_schema"])
        configuration = Config.from_json(details["configuration"])
        return AITemplate(
            input_schema=input_schema,
            output_schema=output_schema,
            configuration=configuration,
            model_class=model_class,
            model_class_path=load_path,
            name=name,
            description=description,
            requirements=requirements,
            code_path=code_path,
            conda_env=conda_env,
            artifacts=artifacts,
        )

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
                and os.path.exists(self.conda_env)
                and (self.conda_env.endswith(".yml") or self.conda_env.endswith(".yaml"))
            ):
                shutil.copy(self.conda_env, os.path.join(version_save_path, "environment.yml"))
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
        with open(os.path.join(version_save_path, "environment"), "w") as environment_file:
            content = [f"MODEL_NAME={self.model_class}"]
            if os.path.exists(os.path.join(version_save_path, "environment.yml")):
                with open(os.path.join(version_save_path, "environment.yml"), "r") as env_yaml:
                    try:
                        conda_env_yaml = yaml.safe_load(env_yaml)
                        content.append(f"CONDA_ENV_NAME={conda_env_yaml.get('name', 'env')}")
                    except yaml.YAMLError as exc:
                        log.error(exc)
            environment_file.write("\n".join(content))
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
            }
            json.dump(content, ai_template_writer, indent=1)


class AI:
    def __init__(
        self,
        ai_template: AITemplate,
        input_params: SchemaParameters,
        output_params: SchemaParameters,
        name,
        configuration: Optional[Config] = None,
        version: int = None,
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
        self.folder_name = self.ai_template.folder_name
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
        self.is_weights_loaded = False

        self.container = None
        self._id = None
        self.model_class = None

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
    def deployed(self) -> Optional[bool]:
        if self.id:
            deployment = self.client.get_deployment(self.id)
            if deployment and deployment.status == "ONLINE":
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
        existing_models: List[Dict[str, str]] = self.ai_template.client.get_model_by_name(self.name)
        if len(existing_models) and not loaded:
            if self.version in [x["version"] for x in existing_models]:
                latest_version: int = self.ai_template.client.get_latest_version_of_model_by_name(self.name)
                self.version = latest_version + 1
                log.info(
                    f"Found an existing for the name and model in the database, "
                    f"setting version to the latest version version: {self.version}"
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
        """Loads an AI from a local or S3 path. If an S3 path is passed, the AI model will be downloaded from S3 directly.

        Args:
            path
            weights_path
            if :param path is a valid path, the model will be loaded from the local path
            if :param path is a valid S3 path, i.e., s3://bucket/prefix/some_model_path, the model will be downloaded from
            S3. Manage S3 access using your AWS credentials.
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
            load_path=os.path.join(download_folder, "AISavedModel"),
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
            **kwargs: Arbitrary keyword arguments
        """
        log.info("Creating database entry...")
        if not self.id:
            self._id = self.client.add_model_full_entry(**kwargs)
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
        """
        if self.id:
            if not overwrite:
                log.warning("Model already exists in the DB and overwrite is not set.")
                return self.id
        else:
            self._id = self._create_database_entry(
                name=self.name,
                version=self.version,
                description=self.description,
                metadata=self.artifacts,
                input_schema=self.input_params.to_json,
                output_schema=self.output_params.to_json,
            )

        modelSavePath = self._upload_model_folder(self.id)
        weights = self._upload_weights(self.id, update_weights, weights_path)
        self.client.update_model(self.id, weights_path=weights, model_save_path=modelSavePath)
        return self.id

    def _upload_model_folder(self, id: str) -> str:
        s3_client = boto3.client("s3")
        path_to_tarfile = os.path.join(self._location, "AISavedModel.tar.gz")
        log.info(f"Compressing AI folder at {self._location}")
        self._compress_folder(path_to_tarfile, self._location)
        object_name = os.path.join(self.folder_name, id, self.name, str(self.version), "AISavedModel.tar.gz")
        with open(path_to_tarfile, "rb") as f:
            s3_client.upload_fileobj(f, self.bucket_name, object_name)
        modelSavePath = os.path.join("s3://", self.bucket_name, object_name)
        log.info(f"Uploaded AI object to '{modelSavePath}'")
        return modelSavePath

    def _upload_weights(self, id: str, update_weights: bool, weights_path: Optional[str]) -> Optional[str]:
        s3_client = boto3.client("s3")
        weights: Optional[str] = None
        if self.weights_path is not None and update_weights:
            if self.weights_path.startswith("s3"):
                weights = self.weights_path
            elif os.path.exists(self.weights_path):
                if os.path.isdir(self.weights_path):
                    path_to_weights_tarfile = os.path.join(
                        self._location, f"{os.path.basename(self.weights_path)}.tar.gz"
                    )
                    log.info(f"Compressing weights at {self.weights_path}, placed at {path_to_weights_tarfile}...")
                    self._compress_folder(path_to_weights_tarfile, self.weights_path)
                    upload_object_name = os.path.join(
                        self.folder_name, "saved_models", id, f"{os.path.basename(self.weights_path)}.tar.gz"
                    )
                else:
                    upload_object_name = os.path.join(
                        self.folder_name, "saved_models", id, os.path.basename(self.weights_path)
                    )
                    path_to_weights_tarfile = self.weights_path
                with open(path_to_weights_tarfile, "rb") as w:
                    log.info("Uploading weights...")
                    s3_client.upload_fileobj(w, self.bucket_name, upload_object_name)
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
        """
        lambda_mode = orchestrator in [Orchestrator.LOCAL_DOCKER_LAMBDA, Orchestrator.AWS_LAMBDA]
        if orchestrator in [
            Orchestrator.LOCAL_DOCKER,
            Orchestrator.LOCAL_DOCKER_LAMBDA,
            Orchestrator.AWS_LAMBDA,
            Orchestrator.AWS_SAGEMAKER,
        ]:
            self._prepare_dependencies(
                worker_count=kwargs.get("worker_count", 1),
                lambda_mode=lambda_mode,
                ai_cache=kwargs.get("ai_cache", 5),
            )
            if not skip_build:
                self.build_image_s2i(
                    self.name,
                    str(self.version),
                    enable_cuda=enable_cuda,
                    from_scratch=kwargs.get("build_all_layers", False),
                )
        elif orchestrator in [Orchestrator.AWS_EKS, Orchestrator.MINIKUBE, Orchestrator.GCP_KS]:
            raise NotImplementedError()
        else:
            raise ValueError(f"Invalid Orchestrator, should be one of {[e for e in Orchestrator]}")
        # build kwargs
        kwargs = {}
        if orchestrator == Orchestrator.LOCAL_DOCKER:
            kwargs["image_name"] = f"{self.name}:{self.version}"
            kwargs["weights_path"] = self.weights_path
            kwargs["lambda_mode"] = lambda_mode
        else:
            if not skip_build:
                ecr_image_name = self.push_model(self.name, str(self.version))
            else:
                region = "us-east-1"
                boto_session = boto3.Session(region_name=region)
                account = boto_session.client("sts").get_caller_identity()["Account"]
                ecr_image_name = f"{account}.dkr.ecr.{region}.amazonaws.com/{self.name}:{self.version}"
            kwargs = dict(client=self.client, name=self.name, version=str(self.version))
            if self.id is None:
                raise LookupError(
                    "Cannot establish id, please make sure you push the AI model to create a database entry"
                )
            existing_deployment = self.client.get_deployment(self.id)
            log.info(f"Existing deployments : {existing_deployment}")
            if existing_deployment is None or "status" not in existing_deployment:
                # check if weights are present in the database
                models = self.client.get_model_by_name_version(self.name, self.version)
                model = models[0]
                log.info(f"Model attributes: {model}")
                assert (
                    model["weightsPath"] is not None
                ), "Weights Path cannot be None in the database for the deployment to finish"
                self.client.deploy(self.id, ecr_image_name, deployment_type=orchestrator.value, properties=properties)
            else:
                if redeploy:
                    self.undeploy()
                else:
                    raise Exception(
                        "Deployment with this version already exists. Try undeploy first or set `redeploy=True`."
                    )
                self.client.set_image(model_id=self.id, ecr_image_name=ecr_image_name)
                if properties:
                    self.client.set_deployment_properties(model_id=self.id, properties=properties)
                self.client.set_deployment_status(model_id=self.id, target_status="ONLINE")

            kwargs["id"] = self.id
        # get predictor
        predictor_obj: DeployedPredictor.Type = PredictorFactory.get_predictor_obj(orchestrator=orchestrator, **kwargs)

        return predictor_obj

    def undeploy(self) -> Optional[bool]:
        if self.id:
            if self.deployed:
                passed = self.client.undeploy(self.id)
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
            if not lambda_mode:
                template = Template(runner_script_s2i)
                args = dict(model_name=self.ai_template.model_class)
            else:
                template = Template(lambda_script)
                args = dict(ai_cache=ai_cache)
            scripts_content: str = template.render(args)
            handler_file.write(scripts_content)

        with open(os.path.join(self._location, dockerd_entrypoint), "w") as entry_point_file:
            template = Template(server_script)
            args = dict(worker_count=worker_count)
            entry_point_file_content: str = template.render(args)
            entry_point_file.write(entry_point_file_content)

    def build_image_s2i(
        self,
        image_name: str,
        version_tag: str = "latest",
        enable_cuda: bool = False,
        from_scratch: bool = False,
    ) -> None:
        start = time.time()
        cwd = os.getcwd()
        os.chdir(self._location)
        environment_file = "environment"
        # check the hash, if it doesn't exist, create one
        files = []
        if self.requirements:
            files.append("requirements.txt")
        if self.conda_env:
            files.append(self.conda_env)
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

        with open(environment_file, "r") as env_file_reader:
            env_list = env_file_reader.readlines()
        client = docker.from_env()
        base_image = f"superai-model-s2i-python3711-{'gpu' if enable_cuda else 'cpu'}:1"
        try:
            _ = client.images.get(base_image)
            log.info(f"Base image '{base_image}' found locally.")
        except ImageNotFound:
            region = boto3.Session().region_name
            account_id = boto3.client("sts").get_caller_identity()["Account"]
            ecr_image_name = f"{account_id}.dkr.ecr.{region}.amazonaws.com/{base_image}"
            log.info(f"Base image not found. Downloading from ECR '{ecr_image_name}'")
            log.info("Logging in to ECR...")
            os.system(f"$(aws ecr get-login --region {region} --no-include-email)")
            os.system(f"docker pull {ecr_image_name}")
            log.info(f"Re-tagging image to '{base_image}'")
            client.images.get(f"{ecr_image_name}").tag(base_image)
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
            new_lines = list(filter(lambda x: "BUILD_PIP" not in x, env_list))
            with open(environment_file, "w") as env_file_writer:
                env_file_writer.writelines(new_lines)
            command = (
                f"s2i build -E {environment_file} "
                f"-v {os.path.join(os.path.expanduser('~'), '.aws')}:/root/.aws "
                f"-v {os.path.join(os.path.expanduser('~'), '.superai')}:/root/.superai "
                f"-v {os.path.join(os.path.expanduser('~'), '.canotic')}:/root/.canotic "
                f"--incremental=True . "
                f"{base_image} {image_name}-pip-layer:{version_tag}"
            )
            self._system(command)
            image = client.images.get(f"{image_name}-pip-layer:{version_tag}")
            tag_time = image.attrs["Metadata"]["LastTagTime"]
            diff = datetime.datetime.utcnow() - datetime.datetime.fromisoformat(tag_time[:26])
            if diff.total_seconds() > 2.0:
                raise Exception(f"Image failed to create, this image is too old {diff.total_seconds()}s")

        with open(environment_file, "r") as env_file_reader:
            env_list = env_file_reader.readlines()
        found_build_pip = any(["BUILD_PIP" in line for line in env_list])
        if not found_build_pip:
            with open(environment_file, "a") as env_file_writer:
                env_file_writer.write("\nBUILD_PIP=false")
        command = (
            f"s2i build -E {environment_file} "
            f"-v {os.path.join(os.path.expanduser('~'), '.aws')}:/root/.aws "
            f"-v {os.path.join(os.path.expanduser('~'), '.superai')}:/root/.superai "
            f"-v {os.path.join(os.path.expanduser('~'), '.canotic')}:/root/.canotic"
            f"--incremental=True . "
            f"{image_name}-pip-layer:{version_tag} {image_name}:{version_tag}"
        )
        self._system(command)
        image = client.images.get(f"{image_name}:{version_tag}")
        tag_time = image.attrs["Metadata"]["LastTagTime"]
        diff = datetime.datetime.utcnow() - datetime.datetime.fromisoformat(tag_time[:26])
        if diff.total_seconds() > 2.0:
            raise Exception(f"Image failed to create, this image is too old ({diff.total_seconds()}s)")
        log.info(f"Built main container `{image_name}:{version_tag}`")
        log.info(f"Time taken to build: {time.time() - start:.2f}s")
        os.chdir(cwd)

    @staticmethod
    def _system(command):
        log.info(f"Running '{command}'")
        process = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE)
        (out, err) = process.communicate()
        return out.decode("utf-8")

    def _create_dockerfile(
        self, worker_count: int = 1, lambda_mode=True, ai_cache=32, enable_cuda=False, force_amd64=True
    ):
        """Build model locally. This involves docker file creation and docker build operations.
        Note that this is supported only in local mode, running this on docker can lead to docker-in-docker problems.
        """
        dockerd_entrypoint = "dockerd-entrypoint.py"

        self._prepare_dependencies(
            worker_count=worker_count,
            lambda_mode=lambda_mode,
            ai_cache=ai_cache,
            dockerd_entrypoint=dockerd_entrypoint,
        )

        dockerfile_content = prepare_dockerfile_string(
            force_amd64=force_amd64,
            enable_cuda=enable_cuda,
            lambda_mode=lambda_mode,
            dockerd_entrypoint=dockerd_entrypoint,
            conda_env=self.conda_env,
            requirements=self.requirements,
            artifacts=self.artifacts,
            location=self._location,
        )

        ################################################################################################################
        # Write dockerfile
        ################################################################################################################
        with open(os.path.join(self._location, "Dockerfile"), "w") as docker_file_writer:
            docker_file_writer.write("\n".join(dockerfile_content))
        log.info("Created Dockerfile...")
        return dockerfile_content  # for testing

    def build_image(self, image_name=None, version_tag="latest"):
        start = time.time()
        cwd = os.getcwd()
        os.chdir(self._location)
        os.environ["DOCKER_BUILDKIT"] = "1"
        docker_command = f"docker build -t {image_name}:{version_tag} --secret id=aws,src=$HOME/.aws/credentials ."
        log.info(f"Running {docker_command}")
        try:
            res = os.system(docker_command)
            end = time.time()
            if res != 0:
                log.error("Some error occurred while building the image.")
                raise Exception("Failed Docker Build. Check build logs for misconfiguration.")
            else:
                log.info(
                    f"Image `{image_name}:{version_tag}` built successfully. Elapsed time: {end - start:.3f} secs."
                )
        except KeyboardInterrupt:
            log.info(f"KeyboardInterrupt occurred")
            raise KeyboardInterrupt()
        os.chdir(cwd)

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
        return push_image(image_name=image_name, version=version)

    def train(
        self,
        model_save_path,
        training_data,
        test_data=None,
        production_data=None,
        encoder_trainable: bool = True,
        decoder_trainable: bool = True,
        hyperparameters: Optional[HyperParameterSpec] = None,
        model_parameters: Optional[ModelParameters] = None,
        callbacks=None,
        validation_data=None,
        train_logger=None,
        orchestrator: Orchestrator = Orchestrator.LOCAL_DOCKER,
    ):
        """Please fill hyperparameters and model parameters accordingly.

        Args:
            validation_data:
            callbacks:
            test_data:
            production_data:
            encoder_trainable:
            decoder_trainable:
            hyperparameters:
            model_parameters:
            model_save_path:
            training_data:
            orchestrator:
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
        return self.model_class.train(
            model_save_path=model_save_path,
            training_data=training_data,
            validation_data=validation_data,
            test_data=test_data,
            production_data=production_data,
            encoder_trainable=encoder_trainable,
            decoder_trainable=decoder_trainable,
            hyperparameters=hyperparameters,
            model_parameters=model_parameters,
            callbacks=callbacks,
        )
