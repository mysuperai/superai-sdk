from __future__ import annotations

import functools
import hashlib
import json
import os
import shutil
import time
from typing import TYPE_CHECKING, Any, Dict, List, Optional

import boto3  # type: ignore
from docker import DockerClient
from docker.errors import ImageNotFound

from superai.config import get_current_env, settings
from superai.log import logger
from superai.meta_ai.ai_helper import aws_ecr_login, get_docker_client
from superai.meta_ai.ai_loader import AILoader
from superai.meta_ai.orchestrators import (
    BaseAIOrchestrator,
    Orchestrator,
    TrainingOrchestrator,
)
from superai.meta_ai.parameters import AiDeploymentParameters
from superai.utils import system

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
        staging_dir = AILoader.save_local(ai)
        from superai.meta_ai import AI

        ai = AI.load(str(staging_dir))

        self.orchestrator = orchestrator
        self._check_orchestrator()

        self.name = ai.name
        self.version = str(ai.version)
        self.entrypoint_class = ai.model_class
        self.environs = ai.environs
        self.location = str(ai._location)
        self.requirements = ai.requirements
        self.conda_env = ai.conda_env
        self.artifacts = ai.artifacts
        self.deployment_parameters = deployment_parameters or AiDeploymentParameters()

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
        """Build the image and return the image name.
        Args:
            cuda_devel
            enable_eia:
            skip_build:
            use_internal: If true, use the internal development base image
            build_all_layers: If true, build all layers from scratch
            download_base: If true, download base image from docker hub

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
            image = self.build_image_s2i(
                self.name,
                self.version,
                enable_cuda=self.deployment_parameters.enable_cuda,
                enable_eia=enable_eia,
                cuda_devel=cuda_devel,
                from_scratch=build_all_layers,
                always_download=download_base,
                use_internal=use_internal,
            )
            logger.info(f"Built image {image}")
        return image

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
        if self.artifacts and "run" in self.artifacts:
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
        """Build the image using s2i

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

        start = time.time()
        os.chdir(self.location)
        changes_in_build = self._track_changes()

        client = get_docker_client()
        base_image = self._get_base_name(
            enable_eia=enable_eia,
            enable_cuda=enable_cuda,
            cuda_devel=cuda_devel,
            k8s_mode=k8s_mode,
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
                base_image_tag=base_image, image_tag=f"{image_name}-pip-layer:{version_tag}"
            )
        # fallback if the above environment adding is not run
        self.environs.add_or_update("BUILD_PIP=false")
        full_image_name = self.full_image_name(image_name, version_tag)
        self._create_prediction_image_s2i(
            base_image_tag=f"{image_name}-pip-layer:{version_tag}", image_tag=full_image_name
        )
        log.info(f"Built main container `{full_image_name}`")
        log.info(f"Time taken to build: {time.time() - start:.2f}s")

        return full_image_name

    def full_image_name(self, image_name, version_tag):
        return f"{image_name}:{version_tag}"

    def _create_prediction_image_s2i(self, base_image_tag, image_tag):
        """Extracted method which creates the prediction image

        Args:
            base_image_tag: Identifier of the base image name for building image
            image_tag: Identifier of the image name to be built
        """
        self.environs.add_or_update("SUPERAI_CONFIG_ROOT", "/tmp/.superai")
        self.environs.add_or_update("SERVICE_TYPE=MODEL")
        self.environs.add_or_update("PERSISTENCE=0")
        self.environs.add_or_update("API_TYPE=REST")
        self.environs.add_or_update("SELDON_MODE=true")
        build_envs = [
            f"-v {os.path.join(os.path.expanduser('~'), '.aws')}:/root/.aws "
            f"-v {os.path.join(os.path.expanduser('~'), '.superai')}:/root/.superai "
            f"-v {os.path.join(os.path.expanduser('~'), '.canotic')}:/root/.canotic "
        ]

        command = (
            f"s2i build -E {self.environs.location} "
            f"{' '.join(build_envs)} "
            f"--incremental=True . "
            f"{base_image_tag} {image_tag}"
        )
        return system(command)

    def _download_base_image(self, base_image: str, client: DockerClient) -> None:
        """Download the base image from ECR
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
        account_id = "185169359328"  # boto3.client("sts").get_caller_identity()["Account"]
        return f"{account_id}.dkr.ecr.{region}.amazonaws.com"

    @staticmethod
    def _get_base_name(
        enable_eia: bool = False,
        enable_cuda: bool = False,
        cuda_devel: bool = False,
        k8s_mode: bool = False,
        version: int = 1,
        use_internal=False,
        python_version: str = "310",
    ) -> str:
        """Get Base Image given the configuration. By default the sagemaker CPU image name will be returned.

        Args:
            enable_eia: Return Elastic Inference base image name
            enable_cuda: Return runtime GPU image name
            cuda_devel: Return development GPU image name
            k8s_mode: Return Kubernetes base image names
            use_internal: Use internal development base image
            python_version: Python version to use, default is 310 = 3.10
        Return:
            String image name
        """
        if enable_eia and (enable_cuda or k8s_mode):
            raise ValueError("Cannot use EIA with other options")
        base_image = f"superai-model-s2i-python{python_version}"

        if cuda_devel:
            base_image += "-gpu-devel"
        elif enable_cuda:
            base_image += "-gpu"
        elif enable_eia:
            base_image += "-eia"
        else:
            base_image += "-cpu"

        if get_current_env() == "dev" or use_internal:
            base_image += "-internal"

        if k8s_mode:
            base_image += "-seldon"

        return f"{base_image}:{version}"


def kwargs_warning(allowed_kwargs: List[str], **kwargs: Dict[str, Any]) -> None:
    if any(k not in allowed_kwargs for k in kwargs):
        log.warning(
            f"Keyword arguments {[k for k in kwargs if k not in allowed_kwargs]} unknown, make sure you are "
            f"passing the right keyword arguments"
        )
