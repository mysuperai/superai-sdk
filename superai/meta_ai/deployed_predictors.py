from __future__ import annotations

import os
import shutil
from abc import ABCMeta, abstractmethod
from concurrent.futures import ThreadPoolExecutor
from typing import TYPE_CHECKING, List, Optional, TypeVar

import docker  # type: ignore
import requests
from docker.errors import APIError  # type: ignore
from docker.models.containers import Container  # type: ignore
from rich import print
from rich.prompt import Confirm

from superai.meta_ai.ai_helper import get_docker_client
from superai.meta_ai.parameters import AiDeploymentParameters
from superai.meta_ai.schema import TaskPredictionInstance
from superai.utils import log

from .exceptions import AIDeploymentException
from .orchestrators import Orchestrator

if TYPE_CHECKING:
    from superai.meta_ai import AIInstance


class DeployedPredictor(metaclass=ABCMeta):
    """Class to collect logic to handle managing deployments.
    Deployments are physical instances of AI models deployed on a cloud provider or locally.
    They provide endpoints to make predictions.

    """

    Type = TypeVar("Type", bound="DeployedPredictor")

    def __init__(
        self,
        orchestrator: Orchestrator,
        ai: AIInstance,
        deploy_properties: AiDeploymentParameters = None,
        local_image_name: Optional[str] = None,
        weights_path: Optional[str] = None,
        *args,
        **kwargs,
    ):
        self.orchestrator = orchestrator
        self.local_image_name = local_image_name
        self.ai_instance = ai
        if isinstance(deploy_properties, dict):
            self.deploy_properties = AiDeploymentParameters.parse_obj(deploy_properties)
        else:
            self.deploy_properties = deploy_properties
        self.weights_path = weights_path
        self.id = None

    @abstractmethod
    def deploy(self, redeploy=False) -> None:
        pass

    @abstractmethod
    def predict(self, input_data):
        pass

    @abstractmethod
    def terminate(self):
        pass

    def to_dict(self) -> dict:
        pass

    @classmethod
    def from_dict(cls, dictionary: dict, client: Optional["Client"] = None) -> "DeployedPredictor":
        if list(dictionary.keys())[0] == "LocalPredictor":
            return LocalPredictor.from_dict(dictionary["LocalPredictor"])
        else:
            return RemotePredictor.from_dict(dictionary["RemotePredictor"], client)


