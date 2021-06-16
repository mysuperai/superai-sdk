from __future__ import annotations

import copy
import datetime
import enum
import json
import os
import re
import shutil
import tarfile
import time
import traceback
from typing import Dict, List, TYPE_CHECKING, Union, Type, Optional
from urllib.parse import urlparse

import boto3  # type: ignore
import cloudpickle as pickle  # type: ignore
import pandas as pd  # type: ignore
import requests
import yaml
from jinja2 import Template

from superai import Client
from superai.apis.meta_ai.meta_ai_graphql_schema import meta_ai_deployment_type_enum
from superai.exceptions import ModelNotFoundError
from superai.log import logger
from superai.meta_ai.deployed_predictors import LocalPredictor, DeployedPredictor, AWSPredictor
from superai.meta_ai.dockerizer import push_image
from superai.meta_ai.parameters import HyperParameterSpec, ModelParameters, Config
from superai.meta_ai.schema import Schema, SchemaParameters
from superai.meta_ai.scripts_contents import runner_script, server_script, entry_script, lambda_script
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


class Mode(str, enum.Enum):
    LOCAL = "LOCAL"
    AWS = "AWS"
    KUBERNETES = "KUBERNETES"


class PredictorFactory(object):
    __predictor_classes = {"local": LocalPredictor, "aws": AWSPredictor}

    @staticmethod
    def get_predictor_obj(mode: Mode, *args, **kwargs) -> "DeployedPredictor.Type":
        """Factory method to get a predictor
        """
        predictor_class = PredictorFactory.__predictor_classes.get(mode.lower())

        if predictor_class:
            return predictor_class(*args, **kwargs)
        raise NotImplementedError(f"The predictor of mode:`{mode}` is not implemented yet.")


