from __future__ import annotations

import enum
import functools
import hashlib
import json
import os
import shutil
import time
from typing import Any, Dict, List, Optional, Union

import boto3  # type: ignore
from docker import DockerClient
from docker.errors import ImageNotFound

from superai import settings
from superai.log import logger
from superai.meta_ai.ai_helper import create_model_entrypoint, create_model_handler
from superai.meta_ai.dockerizer import aws_ecr_login, get_docker_client
from superai.meta_ai.environment_file import EnvironmentFileProcessor
from superai.meta_ai.parameters import AiDeploymentParameters
from superai.utils import system

log = logger.get_logger(__name__)


class BaseAIOrchestrator(str, enum.Enum):
    pass


class Orchestrator(BaseAIOrchestrator):
    LOCAL_DOCKER = "LOCAL_DOCKER"
    LOCAL_DOCKER_LAMBDA = "LOCAL_DOCKER_LAMBDA"
    LOCAL_DOCKER_K8S = "LOCAL_DOCKER_K8S"
    MINIKUBE = "MINIKUBE"
    AWS_SAGEMAKER = "AWS_SAGEMAKER"
    AWS_SAGEMAKER_ASYNC = "AWS_SAGEMAKER_ASYNC"
    AWS_LAMBDA = "AWS_LAMBDA"
    AWS_EKS = "AWS_EKS"