class LocalPredictor(DeployedPredictor):
    def __init__(self, *args, remove=True, **kwargs):
        super(LocalPredictor, self).__init__(*args, **kwargs)

        self.client = get_docker_client()
        self.lambda_mode = self.orchestrator in [Orchestrator.LOCAL_DOCKER_LAMBDA, Orchestrator.AWS_LAMBDA]
        self.enable_cuda = self.deploy_properties.enable_cuda
        self.k8s_mode = self.orchestrator == Orchestrator.LOCAL_DOCKER_K8S or None
        self.container_name = self.local_image_name.replace(":", "_")
        self.weights_volume = self.deploy_properties.mount_path if self.k8s_mode else "/opt/ml/model/"
        self.kwargs = kwargs
        self.remove = remove

    def deploy(self, redeploy=False) -> None:
        try:
            try:
                container = self.client.containers.get(self.container_name)
                if not redeploy:
                    log.error(f"Container {self.container_name} already exists. Use `redeploy` to force redeployment.")
                    return
                log.warning(
                    "Container with identical name and version already running. "
                    "Stopping before restarting with new image."
                )

                container.kill()
                container.wait()
            except Exception as e:
                log.debug(f"Ignorable exception: {e}")

            log.info(f"Starting new container with name {self.container_name}.")
            envs = dict(MNT_PATH=self.weights_volume)
            if self.deploy_properties.envs:
                envs.update(self.deploy_properties.envs)
            self.container: Container = self.client.containers.run(
                image=self.local_image_name,
                name=self.container_name,
                detach=True,
                remove=self.remove,
                environment=envs,
                volumes=self._get_volumes(self.weights_volume),
                ports=self._get_port_assignment(),
                device_requests=self._get_device_requests(),
            )
            log.info("Started container in serving mode.")
        except APIError as e:
            log.error(
                "Could not run docker container. "
                "Is docker running or is there already a container running under the same ports?",
                exc_info=e,
            )
            self.container = None

    def predict(self, input, mime="application/json"):
        if self.container is None:
            self.container: Container = self.client.containers.get(self.container_name)

        if self.lambda_mode:
            url = "http://localhost:9000/2015-03-31/functions/function/invocations"
        elif self.k8s_mode:
            url = "http://localhost:9000/api/v1.0/predictions"
        else:
            url = "http://localhost/invocations"
        headers = {"Content-Type": mime}
        if mime.endswith("json"):
            res = requests.post(url, json=input, headers=headers)
        else:
            if os.path.exists(input):
                with open(input, "rb") as f:
                    payload = f.read()
            else:
                payload = input
            res = requests.post(url, data=payload, headers=headers)
        if res.status_code == 200:
            return TaskPredictionInstance.validate_prediction(res.json())
        message = f"Error, received error code {res.status_code}: {res.text}"
        log.error(message)

    def log(self):
        if self.container is None:
            log.warning("No container running. Cannot print logs.")
            return

        log.info("Showing container logs now. Try Ctrl/Cmd-C to exit!")
        end = False

        def printer():
            for line in self.container.logs(stream=True):
                if end:
                    return
                print(line.decode("UTF-8"), end="")

        try:
            with ThreadPoolExecutor() as executor:
                executor.submit(printer)
        except KeyboardInterrupt:
            end = True
            print()
            leave_running = Confirm.ask("Leave container running?")
            if not leave_running:
                self.terminate()
            else:
                log.info(f"Container is running in the backgourd with id:{self.container.id}")

    def terminate(self):
        log.info("Stopping container")
        self.container.stop()

    def _get_port_assignment(self):
        if self.lambda_mode:
            return {8080: 9000}
        elif self.k8s_mode:
            return {9000: 9000}
        else:
            return {8080: 80, 8081: 8081}

    def _get_volumes(self, weights_volume: str):
        return (
            {
                os.path.abspath(self.weights_path): {
                    "bind": weights_volume,
                    "mode": "rw",
                }
            }
            if self.weights_path is not None
            else {}
        )

    def _get_device_requests(self):
        return (
            [docker.types.DeviceRequest(count=-1, capabilities=[["gpu"]])]
            if self.enable_cuda and shutil.which("nvidia-container-runtime") is not None
            else None
        )

    def to_dict(self) -> dict:
        dictionary = {"deploy_properties": self.deploy_properties.dict_for_db()}
        dictionary["deploy_properties"]["weights_path"] = self.weights_path
        return dictionary

    @classmethod
    def from_dict(cls, dictionary, client: Optional["Client"] = None) -> "LocalPredictor":
        return cls(existing=False, remove=True, **dictionary)