class AITemplate:
    def __init__(
        self,
        input_schema: Schema,
        output_schema: Schema,
        configuration: Config,
        model_class: Optional[Type["BaseModel"]],
        name: str,
        description: str,
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
            model_class: An instance of a subclass of :class:`~BaseModel`. This class is serialized using the CloudPickle
                         library. Any dependencies of the class should be included in one of the following locations:

                                - The SuperAI library.
                                - Package(s) listed in the model's Conda environment, specified by
                                  the ``conda_env`` parameter.
                                - One or more of the files specified by the ``code_path`` parameter.

                             Note: If the class is imported from another module, as opposed to being defined in the
                             ``__main__`` scope, the defining module should also be included in one of the listed
                             locations.
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
        try:
            self.model_class: BaseModel = model_class(
                input_schema=input_schema, output_schema=output_schema, configuration=configuration
            )
        except TypeError as e:
            log.info(f"Encountered error while processing model_class : {e}")
            self.model_class: BaseModel = model_class  # type: ignore
        except Exception as e:
            raise Exception("Something went wrong while loading model_class: ", e)
            # Reloading model_class in cloudpickle causes recursive failures. Usage of this object is a workaround.
        self._ai_class_dump = None

    @classmethod
    def load_local(cls, load_path: str) -> "AITemplate":
        with open(os.path.join(load_path, "AITemplateSaveFile.json"), "r") as json_file:
            details = json.load(json_file)
        requirements = os.path.join(load_path, "requirements.txt") if details.get("requirements") is not None else None
        conda_env = os.path.join(load_path, "conda.yml") if details.get("conda_env") is not None else None
        code_path = details.get("code_path")
        artifacts = details.get("artifacts")
        if details.get("ai_class_path") is not None:
            log.info(f"model_class associated. Loading it from ai_model file in {load_path}...")
            with open(os.path.join(load_path, "ai_model"), "rb") as pickleReader:
                ai_class = pickle.loads(pickleReader.read(), fix_imports=True)
        else:
            log.info(
                f"No model_class associated, please make sure you have `ai_class_path` mentioned"
                f" in AITemplateSaveFile.json"
            )
            ai_class = None

        name = details["name"]
        description = details["description"]
        input_schema = Schema.from_json(details["input_schema"])
        output_schema = Schema.from_json(details["output_schema"])
        configuration = Config.from_json(details["configuration"])
        return AITemplate(
            input_schema,
            output_schema,
            configuration,
            ai_class,
            name,
            description,
            requirements,
            code_path,
            conda_env,
            artifacts,
        )

    def save(self, version_save_path):
        # cloudpickle save the model_class
        ai_class_file = os.path.join(version_save_path, "ai_model")
        assert not os.path.exists(
            ai_class_file
        ), f"Cannot overwrite locally existing model in {version_save_path}. Please update version"
        if self._ai_class_dump is None:
            self.model_class.model = None
            self._ai_class_dump = pickle.dumps(self.model_class)
        with open(ai_class_file, "wb") as ai_writer:
            ai_writer.write(self._ai_class_dump)

        # copy requirements file and conda_env
        if self.conda_env is not None:
            if type(self.conda_env) == dict:
                with open(os.path.join(version_save_path, "conda.yml"), "w") as conda_file:
                    yaml.dump(self.conda_env, conda_file, default_flow_style=False)
            elif (
                type(self.conda_env) == str
                and os.path.exists(self.conda_env)
                and (self.conda_env.endswith(".yml") or self.conda_env.endswith(".yaml"))
            ):
                shutil.copy(self.conda_env, os.path.join(version_save_path, "conda.yml"))
            else:
                raise ValueError("Make sure conda_env is a valid path to a .yml file or a dictionary.")
        log.info("Copying all code_path content")
        if self.code_path is not None:
            assert (
                type(self.code_path) == list and type(self.code_path) != str
            ), "Types don't match for code_path, please pass a list of strings."
            for path in self.code_path:
                shutil.copytree(path, os.path.join(version_save_path, os.path.basename(path)))
        if self.requirements is not None:
            if type(self.requirements) == str and os.path.exists(self.requirements):
                shutil.copy(self.requirements, os.path.join(version_save_path, "requirements.txt"))
            elif type(self.requirements) == list:
                with open(os.path.join(version_save_path, "requirements.txt"), "w") as requirements_file:
                    requirements_file.write("\n".join(self.requirements))
            else:
                raise ValueError(
                    "Make sure requirements is a list of requirements or valid path to requirements.txt file"
                )
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
                "ai_class_path": ai_class_file,
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

        self.model_class = copy.deepcopy(ai_template.model_class)
        self.model_class.update_parameters(input_params, output_params)
        self.is_weights_loaded = False

        self.container = None
        self._id = None

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
                        s3_path = [entry for entry in all_models if entry["version"] == ending][0]["modelSavePath"]
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

    def update_ai_class(self, model_class: "BaseModel"):
        """Updates the model_class. Running this operation will increase the AI version.

        Args:
            model_class: An instance of a subclass of :class:`~BaseModel`.
        """
        if self.version is not None:
            self.version += 1
        else:
            self.version = 1
        self.model_class = model_class
        self._model_class_dump = None
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
        ai_class: Optional["BaseModel"] = None,
    ):
        """
        Updates the AI.

        Args:
            version: New AI version number. If the version number already exists, this method will fail.
            stage: New AI stage.
            weights_path: New path to a file or directory containing model data.
            ai_class: An instance of a subclass of :class:`~BaseModel`.
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
            self._model_class_dump = None
            self.model_class = ai_class
            self.save(overwrite=True)
        log.info("AI.update complete!")
        self.push()

    def predict(self, inputs):
        """Predicts from model_class and ensures that predict method adheres to schema in ai_definition.

        Args:
            inputs
        """
        if not self.is_weights_loaded:
            if self.weights_path is not None:
                self.model_class.load_weights(self.weights_path)
            self.is_weights_loaded = True
        output = self.model_class.predict(inputs)
        return output

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

    def push(self, update_weights: bool = False, weights_path: Optional[str] = None, overwrite=False) -> str:
        """Pushes the saved model to S3, creates an entry and enters the S3 URI in the database.

        Args:
            update_weights: Update weights in s3 or not
            weights_path: Path to weights in s3
        """
        if self.id and not overwrite:
            log.info("Model already exists in the DB and overwrite is not set.")
            return self.id
        s3_client = boto3.client("s3")

        path_to_tarfile = os.path.join(self._location, "AISavedModel.tar.gz")
        with tarfile.open(path_to_tarfile, "w:gz") as tar:
            tar.add(self._location, arcname="ai")
        object_name = os.path.join(self.folder_name, self.name, str(self.version), "AISavedModel.tar.gz")
        with open(path_to_tarfile, "rb") as f:
            s3_client.upload_fileobj(f, self.bucket_name, object_name)
        modelSavePath = os.path.join("s3://", self.bucket_name, object_name)
        log.info(f"Uploaded AI object to '{modelSavePath}'")
        weights: Optional[str] = None
        if self.weights_path is not None and update_weights:
            if self.weights_path.startswith("s3"):
                weights = self.weights_path
            elif os.path.exists(self.weights_path):
                if os.path.isdir(self.weights_path):
                    path_to_weights_tarfile = os.path.join(
                        self._location, f"{os.path.basename(self.weights_path)}.tar.gz"
                    )
                    with tarfile.open(path_to_weights_tarfile, "w:gz") as tar_weights:
                        log.info("Compressing weights...")
                        tar_weights.add(self.weights_path, arcname=os.path.basename(self.weights_path))
                    upload_object_name = os.path.join(
                        self.folder_name, "saved_models", f"{os.path.basename(self.weights_path)}.tar.gz"
                    )
                else:
                    upload_object_name = os.path.join(
                        self.folder_name, "saved_models", os.path.basename(self.weights_path)
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
        return self._create_database_entry(
            name=self.name,
            version=self.version,
            description=self.description,
            metadata=self.artifacts,
            input_schema=self.input_params.to_json,
            output_schema=self.output_params.to_json,
            weights_path=weights,
            model_save_path=modelSavePath,
        )

    def deploy(
        self,
        mode: "Mode" = Mode.LOCAL,
        skip_build: bool = False,
        remote_type: meta_ai_deployment_type_enum = "AWS_SAGEMAKER",
        **kwargs,
    ) -> "DeployedPredictor.Type":
        """Here we need to create a docker container with superai-sk installed. Then we need to create a server script
        and prediction script, which basically calls ai.predict.
        We need to pass the ai model inside the image, install conda env or requirements.txt as required.
        Serve local: run the container locally using Cli (in a separate thread)
        Serve sagemaker: create endpoint after pushing container to ECR

        Args:
            mode: Which mode to deploy.
            skip_build: Skip building

            # Hidden kwargs
            lambda_mode: Create a dockerfile in lambda mode, true by default
            worker_count: Number of workers to use for serving with Sagemaker.
            ai_cache: Cache of ai objects for a lambda, 5 by default considering the short life of a lambda function
        """
        if mode == Mode.LOCAL or mode == Mode.AWS:
            self._create_dockerfile(
                worker_count=kwargs.get("worker_count", 1),
                lambda_mode=kwargs.get("lambda_mode", True),
                ai_cache=kwargs.get("ai_cache", 5),
            )
            if not skip_build:
                self.build_image(self.name, str(self.version))
        elif mode == Mode.KUBERNETES:
            raise NotImplementedError()
        else:
            raise ValueError("Invalid Mode, should be one of ['LOCAL', 'AWS', 'KUBERNETES]")
        # build kwargs
        kwargs = {}
        if mode == Mode.LOCAL:
            kwargs["image_name"] = f"{self.name}:{self.version}"
            kwargs["weights_path"] = self.weights_path
            kwargs["lambda_mode"] = kwargs.get("lambda_mode", False)
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
            assert self.id is not None, "Please make sure you push the AI model to create a database entry"
            existing_deployment = self.client.get_deployment(self.id)
            log.info(f"Existing deployments : {existing_deployment}")
            if existing_deployment is None or "status" not in existing_deployment:
                self.client.deploy(self.id, ecr_image_name, deployment_type=remote_type)
            elif existing_deployment["status"] == "OFFLINE":
                self.client.set_image(model_id=self.id, ecr_image_name=ecr_image_name)
                self.client.set_deployment_status(model_id=self.id, target_status="ONLINE")
            kwargs["id"] = self.id
        # get predictor
        predictor_obj: DeployedPredictor.Type = PredictorFactory.get_predictor_obj(mode=mode, **kwargs)

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

    @classmethod
    def load_api(cls, model_path, mode: Mode) -> "DeployedPredictor.Type":
        ai_object: Optional["AI"] = cls.load(model_path)
        assert ai_object is not None, "Need an AI object associated with the class to load"
        # TODO: If we pass a model_path like `model://...`, check if there is an endpoint entry, and check
        #  if endpoint is serving.
        # if endpoint is not serving:
        return ai_object.deploy(mode)

    def _create_dockerfile(self, worker_count: int = 1, lambda_mode=True, ai_cache=32):
        """Build model locally. This involves docker file creation and docker build operations.
        Note that this is supported only in local mode, running this on docker can lead to docker-in-docker problems.
        """
        homedir = "/home/model-server/"
        dockerd_entrypoint = "dockerd-entrypoint.py"

        with open(os.path.join(self._location, "handler.py"), "w") as handler_file:
            if not lambda_mode:
                handler_file.write(runner_script)
            else:
                template = Template(lambda_script)
                args = dict(ai_cache=ai_cache)
                lambda_file_content: str = template.render(args)
                handler_file.write(lambda_file_content)

        with open(os.path.join(self._location, dockerd_entrypoint), "w") as entry_point_file:
            template = Template(server_script)
            args = dict(worker_count=worker_count)
            entry_point_file_content: str = template.render(args)
            entry_point_file.write(entry_point_file_content)

        dockerfile_content = [
            "# syntax=docker/dockerfile:1.2",
            "FROM continuumio/miniconda3",
        ]
        if not lambda_mode:
            dockerfile_content.extend(
                [
                    "\nRUN mkdir -p /usr/share/man/man1",
                    "\nRUN apt-get update "
                    "&& apt-get -y install --no-install-recommends build-essential ca-certificates default-jdk curl "
                    "&& rm -rf /var/lib/apt/lists/*",
                    "\nLABEL com.amazonaws.sagemaker.capabilities.multi-models=true",
                    "LABEL com.amazonaws.sagemaker.capabilities.accept-bind-to-port=true",
                ]
            )
        else:
            dockerfile_content.extend(
                [
                    "RUN apt-get update && "
                    "apt-get -y install --no-install-recommends build-essential ca-certificates g++"
                    " make cmake unzip libcurl4-openssl-dev curl "
                    "&& rm -rf /var/lib/apt/lists/*"
                ]
            )
        dockerfile_content.append(f"RUN mkdir -p {homedir}")
        # create conda env
        if self.conda_env is not None:
            dockerfile_content.extend(
                [
                    f"COPY conda.yml {homedir}",
                    f"RUN conda env create -f {os.path.join(homedir, 'conda.yml')} -n env",
                    f"RUN echo \"source activate $(head -1 {os.path.join(homedir, 'conda.yml')} "
                    f"| cut -d' ' -f2)\" > ~/.bashrc",
                    f"ENV PATH /opt/conda/envs/$(head -1 {os.path.join(homedir, 'conda.yml')} "
                    f"| cut -d' ' -f2)/bin:$PATH",
                ]
            )
        else:
            dockerfile_content.extend(
                [
                    "RUN conda create -n env python=3.7.10",
                    'RUN echo "source activate env" > ~/.bashrc',
                    "ENV PATH /opt/conda/envs/env/bin:$PATH",
                ]
            )
        env_name = "env"

        dockerfile_content.append(
            f'SHELL ["conda", "run", "--no-capture-output", "-n", "{env_name}", "/bin/bash", "-c"]'
        )

        # install serving requirements
        if not lambda_mode:
            serving_reqs = "multi-model-server sagemaker-inference retrying awscli~=1.18.195"
        else:
            serving_reqs = "awslambdaric awscli~=1.18.195"
        dockerfile_content.append(f"RUN pip install {serving_reqs}")

        # install pip requirements
        superai_reqs = "superai_schema superai"
        dockerfile_content.extend(
            [
                'RUN echo "export SUPERAI_CONFIG_ROOT=/tmp/.superai" >> ~/.bashrc',
                "ARG AWS_DEFAULT_REGION=us-east-1",
                "RUN --mount=type=secret,id=aws,target=/root/.aws/credentials,required=true"
                " --mount=type=cache,target=/opt/conda/pkgs "
                f"aws codeartifact login --tool pip --domain superai --repository pypi-superai && "
                f"pip install --no-cache-dir  {superai_reqs}",
            ]
        )
        dockerfile_content.extend(
            [
                f"",
                f"### Model specific dependencies ",
                f"",
            ],
        )
        #
        # Custom install commands (require copy of workdir)
        #
        dockerfile_content.extend(
            [
                f"WORKDIR {homedir}",
            ]
        )
        if self.requirements:
            # Only copy and install requirements file to allow better caching
            dockerfile_content.extend(
                [
                    "COPY requirements.txt . ",
                    "RUN --mount=type=secret,id=aws,target=/root/.aws/credentials,required=true"
                    " --mount=type=cache,target=/opt/conda/pkgs "
                    f"aws codeartifact login --tool pip --domain superai --repository pypi-superai && "
                    "pip install -r requirements.txt",
                ]
            )
        # Copy complete contents of local folder
        dockerfile_content.extend(
            [
                f"COPY . {homedir}",
            ],
        )
        if self.artifacts is not None:
            if "run" in self.artifacts:
                dockerfile_content.extend(
                    [
                        f"RUN chmod +x {os.path.join(homedir, self.artifacts['run'])}",
                        "RUN --mount=type=secret,id=aws,target=/root/.aws/credentials,required=true "
                        "--mount=type=cache,target=/opt/conda/pkgs "
                        f"aws codeartifact login --tool pip --domain superai --repository pypi-superai && "
                        f"bash {os.path.join(homedir, self.artifacts['run'])}",
                    ]
                )
        if not lambda_mode:
            dockerfile_content.extend(
                [
                    f"RUN chmod +x {os.path.join(homedir, dockerd_entrypoint)}",
                    f'ENTRYPOINT ["conda", "run", "--no-capture-output", "-n", "{env_name}", "python",'
                    f' "{os.path.join(homedir, dockerd_entrypoint)}"]',
                    'CMD ["serve"]',
                ]
            )
        else:
            rie_url = (
                "https://github.com/aws/aws-lambda-runtime-interface-emulator/releases/latest/download/aws-lambda-rie"
            )
            with open(os.path.join(self._location, "entry_script.sh"), "w") as entry_file_writer:
                template = Template(entry_script)
                entry_script_args = dict(env=env_name)
                entry_file_content: str = template.render(entry_script_args)
                entry_file_writer.write(entry_file_content)
            dockerfile_content.extend(
                [
                    f"ADD {rie_url} /usr/local/bin/aws-lambda-rie",
                    f"RUN chmod +x /usr/local/bin/aws-lambda-rie && chmod +x {os.path.join(homedir, 'entry_script.sh')}",
                    f"ENTRYPOINT [\"{os.path.join(homedir, 'entry_script.sh')}\"]",
                    'CMD ["handler.processor"]',
                ]
            )
        with open(os.path.join(self._location, "Dockerfile"), "w") as docker_file_writer:
            docker_file_writer.write("\n".join(dockerfile_content))
        log.info("Created Dockerfile...")

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
        mode: Mode = Mode.LOCAL,
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
            mode:
        """
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

    model_entries = client.get_model_by_name(ai_name)
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
