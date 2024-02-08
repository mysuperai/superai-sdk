import datetime
import json
import os
from pathlib import Path
from typing import Optional, Union

from superai.config import get_ai_bucket
from superai.log import get_logger
from superai.meta_ai import AI, AIInstance, TrainingOrchestrator
from superai.meta_ai.ai_helper import ecr_full_name, upload_dir
from superai.meta_ai.dataset import DatasetMetadata
from superai.meta_ai.parameters import (
    AiDeploymentParameters,
    HyperParameterSpec,
    ModelParameters,
    TrainingParameters,
)
from superai.meta_ai.schema import TrainerOutput

log = get_logger(__name__)
DEPLOYMENT_PARAMETERS_SUBKEY = (
    "deployment_parameters"  # Used to access deployment parameters in the training parameters
)


class AITrainer:
    """Trainer class for AI.
    Contains logic to prepare and execute training for an AI."""

    def __init__(self, ai: AI, ai_instance: Optional[AIInstance] = None):
        self.ai = ai
        self.ai_instance = ai_instance

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
        self.ai._init_model_class(load_weights=True)
        model_class = self.ai._model_class_instance

        if train_logger is not None:
            model_class.update_logger_path(train_logger)
        else:
            model_class.update_logger_path(
                os.path.join(
                    self.ai._location,
                    "logs/fit/" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S"),
                ),
            )
        log.info(f"If tensorboard callback is present, logging in {model_class.logger_dir}")
        return model_class.train(
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

    def training_deploy(
        self,
        training_data_dir: Optional[Union[str, Path]] = None,
        skip_build: bool = False,
        properties: Optional[Union[dict, AiDeploymentParameters]] = None,
        training_parameters: Optional[TrainingParameters] = None,
        enable_cuda: bool = False,
        app_id: Optional[str] = None,
        task_name: Optional[str] = None,
        dataset_metadata: Optional[DatasetMetadata] = None,
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
            build_all_layers: Perform a fresh build of all layers
            envs: Pass custom environment variables to the deployment. Should be a dictionary like
                  {"LOG_LEVEL": "DEBUG", "OTHER": "VARIABLE"}
            download_base: Always download the base image to get the latest version from ECR
        """
        if training_data_dir is None and app_id is None:
            raise ValueError("Either app_id or training_data_dir is required")
        if training_data_dir is not None and app_id is not None:
            raise ValueError("Only one of app_id or training_data_dir is allowed")

        # TODO: add method which works with local training
        orchestrator = TrainingOrchestrator.AWS_EKS
        kwargs.pop("orchestrator", None)

        properties = properties or {}
        dataset_metadata = dataset_metadata or DatasetMetadata()

        deployment_parameters = AiDeploymentParameters.merge_deployment_parameters(
            self.ai.default_deployment_parameters, properties, enable_cuda
        )
        loaded_parameters = {}
        if not skip_build:
            # Build image and merge all parameters
            loaded_parameters = self._prepare_training(
                orchestrator, deployment_parameters, training_parameters, skip_build, **kwargs
            )

        # Create a training template
        template_id = self._get_or_create_training_entry(
            ai_instance_id=self.ai_instance.id, properties=loaded_parameters, app_id=app_id
        )
        log.info(
            f"Starting training for ai_instance_id={self.ai_instance.id} template_id="
            f"{template_id} with properties={loaded_parameters} and deployment_parameters={deployment_parameters} "
        )

        source_checkpoint_id = self.ai_instance.get_checkpoint().id  # TODO: Allow passing of checkpoint id
        log.info(f"Using source checkpoint {source_checkpoint_id} for training")

        if training_data_dir is not None:
            log.info(f"Using local training data from {training_data_dir}")
            # Create the database entry for the training, initially in stopped state
            instance_id = self.ai._client.create_training_entry(
                ai_instance_id=self.ai_instance.id,
                properties=loaded_parameters,
                starting_state="STOPPED",
                template_id=template_id,
                source_checkpoint_id=source_checkpoint_id,
            )
            self._upload_training_data(training_data_dir, training_id=instance_id)
        else:
            log.info(f"Using app_id={app_id} and task_name={task_name} to retrieve training data")
            instance_id = self.ai._client.start_training_from_app_model_template(
                app_id=app_id,
                ai_instance_id=self.ai_instance.id,
                task_name=task_name,
                training_template_id=template_id,
                checkpoint_id=source_checkpoint_id,
                current_properties=loaded_parameters,
                dataset_metadata=dataset_metadata.dict(exclude_none=True, exclude_unset=True),
            )
        # Start the training in the backend
        instance = self.ai._client.update_training_instance(instance_id, app_id, state="STARTING")
        log.info(f"Created training instance : {instance}. Will be started in the backend")
        return instance

    def _prepare_training(self, orchestrator, deployment_parameters, training_parameters, skip_build, **kwargs) -> dict:
        """Prepares image and parameters for training

        1. Builds the model if not skipped
        2. Uploads the model to ECR
        3. Queries the default training parameters and merges with the provided ones
        4. Add the deployment parameters to the training parameters (contain hardware requirements)

        Args:
            orchestrator: The orchestrator to use for training (currently only AWS EKS is supported)
            deployment_parameters: Deployment parameters, e.g. hardware requirements
            training_parameters: Training parameters
            skip_build: Skip building
            **kwargs: Additional kwargs for the image builder

        Returns:

        """
        # Build image and compile deployment properties
        self.ai.build(
            orchestrator,
            deployment_parameters=deployment_parameters,
            skip_build=skip_build,
            **kwargs,
        )

        global_image_name, *_ = ecr_full_name(image_name=self.ai.name, version=self.ai.version, model_id=self.ai.id)

        if not skip_build:
            self.ai.push_image(self.ai._local_image)
        self.ai._client.update_ai(template_id=self.ai.id, trainable=True)

        # Merge training parameters with default ones
        if training_parameters:
            if isinstance(training_parameters, dict):
                train_obj = TrainingParameters()
                train_obj.from_dict(training_parameters)
            loaded_parameters = json.loads(train_obj.to_json())
        else:
            loaded_parameters = self.ai._client.get_ai(template_id=self.ai.id)["default_training_parameters"] or {}
            if isinstance(loaded_parameters, str):
                loaded_parameters = json.loads(loaded_parameters)

        # Merge parameters with deployment parameters
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
        """(Deprecated) Start a training from an app. This method is deprecated and will be removed in future versions.
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

    def _get_or_create_training_entry(self, ai_instance_id: str, app_id: str = None, properties=None):
        """
        Get or create a training template entry for a given AI instance ID and app ID.

        Args:
            ai_instance_id: The ID of the AI instance.
            app_id: The ID of the app.
            properties: The properties of the training template.

        Returns:
            The ID of the training template.
        """
        # Set default properties to an empty dictionary if none is provided
        properties = properties or {}

        # Check if a training template entry already exists
        existing_templates = self.ai._client.list_training_templates(ai_instance_id=ai_instance_id, app_id=app_id)
        if existing_templates:
            template_id = existing_templates[0].id
            log.info(f"Found existing training template with ID {template_id}")
            if properties:
                # Update the properties of the existing training template if properties are provided
                self.ai._client.update_training_template(template_id=template_id, properties=properties)
        else:
            # Create a new training template entry if none exists
            template_id = self.ai._client.create_training_template_entry(
                ai_instance_id=ai_instance_id, properties=properties, app_id=app_id
            )["id"]
            log.info(f"Created new training template with ID {template_id}")

        return template_id

    def _upload_training_data(self, local_directory: str, training_id: str) -> str:
        training_data_path = os.path.join("training/data", training_id)
        # TODO: replace s3 push with push via signed url or similar
        local_directory_path = Path(local_directory)
        upload_dir(local_directory_path, training_data_path, get_ai_bucket(), prefix="/")
        log.info(f"Uploaded Training data to {training_data_path}.")
        return training_data_path
