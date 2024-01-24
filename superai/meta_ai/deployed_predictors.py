from __future__ import annotations

import os
import shutil
from abc import ABCMeta, abstractmethod
from concurrent.futures import ThreadPoolExecutor
from typing import TYPE_CHECKING, Optional, TypeVar

import docker  # type: ignore
import requests
from docker.errors import APIError  # type: ignore
from docker.models.containers import Container  # type: ignore
from rich import print
from rich.prompt import Confirm
from superai_builder.docker.client import get_docker_client

from superai.meta_ai.exceptions import AIDeploymentException
from superai.meta_ai.parameters import AiDeploymentParameters
from superai.meta_ai.schema import TaskPredictionInstance
from superai.utils import log

if TYPE_CHECKING:
    from superai.meta_ai import AIInstance, Orchestrator


class DeployedPredictor(metaclass=ABCMeta):
    """Class to collect logic to handle managing deployments.
    Deployments are physical instances of AI models deployed on a cloud provider or locally.
    They provide endpoints to make predictions.

    """

    Type = TypeVar("Type", bound="DeployedPredictor")

    def __init__(
        self,
        orchestrator: Orchestrator,
        ai: Optional[AIInstance] = None,
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
    def from_dict(
        cls, dictionary: dict, client: Optional["Client"] = None, ai: Optional["AI"] = None
    ) -> "DeployedPredictor":
        if list(dictionary.keys())[0] == "LocalPredictor":
            return LocalPredictor.from_dict(dictionary["LocalPredictor"], ai=ai)
        else:
            return RemotePredictor.from_dict(dictionary["RemotePredictor"], client=client)


class LocalPredictor(DeployedPredictor):
    ENDPOINT_SUFFIX = "api/v1.0/predictions"

    def __init__(self, *args, port=9000, remove=True, rest_workers=1, grpc_workers=0, **kwargs):
        """_summary_

        Parameters
        ----------
        port : int, optional
            Local exposed host port, by default 9000
        remove : bool, optional
            Remove container after stopping, by default True
        rest_workers : int, optional
            How many REST workers are spawned for the predictor, by default 1
        grpc_workers : int, optional
            How many GRPC workers are spawned for the predictor., by default 0 disables GRPC
        """
        super(LocalPredictor, self).__init__(*args, **kwargs)

        self.client = get_docker_client()
        self.enable_cuda = self.deploy_properties.enable_cuda
        self.container_name = self.local_image_name.replace(":", "_") + "_" + os.environ.get("RUN_UUID", "")
        self.weights_volume = self.deploy_properties.mount_path
        self.kwargs = kwargs
        self.remove = remove
        self.container = None
        if os.environ.get("JENKINS_URL") is not None:
            import netifaces

            self.ip_address = netifaces.ifaddresses("docker0")[netifaces.AF_INET][0]["addr"]
        else:
            self.ip_address = "localhost"
        self.port = port
        self.timeout = 120
        self.grpc_workers = grpc_workers
        self.rest_workers = rest_workers

        if self.weights_path and "s3://" in self.weights_path:
            from superai.meta_ai import AILoader

            self.weights_path = AILoader._load_weights(self.weights_path)

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

            envs["GRPC_WORKERS"] = self.grpc_workers
            envs["GUNICORN_WORKERS"] = self.rest_workers
            envs["AWS_ACCESS_KEY_ID"] = os.environ.get("AWS_ACCESS_KEY_ID", "")
            envs["AWS_SECRET_ACCESS_KEY"] = os.environ.get("AWS_SECRET_ACCESS_KEY", "")

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
                stderr=True,
            )
            log.info("Started container in serving mode.")
        except APIError as e:
            log.error(
                "Could not run docker container. "
                "Is docker running or is there already a container running under the same ports?",
                exc_info=e,
            )
            self.container = None

    def _get_endpoint(self):
        return f"http://{self.ip_address}:{self.port}/{self.ENDPOINT_SUFFIX}"

    def predict(self, input, mime="application/json"):
        if self.container is None:
            self.container: Container = self.client.containers.get(self.container_name)
        container_state = self.container.attrs["State"]
        assert container_state["Status"] == "running", "Container is not running"

        url = self._get_endpoint()

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

    def ping(self) -> bool:
        """
        Check if the exposed port is live.

        Returns
        -------
        bool
            True if the port is live, False otherwise.
        """
        try:
            response = requests.post(self._get_endpoint(), timeout=3)
            # 400 is returned if the server is running since the model complains about missing payload
            return response.status_code == 400
        except requests.RequestException:
            return False

    def wait_until_ready(self, timeout=30) -> bool:
        """
        Wait until the exposed port is live.

        Returns
        -------
        bool
            True if the port is live, False otherwise.
        """
        import time

        start_time = time.time()
        while not self.ping() and time.time() - start_time < timeout:
            time.sleep(1)
        return self.ping()

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
                log.info(f"Container is running in the background with id:{self.container.id}")

    def terminate(self):
        if self.container is None:
            self.container: Container = self.client.containers.get(self.container_name)

        log.info("Stopping container")
        self.container.stop()
        self.container = None  # Set container to None so invocations to log() return immediately

    def _get_port_assignment(self):
        return {self.port: self.port}

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
        dictionary = {
            "deploy_properties": self.deploy_properties.dict_for_db(),
            "local_image_name": self.local_image_name,
            "weights_path": self.weights_path,
        }

        return dictionary

    @classmethod
    def from_dict(cls, dictionary, client: Optional["Client"] = None, ai: Optional["AI"] = None) -> "LocalPredictor":
        from superai.meta_ai import Orchestrator

        return cls(existing=False, remove=True, ai=ai, orchestrator=Orchestrator.LOCAL_DOCKER_K8S, **dictionary)


