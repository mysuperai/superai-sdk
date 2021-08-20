import os
from abc import ABCMeta, abstractmethod
from concurrent.futures import ThreadPoolExecutor
from typing import TypeVar

import docker  # type: ignore
import requests
from colorama import Fore, Style  # type: ignore
from docker.errors import APIError  # type: ignore
from docker.models.containers import Container  # type: ignore
from rich import print
from rich.prompt import Confirm

from superai import Client
from superai.meta_ai.schema import EasyPredictions
from superai.utils import log


class DeployedPredictor(metaclass=ABCMeta):
    Type = TypeVar("Type", bound="DeployedPredictor")

    def __init__(self, *args, **kwargs):
        pass

    @abstractmethod
    def predict(self, input_data):
        pass

    @abstractmethod
    def terminate(self):
        pass


class LocalPredictor(DeployedPredictor):
    def __init__(self, *args, existing=False, remove=True, **kwargs):
        super(LocalPredictor, self).__init__(*args, **kwargs)
        client = docker.from_env()
        self.lambda_mode = kwargs.get("lambda_mode", False)
        container_name = kwargs["image_name"].replace(":", "_")
        if not existing:
            try:
                try:
                    container = client.containers.get(container_name)
                    log.warning(
                        "Container with identical name and version already running. "
                        "Stopping before restarting with new image."
                    )
                    container.kill()
                except Exception as e:
                    pass

                log.info(f"Starting new container with name {container_name}.")
                self.container: Container = client.containers.run(
                    image=kwargs["image_name"],
                    name=container_name,
                    detach=True,
                    remove=remove,
                    volumes={
                        os.path.abspath(kwargs["weights_path"]): {
                            "bind": "/opt/ml/model/",
                            "mode": "rw",
                        }
                    },
                    ports={8080: 9000} if self.lambda_mode else {8080: 80, 8081: 8081},
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

    def predict(self, input, mime="application/json"):
        if self.lambda_mode:
            url = f"http://localhost:9000/2015-03-31/functions/function/invocations"
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


class AWSPredictor(DeployedPredictor):
    def __init__(self, client: Client, id: str, **kwargs):
        super().__init__()
        self.client = client
        self.id = id
        target_status = kwargs.get("target_status", "ONLINE")
        client.set_deployment_status(model_id=self.id, target_status=target_status)

    def predict(self, input, **kwargs):
        if self.client.check_endpoint_is_available(self.id):
            result = self.client.predict_from_endpoint(self.id, input)
            output = EasyPredictions(result).value
            return output
        else:
            log.error("Prediction failed as endpoint does not seem to exist, please redeploy.")
            raise LookupError("Endpoint does not exist, redeploy")

    def terminate(self):
        self.client.set_deployment_status(model_id=self.id, target_status="OFFLINE")
