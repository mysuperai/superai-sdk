from __future__ import annotations

import os
import shutil
from abc import ABCMeta, abstractmethod
from concurrent.futures import ThreadPoolExecutor
from typing import Optional, TypeVar

import docker  # type: ignore
import requests
from colorama import Fore, Style  # type: ignore
from docker.errors import APIError  # type: ignore
from docker.models.containers import Container  # type: ignore
from rich import print
from rich.prompt import Confirm

from superai import Client
from superai.meta_ai.dockerizer import get_docker_client
from superai.meta_ai.image_builder import Orchestrator
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

    def __init__(self, *args, **kwargs):
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
    def __init__(self, *args, deploy_properties: dict, existing=False, remove=True, **kwargs):
        super(LocalPredictor, self).__init__(*args, **kwargs)
        client = get_docker_client()
        self.deploy_properties = deploy_properties
        self.lambda_mode = deploy_properties.get("lambda_mode", False)
        self.enable_cuda = deploy_properties.get("enable_cuda", False)
        self.k8s_mode = deploy_properties.get("k8s_mode", False)
        self.ai = kwargs.get("ai")
        self.weights_path = deploy_properties.get("weights_path") or self.ai.weights_path
        container_name = deploy_properties["image_name"].replace(":", "_")
        weights_volume = deploy_properties["kubernetes_config"]["mountPath"] if self.k8s_mode else "/opt/ml/model/"
        if not existing:
            try:
                try:
                    container = client.containers.get(container_name)
                    log.warning(
                        "Container with identical name and version already running. "
                        "Stopping before restarting with new image."
                    )
                    container.kill()
                    container.wait()
                except Exception as e:
                    log.debug(f"Ignorable exception: {e}")

                log.info(f"Starting new container with name {container_name}.")
                self.container: Container = client.containers.run(
                    image=deploy_properties["image_name"],
                    name=container_name,
                    detach=True,
                    remove=remove,
                    environment=dict(MNT_PATH=weights_volume),
                    volumes=self._get_volumes(weights_volume),
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
        else:
            self.container: Container = client.containers.get(container_name)
            log.info("Initialized LocalPredictor with already running container.")
        self.kwargs = kwargs

    def predict(self, input, mime="application/json"):
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
        dictionary = {"deploy_properties": self.deploy_properties}
        dictionary["deploy_properties"]["weights_path"] = self.weights_path
        return dictionary

    @classmethod
    def from_dict(cls, dictionary, client: Optional[Client] = None) -> "LocalPredictor":
        return cls(existing=False, remove=True, **dictionary)


class RemotePredictor(DeployedPredictor):
    """A predictor that runs on a remote machine."""

    def __init__(self, client: Client, deploy_properties: dict, **kwargs):
        super().__init__()
        self.client = client
        self.id = deploy_properties["id"]
        self.target_status = deploy_properties.get("target_status", "ONLINE")
        client.set_deployment_status(deployment_id=self.id, target_status=self.target_status)

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
        return dict(id=self.id, target_status=self.target_status)

    @classmethod
    def from_dict(cls, dictionary, client: Optional[Client] = None) -> "RemotePredictor":
        client = client or Client()
        return cls(client=client, id=dictionary["id"], target_status=dictionary["target_status"])


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
    def get_predictor_obj(
        orchestrator: Orchestrator, deploy_properties: dict, *args, **kwargs
    ) -> "DeployedPredictor.Type":
        """Factory method to get a predictor"""
        predictor_class = PredictorFactory.__predictor_classes.get(orchestrator)
        log.info("Creating predictor of type: {} with properties: {}".format(predictor_class, deploy_properties))

        if predictor_class:
            return predictor_class(deploy_properties=deploy_properties, *args, **kwargs)
        raise NotImplementedError(f"The predictor of orchestrator:`{orchestrator}` is not implemented yet.")

    @classmethod
    def is_remote(cls, orchestrator: str) -> bool:
        return cls.__predictor_classes.get(orchestrator) is RemotePredictor