class RemotePredictor(DeployedPredictor):
    """A predictor that runs on a remote machine."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from superai.client import Client

        self.client = Client.from_credentials()

    def load(self) -> bool:
        """Load existing predictor from database.

        Returns:
            True if predictor was loaded, False otherwise.
        """
        existing_deployment = self._get_existing_deployment()
        if existing_deployment:
            self.id = existing_deployment.id
            log.info(f"Loaded existing deployment with id {self.id}.")
            return True
        return False

    def deploy(self, redeploy=False, wait_time_seconds=1) -> str:
        """Deploy the image to the remote orchestrator.
        Can block and wait for the deployment to be ready.

        Args:
            redeploy: Allow redeploying existing deployment.
            wait_time_seconds: Time to wait for deployment to be ready.

        Returns:
            Id of deployment

        """
        c = self.client
        # Check if AI id is present
        if self.ai_instance.id is None:
            raise LookupError("Cannot find AI id, please make sure you push the AI model to create a database entry")

        self.load()

        if self.id:
            if not redeploy:
                raise AIDeploymentException(
                    "Deployment with this version already exists. Try undeploy() first or set `deploy(redeploy=True)`."
                )
            else:
                self.terminate(wait_seconds=5)
        else:
            # Create new deployment entry if no existing deployment is found
            self.id = c.deploy(self.ai_instance.id)
            log.info(f"Created new deployment with id {self.id}.")

        # Update deployment properties and AI instance
        c.set_deployment_properties(deployment_id=self.id, properties=self.deploy_properties.dict_for_db())

        # Set deployment status to ONLINE and fetch deployment details
        finished = c.set_deployment_status(deployment_id=self.id, target_status="ONLINE", timeout=wait_time_seconds)
        deployment = c.get_deployment(self.id)
        if not finished:
            log.warning(f"Deployment is getting ready in the background: {deployment}")
        else:
            log.info(f"Deployment finished and ready for predictions: {deployment}")
        return self.id

    def _get_existing_deployment(self):
        """Get existing deployment based on AI instance id
        Either fetch explicit deployment_id from ai_instance.served_by or
        fetch all deployments for this AI instance and use the first one.
        """
        c = self.client
        # Fetch served_by field if not present
        if not self.ai_instance.served_by:
            ai_instance_dict = c.get_ai_instance(self.ai_instance.id)
            if ai_instance_dict:
                self.ai_instance.served_by = ai_instance_dict.served_by

        # Check if deployment with the same version already exists
        existing_deployment = c.get_deployment(self.ai_instance.served_by) if self.ai_instance.served_by else None
        if not existing_deployment:
            list_deployments = c.list_deployments(model_id=self.ai_instance.id)
            if list_deployments:
                log.info(f"Found {len(list_deployments)} deployments for this AI instance. Using the first one.")
                existing_deployment = list_deployments[0]
        return existing_deployment

    def predict(self, input, wait_time_seconds=180, **kwargs) -> List[TaskPredictionInstance]:
        if self.client.check_endpoint_is_available(self.id):
            input_data, parameters = input.get("data", {}), input.get("parameters", {})
            return self.client.predict_from_endpoint(
                deployment_id=self.id,
                input_data=input_data,
                parameters=parameters,
                model_id=self.ai_instance.id,
                timeout=wait_time_seconds,
            )
        else:
            log.error("Prediction failed as endpoint does not seem to exist, please redeploy.")
            raise LookupError("Endpoint does not exist, redeploy")

    def terminate(self, wait_seconds=1):
        """Terminate the deployment.
        Args:
            wait_seconds: Seconds to wait for the deployment to terminate.
        """
        id = self.id or self.ai_instance.served_by
        log.info(f"Terminating deployment with id {id}, waiting {wait_seconds} seconds for backend action.")
        self.client.set_deployment_status(deployment_id=id, target_status="OFFLINE", timeout=wait_seconds)

    def to_dict(self) -> dict:
        return dict(id=self.id)

    @classmethod
    def from_dict(cls, dictionary, client: Optional["Client"] = None) -> "RemotePredictor":
        from superai.client import Client

        client = client or Client.from_credentials()
        return cls(client=client, id=dictionary["id"])


class PredictorFactory(object):
    __predictor_classes = {
        "LOCAL_DOCKER_K8S": LocalPredictor,
        "AWS_EKS": RemotePredictor,
    }

    @staticmethod
    def get_predictor_obj(*args, orchestrator: Orchestrator, **kwargs) -> "DeployedPredictor.Type":
        """Factory method to get a predictor"""
        if isinstance(orchestrator, str):
            try:
                orchestrator = Orchestrator[orchestrator]
            except KeyError as e:
                raise ValueError(
                    f"Unknown orchestrator: {orchestrator}. Try one of: {', '.join(Orchestrator.__members__.values())}"
                ) from e

        predictor_class = PredictorFactory.__predictor_classes.get(orchestrator)
        log.info(f"Creating predictor of type: {predictor_class} with kwargs: {kwargs}")

        if predictor_class:
            return predictor_class(orchestrator, *args, **kwargs)
        raise NotImplementedError(f"The predictor of orchestrator:`{orchestrator}` is not implemented yet.")

    @classmethod
    def is_remote(cls, orchestrator: str) -> bool:
        return cls.__predictor_classes.get(orchestrator) is RemotePredictor
