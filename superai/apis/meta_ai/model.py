from __future__ import annotations

import json
import time
from typing import TYPE_CHECKING, List, Optional, Union

import click
from rich import box
from rich.console import Console
from rich.live import Live
from rich.table import Table
from sgqlc.operation import Operation

from superai.apis.meta_ai.meta_ai_graphql_schema import (
    TrainingParameters,
    download_artifact_async,
    meta_ai_deployment,
    meta_ai_deployment_bool_exp,
    meta_ai_deployment_insert_input,
    meta_ai_deployment_pk_columns_input,
    meta_ai_deployment_purpose_enum,
    meta_ai_deployment_set_input,
    meta_ai_deployment_status_enum,
    meta_ai_deployment_status_enum_comparison_exp,
    meta_ai_deployment_type_enum,
    meta_ai_model_bool_exp,
    meta_ai_prediction,
    meta_ai_prediction_state_enum,
    meta_ai_training_instance,
    meta_ai_training_instance_insert_input,
    meta_ai_training_instance_order_by,
    meta_ai_training_instance_pk_columns_input,
    meta_ai_training_instance_set_input,
    meta_ai_training_template,
    meta_ai_training_template_insert_input,
    meta_ai_training_template_pk_columns_input,
    meta_ai_training_template_set_input,
    mutation_root,
    query_root,
    subscription_root,
    uuid,
    uuid_comparison_exp,
)
from superai.log import console, get_logger

from .base import AiApiBase
from .session import (  # type: ignore
    GraphQlException,
    MetaAISession,
    MetaAIWebsocketSession,
)

log = get_logger(__name__)


if TYPE_CHECKING:
    from superai.meta_ai.schema import TaskPredictionInstance


class PredictionError(Exception):
    """Prediction Error"""


class DeploymentException(Exception):
    """All deployment API mixin exceptions"""


