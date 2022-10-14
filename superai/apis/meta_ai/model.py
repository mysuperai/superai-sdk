import json
import time
from abc import ABC
from typing import Dict, List, Optional, Union

from rich import box
from rich.console import Console
from rich.live import Live
from rich.table import Table
from sgqlc.operation import Operation

from superai.apis.meta_ai.meta_ai_graphql_schema import (
    RawPrediction,
    download_artifact_async,
    meta_ai_assignment_enum,
    meta_ai_deployment,
    meta_ai_deployment_bool_exp,
    meta_ai_deployment_insert_input,
    meta_ai_deployment_pk_columns_input,
    meta_ai_deployment_purpose_enum,
    meta_ai_deployment_set_input,
    meta_ai_deployment_status_enum,
    meta_ai_deployment_status_enum_comparison_exp,
    meta_ai_deployment_type_enum,
    meta_ai_model,
    meta_ai_model_insert_input,
    meta_ai_model_pk_columns_input,
    meta_ai_model_set_input,
    meta_ai_prediction,
    meta_ai_prediction_state_enum,
    meta_ai_training_instance,
    meta_ai_training_instance_insert_input,
    meta_ai_training_instance_pk_columns_input,
    meta_ai_training_instance_set_input,
    meta_ai_training_template,
    meta_ai_training_template_insert_input,
    meta_ai_training_template_pk_columns_input,
    meta_ai_training_template_set_input,
    meta_ai_visibility_enum,
    mutation_root,
    query_root,
    subscription_root,
    uuid,
    uuid_comparison_exp,
)
from superai.log import logger

from .session import (  # type: ignore
    GraphQlException,
    MetaAISession,
    MetaAIWebsocketSession,
)

log = logger.get_logger(__name__)
BASE_FIELDS = ["name", "version", "id", "ai_worker_id", "visibility", "trainable"]
EXTRA_FIELDS = [
    "description",
    "model_save_path",
    "weights_path",
    "input_schema",
    "output_schema",
    "served_by",
    "default_training_parameters",
    "image",
    "deployment_parameters",
]


class PredictionError(Exception):
    pass


