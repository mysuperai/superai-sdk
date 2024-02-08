from __future__ import annotations

import contextlib
import os
import re
import tempfile
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING, Dict, List, Union

import attr
import attrs.validators
import boto3  # type: ignore
import botocore.exceptions
import yaml
from pydantic import BaseModel as PydanticBaseModel
from pydantic import ValidationError

from superai.apis.meta_ai.meta_ai_graphql_schema import meta_ai_template
from superai.config import get_ai_bucket, get_current_env, settings
from superai.log import logger
from superai.meta_ai.ai_helper import (
    _ai_name_validator,
    _ai_version_validator,
    _path_exists_validator,
    confirm_action,
    get_user_model_class,
    push_image,
)
from superai.meta_ai.ai_loader import AILoader
from superai.meta_ai.environment_file import EnvironmentFileProcessor
from superai.meta_ai.exceptions import (
    AIException,
    ModelAlreadyExistsError,
    ModelNotFoundError,
)
from superai.meta_ai.parameters import (
    AiDeploymentParameters,
    Config,
    HyperParameterSpec,
    ModelParameters,
    TrainingParameters,
)
from superai.meta_ai.schema import (
    Schema,
    SchemaParameters,
    TaskBatchInput,
    TaskInput,
    TaskPredictionInstance,
    TrainerOutput,
)

from .. import SuperAIAWSException
from ..apis.meta_ai.session import GraphQlException
from .orchestrators import BaseAIOrchestrator, Orchestrator

DEFAULT_VERSION = "1.0"

if TYPE_CHECKING:
    from superai.meta_ai import AIInstance, BaseAI

log = logger.get_logger(__name__)


