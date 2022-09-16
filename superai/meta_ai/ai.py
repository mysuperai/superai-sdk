from __future__ import annotations

import datetime
import enum
import json
import os
import re
import shutil
import tarfile
import time
import traceback
from pathlib import Path
from typing import TYPE_CHECKING, Dict, List, Optional, Tuple, Union
from urllib.parse import urlparse

import boto3  # type: ignore
import requests
from pydantic import ValidationError
from rich.prompt import Confirm

from superai import settings
from superai.log import logger
from superai.meta_ai.ai_helper import (
    find_root_model,
    get_user_model_class,
    list_models,
    upload_dir,
)
from superai.meta_ai.ai_template import AITemplate
from superai.meta_ai.config_parser import AIConfig, InstanceConfig
from superai.meta_ai.deployed_predictors import DeployedPredictor, PredictorFactory
from superai.meta_ai.dockerizer import ecr_full_name, push_image
from superai.meta_ai.environment_file import EnvironmentFileProcessor
from superai.meta_ai.exceptions import ModelDeploymentError, ModelNotFoundError
from superai.meta_ai.image_builder import (
    AiImageBuilder,
    BaseAIOrchestrator,
    Orchestrator,
    TrainingOrchestrator,
)
from superai.meta_ai.parameters import (
    AiDeploymentParameters,
    Config,
    HyperParameterSpec,
    ModelParameters,
    TrainingParameters,
)
from superai.meta_ai.schema import (
    SchemaParameters,
    TaskBatchInput,
    TaskInput,
    TaskPredictionInstance,
    TrainerOutput,
)
from superai.utils import retry