class DeploymentApiMixin(AiApiBase):
    """Deployment API"""

    _resource = "deployment"

    @property
    def resource(self):
        return self._resource

    def deploy(
        self,
        ai_instance_id: str = None,
        deployment_type: meta_ai_deployment_type_enum = "AWS_EKS_ASYNC",
        purpose: str = "SERVING",
        properties: dict = None,
        initial_status: meta_ai_deployment_status_enum = "OFFLINE",
        wait: bool = False,
    ) -> Optional[str]:
        """Mutation query to create a new entry in the deployment table, should deploy an endpoint in the action handler
        and store the endpoint name in the table.

        Args:
            ai_instance_id:
            deployment_type: type of backend deployment
            purpose:
            properties: dict, as in AITemplate.deployment_parameters
            wait: bool, if True, wait for the deployment to be completed before returning.
            initial_status:

        Returns:
            str: id of the newly created deployment
        """
        op = Operation(mutation_root)
        op.insert_meta_ai_deployment_one(
            object=meta_ai_deployment_insert_input(
                ai_instance_id=ai_instance_id,
                type=meta_ai_deployment_type_enum(deployment_type),
                purpose=meta_ai_deployment_purpose_enum(purpose),
                target_status=meta_ai_deployment_status_enum(initial_status),
                properties=json.dumps(properties),
            )
        ).__fields__("id", "ai_instance_id", "target_status", "created_at")
        data = self.ai_session.perform_op(op)
        log.info(f"Created new deployment: {data}")
        deployment_id = (op + data).insert_meta_ai_deployment_one.id
        if wait:
            try:
                self._wait_for_state_change(deployment_id, field="status", target_status=initial_status)
            except Exception as e:
                raise DeploymentException("Deployment failed") from e
        return deployment_id

    def _set_target_status(
        self, deployment_id: str, target_status: Union[meta_ai_deployment_status_enum, str]
    ) -> meta_ai_deployment_status_enum:
        op = Operation(mutation_root)
        op.update_meta_ai_deployment_by_pk(
            _set=meta_ai_deployment_set_input(target_status=target_status),
            pk_columns=meta_ai_deployment_pk_columns_input(id=deployment_id),
        ).__fields__("target_status")
        data = self.ai_session.perform_op(op)
        try:
            return (op + data).update_meta_ai_deployment_by_pk.target_status
        except Exception as e:
            raise DeploymentException(
                "Could not set target status. Check if you have Ownership for this deployment."
            ) from e

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

    def update_deployment(self, deployment_id: str, timeout: int = 600) -> bool:
        """This function will perform a seamless update of the deployment if the backend type supports it.
        This enables no-downtime deployments."""
        log.info(f"Starting seamless update of deployment {deployment_id}")
        # Set to neutral state first to trigger event handler in any case
        self._set_target_status(deployment_id, "UNKNOWN")
        time.sleep(1)
        self._set_target_status(deployment_id, "UPDATING")
        # The backend will perform the update and finally set the status to ONLINE
        return self._wait_for_state_change(deployment_id, field="status", target_status="ONLINE", timeout=timeout)

    def _wait_for_state_change(self, deployment_id: str, field: str, target_status, timeout=600):
        end_time = time.time() + timeout
        retries = 0
        sleep_time = min(timeout, 10)
        with console.status("[bold green]Waiting for status change..."):
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
                time.sleep(sleep_time)
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
        data = self.ai_session.perform_op(op)
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
        data = self.ai_session.perform_op(op)
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
        ).__fields__("id", "ai_instance_id", "properties")
        data = self.ai_session.perform_op(op)
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
            "status",
            "target_status",
            "created_at",
            "updated_at",
            "purpose",
            "properties",
            "min_instances",
            "scale_in_timeout",
            "ai_instance_id",
            "type",
        )
        data = self.ai_session.perform_op(opq)
        return (opq + data).meta_ai_deployment_by_pk

    def list_deployments(
        self,
        model_id: Optional[str] = None,
        model_name: Optional[str] = None,
        status: Optional[meta_ai_deployment_status_enum] = None,
    ) -> List[meta_ai_deployment]:
        """Retrieves list of deployments.
        Allows filtering by model_id, model_name or status.

        Args:
            model_id: str
            model_name: str
            status: meta_ai_deployment_status_enum
                One of "FAILED", "MAINTENANCE", "OFFLINE", "ONLINE", "PAUSED", "STARTING", "UNKNOWN"

        """
        opq = Operation(query_root)
        filters = {}
        if model_id:
            filters["ai_instance_id"] = uuid_comparison_exp(_eq=model_id)
        if model_name:
            filters["model"] = meta_ai_model_bool_exp({"name": {"_eq": model_name}})
        if status:
            filters["status"] = meta_ai_deployment_status_enum_comparison_exp(_eq=status)
        deployments = opq.meta_ai_deployment(where=meta_ai_deployment_bool_exp(**filters))
        models = deployments.modelv2s()
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
        data = self.ai_session.perform_op(opq)
        return (opq + data).meta_ai_deployment

    def check_endpoint_is_available(self, deployment_id) -> bool:
        """Query to check if there is an active deployment"""
        deployment = self.get_deployment(deployment_id)
        return deployment is not None and deployment["status"] == "ONLINE"

    def get_prediction_error(self, prediction_id: str) -> Optional[meta_ai_prediction]:
        op = Operation(query_root)
        p = op.meta_ai_prediction_by_pk(id=prediction_id)
        p.__fields__("error_message", "state", "completed_at", "started_at")
        data = self.ai_session.perform_op(op)
        try:
            return (op + data).meta_ai_prediction_by_pk
        except AttributeError:
            log.info(f"No prediction found for prediction_id:{prediction_id}.")

    def wait_for_prediction_completion(
        self,
        prediction_id: str,
        app_id: str = None,
        timeout: int = 180,
    ):
        """Wait for a prediction to complete.
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

        def generate_table(id_, state) -> Table:
            """Make a new table."""
            table = Table(box=box.MINIMAL)
            table.add_column("Prediction ID")
            table.add_column("Current State")
            table.add_row(str(id_), str(state))
            return table

        with Live(generate_table(prediction_id, ""), auto_refresh=False, transient=True, console=console) as live:
            while time.time() - start < timeout:
                data = next(sess.perform_op(opq))
                res: meta_ai_prediction = (opq + data).meta_ai_prediction_by_pk
                live.update(generate_table(prediction_id, res.state), refresh=True)
                if res.state == meta_ai_prediction_state_enum.COMPLETED:
                    return res
                elif res.state == meta_ai_prediction_state_enum.FAILED:
                    error_object = self.get_prediction_error(prediction_id)
                    error = str(error_object.error_message)
                    log.warning("Prediction failed while waiting for completion", extra={"error": error})
                    raise PredictionError(error)
            raise TimeoutError("Waiting for Prediction result timed out. Try increasing timeout.")

    def get_prediction_with_data(self, prediction_id: str, app_id: str = None) -> Optional[meta_ai_prediction]:
        """Retrieve existing prediction with data from database.
        Args:
            prediction_id: str
                id of existing prediction
            app_id: str
                id of app the predection belongs to, used for authentication.
                For predictions created without an app_id, this argument is not required.

        Returns:

        """
        op = Operation(query_root)
        p = op.meta_ai_prediction_by_pk(id=prediction_id)
        p.__fields__("id", "state", "created_at", "completed_at", "started_at", "error_message")
        p.model.__fields__("id", "name")
        p.instances().__fields__("id", "output", "score")
        data = self.ai_session.perform_op(op, app_id=app_id)
        try:
            return (op + data).meta_ai_prediction_by_pk
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
        data = self.ai_session.perform_op(opq)
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
    ) -> TaskPredictionInstance:
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
        if input_data is None:
            raise ValueError("Input data must be specified.")

        prediction_id = self.submit_prediction_request(
            deployment_id=deployment_id, model_id=model_id, input_data=input_data, parameters=parameters
        )
        log.info(f"Submitted prediction request with id: {prediction_id}")

        # Wait for prediction to complete
        state = self.wait_for_prediction_completion(prediction_id=prediction_id, timeout=timeout)
        log.info(f"Prediction {prediction_id} completed with state={state}")

        # Retrieve finished data
        prediction: query_root.meta_ai_prediction = self.get_prediction_with_data(prediction_id=prediction_id)
        from superai.meta_ai.schema import TaskPredictionInstance

        return [
            TaskPredictionInstance(prediction=instance.output, score=instance.score)
            for instance in prediction.instances
        ][0]

    def predict_from_endpoint_async(
        self,
        model_id: str = None,
        deployment_id: str = None,
        input_data: dict = None,
        parameters: dict = None,
    ) -> str:
        """Predict with endpoint using input data and custom parameters.
        Endpoint is identified either by specific deployment_id or inferred using the model_id.

        Returns a prediction uuid.

        Args:
            deployment_id: id of the model. Will map to an assigned deployment in the backend
            model_id: id of the model deployed, acts as the primary key of the deployment
            input_data: raw data or reference to stored object
            parameters: parameters for the model inference

        """
        if model_id is None and deployment_id is None:
            raise ValueError("Either model_id or deployment_id must be specified.")
        if not input_data:
            raise ValueError("Input data must be specified.")

        prediction_id = self.submit_prediction_request(
            deployment_id=deployment_id, model_id=model_id, input_data=input_data, parameters=parameters
        )
        return prediction_id


class TrainingException(Exception):
    """All training API exceptions"""


class TrainApiMixin(AiApiBase):
    """Training API"""

    _resource = "train"

    @property
    def resource(self):
        return self._resource

    def create_training_template_entry(
        self, ai_instance_id: Union[uuid, str], properties: dict, app_id: uuid = None, description: Optional[str] = None
    ) -> Optional[meta_ai_training_template]:
        """Creates a new training template entry.

        Returns: the id of the created entry

        Args:
            ai_instance_id: id of the ai instance
            properties: the default properties that will get inherited during trainings
            app_id: id of the app the template belongs to
            description: Description of template
        """

        op = Operation(mutation_root)
        op.insert_meta_ai_training_template_one(
            object=meta_ai_training_template_insert_input(
                ai_instance_id=ai_instance_id,
                app_id=app_id,
                properties=json.dumps(properties),
                description=description,
            )
        ).__fields__("id", "app_id", "ai_instance_id", "properties", "description")
        try:
            data = self.ai_session.perform_op(op, app_id=app_id)
            log.info(f"Created training template {data}")
            return (op + data).insert_meta_ai_training_template_one
        except GraphQlException as e:
            if "duplicate" in str(e):
                raise TrainingException(
                    "Training template already exists. Currently only one template is allowed per app/model."
                ) from e

    def update_training_template(
        self,
        template_id: Optional[str] = None,
        ai_instance_id: Optional[str] = None,
        app_id: Optional[str] = None,
        properties: Optional[dict] = None,
        description: Optional[str] = None,
    ):
        """Update existing training template entry.

        Returns: the id of the updated entry

        Args:
            app_id: id of the app the template belongs to
            ai_instance_id: id of the AI instance
            properties: the default properties that will get inherited during trainings
            description: optional description for the template
            template_id:
        """
        op = Operation(mutation_root)
        if not template_id:
            templates = self.list_training_templates(ai_instance_id, app_id)
            if len(templates) < 1:
                raise TrainingException("Cannot update template. Template does not exist.")
            template_id = templates[0].id

        update_dict = {}
        if properties:
            update_dict["properties"] = json.dumps(properties)
        if description:
            update_dict["description"] = description

        op.update_meta_ai_training_template_by_pk(
            _set=meta_ai_training_template_set_input(**update_dict),
            pk_columns=meta_ai_training_template_pk_columns_input(id=str(template_id)),
        ).__fields__("id", "app_id", "ai_instance_id", "properties", "description")
        data = self.ai_session.perform_op(op, app_id=app_id)
        log.info(f"Updated training template {data}")
        return (op + data).update_meta_ai_training_template_by_pk.id

    def list_training_templates(
        self, ai_instance_id: Union[uuid, str], app_id: uuid = None
    ) -> List[meta_ai_training_template]:
        """Finds training templates from the app id and model id keys.

        Returns: the training templates

        Args:
            app_id: app id for the template
            ai_instance_id: model if for the template
        """
        app_id_str = str(app_id) if app_id else None
        op = Operation(query_root)

        filters = {
            "ai_instance_id": {"_eq": ai_instance_id},
            "app_id": {"_eq": app_id_str} if app_id_str else {"_is_null": True},
        }
        op.meta_ai_training_template(where=filters).__fields__("id", "name", "properties", "created_at", "description")
        instance_data = self.ai_session.perform_op(op, app_id=app_id)
        try:
            q_out = (op + instance_data).meta_ai_training_template
        except AttributeError:
            log.info(f"No training templates found for app_id={app_id_str}, model_id={ai_instance_id}.")
            return []

        return q_out

    def get_training_template(
        self, template_id: Union[uuid, str], app_id: Optional[uuid]
    ) -> Optional[meta_ai_training_template]:
        """Query single training template by id if it exists.

        Returns: the training template

        Args:
            template_id: id of the template
            app_id: app id for the template
        """
        op = Operation(query_root)

        op.meta_ai_training_template_by_pk(id=str(template_id)).__fields__(
            "id",
            "properties",
            "created_at",
            "description",
            "app_id",
            "model_id",
            "ai_instance_id",
            "name",
        )
        instance_data = self.ai_session.perform_op(op, app_id=app_id)
        try:
            q_out = (op + instance_data).meta_ai_training_template_by_pk
        except AttributeError:
            log.exception(f"No training template found for id={template_id}")
            return

        return q_out

    def delete_training_template(self, id: uuid, app_id: uuid):
        """Deletes an existing template.

        Returns: the id of the deleted entry

        Args:
            id: the id of the template you want to remove
            app_id: ref app id for the template
        """
        op = Operation(mutation_root)
        op.delete_meta_ai_training_template_by_pk(id=id).__fields__("id")
        data = self.ai_session.perform_op(op, app_id=app_id)
        return (op + data).delete_meta_ai_training_template_by_pk.id

    def create_training_entry(
        self,
        ai_instance_id: Union[uuid, str],
        app_id: Optional[uuid] = None,
        properties: Optional[dict] = None,
        starting_state: Optional[str] = "STARTING",
        template_id: Optional[uuid] = None,
        source_checkpoint_id=None,
    ):
        """Insert a new training instance, triggering a new training run

        Returns: the id of the started training

        Args:
            ai_instance_id: id of the AI instance
            app_id: id of the app the template belongs to
            properties: the default properties that will get inherited during trainings
            starting_state: the starting state of the training
            template_id: id of the template to use
            source_checkpoint_id: id of the checkpoint to use as a starting weights

        """
        assert source_checkpoint_id
        assert starting_state in [None, "STOPPED", "STARTING"], "starting_state must be one of: STOPPED, STARTING"
        properties = properties or {}

        # Each training run needs a template to start from
        template = self._find_training_template(ai_instance_id, app_id, properties, template_id)

        if not properties and template:
            log.info("No properties specified. Using default properties from template.")
            properties = template["properties"]
        else:
            log.warning("No training properties specified. Falling back to empty properties `{}`.")

        op = Operation(mutation_root)

        op.insert_meta_ai_training_instance_one(
            object=meta_ai_training_instance_insert_input(
                training_template_id=template_id or template.id if template else None,
                current_properties=json.dumps(properties),
                source_checkpoint_id=source_checkpoint_id,
                state=starting_state,
                modelv2_id=ai_instance_id,
            )
        ).__fields__("id", "training_template_id", "current_properties", "source_checkpoint_id", "state")

        data = self.ai_session.perform_op(op, app_id=app_id)

        log.info(f"Created training instance {data}")
        return (op + data).insert_meta_ai_training_instance_one.id

    def _find_training_template(self, ai_instance_id, app_id, properties, template_id) -> meta_ai_training_template:
        template = None
        if template_id:
            log.info(f"Using template_id={template_id}")
            template = self.get_training_template(str(template_id), app_id=app_id)
        elif app_id:
            # Pick one of the templates for this app
            templates = self.list_training_templates(ai_instance_id, app_id)
            if len(templates) < 1:
                log.warning("No existing template found. Creating new one automatically.")
                template = self.create_training_template_entry(ai_instance_id, properties, app_id)
            else:
                template = templates[0]
            log.info(f"Creating new training run based on exising template: {template}")
        return template

    def list_trainings(
        self,
        app_id: uuid = None,
        ai_instance_id: uuid = None,
        state: str = "",
        limit=10,
    ) -> List[meta_ai_training_instance]:
        """Finds training instances from the app id and model id keys.

        Returns: the training runs

        Args:
            app_id: ref app id for the template
            ai_instance_id: ref model if for the template
            state: by default this quries for IN_PROGRESS run, but can be one the state in training state enum
            limit: the maximum number of results to return

        """
        op = Operation(query_root)

        filters = {}
        if state:
            filters["state"] = {"_eq": state}
        if ai_instance_id:
            filters["modelv2_id"] = {"_eq": ai_instance_id}
        if app_id:
            filters["training_template"] = {}
            filters["training_template"]["app_id"] = {"_eq": app_id}
        instance_query = dict(
            where=filters, limit=limit, order_by=[meta_ai_training_instance_order_by(created_at="desc")]
        )
        log.warning("Without providing an app_id, only trainings without associated apps will be shown.")
        op.meta_ai_training_instance(**instance_query).__fields__(
            "state", "id", "created_at", "artifacts", "modelv2_id", "training_template_id", "updated_at"
        )
        instance_data = self.ai_session.perform_op(op, app_id=app_id)
        instances = (op + instance_data).meta_ai_training_instance

        log.info(
            f"Showing a total of {len(instances)}, training instances for app_id:{app_id}, ai_instance:{ai_instance_id}."
        )
        return instances

    def delete_training(self, id: uuid, app_id: uuid):
        """Deletes an existing training run.

        Returns: the id of the deleted entry

        Args:
            id: the id of the training run you want to remove
            app_id: ref app id for the training run
        """
        op = Operation(mutation_root)
        op.delete_meta_ai_training_instance_by_pk(id=id).__fields__("id")
        data = self.ai_session.perform_op(op, app_id=app_id)
        return (op + data).delete_meta_ai_training_instance_by_pk.id

    def update_training_instance(self, instance_id: uuid, app_id: Union[click.UUID, str] = None, state: str = None):
        assert state in {None, "STARTING"}, "Only STARTING state is supported for now."
        op = Operation(mutation_root)

        op.update_meta_ai_training_instance_by_pk(
            _set=meta_ai_training_instance_set_input(**dict(state=state)),
            pk_columns=meta_ai_training_instance_pk_columns_input(id=instance_id),
        ).__fields__("id", "modelv2_id", "current_properties", "state")
        data = self.ai_session.perform_op(op, app_id=app_id)
        return (op + data).update_meta_ai_training_instance_by_pk.id

    def get_training_instance(self, id: uuid, app_id: Optional[uuid] = None) -> meta_ai_training_instance:
        """Finds a training instance from the app id and model id keys.

        Returns: the training run

        Args:
            id: the id of the training run you want to fetch
            app_id: app id for the training run if it was based on app data
        """
        op = Operation(query_root)
        op.meta_ai_training_instance_by_pk(id=id).__fields__(
            "state", "id", "created_at", "artifacts", "modelv2_id", "training_template_id", "updated_at"
        )
        data = self.ai_session.perform_op(op, app_id=app_id)
        return (op + data).meta_ai_training_instance_by_pk

    def start_training_from_app_model_template(
        self,
        app_id: uuid,
        ai_instance_id: uuid,
        task_name: str,
        training_template_id: uuid,
        checkpoint_id: str,
        current_properties: Optional[dict] = None,
        dataset_metadata: Optional[dict] = None,
        timeout=300,
    ) -> uuid:
        """Starts a training given the app_id, ai_instance_id, task_name, training_template_id. This automatically creates a
        dataset from the app, and starts training from the training_template_id.

        Args:
            app_id: App ID
            ai_instance_id: AI Instance ID
            task_name: Task name of the tasks to be trained on
            checkpoint_id: ID of the AI checkpoint to be used as a starting point
            training_template_id: ID of the training template
            current_properties: properties to be passed to the training
            dataset_metadata: dataset metadata passed to training, can contain training/testing/validation splits
        Returns:
             Instance ID of the training created
        """

        opq = Operation(query_root)
        request = TrainingParameters(
            app_id=app_id,
            model_id=ai_instance_id,
            task_name=task_name,
            checkpoint_id=checkpoint_id,
            training_template_id=training_template_id,
        )
        if current_properties:
            request["current_properties"] = json.dumps(current_properties)
        if dataset_metadata:
            request["metadata"] = json.dumps(dataset_metadata)
        opq.start_training(request=request).__fields__("training_instance_id")
        data = self.ai_session.perform_op(opq, app_id=app_id, timeout=timeout)
        res = (opq + data).start_training
        training_instance_id = res.training_instance_id
        return training_instance_id

    def get_artifact_download_url(
        self, model_id: Union[str, uuid], artifact_type: str, app_id: uuid = None, timeout: int = 360
    ) -> str:
        """Get the download url for an artifact.

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

        if artifact_type not in ["weights", "source"]:
            raise ValueError("artifact_type must be one of ['weights', 'source']")

        sess = MetaAIWebsocketSession(app_id=app_id)

        # Start artifact compression in backend and get operation id
        op = Operation(mutation_root)
        op.download_artifact_async(artifact_type=artifact_type, model_id=model_id)

        data = next(sess.perform_op(op))
        download_id = (op + data).download_artifact_async

        # Query id for results until ready
        start = time.time()
        console = Console()
        with console.status(f"Waiting for artifact preparation to complete for model_id={model_id}"):
            while time.time() - start < timeout:
                os = Operation(subscription_root)
                result = os.download_artifact_async(id=download_id)
                result.__fields__("id", "errors")
                result.output.__fields__("url")
                data = next(sess.perform_op(os))
                res: download_artifact_async = (os + data).download_artifact_async
                if res.errors:
                    error = res.errors["error"] if "error" in res.errors else res.errors
                    raise TrainingException(f"Error while preparing model artifact: {error}")
                if res.output:
                    console.log("Artifact ready for download")
                    return res.output.url
            raise TimeoutError("Waiting for Artifact download url timed out. Try increasing timeout.")