class ModelApiMixin(ABC):
    _resource = "model"

    def __init__(self):
        self.sess = MetaAISession()

    @property
    def resource(self):
        return self._resource

    @staticmethod
    def _fields(verbose):
        return BASE_FIELDS + EXTRA_FIELDS if verbose else BASE_FIELDS

    @staticmethod
    def _output_formatter(entries, to_json):
        if not to_json:
            return entries
        elif isinstance(entries, (list, tuple)):
            return [entry.__json_data__ for entry in entries]
        else:
            return entries.__json_data__  # single instance

    def get_all_models(self, to_json=False, verbose=False) -> List[Union[meta_ai_model, Dict]]:
        op = Operation(query_root)
        op.meta_ai_model().__fields__(*self._fields(verbose))
        data = self.sess.perform_op(op)
        return self._output_formatter((op + data).meta_ai_model, to_json)

    def get_model(self, model_id, to_json=False) -> Optional[Union[meta_ai_model, Dict]]:
        op = Operation(query_root)
        op.meta_ai_model_by_pk(id=model_id).__fields__(
            "name",
            "version",
            "id",
            "ai_worker_id",
            "description",
            "visibility",
            "input_schema",
            "output_schema",
            "root_id",
            "served_by",
            "trainable",
            "default_training_parameters",
            "image",
            "deployment_parameters",
        )
        data = self.sess.perform_op(op)
        return self._output_formatter((op + data).meta_ai_model_by_pk, to_json)

    def get_model_by_name(self, name, to_json=False, verbose=False) -> List[Union[meta_ai_model, Dict]]:
        op = Operation(query_root)
        op.meta_ai_model(where={"name": {"_eq": name}}).__fields__(*self._fields(verbose))
        data = self.sess.perform_op(op)
        return self._output_formatter((op + data).meta_ai_model, to_json)

    def get_model_by_name_version(
        self, name, version, to_json=False, verbose=False
    ) -> List[Union[meta_ai_model, Dict]]:
        op = Operation(query_root)
        op.meta_ai_model(where={"name": {"_eq": name}, "version": {"_eq": version}}).__fields__(*self._fields(verbose))
        data = self.sess.perform_op(op)
        return self._output_formatter((op + data).meta_ai_model, to_json)

    def list_model_versions(
        self, model_id, to_json=False, verbose=False, sort_by_version=True, ascending=True
    ) -> List[Union[meta_ai_model, Dict]]:
        """
        List all versions of a model which share a common root model (given by the root_id).
        Args:
            model_id: uuid
                Does not need to be the id of the root model.
            to_json:
                If True, returns a list of dictionaries instead of schema objects.
            verbose:
                If True, returns all model fields.
            sort_by_version: bool
                Sort list by version number, depending on `ascending`
            ascending: bool
                If True, sort in ascending order. Root model is always first.
                If False, sort in descending order, most recent model first.

        Returns:

        """
        op = Operation(query_root)
        # We query the root_model and then its sibling_models which gives us the whole lineage
        op.meta_ai_model_by_pk(id=model_id).root_model().sibling_models().__fields__(*self._fields(verbose=verbose))
        data = self.sess.perform_op(op)
        models = (op + data).meta_ai_model_by_pk.root_model.sibling_models
        if sort_by_version:
            models = sorted(models, key=lambda x: x.version, reverse=not ascending)
        return self._output_formatter(models, to_json)

    def get_root_model(self, model_id, to_json=False, verbose=False) -> Optional[Union[meta_ai_model, Dict]]:
        """
        Get the root model,  i.e. the model that is the parent of all other models.
        Currently, thats always the one with version=1.

        Args:
            model_id: uuid
                Id of one of the models in the lineage.
            to_json:
                If True, returns a list of dictionaries instead of schema objects.
            verbose:
                If True, returns all model fields.

        Returns:

        """
        op = Operation(query_root)
        # We query the root_model and then its sibling_models which gives us the whole lineage
        op.meta_ai_model_by_pk(id=model_id).root_model().__fields__(*self._fields(verbose=verbose))
        data = self.sess.perform_op(op)
        models = (op + data).meta_ai_model_by_pk.root_model
        return self._output_formatter(models, to_json)

    def get_latest_model(self, model_id, to_json=False, verbose=False) -> Optional[Union[meta_ai_model, Dict]]:
        """
        Get the latest (highest) model version of a model.


        Returns:
            meta_ai_model
        """
        # Get sorted model list
        models = self.list_model_versions(model_id, sort_by_version=True, ascending=False, verbose=verbose)
        return self._output_formatter(models[0], to_json)

    def add_model(
        self,
        name: str,
        description: str = "",
        version: int = 1,
        stage: str = "LOCAL",
        metadata: str = None,
        visibility: meta_ai_visibility_enum = "PRIVATE",
        root_id: str = None,
        input_schema: dict = None,
        output_schema: dict = None,
        model_save_path: str = "",
        weights_path: str = "",
        default_training_parameters: dict = None,
        trainable: bool = False,
        image: str = None,
        deployment_parameters: Optional[Union[dict, "DeploymentParameters"]] = None,
    ) -> str:
        """
        Add a new model to the database.
        Args:
            name:
                Name of the model.
            description:
                Description of the model.
            version:
                Version of the model.
            stage:
                Stage of the model.
            metadata:
                Metadata of the model. Currently, this is a JSON string.
            visibility:
                Visibility of the model. PUBLIC or PRIVATE.
                PUBLIC models can be used by anyone.
                PRIVATE models can only be used by the user who created it.
            root_id:
                Id of the root model. Establishes the lineage of the model.
                Is mainly used in retraining a model and storing the weights of the model in a new version.
            input_schema:
                Input schema of the model. Is used to match data to compatible models.
            output_schema:
                Output schema of the model.
            model_save_path:
                URI to the stored model source code.
            weights_path:
                URI to the stored model weights.
            default_training_parameters:
                Default training parameters for the model. Can be used to create training templates.
            trainable:
                If True, the model can be trained and a `train` method exists.
            image:
                Path to the docker image containing the model execution environment.
                Will be used for prediction serving and training.
            deployment_parameters:
                Parameters for the deployment in the backend. Mainly contains hardware and scaling parameters.

        Returns:

        """
        from superai.meta_ai.parameters import AiDeploymentParameters

        deployment_parameters = deployment_parameters or {}
        if not isinstance(deployment_parameters, AiDeploymentParameters):
            deployment_parameters = AiDeploymentParameters.parse_obj(deployment_parameters)
        op = Operation(mutation_root)
        op.insert_meta_ai_model_one(
            object=meta_ai_model_insert_input(
                name=name,
                description=description,
                version=version,
                metadata=json.dumps(metadata) if metadata is not None else metadata,
                visibility=visibility,
                input_schema=json.dumps(input_schema),
                output_schema=json.dumps(output_schema),
                model_save_path=model_save_path,
                weights_path=weights_path,
                root_id=root_id,
                stage=stage,
                trainable=trainable,
                image=image,
                default_training_parameters=json.dumps(default_training_parameters)
                if default_training_parameters is not None
                else default_training_parameters,
                deployment_parameters=deployment_parameters.json_for_db(),
            )
        ).__fields__(
            "name", "version", "id", "stage", "description", "visibility", "root_id", "image", "deployment_parameters"
        )
        data = self.sess.perform_op(op)
        log.info(f"Created new model: {data}")
        return (op + data).insert_meta_ai_model_one.id

    def update_model(self, model_id: str, **kwargs) -> str:
        """
        Update a model based with specified keyword arguments.
        E.g. update_model(model_id, description="new_description")

        Args:
            model_id:
            default_training_parameters: dict
            description: str
            image: str
            input_schema: dict
            metadata: dict
            output_schema: dict
            served_by: str
            stage: str
            trainable: bool
            visibility: str
            deployment_parameters: dict

        Returns:
            str: Id of the updated model.

        """
        from superai.meta_ai.parameters import AiDeploymentParameters

        deployment_parameters = kwargs.get("deployment_parameters", {})
        if not isinstance(deployment_parameters, AiDeploymentParameters):
            deployment_parameters = AiDeploymentParameters.parse_obj(deployment_parameters)
        kwargs["deployment_parameters"] = deployment_parameters.json_for_db()

        op = Operation(mutation_root)
        op.update_meta_ai_model_by_pk(
            _set=meta_ai_model_set_input(**kwargs),
            pk_columns=meta_ai_model_pk_columns_input(id=model_id),
        ).__fields__("id", *kwargs.keys())
        data = self.sess.perform_op(op)
        return (op + data).update_meta_ai_model_by_pk.id

    def update_model_by_name_version(self, name: str, version: int, **kwargs) -> str:
        """
        Update a model (identified by name and version) with specified keyword arguments
        E.g. update_model_by_name_version(name="model123", version=1, description="new_description")

        Args:
            model_id:
            default_training_parameters: dict
            description: str
            image: str
            input_schema: dict
            metadata: dict
            output_schema: dict
            served_by: str
            stage: str
            trainable: bool
            visibility: str

        Returns:
            str: Id of the updated model.

        """
        if name is None or version is None:
            raise ValueError("name and version must be specified")
        if kwargs is None:
            raise ValueError("At least one kwarg must be specified")
        opq = Operation(query_root)
        opq.meta_ai_model(
            where={"name": {"_eq": name}, "version": {"_eq": version}},
        ).__fields__("name", "version", "id", "stage")
        data = self.sess.perform_op(opq)
        res = (opq + data).meta_ai_model
        if len(res) == 0:
            raise Exception(f"Could not find any matching entries with {name}:{version}")
        idx = res[0].id
        return self.update_model(idx, **kwargs)

    def get_latest_version_of_model_by_name(self, name: str) -> int:
        opq = Operation(query_root)
        opq.meta_ai_model(where={"name": {"_eq": name}}).__fields__("version")
        data = self.sess.perform_op(opq)
        res = (opq + data).meta_ai_model
        if len(res) == 0:
            raise Exception(f"Could not find any entries with model name `{name}`")
        else:
            res = list(map(lambda x: x.version, res))
            return sorted(res, reverse=True)[0]

    def delete_model(self, idx) -> str:
        op = Operation(mutation_root)
        op.delete_meta_ai_model_by_pk(id=idx).__fields__("name", "version", "id")
        data = self.sess.perform_op(op)
        return (op + data).delete_meta_ai_model_by_pk.id

    def add_app_mapping(self, idx, app_id, assignment="RAW", active=False, threshold=0.1):
        op = Operation(mutation_root)
        op.insert_meta_ai_app_one(
            model_id=idx,
            id=app_id,
            assigned=meta_ai_assignment_enum(assignment),
            active=active,
            threshold=threshold,
        ).__fields__("id")
        data = self.sess.perform_op(op)
        log.info(f"Created a new app mapping for app_id {app_id} and model {idx}: {data}")
        app_id = (op + data).insert_meta_ai_app_one.id
        return app_id


