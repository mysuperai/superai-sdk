import typing
from pathlib import Path
from typing import List, Optional, Union

import attr
import yaml
from pydantic import BaseModel

from superai.apis.meta_ai.meta_ai_graphql_schema import meta_ai_modelv2
from superai.config import get_current_env
from superai.log import get_logger
from superai.meta_ai import AI
from superai.meta_ai.ai_checkpoint import CheckpointTag
from superai.meta_ai.ai_helper import _not_none_validator, confirm_action
from superai.meta_ai.deployed_predictors import RemotePredictor
from superai.meta_ai.exceptions import (
    AIException,
    DockerImageNotFoundError,
    ModelNotFoundError,
)
from superai.meta_ai.orchestrators import Orchestrator
from superai.meta_ai.parameters import AiDeploymentParameters, TrainingParameters
from superai.meta_ai.schema import TaskPredictionInstance

log = get_logger(__name__)

if typing.TYPE_CHECKING:
    from superai.meta_ai.ai import AI
    from superai.meta_ai.ai_checkpoint import AICheckpoint


@attr.define()
class AIInstance:
    """Contains data about an AI instance.
    AI instances are concrete instances of an AI and namespaced to a specific user or organization.
    AI instances are used as a collection of checkpoints and other metadata and properties related to a specific AI model.
    The checkpoints are used to deploy the model and predict.

    This class provides a simple interface for creating, updating and deleting AI instances. An instance can be created
    using a pre-defined template or a custom one.

        Example:
            t1 = AI_Template.load("enrique/template1:v1")
                t1.create_instance()
            ai = AiInstance(t1.id)  # Create an instance using a pre-defined template # TODO: Enable this instantiation methos
                 AiInstance.create(template_id = t1.id)

    Attributes:
        template_id: A string representing the id of the template used to create the instance.
        id: A string representing the id of the AI instance.
        name: A string representing the name of the AI instance.
        checkpoint_tag: A field controlling the currently used checkpoint.
        model_id: A string representing the id of the model used to create the AI instance.
        created_at: A string representing the date and time the AI instance was created.
        updated_at: A string representing the date and time the AI instance was last updated.
        description: A string representing the description of the AI instance.
        served_by: A string representing the Deployment used to serve the AI instance.
        deployment_parameters: A dictionary representing the parameters used to deploy the AI instance.
        editor_id: A string representing the id of the user who edited the AI instance last.
        owner_id: A string representing the id of the user who owns the AI instance.
        organization_id: A string representing the id of the organization that owns the AI instance.

    """

    name: str
    template_id: str = attr.field(validator=_not_none_validator)
    checkpoint_tag: CheckpointTag = attr.field(default=CheckpointTag.LATEST)
    id: str = attr.field(default=None)
    created_at: str = attr.field(default=None)
    updated_at: str = attr.field(default=None)
    description: str = attr.field(default=None)
    served_by: str = attr.field(default=None)
    deployment_parameters: dict = attr.field(default=None, repr=False)
    editor_id: str = attr.field(default=None)
    owner_id: int = attr.field(default=None)
    organization_id: int = attr.field(default=None)
    ai_worker_id: str = attr.field(default=None)
    ai_worker_username: str = attr.field(default=None)
    visibility: Optional[str] = attr.field(default="PRIVATE", validator=attr.validators.in_(["PRIVATE", "PUBLIC"]))
    _predictor: Optional[RemotePredictor] = attr.field(default=None, repr=False)

    _client: Optional["Client"] = attr.field(default=None, repr=False)

    @property
    def client(self):
        from superai.client import Client

        if self._client is None:
            self._client = Client.from_credentials()
        return self._client

    @classmethod
    def load(cls, id):
        # Load the ai_instance from the backend data
        from superai.client import Client

        client = Client.from_credentials()
        backend_data = client.get_ai_instance(id, to_json=True)
        if not backend_data:
            raise ModelNotFoundError(f"AI instance with id {id} not found")
        return cls.from_dict(backend_data)

    def reload(self):
        """Reloads the AI instance from the backend."""
        if self.id is None:
            raise AIException("AI instance not saved. Please save the instance first.")
        return self.load(self.id)

    def save(self):
        """Saves the AI instance to the backend
        Includes check for existing instance.
        """
        # Check for existing instance
        ai_instance = self.client.get_ai_instance_by_name(self.name, self.template_id)
        if ai_instance:
            self.id = ai_instance.id

        if self.id is None:
            # Try first to fetch existing instance
            self.id = self.client.create_ai_instance(self)
            log.info("New AI instance created")
        else:
            log.info("AI instance already exists. Updating the instance.")
            self.update()

        return self

    @classmethod
    def instantiate(
        cls, ai: "AI", name: str = None, weights_path: str = None, force_clone_checkpoint: bool = False, **kwargs
    ) -> "AIInstance":
        """Instantiate an AI instance from an AI.
        Allows setting weights and other parameters.

        Args:
            ai: The AI to instantiate.
            name: The name of the AI instance, if not provided, the name of the AI will be used.
            weights_path: The path to the weights to use for the AI instance, if not provided, the default AI checkpoint will be used.
            force_clone_checkpoint: If True, will clone the template checkpoint even if a checkpoint already exists.
            **kwargs: Additional parameters to pass to the AI instance.
        """
        instance = AIInstance(template_id=ai.id, name=name or ai.name, **kwargs)
        instance.save()

        existing_checkpoint = instance.get_checkpoint()
        if weights_path:
            if existing_checkpoint:
                existing_checkpoint.save(weights_path=weights_path, overwrite=True)
            else:
                from superai.meta_ai.ai_checkpoint import AICheckpoint

                AICheckpoint(template_id=ai.id, weights_path=weights_path, ai_instance_id=instance.id).save()
        elif not existing_checkpoint or force_clone_checkpoint:
            instance._clone_template_checkpoint(ai)

        # Reload the instance to get the latest data from backend
        instance = instance.reload()

        return instance

    def _clone_template_checkpoint(self, ai: "AI") -> "AICheckpoint":
        """Will create a new checkpoint with the same name and tag as the template checkpoint but scoped to the AI instance."""
        if not self.id:
            raise AIException("AI instance not saved. Please save the instance first.")
        # Get the template checkpoint
        template_checkpoint = ai.get_default_checkpoint()

        # Replace already existing latest checkpoint
        latest = self.get_checkpoint("LATEST")

        # Clone the checkpoint
        clone = template_checkpoint.create_clone(ai_instance_id=self.id, tag=None if latest else "LATEST")

        if latest:
            log.info("Replacing existing latest checkpoint of the AI instance")
            from .ai_checkpoint import AICheckpoint

            AICheckpoint._transfer_tag(latest, clone, "LATEST")

        return clone

    def update(
        self,
        deployment_parameters=None,
        name=None,
        description=None,
        checkpoint_tag=None,
        served_by=None,
        visibility=None,
    ):
        if deployment_parameters is not None:
            self.deployment_parameters = deployment_parameters
        if name is not None:
            self.name = name
        if description is not None:
            self.description = description
        if checkpoint_tag is not None:
            self.checkpoint_tag = checkpoint_tag
        if visibility is not None:
            self.visibility = visibility

        changed = {
            "deployment_parameters": self.deployment_parameters,
            "name": self.name,
            "description": self.description,
            "checkpoint_tag": self.checkpoint_tag,
            "visibility": self.visibility,
        }

        # Only set this when not-null to not overwrite existing value in backend
        if served_by:
            changed["served_by"] = served_by
            self.served_by = served_by

        self.client.update_ai_instance(
            self.id,
            **changed,
        )
        log.debug(f"AI instance {self} updated")

    def delete(self):
        self.client.delete_ai_instance(self.id)

    def to_dict(self, only_db_fields=False, exclude_none=False):
        """Converts the object to a json string."""

        def filter_fn(attr, value):
            name = attr.name
            if name.startswith("_"):
                # Ignore private fields
                return False
            if only_db_fields and name not in meta_ai_modelv2.__field_names__:
                # Ignore non-db fields
                return False
            if exclude_none and value is None:
                # Ignore null values
                return False

            return True

        json_data = attr.asdict(self, filter=filter_fn)
        return json_data

    def assign_to_project(self, project_id: str):
        self.client.project_set_model(app_id=project_id, assignment="TASK", instance_id=self.id)
        log.info(f"AI instance {self.id} assigned to project {project_id}")

    def remove_from_project(self, project_id: str):
        removed = self.client.delete_ai_project_assignment(app_id=project_id, instance_id=self.id)
        if not removed:
            raise AIException(
                f"Failed to remove AI instance {self.id} from project {project_id}. Could not find assignment."
            )
        log.info(f"AI instance {self} removed from project {project_id}")

    def get_checkpoint(self, tag: Optional[str] = None) -> Optional["AICheckpoint"]:
        """Get the checkpoint for the AI instance

        By default, returns the checkpoint with the tag specified in the instance.

        """
        from superai.meta_ai import AICheckpoint

        tag = tag or self.checkpoint_tag

        # Get the default checkpoint for the instance
        return AICheckpoint.load_by_instance_and_tag(ai_instance_id=self.id, tag=tag)

    def list_checkpoints(self) -> List["AICheckpoint"]:
        """Get the checkpoint for the AI instance

        By default, returns the checkpoint with the tag specified in the instance.

        """
        from superai.meta_ai import AICheckpoint

        # Get the default checkpoint for the instance
        return AICheckpoint.list_checkpoints(ai_instance_id=self.id)

    def deploy(
        self,
        redeploy: bool = False,
        wait_time_seconds: int = 1,
        orchestrator: Union[Orchestrator, str] = Orchestrator.AWS_EKS_ASYNC,
    ) -> "RemotePredictor":
        """Deploys the model to the remote backend to serve predictions.
        Can wait for the deployment to be ready.

        Args:
            redeploy: Allow un-deploying existing deployment and replacing it.
            wait_time_seconds: Time to wait for the deployment to be ready.
        Internal-Args:
            orchestrator: Orchestrator to use for deployment.

        """

        if redeploy and get_current_env() == "prod":
            confirm_action()

        ai = AI.load_essential(self.template_id)

        if not ai.image:
            raise DockerImageNotFoundError(
                "AI has no Docker image stored. Try ai.build() and ai.push_image() on the AI object first."
            )
        orchestrator = Orchestrator(orchestrator)
        predictor_obj: RemotePredictor = RemotePredictor(
            orchestrator=orchestrator,
            deploy_properties=ai.default_deployment_parameters,
            ai=self,
        )
        deployment_id = predictor_obj.deploy(redeploy=redeploy, wait_time_seconds=wait_time_seconds)
        self._predictor = predictor_obj

        self.served_by = deployment_id
        self.update(served_by=deployment_id)

        return predictor_obj

    def predict(self, input_data: dict, params: dict = None, wait_time_seconds=180) -> TaskPredictionInstance:
        """Predict with remote predictor.

        Args:
            input_data: Input data to send to the predictor.
            params: Optional parameters to send to the predictor.
            wait_time_seconds: Time to wait for the prediction to be ready.

        Returns:
            List of TaskPredictionInstance objects.

        """
        if not self._predictor:
            self._predictor = RemotePredictor(ai=self, orchestrator=Orchestrator.AWS_EKS_ASYNC)
            existing = self._predictor.load()
            if not existing:
                raise AIException("AI instance not deployed. Please deploy first with ai_instance.deploy().")
        return self._predictor.predict(input=dict(data=input_data, params=params), wait_time_seconds=wait_time_seconds)

    def undeploy(self, wait_time_seconds=1) -> Optional[bool]:
        """Undeploy the model from the remote backend.

        Args:
            wait_time_seconds: Number of seconds to wait for the deployment to be undeployed. Otherwise, process will continue async.
        """
        if self.id:
            if not self.served_by:
                raise AIException("AI instance not deployed. Please deploy first with ai_instance.deploy().")
            if not self._predictor:
                self._predictor = RemotePredictor(ai=self, orchestrator=Orchestrator.AWS_EKS_ASYNC)
            self._predictor.terminate(wait_seconds=wait_time_seconds)
        else:
            log.info("No ID found. Is the AI instance registered in the Database?")
            return None

    def train(
        self,
        app_id: Optional[str] = None,
        local_path: Optional[Union[str, Path]] = None,
        deployment_parameters: Optional[Union[dict, AiDeploymentParameters]] = None,
        training_parameters: Optional[TrainingParameters] = None,
        skip_build: bool = True,
        dataset_metadata: Optional["DatasetMetadata"] = None,
        **kwargs,
    ) -> dict:
        """Trains the AI instance (remotely).
        Supports providing data from local path or from an existing project via app_id.

        The training is done asynchronously. To check the status of the training,
            use the `client.get_training_instance` method with the training id.

        """
        # Check for XOR of app_id and local_path
        if (app_id is None and local_path is None) or (app_id is not None and local_path is not None):
            raise AIException("Either app_id or local_path must be specified.")

        from superai.meta_ai import AI
        from superai.meta_ai.ai_trainer import AITrainer

        ai = AI.load_essential(self.template_id)
        trainer = AITrainer(ai, self)
        return trainer.training_deploy(
            app_id=app_id,
            training_data_dir=local_path,
            properties=deployment_parameters,
            training_parameters=training_parameters,
            skip_build=skip_build,
            dataset_metadata=dataset_metadata,
            **kwargs,
        )

    @classmethod
    def from_dict(cls, data: dict):
        """Creates a AiInstance object from a dict."""
        return cls(**data)


