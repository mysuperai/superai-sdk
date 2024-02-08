from __future__ import annotations

import functools
import os
import time
from typing import TYPE_CHECKING, Any, Dict, List, Optional

import boto3  # type: ignore

from superai.config import settings
from superai.log import logger
from superai.meta_ai.ai_loader import AILoader
from superai.meta_ai.orchestrators import (
    BaseAIOrchestrator,
    Orchestrator,
    TrainingOrchestrator,
)
from superai.meta_ai.parameters import AiDeploymentParameters

log = logger.get_logger(__name__)

if TYPE_CHECKING:
    from superai.meta_ai import AI


def reset_workdir(function):
    @functools.wraps(function)
    def decorator(*args, **kwargs):
        cwd = os.getcwd()
        try:
            return function(*args, **kwargs)
        finally:
            os.chdir(cwd)

    return decorator


class AiImageBuilder:
    """Responsible for building the image.
    Inputs are mainly parameters for different orchestrator types and image name.

    Under the hood we built on top of a base image and adding AI source code with S2I.
    """

    ALLOWED_ORCHESTRATOR = BaseAIOrchestrator

    def __init__(
        self,
        orchestrator: BaseAIOrchestrator,
        ai: AI,
        deployment_parameters: Optional[AiDeploymentParameters] = None,
        overwrite: bool = False,
    ):
        """

        Args:
            orchestrator: Determines build strategy
        """
        staging_dir = AILoader.save_local(ai, overwrite=overwrite)
        from superai.meta_ai import AI

        ai = AI.load(str(staging_dir))

        self.orchestrator = orchestrator
        self._check_orchestrator()

        self.name = ai.name
        self.version = str(ai.version)
        self.entrypoint_class = ai.model_class
        self.environs = ai._environs
        self.location = str(ai._location)
        self.requirements = ai.requirements
        self.conda_env = ai.conda_env
        self.artifacts = ai.artifacts
        self.deployment_parameters = deployment_parameters or AiDeploymentParameters()
        self.staging_dir = staging_dir
        self.model_class_path = ai.model_class_path

    def _check_orchestrator(self) -> None:
        """Check if the orchestrator is valid for the current builder class.
        Subclasses should overwrite `ALLOWED_ORCHESTRATOR`.
        """
        if not isinstance(self.orchestrator, self.ALLOWED_ORCHESTRATOR):
            raise ValueError(
                f"Invalid Orchestrator={type(self.orchestrator)}, should be one of {list(self.ALLOWED_ORCHESTRATOR)}"
            )

    def prepare_entrypoint(self) -> None:
        """Prepare entrypoints and environment variables for the image."""
        if self.orchestrator in [
            Orchestrator.AWS_EKS,
            Orchestrator.AWS_EKS_ASYNC,
            Orchestrator.LOCAL_DOCKER_K8S,
            TrainingOrchestrator.AWS_EKS,
            TrainingOrchestrator.LOCAL_DOCKER_K8S,
        ]:
            # No handler needed for EKS
            return
        else:
            raise NotImplementedError()

    def prepare(self):
        self.prepare_entrypoint()

    def build_image(self, skip_build: bool = False) -> str:
        """Build the image and return the image name.
        Args:
            skip_build:

        Returns:
            full image name

        """
        # Updating environs before image builds
        envs = self.deployment_parameters.dict().get("envs") or {}
        for key, value in envs.items():
            self.environs.add_or_update(key, value)

        self.prepare()
        if skip_build:
            image = self.full_image_name(self.name, self.version)
            logger.info(f"Skipping build, using existing image {image} if available.")
        else:
            image = self.build_image_superai_builder(
                self.name, self.version, user_base_image=self.deployment_parameters.base_image
            )
            logger.info(f"Built image {image}")
        return image

    @reset_workdir
    def build_image_superai_builder(
        self,
        image_name: str,
        version_tag: str = "latest",
        python_version: str = "3.10",
        user_base_image: Optional[str] = None,
    ) -> str:
        """Build the image using superai builder

        Args:
            image_name: Name of the image to be built
            version_tag: Version tag of the image
            python_version: Python version to use, default is 310 = 3.10
            user_base_image: Base image provided by the user
        Returns:
            String image name
        """
        start = time.time()
        os.chdir(self.location)

        base_image = self._get_base_image(self.deployment_parameters, python_version, user_base_image)
        full_image_name = self.full_image_name(image_name, version_tag)

        self.environs.add_or_update("SUPERAI_CONFIG_ROOT", "/tmp/.superai")
        self.environs.add_or_update("SERVICE_TYPE=MODEL")
        self.environs.add_or_update("PERSISTENCE=0")
        self.environs.add_or_update("API_TYPE=REST")
        self.environs.add_or_update("SELDON_MODE=true")

        builder = AILoader.builder
        dockerfile_path = builder.get_dockerfile_path()
        # examples/ai/my_ai_project/code.MyModel.MyModel -> examples.ai.my_ai_project.code.MyModel.MyModel
        model_class_path = str(self.model_class_path).replace("/", ".")
        schema_object = builder.get_schema_object(
            dockerfile_path=dockerfile_path,
            full_image_name=full_image_name,
            entrypoint_class=self.entrypoint_class,
            model_class_path=model_class_path,
            base_image=base_image,
            environs=self.environs.to_dict(),
            region=settings.region,
        )
        builder.run(schema_object=schema_object, run_os=True)

        log.info(f"Built main container `{full_image_name}`")
        log.info(f"Time taken to build: {time.time() - start:.2f}s")

        return full_image_name

    @staticmethod
    def _get_base_image(
        deployment_parameters: AiDeploymentParameters,
        python_version: str = "3.10",
        user_base_image: Optional[str] = None,
    ):
        """Decide which base image to use based on the deployment parameters."""

        # Assert that python_version is in correct format, e.g. '3.10'
        if len(python_version.split(".")) != 2:
            raise ValueError(f"Invalid python version {python_version}, should be like '3.10'")

        default_image = f"python:{python_version}-slim-buster"
        gpu_image = "nvidia/cuda:11.8.0-runtime-ubuntu22.04"

        return user_base_image or (gpu_image if deployment_parameters.enable_cuda else default_image)

    @staticmethod
    def full_image_name(image_name, version_tag):
        return f"{image_name}:{version_tag}"

    @staticmethod
    def _get_docker_registry(region: str) -> str:
        account_id = "185169359328"  # boto3.client("sts").get_caller_identity()["Account"]
        return f"{account_id}.dkr.ecr.{region}.amazonaws.com"


def kwargs_warning(allowed_kwargs: List[str], **kwargs: Dict[str, Any]) -> None:
    if any(k not in allowed_kwargs for k in kwargs):
        log.warning(
            f"Keyword arguments {[k for k in kwargs if k not in allowed_kwargs]} unknown, make sure you are "
            f"passing the right keyword arguments"
        )