class DeploymentApiMixin(ABC):
    _resource = "deployment"

    def __init__(self):
        self.sess = MetaAISession()

    @property
    def resource(self):
        return self._resource

    def deploy(
        self,
        model_id: str,
        deployment_type: meta_ai_deployment_type_enum = "AWS_EKS",
        purpose: str = "SERVING",
        properties: dict = None,
        initial_status: meta_ai_deployment_status_enum = "OFFLINE",
        wait: bool = False,
    ) -> Optional[str]:
        """Mutation query to create a new entry in the deployment table, should deploy an endpoint in the action handler
        and store the endpoint name in the table.

        Args:
            deployment_type: type of backend deployment
            purpose:
            model_id:
            properties: dict, as in AITemplate.deployment_parameters
            wait: bool, if True, wait for the deployment to be completed before returning.

        Returns:
            str: id of the newly created deployment
        """
        existing_deployment = self.get_deployment(model_id)
        if "status" not in existing_deployment:
            op = Operation(mutation_root)
            op.insert_meta_ai_deployment_one(
                object=meta_ai_deployment_insert_input(
                    model_id=model_id,
                    type=meta_ai_deployment_type_enum(deployment_type),
                    purpose=meta_ai_deployment_purpose_enum(purpose),
                    target_status=meta_ai_deployment_status_enum(initial_status),
                    properties=json.dumps(properties),
                )
            ).__fields__("id", "model_id", "target_status", "created_at")
            data = self.sess.perform_op(op)
            log.info(f"Created new deployment: {data}")
            deployment_id = (op + data).insert_meta_ai_deployment_one.id
            if wait:
                try:
                    self._wait_for_state_change(deployment_id, field="status", target_status=initial_status)
                except Exception as e:
                    log.warning(f"Exception during wait, aborting wait: {e}")
            return deployment_id
        else:
            log.info(f"Deployment already exists with properties: {existing_deployment} ")
            return None

    def _set_target_status(
        self, deployment_id: str, target_status: meta_ai_deployment_status_enum
    ) -> meta_ai_deployment_status_enum:
        op = Operation(mutation_root)
        op.update_meta_ai_deployment_by_pk(
            _set=meta_ai_deployment_set_input(target_status=target_status),
            pk_columns=meta_ai_deployment_pk_columns_input(id=deployment_id),
        ).__fields__("target_status")
        data = self.sess.perform_op(op)
        try:
            return (op + data).update_meta_ai_deployment_by_pk.target_status
        except:
            raise Exception("Could not set target status. Check if you have Ownership for this deployment.")

    def set_deployment_status(
        self, deployment_id: str, target_status: meta_ai_deployment_status_enum, timeout: int = 600
    ) -> bool:
        """Change status field of an existing deployment.

        Args:
            deployment_id: The UUID of the deployment
            target_status: The designated status of the deployment which the backend will fulfill
            timeout: The number of seconds to wait for a status change in a polling fashion
        """
        # Set to neutral state first to trigger event handler in any case
        self._set_target_status(deployment_id, "UNKNOWN")
        time.sleep(1)
        self._set_target_status(deployment_id, target_status)
        return self._wait_for_state_change(deployment_id, field="status", target_status=target_status, timeout=timeout)

    def _wait_for_state_change(self, deployment_id: str, field: str, target_status, timeout=600):
        console = Console()
        end_time = time.time() + timeout
        retries = 0
        with console.status("[bold green]Waiting for status change...") as status:
            while time.time() < end_time:
                backend_status = self.get_deployment(deployment_id)[field]
                if backend_status == target_status:
                    console.log(f"[green]Success: [b]{field}[/b] achieved [b]{target_status}[/b]")
                    return True
                if retries % 10 == 0:
                    console.log(
                        f"waiting for [yellow]{field}[/]==[green]{target_status}[/] "
                        f"- retry {retries}, time {retries * 10} seconds"
                    )
                time.sleep(10)
                retries += 1

        console.log(f"[red][b]{field}[/b] did not reach [b]{target_status}[/b] after [b]{timeout}[/b] seconds")
        return False

    def set_min_instances(self, deployment_id: str, min_instances: int) -> object:
        """Change minimum instances of an existing deployment.
        Setting `min_instances=0` allows the backend to automatically pause deployments to save resources.
        To set the timeout for this behaviour, use `set_scale_in_timeout`.

        Args:
            deployment_id:
            min_instances:
        """
        assert min_instances >= 0, "min_instances needs to be non-negative"
        op = Operation(mutation_root)
        op.update_meta_ai_deployment_by_pk(
            _set=meta_ai_deployment_set_input(min_instances=min_instances),
            pk_columns=meta_ai_deployment_pk_columns_input(id=deployment_id),
        ).__fields__("id", "model_id", "min_instances")
        data = self.sess.perform_op(op)
        return (op + data).update_meta_ai_deployment_by_pk

    def set_scale_in_timeout(self, deployment_id: str, timeout_mins: int) -> object:
        """Change scale in timeout of an existing deployment.
        After a deployment makes no predictions for `timeout_mins` minutes, it gets `PAUSED`.
        A paused deployment has no active computing resources.
        To resume a paused deployment, you can use `set_deployment_status(deployment_id=..., target_status=ONLINE)`

        Args:
            deployment_id:
            timeout_mins:
        """
        op = Operation(mutation_root)
        op.update_meta_ai_deployment_by_pk(
            _set=meta_ai_deployment_set_input(scale_in_timeout=timeout_mins),
            pk_columns=meta_ai_deployment_pk_columns_input(id=deployment_id),
        ).__fields__("id", "model_id", "scale_in_timeout")
        data = self.sess.perform_op(op)
        return (op + data).update_meta_ai_deployment_by_pk

    def set_deployment_properties(self, deployment_id: str, properties: dict) -> object:
        """Change properties of a deployment used next time a deployment instance is created.

        Args:
            deployment_id: str
            properties: dict
        """
        op = Operation(mutation_root)
        op.update_meta_ai_deployment_by_pk(
            _set=meta_ai_deployment_set_input(properties=json.dumps(properties)),
            pk_columns=meta_ai_deployment_pk_columns_input(id=deployment_id),
        ).__fields__("id", "model_id", "properties")
        data = self.sess.perform_op(op)
        return (op + data).update_meta_ai_deployment_by_pk

    def undeploy(self, deployment_id: str) -> bool:
        """Stop a running deployment.
        Return True if stopped successfully.
        Args:
            deployment_id:
        """
        return self.set_deployment_status(
            deployment_id=deployment_id, target_status=meta_ai_deployment_status_enum.OFFLINE
        )

    def get_deployment(self, deployment_id: str) -> dict:
        """Retrieves deployment entry"""
        opq = Operation(query_root)
        opq.meta_ai_deployment_by_pk(id=deployment_id).__fields__(
            "id",
            "model_id",
            "status",
            "target_status",
            "created_at",
            "updated_at",
            "purpose",
            "properties",
            "min_instances",
            "scale_in_timeout",
        )
        data = self.sess.perform_op(opq)
        res = (opq + data).meta_ai_deployment_by_pk
        return res

    def list_deployments(
        self, model_id: Optional[str] = None, status: Optional[meta_ai_deployment_status_enum] = None
    ) -> List[meta_ai_deployment]:
        """
        Retrieves list of deployments.
        Allows filtering by model_id or status.

        Args:
            model_id: str
            status: meta_ai_deployment_status_enum
                One of "FAILED", "MAINTENANCE", "OFFLINE", "ONLINE", "PAUSED", "STARTING", "UNKNOWN"

        """
        opq = Operation(query_root)
        filter = {}
        if model_id:
            filter["model_id"] = uuid_comparison_exp(_eq=model_id)
        if status:
            filter["status"] = meta_ai_deployment_status_enum_comparison_exp(_eq=status)
        deployments = opq.meta_ai_deployment(where=meta_ai_deployment_bool_exp(**filter))
        models = deployments.model()
        models.__fields__("name", "id")
        deployments.__fields__(
            "id",
            "status",
            "target_status",
            "created_at",
            "updated_at",
            "purpose",
            "properties",
            "min_instances",
            "scale_in_timeout",
        )
        data = self.sess.perform_op(opq)
        res = (opq + data).meta_ai_deployment
        return res

    def check_endpoint_is_available(self, deployment_id) -> bool:
        """Query to check if there is an active deployment"""
        deployment = self.get_deployment(deployment_id)
        if deployment is not None:
            if deployment["status"] == "ONLINE":
                return True
        return False

    def get_prediction_error(self, prediction_id: str):
        op = Operation(query_root)
        p = op.meta_ai_prediction_by_pk(id=prediction_id)
        p.__fields__("error_message", "state", "completed_at", "started_at")
        data = self.sess.perform_op(op)
        try:
            output = (op + data).meta_ai_prediction_by_pk
            return output
        except AttributeError:
            log.info(f"No prediction found for prediction_id:{prediction_id}.")

    def wait_for_prediction_completion(
        self,
        prediction_id: str,
        app_id: str = None,
        timeout: int = 180,
    ):
        """
        Wait for a prediction to complete.
        Complete is either when the prediction is finished properly or it failed.
        Args:
            prediction_id: str
                id of existing prediction
            app_id: str (optional)
                id of app the predection belongs to, used for authentication
                Predictions could be created without an app_id.
            timeout: int
                timeout in seconds. Default is 180 seconds.
                No upper limit is imposed even though predictions should never take
                 longer than a fresh model deployment.
                60 seconds * 15 minutes worst case deployment time = 900 seconds.

        Returns:
            str: prediction status

        """
        sess = MetaAIWebsocketSession(app_id=app_id)
        opq = Operation(subscription_root)
        prediction = opq.meta_ai_prediction_by_pk(id=prediction_id)
        prediction.__fields__("state")
        start = time.time()

        def generate_table(id, state) -> Table:
            """Make a new table."""
            table = Table(box=box.MINIMAL)
            table.add_column("ID")
            table.add_column("Current State")
            table.add_row(str(id), str(state))
            return table

        with Live(generate_table(prediction_id, ""), auto_refresh=False, transient=True) as live:
            while time.time() - start < timeout:
                data = next(sess.perform_op(opq))
                res: meta_ai_prediction = (opq + data).meta_ai_prediction_by_pk
                live.update(generate_table(prediction_id, res.state), refresh=True)
                if res.state == meta_ai_prediction_state_enum.COMPLETED:
                    return res
                elif res.state == meta_ai_prediction_state_enum.FAILED:
                    error_object = self.get_prediction_error(prediction_id)
                    logger.warning(f"Prediction failed while waiting for completion:\n {error_object.error_message}")
                    raise PredictionError(error_object["error_message"])
            else:
                raise TimeoutError("Waiting for Prediction result timed out. Try increasing timeout.")

    @staticmethod
    def get_prediction_with_data(prediction_id: str, app_id: str = None) -> Optional[meta_ai_prediction]:
        """
        Retrieve existing prediction with data from database.
        Args:
            prediction_id: str
                id of existing prediction
            app_id: str
                id of app the predection belongs to, used for authentication.
                For predictions created without an app_id, this argument is not required.

        Returns:

        """
        sess = MetaAISession(app_id=app_id)
        op = Operation(query_root)
        p = op.meta_ai_prediction_by_pk(id=prediction_id)
        p.__fields__("id", "state", "created_at", "completed_at", "started_at", "error_message")
        p.model.__fields__("id", "name", "version")
        p.instances().__fields__("id", "output", "score")
        data = sess.perform_op(op)
        try:
            output = (op + data).meta_ai_prediction_by_pk
            return output
        except AttributeError:
            log.info(f"No prediction found for prediction_id:{prediction_id}.")
            return None

    def submit_prediction_request(
        self, model_id: str = None, input_data: dict = None, deployment_id=None, parameters: dict = None
    ) -> str:
        """Submit a prediction request using input data and custom parameters.
        Will use either a specific deployment or a deployment assigned to the model.
        Returns the prediction id.
        The prediction id can be awaited using the `wait_for_prediction_completion` method.

        Args:
            deployment_id: id of the deployment
            model_id: id of the model. Will map to an assigned deployment in the backend
            input_data: raw data or reference to stored object
            parameters: parameters for the model inference
        """
        if model_id is None and deployment_id is None:
            raise ValueError("Either model_id or deployment_id must be specified.")
        if not input_data:
            raise ValueError("Input data must be specified.")
        request = {
            "model_id": model_id,
            "deployment_id": deployment_id,
            "data": json.dumps(input_data),
            "parameters": json.dumps(parameters),
        }
        opq = Operation(query_root)
        opq.predict_with_deployment_async(request=request).__fields__("prediction_id")
        data = self.sess.perform_op(opq)
        res = (opq + data).predict_with_deployment_async
        prediction_id = res.prediction_id
        return prediction_id

    def predict_from_endpoint(
        self,
        model_id: str = None,
        deployment_id: str = None,
        input_data: dict = None,
        parameters: dict = None,
        timeout: int = 180,
    ) -> List[RawPrediction]:
        """Predict with endpoint using input data and custom parameters.
        Endpoint is identified either by specific deployment_id or inferred using the model_id.

        Returns a list of tuples of the form (output, score).

        Args:
            deployment_id: id of the model. Will map to an assigned deployment in the backend
            model_id: id of the model deployed, acts as the primary key of the deployment
            input_data: raw data or reference to stored object
            parameters: parameters for the model inference
            timeout: timeout in seconds to await for a prediction

        """
        if model_id is None and deployment_id is None:
            raise ValueError("Either model_id or deployment_id must be specified.")
        if not input_data:
            raise ValueError("Input data must be specified.")

        prediction_id = self.submit_prediction_request(
            deployment_id=deployment_id, model_id=model_id, input_data=input_data, parameters=parameters
        )
        logger.info(f"Submitted prediction request with id: {prediction_id}")

        # Wait for prediction to complete
        state = self.wait_for_prediction_completion(prediction_id=prediction_id, timeout=timeout)
        logger.info(f"Prediction {prediction_id} completed with state={state}")

        # Retrieve finished data
        prediction: query_root.meta_ai_prediction = self.get_prediction_with_data(prediction_id=prediction_id)
        return [
            RawPrediction(json_data={"output": instance.output, "score": instance.score})
            for instance in prediction.instances
        ]