DEPLOYMENT_PARAMETERS_SUBKEY = (
    "deployment_parameters"  # Used to access deployment parameters in the training parameters
)

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
        self.model_class: Optional[BaseModel] = None
        # ID of deployment serving predictions
        self.served_by: Optional[str] = None

    def _init_model_class(self, load_weights=True, force_reload=False):
        """
        Initializes the BaseModel class.

        Args:
            load_weights: bool
                Will also load weights if True.
            force_reload:
                Will reload the model class even if it was already loaded before.

        """
        if self.model_class is None or force_reload:
            model_class_template = get_user_model_class(
                model_name=self.model_class_name, save_location=self._location, path=self.model_class_path
            )
            self.model_class: BaseModel = model_class_template(
                input_schema=self.ai_template.input_schema,
                output_schema=self.ai_template.output_schema,
                configuration=self.ai_template.configuration,
            )
            self.model_class.update_parameters(self.input_params, self.output_params)

            if load_weights and (not self.is_weights_loaded or force_reload):
                if self.weights_path is not None:
                    self.model_class.load_weights(self.weights_path)
                self.is_weights_loaded = True

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
        if self.id and self.served_by:
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
        os.makedirs(download_folder, exist_ok=True)
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
                os.makedirs(download_folder, exist_ok=True)
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
            deployment_parameters: Hardware and scaling parameters for the model.
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

    def predict(self, inputs: Union[TaskInput, List[dict]]) -> List[TaskPredictionInstance]:
        """Predicts from model_class and ensures that predict method adheres to schema in ai_definition.

        Args:
            inputs

        Returns:
            List of TaskPredictions
            Each TaskPredictionInstance corresponds to a single prediction instance.
            Models can output multiple instances per input.
        """
        self._init_model_class(load_weights=True)

        if not isinstance(inputs, TaskInput):
            try:
                TaskInput.parse_obj(inputs)
            except ValidationError as e:
                log.warning(
                    f"AI input could not be parsed as TaskInput. This could be enforced in future versions! {e}"
                )

        output = self.model_class.predict(inputs)
        result = TaskPredictionInstance.validate_prediction(output)
        return result

    def predict_batch(self, inputs: Union[List[List[dict]], TaskBatchInput]) -> List[List[TaskPredictionInstance]]:
        """Predicts a batch of inputs from model_class and ensures that predict method adheres to schema in ai_definition.

        Args:
            inputs

        Returns:
            Batch of lists of TaskPredictions
            Each TaskPredictionInstance corresponds to a single prediction instance.
            For each input in the batch we expect a list of prediction instances.

        """
        self._init_model_class(load_weights=True)

        if not isinstance(inputs, TaskBatchInput):
            try:
                TaskBatchInput.parse_obj(inputs)
            except ValidationError as e:
                log.warning(
                    f"AI input could not be parsed as TaskBatchInput. This could be enforced in future versions! {e}"
                )

        batch = self.model_class.predict_batch(inputs)
        result = TaskPredictionInstance.validate_prediction_batch(batch)
        return result

    def save(self, path: str = ".AISave", overwrite: bool = False):
        """Saves the model locally.

        Args:
            path:
            overwrite:
        """
        save_path = os.path.join(path, self.name)
        os.makedirs(save_path, exist_ok=True)

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
                deployment_parameters=self.ai_template.deployment_parameters,
            )

        modelSavePath = self._upload_model_folder(self.id)
        weights = self._upload_weights(self.id, update_weights, weights_path)
        self.client.update_model(
            self.id,
            weights_path=weights,
            model_save_path=modelSavePath,
            deployment_parameters=self.ai_template.deployment_parameters,
        )
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
                log.warning("Weights path provided were invalid, weights will not be uploaded")
        else:
            log.warning("No weights path given, weights will not be uploaded")
            if weights_path is not None:
                weights = weights_path
        return weights

    def deploy(
        self,
        orchestrator: Union[str, "Orchestrator"] = Orchestrator.LOCAL_DOCKER,
        skip_build: bool = False,
        properties: Optional[Union[dict, AiDeploymentParameters]] = None,
        enable_cuda: bool = False,
        enable_eia: bool = False,
        cuda_devel: bool = False,
        redeploy: bool = False,
        build_all_layers: bool = False,
        download_base: bool = False,
        use_internal: bool = False,
    ) -> "DeployedPredictor":
        """
        Deploys the model to the specified orchestrator.

        Args:
            orchestrator: Which orchestrator to be used to deploy.
            skip_build: Skip building
            enable_cuda: Create CUDA-Compatible image
            enable_eia: Create Elastic Inference compatible image
            cuda_devel: Create development CUDA image
            properties: Optional variable to override hardware and scaling deployment parameters from the AI template.
            redeploy: Allow un-deploying existing deployment and replacing it.
            build_all_layers: Perform a fresh build of all layers
            download_base: Always download the base image to get the latest version from ECR
            use_internal: Use internal development base image. Only accessible for super.AI developers.

        """

        if redeploy and settings.current_env == "prod":
            confirmed = Confirm.ask(
                "Do you [bold]really[/bold] want to redeploy a [red]production[/red] AI? "
                "This can negatively impact Data Programs relying on the existing AI."
            )
            if not confirmed:
                log.warning("Aborting deployment")
                raise ModelDeploymentError("Deployment aborted by User")

        if isinstance(orchestrator, str):
            try:
                orchestrator = Orchestrator[orchestrator]
            except KeyError:
                raise ValueError(
                    f"Unknown orchestrator: {orchestrator}. Try one of: {', '.join(Orchestrator.__members__.values())}"
                )

        deployment_parameters = self._merge_deployment_parameters(properties, enable_cuda)
        # Build image and compile deployment properties
        local_image_name, global_image_name = self.build(
            orchestrator,
            enable_eia=enable_eia,
            skip_build=skip_build,
            cuda_devel=cuda_devel,
            use_internal=use_internal,
            deployment_parameters=deployment_parameters,
            build_all_layers=build_all_layers,
            download_base=download_base,
        )

        if PredictorFactory.is_remote(orchestrator):
            if not skip_build:
                self.push_model(image_name=local_image_name)

        predictor_obj: DeployedPredictor = PredictorFactory.get_predictor_obj(
            orchestrator=orchestrator,
            local_image_name=local_image_name,
            deploy_properties=deployment_parameters,
            weights_path=self.weights_path,
            client=self.client,
            ai=self,
        )
        predictor_obj.deploy(redeploy=redeploy)

        return predictor_obj

    def _merge_deployment_parameters(self, properties: Union[dict, AiDeploymentParameters], enable_cuda):
        """
        Merges deployment parameters from the AI template and the user-provided deployment parameters.
        Precedence is given to the user-provided deployment parameters.

        Args:
            properties: Optional variable to override hardware and scaling deployment parameters from the AI template.
            enable_cuda: Legacy kwarg for backwards compatibility.

        Returns:

        """
        # Parse properties into DeploymentParameters object
        properties = AiDeploymentParameters.parse_from_optional(properties)
        if enable_cuda:
            log.warning("enable_cuda is deprecated and will be removed in future versions. Use `properties` instead.")
            properties.enable_cuda = enable_cuda
        # Merge properties with deployment parameters from AI template with precedence to properties
        template_deployment_parameters = self.ai_template.deployment_parameters.dict_for_db()
        template_deployment_parameters.update(properties.dict_for_db())
        deployment_parameters = AiDeploymentParameters.parse_obj(template_deployment_parameters)
        return deployment_parameters

    def build(
        self,
        orchestrator: BaseAIOrchestrator,
        deployment_parameters: Optional[AiDeploymentParameters] = None,
        enable_eia: bool = False,
        skip_build=False,
        cuda_devel=False,
        use_internal=False,
        build_all_layers=False,
        download_base=False,
    ) -> Tuple[str, str]:
        """
        Build the image and return the image name.
        Args:
            orchestrator:
            deployment_parameters: Optional deployment parameters to override the default deployment parameters.
            enable_eia:
            skip_build: Skip building and return the image name which would be built.
            cuda_devel:
            use_internal:
                Use the internal development base image
            build_all_layers: Force a fresh build of all layers
            download_base: Force redownload of the base image

        Returns:
            Tuple[str,str]: The local image name and the global image name.

        """
        image_builder = AiImageBuilder(
            orchestrator,
            entrypoint_class=self.ai_template.model_class,
            location=self._location,
            name=self.name,
            version=self.version,
            environs=self.environs,
            requirements=self.requirements,
            conda_env=self.conda_env,
            artifacts=self.artifacts,
            deployment_parameters=deployment_parameters or self.ai_template.deployment_parameters,
        )

        if skip_build:
            local_image_name = image_builder.full_image_name(self.name, self.version)
        else:
            local_image_name = image_builder.build_image(
                cuda_devel=cuda_devel,
                enable_eia=enable_eia,
                skip_build=skip_build,
                use_internal=use_internal,
                build_all_layers=build_all_layers,
                download_base=download_base,
            )
        global_image_name, *_ = ecr_full_name(image_name=self.name, version=self.version, model_id=self.id)

        return local_image_name, global_image_name

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
            if ":" in image_name:
                version = image_name.split(":")[1]
                image_name = image_name.split(":")[0]
            else:
                version = str(self.version)
        id = self.id
        if id is None:
            raise Exception("No ID found. AI needs to be registered  via `push()` first.")
        full_name = push_image(image_name=image_name, model_id=id, version=version)
        self.client.update_model(id, image=full_name)
        return full_name

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
    ) -> TrainerOutput:
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
        self._init_model_class(load_weights=True)

        if train_logger is not None:
            self.model_class.update_logger_path(train_logger)
        else:
            self.model_class.update_logger_path(
                os.path.join(self._location, "logs/fit/" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")),
            )
        log.info(f"If tensorboard callback is present, logging in {self.model_class.logger_dir}")
        train_instance_output = self.model_class.train(
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
        return train_instance_output

    @classmethod
    def from_settings(cls, ai_template: AITemplate, instance: InstanceConfig) -> AI:
        if instance.input_params is None:
            input_params = SchemaParameters()
        elif isinstance(instance.input_params, str):
            input_params = SchemaParameters.from_json(json.loads(instance.input_params))
        else:
            input_params = SchemaParameters.from_json(instance.input_params)

        if instance.output_params is None:
            output_params = SchemaParameters()
        elif isinstance(instance.output_params, str):
            output_params = SchemaParameters.from_json(json.loads(instance.output_params))
        else:
            output_params = SchemaParameters.from_json(instance.output_params)

        if instance.configuration is None:
            configuration = None
        elif isinstance(instance.configuration, str):
            configuration = Config.from_json(json.loads(instance.configuration))
        else:
            configuration = Config.from_json(instance.configuration)

        return AI(
            ai_template=ai_template,
            input_params=input_params,
            output_params=output_params,
            configuration=configuration,
            name=instance.name,
            version=instance.version,
            description=instance.description,
            weights_path=instance.weights_path,
            overwrite=instance.overwrite,
        )

    def training_deploy(
        self,
        training_data_dir: Optional[Union[str, Path]] = None,
        skip_build: bool = False,
        properties: Optional[dict, AiDeploymentParameters] = None,
        training_parameters: Optional[TrainingParameters] = None,
        use_internal: bool = False,
        enable_cuda: bool = False,
        app_id: Optional[str] = None,
        task_name: Optional[str] = None,
        metadata: dict = None,
        **kwargs,
    ):
        """Here we need to create a docker container with superai-sdk installed. Then we will create a run script

        Args:
            app_id: Application ID to be used for retrieving training data, Either app_id or training_data_dir is required
            task_name: Task name to be used for retrieving training data, Only used together with app_id.
            metadata: Metadata used for display in UI
            skip_build: Skip building
            properties: An optional dictionary with hardware properties for training run execution.
            training_data_dir: Path to local training data, Either app_id or training_data_dir is required
            training_parameters: A TrainingParameters object used for all training parameters to be passed to
                                BaseModel train method

            # Hidden kwargs
            enable_cuda: Create CUDA-Compatible image
            cuda_devel: Create development CUDA image
            build_all_layers: Perform a fresh build of all layers
            envs: Pass custom environment variables to the deployment. Should be a dictionary like
                  {"LOG_LEVEL": "DEBUG", "OTHER": "VARIABLE"}
            download_base: Always download the base image to get the latest version from ECR
            use_internal: Use internal development base image. Only accessible for super.AI developers.
        """
        if training_data_dir is None and app_id is None:
            raise ValueError("Either app_id or training_data_dir is required")
        if training_data_dir is not None and app_id is not None:
            raise ValueError("Only one of app_id or training_data_dir is allowed")
        if app_id is not None and task_name is None:
            raise ValueError("task_name is required when app_id is provided")

        # TODO: add method which works with local training
        orchestrator = TrainingOrchestrator.AWS_EKS
        kwargs.pop("orchestrator", None)

        properties = properties or {}
        metadata = metadata or {}
        deployment_parameters = self._merge_deployment_parameters(properties, enable_cuda)

        # Build image and merge all parameters
        loaded_parameters = self._prepare_training(
            orchestrator, deployment_parameters, training_parameters, skip_build, use_internal, **kwargs
        )

        # Create a training template
        template_id = self._get_or_create_training_entry(model_id=self.id, properties=loaded_parameters, app_id=app_id)
        log.info(
            f"Starting training for model_id={self.id} template_id="
            f"{template_id} with properties={loaded_parameters} and deployment_parameters={deployment_parameters} "
        )
        if training_data_dir is not None:
            log.info(f"Using local training data from {training_data_dir}")
            # Create the database entry for the training, initially in stopped state
            instance_id = self.client.create_training_entry(
                model_id=self.id,
                properties=loaded_parameters,
                starting_state="STOPPED",
                template_id=template_id,
            )
            self._upload_training_data(training_data_dir, training_id=instance_id)
        else:
            log.info(f"Using app_id={app_id} and task_name={task_name} to retrieve training data")
            instance_id = self.client.start_training_from_app_model_template(
                app_id=app_id,
                model_id=self.id,
                task_name=task_name,
                training_template_id=template_id,
                current_properties=loaded_parameters,
                metadata=metadata,
            )

        # Start the training in the backend
        instance = self.client.update_training_instance(instance_id, state="STARTING")
        log.info(f"Created training instance : {instance}. Will be started in the backend")

    def _prepare_training(
        self, orchestrator, deployment_parameters, training_parameters, skip_build, use_internal, **kwargs
    ) -> dict:
        """
        Prepares image and parameters for training

        1. Builds the model if not skipped
        2. Uploads the model to ECR
        3. Queries the default training parameters and merges with the provided ones
        4. Add the deployment parameters to the training parameters (contain hardware requirements)



        Args:
            orchestrator: The orchestrator to use for training (currently only AWS EKS is supported)
            deployment_parameters: Deployment parameters, e.g. hardware requirements
            training_parameters: Training parameters
            skip_build: Skip building
            use_internal: Use internal development base image. Only accessible for super.AI developers.
            **kwargs: Additional kwargs for the image builder

        Returns:

        """
        # Build image and compile deployment properties
        local_image_name, global_image_name = self.build(
            orchestrator,
            deployment_parameters=deployment_parameters,
            use_internal=use_internal,
            skip_build=skip_build,
            **kwargs,
        )
        if not skip_build:
            self.push_model(image_name=local_image_name)
        self.client.update_model(model_id=self.id, trainable=True)

        # Merge training parameters with default ones
        if training_parameters:
            if isinstance(training_parameters, dict):
                obj = TrainingParameters().from_dict(training_parameters)
                training_parameters = obj
            loaded_parameters = json.loads(training_parameters.to_json())
        else:
            loaded_parameters = self.client.get_model(model_id=self.id)["default_training_parameters"] or {}
            if isinstance(loaded_parameters, str):
                loaded_parameters = json.loads(loaded_parameters)

        # Merge parameters with deployment parameters
        # TODO: correctly load parameters in backend
        loaded_parameters[DEPLOYMENT_PARAMETERS_SUBKEY] = deployment_parameters.dict_for_db()
        if deployment_parameters.enable_cuda:
            # Legacy path to enable GPU training
            loaded_parameters["enable_cuda"] = deployment_parameters.enable_cuda

        return loaded_parameters

    def start_training_from_app(
        self,
        app_id: str,
        task_name: str,
        current_properties: Optional[dict] = None,
        training_parameters: Optional[TrainingParameters] = None,
        metadata: Optional[dict] = None,
        skip_build=False,
        use_internal: bool = False,
        **kwargs,
    ):
        """
        (Deprecated) Start a training from an app. This method is deprecated and will be removed in future versions.
        Use training_deploy(app_id=..., task_name=...) instead.
        """
        # TODO: remove this method in future versions
        log.warning(
            "start_training_from_app is deprecated and will be removed in future versions. Use training_deploy instead."
        )
        self.training_deploy(
            app_id=app_id,
            task_name=task_name,
            properties=current_properties,
            training_parameters=training_parameters,
            metadata=metadata,
            skip_build=skip_build,
            use_internal=use_internal,
            **kwargs,
        )

    def _get_or_create_training_entry(self, model_id: str, app_id: str = None, properties: dict = {}):
        existing_template_id = self.client.get_training_templates(model_id=model_id, app_id=app_id)
        if len(existing_template_id):
            template_id = existing_template_id[0].id
            log.info(f"Found existing template {existing_template_id}")
            if properties:
                self.client.update_training_template(template_id=template_id, properties=properties)

        else:
            template_id = self.client.create_training_template_entry(
                model_id=model_id, properties=properties, app_id=app_id
            )["id"]
            log.info(f"Created template : {template_id}")
            template_id = template_id
        return template_id


def obtain_object_template_config(config_file: Union[Path, str]) -> Tuple[AI, AITemplate, AIConfig]:
    """
    From the config file, obtain the AITemplate, AI instance and the config
    Args:
        config_file: Path to config file
    Returns:
        Tuple of AI instance, AITemplate and AIConfig
    """

    config_data = AIConfig(_env_file=str(config_file))

    ai_template_object = AITemplate.from_settings(config_data.template)
    ai_object = AI.from_settings(ai_template_object, config_data.instance)

    return ai_object, ai_template_object, config_data