@attr.define()
class AI:
    """Create an AI object containing all necessary information to train and deploy a model.


    Args:
        configuration: Deprecated. Configuration of the AI
        input_schema: Input Schema of the AI
        output_schema: Output Schema of the AI
        name: Name of the AI template

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
        description: Description of the AI template
        requirements: A list of PyPI requirements or the path to a requirements.txt file. If both this
                         parameter and the :param: conda_env are specified then conda dependencies will
                         be installed first followed by pip dependencies.
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
        default_deployment_parameters: Optional; Specification for the hardware (e.g. GPU) and
                                scaling configuration (e.g. throughput) of the model.

        training_deployment_parameters (Optional[Union[AiDeploymentParameters, dict]]):
            Specification for the hardware and scaling configuration during model training.
        training_parameters (Optional[Union[TrainingParameters, dict]]): Model training parameters. They are passed through
            to the model during training.

        parameters: Optional; Deprecated; Parameters to be passed to the model, could be the model architecture parameters,
                       or training parameters.
                       For example: parameters=MyModel.params_schema.parameters(conv_layers=None,
                                                                num_conv_layers=None,
                                                                filter_size=3,
                                                                num_filters=32,
                                                                strides=(1, 1),
                                                                padding='valid',
                                                                dilation_rate=(1, 1),
                                                               conv_use_bias=True)
        version (Optional[str]): Version of the AI, defaults to DEFAULT_VERSION. The version schema is a
                    shorter form of semantic version specification. For example, "1.0" is supported indicating
                    {major}.{minor} version while "1.0.0" is not supported.

        weights_path (Optional[Union[Path, str]]): Path to the model's weights file.
        weights: (Optional)
            p = Prompt("test")

            p1 = Prompt.load("m1/dfd/sdfs")

            AI_Tempalte(..., checkpoint=p)

        environs (Optional[EnvironmentVariables]): Environment variables to be loaded in the container.
        image (Optional[str]): Name of the remote docker image, including the registry and tag.

        Private fields:
        _model_class_instance (Optional[BaseModel]): Instance of the BaseModel class.
        _location (Optional[Path]): Location of the AI.
        _id (Optional[str]): Unique identifier of the AI.
        _is_weights_loaded (bool): Flag indicating if the model's weights have been loaded.
        _served_by (Optional[str]): Identifier of the serving deployment.
        _deployed (bool): Flag indicating if the model has been deployed.
        _local_image (Optional[str]): Name of the local docker image. Only populated if the model has been built.
    """

    name: str = attr.field(validator=_ai_name_validator)
    model_class: Optional[str] = None
    description: Optional[str] = None
    configuration: Optional[Config] = None
    version: Optional[str] = attr.field(default=DEFAULT_VERSION, validator=_ai_version_validator)
    weights_path: Optional[Union[Path, str]] = attr.field(
        default=None, validator=attrs.validators.optional(_path_exists_validator)
    )
    input_schema: Optional[Schema] = attr.field(default={}, converter=Schema.parse_obj)
    output_schema: Optional[Schema] = attr.field(default={}, converter=Schema.parse_obj)
    model_class_path: Union[str, Path] = attr.field(default=".", converter=Path, validator=_path_exists_validator)
    requirements: Optional[Union[str, List[str]]] = None
    code_path: Optional[Union[str, List[str], Path, List[Path]]] = []
    conda_env: Optional[Union[str, Dict]] = None
    dockerfile: Optional[Union[str, Path]] = None
    artifacts: Optional[Dict] = None
    parameters: Optional[dict] = None
    default_deployment_parameters: Optional[Union[AiDeploymentParameters, dict]] = attr.field(default=None, repr=False)
    training_deployment_parameters: Optional[Union[AiDeploymentParameters, dict]] = attr.field(default=None, repr=False)
    default_training_parameters: Optional[Union[TrainingParameters, dict]] = attr.field(default=None, repr=False)
    input_params: Optional[SchemaParameters] = attr.field(default=None, repr=False)
    output_params: Optional[SchemaParameters] = attr.field(default=None, repr=False)
    trainable: bool = False
    image: Optional[str] = None
    default_image: Optional[str] = None
    default_checkpoint: Optional[str] = None
    visibility: Optional[str] = attr.field(default="PRIVATE", validator=attr.validators.in_(["PRIVATE", "PUBLIC"]))
    owner_id: Optional[str] = None
    organization_id: Optional[str] = None
    metadata: Optional[dict] = attr.field(default={}, repr=False)
    _model_save_path: Optional[str] = None
    _created_at: Optional[datetime] = None
    _updated_at: Optional[datetime] = None
    _model_class_instance: Optional[BaseAI] = None
    _environs: Optional[EnvironmentFileProcessor] = attr.field(default=None, repr=False)
    _client: Optional["Client"] = attr.field(default=None, repr=False)
    _location: Optional[Path] = attr.field(default=None)
    id: Optional[str] = None
    _is_weights_loaded: bool = False
    _served_by: Optional[str] = None
    _deployed: bool = False
    _local_image: Optional[str] = None

    def __attrs_post_init__(self):
        self.default_deployment_parameters = AiDeploymentParameters.parse_from_optional(
            self.default_deployment_parameters
        )
        if self._location is None:
            self._location = self.model_class_path
        self._environs = EnvironmentFileProcessor(str(self._location), data=self._environs)
        # Cast code path to Path type
        if isinstance(self.code_path, str):
            self.code_path = [self.code_path]
        for i, path in enumerate(self.code_path):
            if isinstance(path, str):
                self.code_path[i] = Path(path)
        from superai import Client

        self._client: Client = Client.from_credentials()

        # Store the AI version in the metadata which gets saved in the database within the save() function
        from . import BaseAI

        self.metadata["base_ai_version"] = BaseAI.VERSION

    def to_dict(self, only_db_fields=False, not_null=False):
        """Converts the object to a json string."""

        def is_null(value):
            return bool(not_null and value is None)

        def filter_fn(attr, value):
            name = attr.name
            if is_null(value):
                return False
            if name.startswith("_"):
                # Ignore private fields
                return False
            return not only_db_fields or name in meta_ai_template.__field_names__

        def serialize(inst, field, value):
            if isinstance(value, EnvironmentFileProcessor):
                return value.to_dict()
            if isinstance(value, Path):
                return str(value)
            if isinstance(value, PydanticBaseModel):
                return value.dict(exclude_none=not_null)
            return value

        json_data = attr.asdict(self, filter=filter_fn, value_serializer=serialize)
        return json_data

    @classmethod
    def from_dict(cls, data: dict):
        """Creates an AI template object from a dict."""
        return cls(**data)

    def _init_model_class(self, load_weights=True, force_reload=False):
        """Initializes the BaseModel class.

        Args:
            load_weights: bool
                Will also load weights if True.
            force_reload:
                Will reload the model class even if it was already loaded before.

        """
        if not self.model_class:
            raise AIException(
                "Model class (model_class) not specified."
                "Model class is the name of the class that inherits from BaseAI."
                "If you are loading an existing AI, use `AI.load()` instead."
                "AI.load_essential() can be used to load an AI without any local functionality."
            )
        if self._model_class_instance is None or force_reload:
            class_path = Path(self.model_class_path)
            if class_path.is_absolute():
                log.warning(
                    "Model class path is absolute. Ensure that the path is given relative to the AI config location."
                )
                class_path = class_path.relative_to(self._location)

            model_class_template = get_user_model_class(
                model_name=self.model_class, save_location=self._location / class_path
            )
            self._model_class_instance: BaseAI = model_class_template(
                input_schema=self.input_schema,
                output_schema=self.output_schema,
                configuration=self.configuration,
            )
            self._model_class_instance.update_parameters(self.input_params, self.output_params)

            if load_weights and (not self._is_weights_loaded or force_reload):
                self._model_class_instance.load_weights(self.weights_path)
                self._is_weights_loaded = True

    @classmethod
    def load(cls, path: str, weights_path: Optional[str, Path] = None, pull_db_data=True) -> "AI":
        """Loads an AI from a local or S3 path.

        If the path is a valid local path, the AI model will be loaded from the local path. If the path is a valid S3
        path, the model will be downloaded from S3. Manage S3 access using your AWS credentials. If the path is a valid
        model path (i.e., prefix is `ai://some_name/version` or `ai://some_name/stage`), the database will be queried
        to find the relevant model and loaded.

        Args:
            path: The path to the AI model.
            weights_path: The path to the model weights file (if any).
            pull_db_data: If True, will pull the latest data from the database.

        Returns:
            An instance of the `AI` class.

        Raises:
            ValueError: If the path is not valid.
        """
        weights_path = Path(weights_path) if weights_path else None

        try:
            return AILoader.load_ai(path, weights_path, pull_db_data=pull_db_data)
        except botocore.exceptions.NoCredentialsError:
            # Handle NoCredentialsError here
            # You can log the error or raise a custom exception
            raise SuperAIAWSException("AWS credentials are missing or invalid. Unable to load AI from S3.")

    @classmethod
    def load_essential(
        cls,
        identifier: str,
    ):
        """Loads an AI from the database without any local functionality."""
        return AILoader.load_essential(identifier)

    def cache_path(self) -> Path:
        """Static cache path for storing the deployed predictor configuration"""
        path = Path(settings.path_for()) / "cache" / os.environ.get("RUN_UUID", f"{self.name}_{self.version}")
        path.mkdir(parents=True, exist_ok=True)
        return path

    @staticmethod
    def is_valid_version(version: str) -> bool:
        """Checks for valid short semantic version.
        Only major and minor versions are supported.
        """
        try:
            if len(version.split(".")) == 2:
                major, minor = version.split(".")
            else:
                major, minor, patch = version.split(".")
            if not major.isdigit() or not minor.isdigit():
                return False
            return int(major) >= 0 and int(minor) >= 0
        except ValueError:
            return False

    def _register(self):
        """Adds an entry in the meta AI database."""
        log.info(f"Creating database entry for {self}.")
        if self.id:
            raise ModelAlreadyExistsError("Model is already registered in the Database.")
        try:
            self.id = self._client.create_ai(self)
        except GraphQlException as e:
            if "Uniqueness violation" not in str(e):
                raise e
            self.id = self._client.list_ai(name=self.name, version=self.version)[0]["id"]
        return self.id

    def predict(self, inputs: Union[TaskInput, List[dict]]) -> TaskPredictionInstance:
        """Predicts from model_class and ensures that predict method adheres to schema in ai_definition.

        Args:
            inputs

        Returns:
           One TaskPrediction
        """
        self._init_model_class(load_weights=True)

        if not isinstance(inputs, TaskInput):
            try:
                TaskInput.parse_obj(inputs)
            except ValidationError as e:
                log.warning(
                    f"AI input could not be parsed as TaskInput. This could be enforced in future versions! {e}"
                )

        output = self._model_class_instance.predict(inputs)
        return TaskPredictionInstance.validate_prediction(output)

    def predict_batch(self, inputs: Union[List[List[dict]], TaskBatchInput]) -> List[TaskPredictionInstance]:
        """Predicts a batch of inputs from model_class and ensures that predict method adheres to schema in
        ai_definition.

        Args:
            inputs

        Returns:
            List of TaskPredictionInstances
            For each input in the batch we expect one prediction instance.

        """
        self._init_model_class(load_weights=True)

        if not isinstance(inputs, TaskBatchInput):
            try:
                TaskBatchInput.parse_obj(inputs)
            except ValidationError as e:
                log.warning(
                    f"AI input could not be parsed as TaskBatchInput. This could be enforced in future versions! {e}"
                )

        batch = self._model_class_instance.predict_batch(inputs)
        return TaskPredictionInstance.validate_prediction_batch(batch)

    def _save_local(self, path: Union[Path, str], overwrite=False) -> Path:
        """Export AI source files and config to local path."""
        return AILoader.save_local(self, overwrite=overwrite, path=path)

    def save(
        self,
        weights_path: Optional[Union[Path, str]] = None,
        overwrite=False,
        upload_source=False,
        create_checkpoint=False,
    ) -> AI:
        """Saves the AI in the backend.
        Allows uploading model source code and creating a checkpoint based on the weights.
        Only runs those steps if necesseary (still missing) or if forced by the user.

        Args:
            weights_path: Path to weights in s3
            overwrite: Overwrite existing entry
            upload_source: Force uploading new source code
            create_checkpoint: Force creating a new checkpoint based on weights_path

        Returns:
            AI object with updated id
        """
        self._load_id()

        if self.id:
            if not overwrite:
                raise AIException(
                    f"AI: {self.name}:{self.version} already exists with id {self.id}. "
                    f"Use `save(overwrite=True)` to overwrite."
                )
            if get_current_env() == "prod":
                confirm_action()
        else:
            self.id = self._register()

        # Only upload source if necessary
        if upload_source or not self._model_save_path:
            self._upload_model_source()

        # Only create checkpoint if necessary
        if create_checkpoint or not self.get_default_checkpoint():
            self.create_checkpoint(weights_path)

        self._client.update_ai_by_object(self)
        return self

    def _upload_model_source(self):
        """Uploads the model source to S3 and stores reference in DB."""
        save_path = AILoader.save_local(self, overwrite=True)
        # Defer uploading until we have a registered id
        bucket_name = get_ai_bucket()
        if not bucket_name:
            raise SuperAIAWSException(
                "Bucket name not found. Make sure you have valid credentials and are using the correct AWS account."
            )
        model_save_path = AILoader.upload_model_folder(save_path, self.id, self.name, self.version, bucket_name)
        self._client.update_ai(
            self.id,
            model_save_path=model_save_path,
        )
        self._model_save_path = model_save_path
        return model_save_path

    def create_checkpoint(self, weights_path: Optional[Union[Path, str]] = None) -> str:
        """Create a default checkpoint for the AI.
        Args:
            weights_path: The path to the model weights file (if any).
        Returns:
            the checkpoint id.
        """
        from superai.meta_ai import AICheckpoint

        # Create default checkpoint and store in database
        weights_path = weights_path or self.weights_path
        if not weights_path:
            log.warning("No weights path provided, passing empty directory.")
            weights_path = tempfile.mkdtemp()

        default_checkpoint = AICheckpoint(template_id=self.id, weights_path=str(weights_path)).save()
        self._client.update_ai(
            self.id,
            default_checkpoint=default_checkpoint.id,
        )
        self.default_checkpoint = default_checkpoint.id
        return default_checkpoint

    def update(self, **fields) -> AI:
        """Update the AI local in the backend.

        Args:
            fields: Fields to update

        Returns:
            AI object with updated fields
        """
        for k, v in fields.items():
            setattr(self, k, v)
        self.save(overwrite=True)
        return self

    def _load_id(self) -> Optional[str]:
        """Load the id from the database if it exists."""
        if not self.id:
            with contextlib.suppress(GraphQlException, IndexError):
                potential_ais = self._client.list_ai(name=self.name, version=self.version)
                if len(potential_ais) > 1:
                    raise AIException(
                        f"Multiple AIs found with name {self.name} and version {self.version}. "
                        f"Please specify the id."
                        f"Found: {potential_ais}"
                    )

                self.id = potential_ais[0].id
                log.info(f"Loaded AI {self.name}:{self.version} with id {self.id}")
        return self.id

    def build(
        self,
        orchestrator: BaseAIOrchestrator = Orchestrator.AWS_EKS,
        deployment_parameters: Optional[AiDeploymentParameters] = None,
        skip_build: bool = False,
        overwrite: bool = True,
    ) -> AI:
        """Build the image and return the image name.
        Args:
            deployment_parameters: Optional deployment parameters to override the default deployment parameters.
            skip_build: Skip building and return the image name which would be built.
            overwrite: Overwrite existing AI staging directory for building.
            orchestrator:

        Returns:
            AI object with the image name set.

        """
        from .image_builder import AiImageBuilder

        image_builder = AiImageBuilder(
            orchestrator,
            ai=self,
            deployment_parameters=deployment_parameters or self.default_deployment_parameters,
            overwrite=overwrite,
        )
        local_image_name = image_builder.build_image(skip_build=skip_build)
        self._local_image = local_image_name

        return self

    def push_image(self, local_image: Optional[str] = None) -> AI:
        """Push model in ECR, involves tagging and pushing.
        Note that your default AWS credentials will be used for this.

        Args:
            local_image: Local image name to push. If not provided, will use the ai._local_image from previous build.

        Returns:
            AI: The AI object with the updated image name.
        """

        if not self.id:
            raise ModelNotFoundError("No ID found. AI needs to be registered via `ai.save()` first.")
        if not (local_image or self._local_image):
            raise AIException("No local image found. Try ai.build() first.")
        local_image = local_image or self._local_image

        full_name = push_image(image_name=local_image, model_id=self.id, version=self.version)
        self._client.update_ai(self.id, image=full_name)
        self.image = full_name
        return self

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
        """Train the AI locally

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
        from superai.meta_ai.ai_trainer import AITrainer

        trainer = AITrainer(self)
        os.environ["IS_TRAINING"] = "True"
        return trainer.train(
            model_save_path=model_save_path,
            training_data=training_data,
            test_data=test_data,
            production_data=production_data,
            weights_path=weights_path,
            encoder_trainable=encoder_trainable,
            decoder_trainable=decoder_trainable,
            hyperparameters=hyperparameters,
            model_parameters=model_parameters,
            callbacks=callbacks,
            validation_data=validation_data,
            train_logger=train_logger,
        )

    @classmethod
    def from_yaml(
        cls,
        yaml_file: Union[Path, str],
        pull_db_data=False,
        override_weights_path: Optional[str] = None,
        add_name_prefix: Optional[str] = None,
    ) -> AI:
        """Create an AI_Template instance from a yaml file
        Args:
            yaml_file: Path to the yaml file
            pull_db_data: If True, will pull the latest data from the database.
            override_weights_path: If provided, will override the weights path in the yaml file.
            add_name_prefix: If provided, will add the prefix to the name in the yaml file.
                This is can be used for CI testing in isolated namespaces.
                Also, the name prefix can be provided via the environment variable AI_NAME_PREFIX.
        """
        add_name_prefix = add_name_prefix or os.environ.get("AI_NAME_PREFIX")

        with open(yaml_file, "r") as f:
            yaml_dict = yaml.safe_load(f)

        # Check for legacy yaml format
        legacy_yaml_dict = cls._check_legacy_yaml(yaml_dict)
        yaml_dict = legacy_yaml_dict or yaml_dict

        ai_id = yaml_dict.get("id")
        if pull_db_data and ai_id:
            db_dict = AILoader._get_ai_dict_by_id(ai_id)
            yaml_dict.update(db_dict)

        if override_weights_path:
            yaml_dict["weights_path"] = override_weights_path

        yaml_dict = cls._remove_patch_from_version(yaml_dict)

        if add_name_prefix:
            prefix = f"{add_name_prefix}-"
            if not yaml_dict["name"].startswith(prefix):
                logger.info(f"Adding name prefix {add_name_prefix} to AI name")
                yaml_dict["name"] = f"{prefix}{yaml_dict['name']}"

        return AI.from_dict(yaml_dict)

    from typing import Optional

    @classmethod
    def from_db(cls, ai_id: Optional[str] = None, ai_uri: Optional[str] = None) -> "AI":
        if ai_id is None and ai_uri is None:
            raise ValueError("Either 'ai_id' or 'ai_uri' must be provided.")

        db_dict = None
        if ai_id:
            db_dict = AILoader._get_ai_dict_by_id(ai_id)

        # Add logic for `ai_uri` if needed

        return AI.from_dict(db_dict)

    @staticmethod
    def _remove_patch_from_version(yaml_input: Dict) -> Dict:
        """Remove the patch version from the version number"""
        yaml_dict = yaml_input.copy()
        version = yaml_dict.get("version")
        if version is not None and re.match(r"^[0-9]+\.[0-9]+\.[0-9]+$", str(version)):
            patch = version.split(".")[2]
            version = str(version).removesuffix(f".{patch}")
            yaml_dict["version"] = version
        return yaml_dict

    @staticmethod
    def _check_legacy_yaml(yaml_dict) -> Optional[Dict]:
        """Previously the yaml config contained separate keys for template and instance and deploy.
        Now the yaml config is flattened.
        This method checks for the old keys and updates the yaml dict to the new format.
        Some keys are redundant. In those cases, the keys in the template section are preferred.

        Args:

        """
        old_sections = ["template", "instance", "deploy"]
        new_dict = {}

        # Prefer name from the instance to keep old compatibility with DP
        name = yaml_dict.get("instance", {}).get("name") or yaml_dict.get("template", {}).get("name")

        legacy = False
        for section in old_sections:
            if section in yaml_dict:
                new_dict.update(yaml_dict[section])
                legacy = True
        if not legacy:
            return None

        # In case of redundancy, prefer keys from the 'template' section
        if "template" in yaml_dict:
            new_dict.update(yaml_dict["template"])

        # Add name from instance
        if name:
            new_dict["name"] = name

        # Rename legacy names to new field names
        rename_map = {
            "deployment_parameters": "default_deployment_parameters",
        }
        for old_name, new_name in rename_map.items():
            if old_name in new_dict:
                new_dict[new_name] = new_dict.pop(old_name)

        # Pop deprecated keys
        deprecated_keys = ["orchestrator", "redeploy"]
        for key in deprecated_keys:
            if key in new_dict:
                logger.warning(f"Key {key} is deprecated. Please use the new format.")
                new_dict.pop(key)

        if "version" in new_dict:
            try:
                _ai_version_validator(None, None, new_dict["version"])
            except AIException:
                logger.exception(
                    "Version is not in the correct format. Please use the new format. Falling back to 1.0.0"
                )
                new_dict["version"] = "1.0.0"

        log.info(f"Updated yaml dict: {new_dict}")
        return new_dict

    def to_yaml(self, yaml_file: Union[Path, str], not_null: bool = True) -> None:
        """Create an AI_Template instance from a yaml file"""
        with open(yaml_file, "w") as f:
            yaml.safe_dump(self.to_dict(not_null=not_null), f)

    def get_default_checkpoint(self) -> Optional["AICheckpoint"]:
        """Get the default checkpoint for this AI"""
        from superai.meta_ai import AICheckpoint

        if self.default_checkpoint:
            return AICheckpoint.load(self.default_checkpoint)
        loaded = AICheckpoint.get_default_template_checkpoint(self.id)
        if loaded:
            self.default_checkpoint = loaded.id
            return loaded

    def create_instance(self, name: str = None, **kwargs) -> AIInstance:
        """Create an instance of this AI.

        The instance is the actual model that can be used for predictions and training and assigned to a
        project/application.

        Args:
            name: Name of the instance, if not provided, will use the name of the template
            **kwargs: Additional arguments to be passed to the instance
        """
        from superai.meta_ai import AIInstance

        self._load_id()
        return AIInstance.instantiate(ai=self, name=name, **kwargs)

    @property
    def local_image(self):
        return self._local_image