class RemotePredictor(DeployedPredictor):
    """A predictor that runs on a remote machine."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from superai.client import Client

        self.client = Client.from_credentials()
        if self.ai_instance is None:
            raise ValueError("AI instance cannot be None for RemotePredictor.")

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

        create_new = False
        if self.id:
            if not redeploy:
                raise AIDeploymentException(
                    "Deployment with this version already exists. Try undeploy() first or set `deploy(redeploy=True)`."
                )
            else:
                current_deployment = c.get_deployment(self.id)
                current_type = current_deployment.type
                if current_type != self.orchestrator.value:
                    log.warning(
                        f"Deployment type changed. Previous {current_type}, now: {self.orchestrator.value}. Will shutdown current deployment and create new."
                    )
                    create_new = True
                    # Only terminate when deployment type differs
                    self.terminate(wait_seconds=15)
                else:
                    # If the type is identical we can just use the seamless update feature
                    create_new = False
        else:
            create_new = True

        if create_new:
            # Create new deployment entry if no existing deployment is found
            self.id = c.deploy(self.ai_instance.id, deployment_type=self.orchestrator.value)
            log.info(f"Created new deployment with id={self.id} and type={self.orchestrator.value}.")

        # Update deployment properties and AI instance
        c.set_deployment_properties(deployment_id=self.id, properties=self.deploy_properties.dict_for_db())
        if create_new:
            finished = c.set_deployment_status(deployment_id=self.id, target_status="ONLINE", timeout=wait_time_seconds)
        else:
            finished = c.update_deployment(deployment_id=self.id, timeout=wait_time_seconds)

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

    def predict(self, input, wait_time_seconds=180, **kwargs) -> TaskPredictionInstance:
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

    def predict_async(self, input, **kwargs) -> str:
        """Predict asynchronously from the remote deployment and return prediction_uuid."""
        input_data, parameters = input.get("data", {}), input.get("parameters", {})
        return self.client.predict_from_endpoint_async(
            deployment_id=self.id,
            input_data=input_data,
            parameters=parameters,
            model_id=self.ai_instance.id,
        )

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