class TrainingOrchestrator(BaseAIOrchestrator):
    LOCAL_DOCKER_K8S = "LOCAL_DOCKER_K8S"
    AWS_EKS = "AWS_EKS"


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
    """
    Responsible for building the image.
    Inputs are mainly parameters for different orchestrator types and image name.

    Under the hood we built on top of a base image and adding AI source code with S2I.
    """

    ALLOWED_ORCHESTRATOR = BaseAIOrchestrator

    def __init__(
        self,
        orchestrator: BaseAIOrchestrator,
        entrypoint_class: str,
        location: str,
        name: str,
        version: Union[str, int],
        environs: EnvironmentFileProcessor,
        requirements: Optional[Union[str, List[str]]] = None,
        conda_env: Optional[Union[str, Dict]] = None,
        artifacts: Optional[Dict] = None,
        deployment_parameters: Optional[AiDeploymentParameters] = None,
    ):
        """

        Args:
            orchestrator: Determines build strategy
            entrypoint_class: Is entrypoint of container process. Should be the class inheriting from BaseModel.
            name: Name of model, used for image name
            version: Version of model, used for image name
            environs: Environment file processor
            location: Location of model in local file system
        """
        self.orchestrator = orchestrator
        self._check_orchestrator()

        self.name = name
        self.version = str(version)
        self.entrypoint_class = entrypoint_class
        self.environs = environs
        self.location = location
        self.requirements = requirements
        self.conda_env = conda_env
        self.artifacts = artifacts
        self.deployment_parameters = deployment_parameters or AiDeploymentParameters()

    def _check_orchestrator(self) -> None:
        """
        Check if the orchestrator is valid for the current builder class.
        Subclasses should overwrite `ALLOWED_ORCHESTRATOR`.
        """
        if not isinstance(self.orchestrator, self.ALLOWED_ORCHESTRATOR):
            raise ValueError(
                f"Invalid Orchestrator={type(self.orchestrator)}, should be one of {[e for e in self.ALLOWED_ORCHESTRATOR]}"
            )

    def prepare_entrypoint(self) -> None:
        """
        Prepare entrypoints and environment variables for the image.

        """
        if self.orchestrator in [
            Orchestrator.LOCAL_DOCKER,
            Orchestrator.AWS_SAGEMAKER,
            Orchestrator.AWS_SAGEMAKER_ASYNC,
        ]:
            with open(os.path.join(self.location, "handler.py"), "w") as handler_file:
                scripts_content = create_model_handler(self.entrypoint_class, lambda_mode=False)
                handler_file.write(scripts_content)
            with open(os.path.join(self.location, "dockerd-entrypoint.py"), "w") as entry_point_file:
                entry_point_file_content = create_model_entrypoint(self.deployment_parameters.sagemaker_worker_count)
                entry_point_file.write(entry_point_file_content)

        elif self.orchestrator in [Orchestrator.LOCAL_DOCKER_LAMBDA, Orchestrator.AWS_LAMBDA]:
            with open(os.path.join(self.location, "handler.py"), "w") as handler_file:
                scripts_content = create_model_handler(
                    self.entrypoint_class, lambda_mode=True, ai_cache=self.deployment_parameters.lambda_ai_cache
                )
                handler_file.write(scripts_content)

        elif self.orchestrator in [
            Orchestrator.AWS_EKS,
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

    def build_image(
        self,
        cuda_devel: bool = False,
        enable_eia: bool = False,
        skip_build: bool = False,
        build_all_layers: bool = False,
        download_base: bool = False,
        use_internal: bool = False,
    ) -> str:
        """
        Build the image and return the image name.
        Args:
            cuda_devel
            enable_eia:
            skip_build:
            use_internal: If true, use the internal development base image

        Returns:
            full image name

        """
        # Updating environs before image builds
        envs = self.deployment_parameters.dict().get("envs") or {}
        for key, value in envs.items():
            self.environs.add_or_update(key, value)

        self.prepare()
        if not skip_build:
            image_name = self.build_image_s2i(
                self.name,
                self.version,
                enable_cuda=self.deployment_parameters.enable_cuda,
                enable_eia=enable_eia,
                cuda_devel=cuda_devel,
                from_scratch=build_all_layers,
                always_download=download_base,
                use_internal=use_internal,
            )
        else:
            image_name = self.full_image_name(self.name, self.version)
        return image_name

    def _track_changes(
        self,
        cache_root: Optional[str] = None,
    ) -> bool:
        if not cache_root:
            cache_root = os.path.join(settings.path_for(), "cache")
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
        cache_folder = os.path.join(cache_root, self.name, self.version)
        os.makedirs(cache_folder, exist_ok=True)

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
                log.info("Detected changes in %s, rebuilding image", file)
                changes_in_build = True
            new_hash[file] = file_hash
        with open(hash_file, "w") as f_hash:
            json.dump(new_hash, f_hash)

        # Store orchestrator type to invalidate cache when orchestrator changes
        orchestrator_type_file = os.path.join(cache_folder, ".orchestrator.txt")
        if not os.path.exists(orchestrator_type_file):
            with open(orchestrator_type_file, "w") as f_orchestrator_cache:
                json.dump({}, f_orchestrator_cache)
        with open(orchestrator_type_file, "r") as f_orchestrator_cache:
            cached_op_type = json.load(f_orchestrator_cache)
            if self.orchestrator != cached_op_type.get("orchestrator"):
                log.info("Orchestrator changed, rebuilding image")
                changes_in_build = True
        with open(orchestrator_type_file, "w") as f_orchestrator_cache:
            json.dump({"orchestrator": self.orchestrator}, f_orchestrator_cache)

        return changes_in_build

    @reset_workdir
    def build_image_s2i(
        self,
        image_name: str,
        version_tag: str = "latest",
        enable_cuda: bool = False,
        enable_eia: bool = False,
        cuda_devel: bool = False,
        from_scratch: bool = False,
        always_download=False,
        use_internal=False,
    ) -> str:
        """
        Build the image using s2i

        Args:
            image_name: Name of the image to be built
            version_tag: Version tag of the image
            enable_cuda: Enable CUDA in the images
            enable_eia: Generate elastic inference compatible image
            cuda_devel: Use CUDA devel base image
            from_scratch: Generate all layers from the scratch
            always_download: Always download the base image
            use_internal: Use internal development image for building the final image
        Returns:
            String image name
        """
        k8s_mode = self.orchestrator in [Orchestrator.AWS_EKS, Orchestrator.LOCAL_DOCKER_K8S]
        lambda_mode = self.orchestrator in [Orchestrator.LOCAL_DOCKER_LAMBDA, Orchestrator.AWS_LAMBDA]

        start = time.time()
        os.chdir(self.location)
        changes_in_build = self._track_changes()

        client = get_docker_client()
        base_image = self._get_base_name(
            enable_eia=enable_eia,
            enable_cuda=enable_cuda,
            cuda_devel=cuda_devel,
            k8s_mode=k8s_mode,
            lambda_mode=lambda_mode,
            use_internal=use_internal,
        )
        if always_download:
            log.info(f"Downloading newest base image {base_image}...")
            self._download_base_image(base_image, client)
            # should rebuild image always from scratch
            from_scratch = True
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
                lambda_mode=lambda_mode,
                k8s_mode=k8s_mode,
            )
        # fallback if the above environment adding is not run
        self.environs.add_or_update("BUILD_PIP=false")
        full_image_name = self.full_image_name(image_name, version_tag)
        self._create_prediction_image_s2i(
            base_image_tag=f"{image_name}-pip-layer:{version_tag}",
            image_tag=full_image_name,
            lambda_mode=lambda_mode,
            k8s_mode=k8s_mode,
        )
        log.info(f"Built main container `{full_image_name}`")
        log.info(f"Time taken to build: {time.time() - start:.2f}s")

        return full_image_name

    def full_image_name(self, image_name, version_tag):
        full_image_name = f"{image_name}:{version_tag}"
        return full_image_name

    def _create_prediction_image_s2i(self, base_image_tag, image_tag, lambda_mode=False, k8s_mode=False):
        """
        Extracted method which creates the prediction image

        Args:
            base_image_tag: Identifier of the base image name for building image
            image_tag: Identifier of the image name to be built
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
        return system(command)

    def _download_base_image(self, base_image: str, client: DockerClient) -> None:
        """
        Download the base image from ECR
        Args:
            base_image: Name of the base image
            client: Docker client
        """
        region = boto3.Session().region_name
        registry_name = self._get_docker_registry(region=region)
        ecr_image_name = f"{registry_name}/{base_image}"
        log.info(f"Downloading image from ECR '{ecr_image_name}'")
        # login to ECR and reload the auth configuration for the Docker client
        aws_ecr_login(region, registry_name)
        client.api.reload_config()
        client.images.pull(ecr_image_name)
        system(f"docker pull {ecr_image_name}")
        log.info(f"Re-tagging image to '{base_image}'")
        client.images.get(ecr_image_name).tag(base_image)

    def _get_docker_registry(self, region: str) -> str:
        account_id = boto3.client("sts").get_caller_identity()["Account"]
        registry_name = f"{account_id}.dkr.ecr.{region}.amazonaws.com"
        return registry_name

    @staticmethod
    def _get_base_name(
        enable_eia: bool = False,
        lambda_mode: bool = False,
        enable_cuda: bool = False,
        cuda_devel: bool = False,
        k8s_mode: bool = False,
        version: int = 1,
        use_internal=False,
    ) -> str:
        """Get Base Image given the configuration. By default the sagemaker CPU image name will be returned.

        Args:
            enable_eia: Return Elastic Inference base image name
            lambda_mode: Return Lambda base image name
            enable_cuda: Return runtime GPU image name
            cuda_devel: Return development GPU image name
            k8s_mode: Return Kubernetes base image names
            use_internal: Use internal development base image
        Return:
            String image name
        """
        if enable_eia and (lambda_mode or enable_cuda or k8s_mode):
            raise ValueError("Cannot use EIA with other options")
        if enable_cuda and lambda_mode:
            raise ValueError("Cannot use CUDA with Lambda")

        base_image = "superai-model-s2i-python3711"

        if cuda_devel:
            base_image += "-gpu-devel"
        elif enable_cuda:
            base_image += "-gpu"
        elif enable_eia:
            base_image += "-eia"
        else:
            base_image += "-cpu"

        if settings.current_env == "dev" or use_internal:
            base_image += "-internal"

        if lambda_mode:
            base_image += "-lambda"
        elif k8s_mode:
            base_image += "-seldon"

        return f"{base_image}:{version}"


def kwargs_warning(allowed_kwargs: List[str], **kwargs: Dict[str, Any]) -> None:
    if any([k not in allowed_kwargs for k in kwargs.keys()]):
        log.warning(
            f"Keyword arguments {[k for k in kwargs.keys() if k not in allowed_kwargs]} "
            f"unknown, make sure you are passing the right keyword arguments"
        )
