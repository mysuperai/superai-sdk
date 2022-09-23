from __future__ import annotations

import os
import shutil
from abc import ABCMeta, abstractmethod
from concurrent.futures import ThreadPoolExecutor
from typing import Optional, TypeVar

import docker  # type: ignore
import requests
from docker.errors import APIError  # type: ignore
from docker.models.containers import Container  # type: ignore
from rich import print
from rich.prompt import Confirm

from superai import Client
from superai.meta_ai.dockerizer import get_docker_client
from superai.meta_ai.image_builder import Orchestrator
from superai.meta_ai.parameters import AiDeploymentParameters
from superai.meta_ai.schema import EasyPredictions
from superai.utils import log


class DeployedPredictor(metaclass=ABCMeta):
    """
    Class to collect logic to handle managing deployments.
    Deployments are physical instances of AI models deployed on a cloud provider or locally.
    They provide endpoints to make predictions.

    TODO: Extract deployment logic from `AI` into here.
    """

    Type = TypeVar("Type", bound="DeployedPredictor")

    def __init__(
        self,
        orchestrator: Orchestrator,
        local_image_name: str,
        ai: "AI",
        deploy_properties: AiDeploymentParameters,
        weights_path: Optional[str] = None,
        *args,
        **kwargs,
    ):
        self.orchestrator = orchestrator
        self.local_image_name = local_image_name
        self.ai = ai
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
    def from_dict(cls, dictionary: dict, client: Optional[Client] = None) -> "DeployedPredictor":
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
            url = f"http://localhost:9000/2015-03-31/functions/function/invocations"
        elif self.k8s_mode:
            url = "http://localhost:9000/api/v1.0/predictions"
        else:
            url = f"http://localhost/invocations"
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
            result = EasyPredictions(res.json()).value
            return result
        else:
            message = "Error , received error code {}: {}".format(res.status_code, res.text)
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
        volumes = {}
        if self.weights_path is not None:
            volumes = {
                os.path.abspath(self.weights_path): {
                    "bind": weights_volume,
                    "mode": "rw",
                }
            }
        return volumes

    def _get_device_requests(self):
        device_requests = None
        if self.enable_cuda and shutil.which("nvidia-container-runtime") is not None:
            device_requests = [docker.types.DeviceRequest(count=-1, capabilities=[["gpu"]])]
        return device_requests

    def to_dict(self) -> dict:
        dictionary = {"deploy_properties": self.deploy_properties.dict_for_db()}
        dictionary["deploy_properties"]["weights_path"] = self.weights_path
        return dictionary

    @classmethod
    def from_dict(cls, dictionary, client: Optional[Client] = None) -> "LocalPredictor":
        return cls(existing=False, remove=True, **dictionary)


class RemotePredictor(DeployedPredictor):
    """A predictor that runs on a remote machine."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client = self.ai.client

    def deploy(self, redeploy=False) -> str:
        """
        Deploy the image to the remote orchestrator.
        Args:
            redeploy:
            orchestrator: Orchestrator to deploy to.
            properties: Properties to deploy with.
            redeploy: Allow redeploying existing deployment.
            skip_build: Skip building and force reuse existing image.

        Returns:
            Id of deployment

        """
        if self.ai.id is None:
            raise LookupError("Cannot find AI id, please make sure you push the AI model to create a database entry")

        self.ai.served_by = self.ai.served_by or self.ai.client.get_model(self.ai.id)["served_by"]
        existing_deployment = self.ai.client.get_deployment(self.ai.served_by) if self.ai.served_by else None

        deployment_exists = not (existing_deployment is None or "status" not in existing_deployment)

        if deployment_exists and not redeploy:
            raise Exception("Deployment with this version already exists. Try undeploy first or set `redeploy=True`.")
        elif redeploy:
            self.ai.undeploy()

        if not deployment_exists:
            self.id = self.client.deploy(self.ai.id, deployment_type=self.orchestrator.value)
            log.info(f"Created new deployment with id {self.id}.")
        else:
            self.id = self.ai.deployment_id
            log.info(f"Reusing existing deployment with id {self.id}.")
        self.ai.served_by = self.id

        self.client.set_deployment_properties(
            deployment_id=self.ai.deployment_id, properties=self.deploy_properties.dict_for_db()
        )
        self.client.update_model(self.ai.id, served_by=self.ai.served_by)

        self.client.set_deployment_status(deployment_id=self.ai.deployment_id, target_status="ONLINE")
        deployment = self.client.get_deployment(self.ai.deployment_id)
        log.info(f"Deployment={deployment} done.")

        return self.id

    def predict(self, input, **kwargs):
        if self.client.check_endpoint_is_available(self.id):
            input_data, parameters = input.get("data", {}), input.get("parameters", {})
            result = self.client.predict_from_endpoint(
                deployment_id=self.id, input_data=input_data, parameters=parameters
            )
            output = EasyPredictions(result).value
            return output
        else:
            log.error("Prediction failed as endpoint does not seem to exist, please redeploy.")
            raise LookupError("Endpoint does not exist, redeploy")

    def terminate(self):
        self.client.set_deployment_status(deployment_id=self.id, target_status="OFFLINE")

    def to_dict(self) -> dict:
        return dict(id=self.id)

    @classmethod
    def from_dict(cls, dictionary, client: Optional[Client] = None) -> "RemotePredictor":
        client = client or Client()
        return cls(client=client, id=dictionary["id"])


class PredictorFactory(object):
    __predictor_classes = {
        "LOCAL_DOCKER": LocalPredictor,
        "LOCAL_DOCKER_LAMBDA": LocalPredictor,
        "LOCAL_DOCKER_K8S": LocalPredictor,
        "AWS_SAGEMAKER": RemotePredictor,
        "AWS_SAGEMAKER_ASYNC": RemotePredictor,
        "AWS_LAMBDA": RemotePredictor,
        "AWS_EKS": RemotePredictor,
    }

    @staticmethod
    def get_predictor_obj(*args, orchestrator: Orchestrator, **kwargs) -> "DeployedPredictor.Type":
        """Factory method to get a predictor"""
        predictor_class = PredictorFactory.__predictor_classes.get(orchestrator)
        log.info("Creating predictor of type: {} with kwargs: {}".format(predictor_class, kwargs))

        if predictor_class:
            return predictor_class(orchestrator, *args, **kwargs)
        raise NotImplementedError(f"The predictor of orchestrator:`{orchestrator}` is not implemented yet.")

    @classmethod
    def is_remote(cls, orchestrator: str) -> bool:
        return cls.__predictor_classes.get(orchestrator) is RemotePredictor