class TrainApiMixin(ABC):
    _resource = "train"

    def __init__(self):
        self.sess = MetaAISession()

    @property
    def resource(self):
        return self._resource

    @staticmethod
    def create_training_template_entry(
        model_id: Union[uuid, str], properties: dict, app_id: uuid = None, description: Optional[str] = None
    ) -> Optional[meta_ai_training_template]:
        """
        Creates a new training template entry.

        Returns: the id of the created entry

        Args:
            model_id: ref model if for the template
            properties: the default properties that will get inherited during trainings
            app_id: ref app id for the template
            description: Description of template
        """
        app_id_str = str(app_id) if app_id else None
        sess = MetaAISession(app_id=app_id_str)
        model_api = ModelApiMixin()
        root_model_id = model_api.get_root_model(model_id=str(model_id))["id"]

        op = Operation(mutation_root)
        op.insert_meta_ai_training_template_one(
            object=meta_ai_training_template_insert_input(
                model_id=root_model_id,
                app_id=app_id,
                properties=json.dumps(properties),
                description=description,
            )
        ).__fields__("id", "app_id", "model_id", "properties", "description")
        try:
            data = sess.perform_op(op)
            log.info(f"Created training template {data}")
            return (op + data).insert_meta_ai_training_template_one
        except GraphQlException as e:
            if "duplicate" in str(e):
                raise Exception(
                    "Training template already exists. Currently only one template is allowed per app/model."
                )

    @staticmethod
    def update_training_template(
        template_id: uuid = None,
        model_id: uuid = None,
        app_id: uuid = None,
        properties: dict = None,
        description: str = None,
    ):
        """
        Update existing training template entry.

        Returns: the id of the updated entry

        Args:
            app_id: ref app id for the template
            model_id: ref model if for the template
            properties: the default properties that will get inherited during trainings
            description: optional description for the template
        """
        app_id_str = str(app_id) if app_id else None
        sess = MetaAISession(app_id=app_id_str)
        op = Operation(mutation_root)
        if not template_id:
            templates = TrainApiMixin.get_training_templates(model_id, app_id)
            if len(templates) < 1:
                raise Exception("Cannot update template. Template does not exist.")
            template_id = templates[0].id

        update_dict = {}
        if properties:
            update_dict["properties"] = json.dumps(properties)
        if description:
            update_dict["description"] = description

        op.update_meta_ai_training_template_by_pk(
            _set=meta_ai_training_template_set_input(**update_dict),
            pk_columns=meta_ai_training_template_pk_columns_input(id=template_id),
        ).__fields__("id", "app_id", "model_id", "properties", "description")
        data = sess.perform_op(op)
        log.info(f"Updated training template {data}")
        return (op + data).update_meta_ai_training_template_by_pk.id

    @staticmethod
    def get_training_templates(model_id: Union[uuid, str], app_id: uuid = None) -> List[meta_ai_training_template]:
        """
        Finds training templates from the app id and model id keys.

        Returns: the training templates

        Args:
            app_id: ref app id for the template
            model_id: ref model if for the template
        """
        app_id_str = str(app_id) if app_id else None
        sess = MetaAISession(app_id=app_id_str)
        op = Operation(query_root)

        root_model_id = ModelApiMixin().get_root_model(model_id=str(model_id))["id"]
        log.info(
            f"Getting training templates indexed by root_model_id={root_model_id} inferred from model_id={model_id}"
        )
        filter = {"model_id": {"_eq": root_model_id}}
        if app_id_str:
            filter["app_id"] = {"_eq": app_id_str}
        else:
            filter["app_id"] = {"_is_null": True}

        op.meta_ai_training_template(where=filter).__fields__("id", "name", "properties", "created_at", "description")
        instance_data = sess.perform_op(op)
        try:
            q_out = (op + instance_data).meta_ai_training_template
        except AttributeError:
            log.info(f"No training templates found for app_id={app_id}, model_id={model_id}.")
            return []

        return q_out

    @staticmethod
    def get_training_template(template_id: uuid, app_id: Optional[uuid]) -> Optional[meta_ai_training_template]:
        """
        Query single training template by id if it exists.

        Returns: the training template

        Args:
            template_id: id of the template
            app_id: app id for the template
        """
        app_id_str = str(app_id) if app_id else None
        sess = MetaAISession(app_id=app_id_str)
        op = Operation(query_root)

        op.meta_ai_training_template_by_pk(id=str(template_id)).__fields__(
            "id",
            "properties",
            "created_at",
            "description",
            "app_id",
            "model_id",
            "name",
        )
        instance_data = sess.perform_op(op)
        try:
            q_out = (op + instance_data).meta_ai_training_template_by_pk
        except AttributeError:
            log.exception(f"No training template found for id={template_id}")
            return

        return q_out

    @staticmethod
    def delete_training_template(id: uuid, app_id: uuid):
        """
        Deletes an existing template.

        Returns: the id of the deleted entry

        Args:
            id: the id of the template you want to remove
            app_id: ref app id for the template
        """
        app_id_str = str(app_id) if app_id else None
        sess = MetaAISession(app_id=app_id_str)
        op = Operation(mutation_root)
        op.delete_meta_ai_training_template_by_pk(id=id).__fields__("id")
        data = sess.perform_op(op)
        return (op + data).delete_meta_ai_training_template_by_pk.id

    def create_training_entry(
        self,
        model_id: Union[uuid, str],
        app_id: Optional[uuid] = None,
        properties: Optional[dict] = None,
        starting_state: Optional[str] = "STARTING",
        template_id: Optional[uuid] = None,
    ):
        """
        Insert a new training instance, triggering a new training run

        Returns: the id of the started training

        Args:
            model_id: ref model if for the training instance
            app_id: ref app id for the training instance, can be used to create dataset from
            properties: this is by default inherited from the default of the template, or can be
            specified as a dict of properties custom for this run
            starting_state: the starting state of the training, can be one of: STOPPED, STARTING
                Stopped starting state can be used to delay the start of the training until data is uploaded
            template_id: the id of the template to use for this training
        """
        assert starting_state in [None, "STOPPED", "STARTING"], "starting_state must be one of: STOPPED, STARTING"
        properties = properties or {}

        app_id_str = str(app_id) if app_id else None
        sess = MetaAISession(app_id=app_id_str)

        template = None
        if template_id:
            log.info(f"Using template_id={template_id}")
            template = self.get_training_template(str(template_id), app_id=app_id)
        elif app_id:
            # Pick one of the templates for this app
            templates = self.get_training_templates(model_id, app_id)
            if len(templates) < 1:
                log.warning("No existing template found. Creating new one automatically.")
                template = self.create_training_template_entry(model_id, properties, app_id)
            else:
                template = templates[0]
            log.info(f"Creating new training run based on exising template: {template}")

        if not properties and template:
            log.info("No properties specified. Using default properties from template.")
            properties = template["properties"]
        else:
            log.warning("No training properties specified. Falling back to empty properties `{}`.")

        op = Operation(mutation_root)

        op.insert_meta_ai_training_instance_one(
            object=meta_ai_training_instance_insert_input(
                training_template_id=template_id or template.get("id") if template else None,
                current_properties=json.dumps(properties),
                model_id=model_id,
                state=starting_state,
            )
        ).__fields__("id", "training_template_id", "current_properties", "model_id", "state")

        data = sess.perform_op(op)

        log.info(f"Created training instance {data}")
        return (op + data).insert_meta_ai_training_instance_one.id

    @staticmethod
    def get_trainings(
        app_id: uuid = None,
        model_id: uuid = None,
        state: str = "",
        limit=10,
    ) -> List[meta_ai_training_instance]:
        """
        Finds training instances from the app id and model id keys.

        Returns: the training runs

        Args:
            app_id: ref app id for the template
            model_id: ref model if for the template
            state: by default this quries for IN_PROGRESS run, but can be one the state in training state enum
            limit: the maximum number of results to return

        """
        app_id_str = str(app_id) if app_id else None
        sess = MetaAISession(app_id=app_id_str)
        op = Operation(query_root)

        filter = {}
        if state:
            filter["state"] = {"_eq": state}
        if model_id:
            filter["model_id"] = {"_eq": model_id}
        if app_id:
            filter["training_template"] = {}
            filter["training_template"]["app_id"] = {"_eq": app_id}
        instance_query = dict(where=filter, limit=limit)
        log.warning("Without providing an app_id, only trainings without associated apps will be shown.")
        op.meta_ai_training_instance(**instance_query).__fields__(
            "state", "id", "created_at", "artifacts", "model_id", "training_template_id", "updated_at"
        )
        instance_data = sess.perform_op(op)
        instances = (op + instance_data).meta_ai_training_instance

        logger.info(
            f"Showing a total of {len(instances)}, training instances for app_id:{app_id}, model_id:{model_id}."
        )
        return instances

    @staticmethod
    def delete_training(id: uuid, app_id: uuid):
        """
        Deletes an existing training run.

        Returns: the id of the deleted entry

        Args:
            id: the id of the training run you want to remove
            app_id: ref app id for the training run
        """
        sess = MetaAISession(app_id=str(app_id))
        op = Operation(mutation_root)
        op.delete_meta_ai_training_instance_by_pk(id=id).__fields__("id")
        data = sess.perform_op(op)
        return (op + data).delete_meta_ai_training_instance_by_pk.id

    @staticmethod
    def update_training_instance(instance_id: uuid, app_id: str = None, state: str = None):
        assert state in [None, "STARTING"], "Only STARTING state is supported for now."

        sess = MetaAISession(app_id=str(app_id) if app_id else None)
        op = Operation(mutation_root)

        op.update_meta_ai_training_instance_by_pk(
            _set=meta_ai_training_instance_set_input(**dict(state=state)),
            pk_columns=meta_ai_training_instance_pk_columns_input(id=instance_id),
        ).__fields__("id", "model_id", "current_properties", "state")
        data = sess.perform_op(op)
        return (op + data).update_meta_ai_training_instance_by_pk.id

    @staticmethod
    def start_training_from_app_model_template(
        app_id: uuid,
        model_id: uuid,
        task_name: str,
        training_template_id: uuid,
        current_properties: Optional[dict] = None,
        metadata: Optional[dict] = None,
    ) -> uuid:
        """
        Starts a training given the app_id, model_id, task_name, training_template_id. This automatically creates a
        dataset from the app, and starts training from the training_template_id.

        Args:
            app_id: App ID
            model_id: Model ID of the model
            task_name: Task name of the tasks to be trained on
            training_template_id: ID of the training template
            current_properties: properties to be passed to the training
            metadata: metadata passed to training
        Returns:
             Instance ID of the training created
        """
        sess = MetaAISession(app_id=str(app_id))

        opq = Operation(query_root)
        request = {
            "app_id": app_id,
            "model_id": model_id,
            "task_name": task_name,
            "training_template_id": training_template_id,
        }
        if current_properties:
            request["current_properties"] = json.dumps(current_properties)
        if metadata:
            request["metadata"] = json.dumps(metadata)
        opq.start_training(request=request).__fields__("training_instance_id")
        data = sess.perform_op(opq)
        res = (opq + data).start_training
        training_instance_id = res.training_instance_id
        return training_instance_id

    @staticmethod
    def get_artifact_download_url(
        model_id: Union[str, uuid], artifact_type: str, app_id: uuid = None, timeout: int = 360
    ) -> str:
        """
        Get the download url for an artifact.

        Parameters
        ----------
        model_id : uuid
            Model UUID for which the artifacts are downloaded.
        app_id : uuid, Optional
            `app_id` is necessary when model was assigned to an app for training.
        artifact_type : str
            Allowed `artifact_type` is one of [weights,source].
        timeout : int, Optional
            Timeout in seconds for the artifact download. Default is 360 seconds.
        """
        app_id_str = str(app_id) if app_id else None

        if artifact_type not in ["weights", "source"]:
            raise ValueError(f"artifact_type must be one of ['weights', 'source']")

        sess = MetaAIWebsocketSession(app_id=app_id_str)

        # Start artifact compression in backend and get operation id
        op = Operation(mutation_root)
        op.download_artifact_async(artifact_type=artifact_type, model_id=model_id)

        data = next(sess.perform_op(op))
        id = (op + data).download_artifact_async

        # Query id for results until ready
        start = time.time()
        console = Console()
        with console.status(f"Waiting for artifact preparation to complete for model_id={model_id}") as status:
            while time.time() - start < timeout:
                os = Operation(subscription_root)
                result = os.download_artifact_async(id=id)
                result.__fields__("id", "errors")
                result.output.__fields__("url")
                data = next(sess.perform_op(os))
                res: download_artifact_async = (os + data).download_artifact_async
                if res.errors:
                    if "error" in res.errors:
                        error = res.errors["error"]
                    else:
                        error = res.errors
                    raise Exception("Error while preparing model artifact: {}".format(error))
                if res.output:
                    console.log("Artifact ready for download")
                    return res.output.url
            else:
                raise TimeoutError("Waiting for Artifact download url timed out. Try increasing timeout.")