class AIInstanceConfig(BaseModel):
    """Simple CI/CD configuration for an AI instance."""

    weights_path: Optional[str] = None
    name: Optional[str] = None


class AIInstanceConfigFile(BaseModel):
    """Simple CI/CD configuration file for an AI instance placed in AI repositories.
    Contains a list of AIInstanceConfig objects used to instantiate multiple AI instances from a single AI template."""

    instances: List[AIInstanceConfig] = []

    def to_yaml(self, path: Union[str, Path]):
        """Saves the AIInstanceConfigFile to a yaml file."""
        with open(path, "w") as f:
            yaml.dump(self.dict(), f)

    @classmethod
    def from_yaml(cls, path: Union[str, Path]):
        """Loads the AIInstanceConfigFile from a yaml file."""
        with open(path, "r") as f:
            data = yaml.safe_load(f)
        return cls(**data)


def instantiate_instances_from_config(
    config: Union[AIInstanceConfigFile, Path], ai: AI, **ai_instance_args
) -> List[AIInstance]:
    """Instantiates AI instances from a config file."""
    instances = []
    if isinstance(config, Path):
        config = AIInstanceConfigFile.from_yaml(config)

    for instance in config.instances:
        ai_instance = AIInstance.instantiate(
            ai, name=instance.name, weights_path=instance.weights_path, **ai_instance_args
        )
        instances.append(ai_instance)
    return instances
