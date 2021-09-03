import json
import time
from abc import ABC
from typing import Tuple

from sgqlc.operation import Operation  # type: ignore

from superai.log import logger
from .session import MetaAISession  # type: ignore


from superai.apis.meta_ai.meta_ai_graphql_schema import (
    meta_ai_model_insert_input,
    meta_ai_model_pk_columns_input,
    meta_ai_model_set_input,
    meta_ai_deployment_insert_input,
    meta_ai_deployment_pk_columns_input,
    meta_ai_deployment_set_input,
    meta_ai_visibility_enum,
    mutation_root,
    query_root,
    meta_ai_deployment_type_enum,
    meta_ai_deployment_purpose_enum,
    meta_ai_deployment_status_enum,
    meta_ai_assignment_enum,
)

log = logger.get_logger(__name__)


class ModelApiMixin(ABC):
    _resource = "model"

    def __init__(self):
        self.sess = MetaAISession()

    @property
    def resource(self):
        return self._resource

    def get_all_models(self):
        op = Operation(query_root)
        op.meta_ai_model().__fields__("name", "version", "id")
        data = self.sess.perform_op(op)
        return (op + data).meta_ai_model

    def get_model(self, idx):
        op = Operation(query_root)
        op.meta_ai_model_by_pk(id=idx).__fields__("name", "version", "id")
        data = self.sess.perform_op(op)
        return (op + data).meta_ai_model_by_pk

    def get_model_by_name(self, name):
        op = Operation(query_root)
        op.meta_ai_model(where={"name": {"_eq": name}}).__fields__(
            "name", "version", "id", "model_save_path", "weights_path"
        )
        data = self.sess.perform_op(op)
        return list(
            map(
                lambda x: {
                    "name": x.name,
                    "version": x.version,
                    "id": x.id,
                    "modelSavePath": x.model_save_path,
                    "weightsPath": x.weights_path,
                },
                (op + data).meta_ai_model,
            )
        )

    def get_model_by_name_version(self, name, version):
        op = Operation(query_root)
        op.meta_ai_model(where={"name": {"_eq": name}, "version": {"_eq": version}}).__fields__(
            "name", "version", "id", "model_save_path", "weights_path"
        )
        data = self.sess.perform_op(op)
        return list(
            map(
                lambda x: {
                    "name": x.name,
                    "version": x.version,
                    "id": x.id,
                    "modelSavePath": x.model_save_path,
                    "weightsPath": x.weights_path,
                },
                (op + data).meta_ai_model,
            )
        )

    def add_model(
        self,
        name: str,
        description: str = "",
        version: int = 1,
        stage: str = "LOCAL",
        metadata: str = None,
        visibility: meta_ai_visibility_enum = "PRIVATE",
    ):
        op = Operation(mutation_root)
        op.insert_meta_ai_model_one(
            object=meta_ai_model_insert_input(
                name=name,
                description=description,
                version=version,
                metadata=metadata,
                visibility=visibility,
                stage=stage,
            )
        ).__fields__("name", "version", "id", "stage", "description")
        data = self.sess.perform_op(op)
        log.info(f"Created new model: {data}")
        return (op + data).insert_meta_ai_model_one.id

    def add_model_full_entry(
        self,
        name: str,
        description: str = "",
        version: int = 1,
        metadata: str = None,
        input_schema: dict = None,
        output_schema: dict = None,
        model_save_path: str = "",
        weights_path: str = "",
        visibility: meta_ai_visibility_enum = "PRIVATE",
    ):
        """Add a complete model entry in the database.

        Args:
            name:
            description:
            version:
            metadata:
            input_schema:
            output_schema:
            model_save_path:
            weights_path:
            visibility:
        """
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
            )
        ).__fields__("name", "version", "id", "description")
        data = self.sess.perform_op(op)
        log.info(f"Created new model: {data}")
        return (op + data).insert_meta_ai_model_one.id

    def update_model(self, idx, **kwargs):
        op = Operation(mutation_root)
        op.update_meta_ai_model_by_pk(
            _set=meta_ai_model_set_input(**kwargs),
            pk_columns=meta_ai_model_pk_columns_input(id=idx),
        ).__fields__("name", "version", "id", "description")
        data = self.sess.perform_op(op)
        return (op + data).update_meta_ai_model_by_pk.id

    def update_model_by_name_version(self, name: str, version: int, **kwargs):
        opq = Operation(query_root)
        opq.meta_ai_model(
            where={"name": {"_eq": name}, "version": {"_eq": version}},
        ).__fields__("name", "version", "id", "stage")
        data = self.sess.perform_op(opq)
        res = (opq + data).meta_ai_model
        if len(res) == 0:
            raise Exception(f"Could not find any matching entries with {name}:{version}")
        idx = res[0].id
        op = Operation(mutation_root)
        op.update_meta_ai_model_by_pk(
            _set=meta_ai_model_set_input(**kwargs),
            pk_columns=meta_ai_model_pk_columns_input(id=idx),
        ).__fields__("name", "version", "id", "description")
        data = self.sess.perform_op(op)
        return (op + data).update_meta_ai_model_by_pk.id

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

    def delete_model(self, idx):
        op = Operation(mutation_root)
        op.delete_meta_ai_model_by_pk(id=idx).__fields__("name", "version", "id")
        data = self.sess.perform_op(op)
        return (op + data).delete_meta_ai_model_by_pk.id


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
        ecr_image_name: str,
        deployment_type: meta_ai_deployment_type_enum = "AWS_SAGEMAKER",
        purpose: str = "SERVING",
        properties: dict = None,
    ):
        """Mutation query to create a new entry in the deployment table, should deploy an endpoint in the action handler
        and store the endpoint name in the table.

        Args:
            deployment_type: type of backend deployment
            purpose:
            model_id:
            ecr_image_name: Can be queried from the meta_ai_table to populate.
            properties: dict
                Possible values (with defaults) are:
                    "sagemaker_instance_type": "ml.m5.xlarge"
                    "sagemaker_initial_instance_count": 1
                    "lambda_memory": 256
                    "lambda_timeout": 30
        """
        existing_deployment = self.get_deployment(model_id)
        if "status" not in existing_deployment:
            op = Operation(mutation_root)
            op.insert_meta_ai_deployment_one(
                object=meta_ai_deployment_insert_input(
                    model_id=model_id,
                    type=meta_ai_deployment_type_enum(deployment_type),
                    purpose=meta_ai_deployment_purpose_enum(purpose),
                    image=ecr_image_name,
                    target_status="ONLINE",
                    properties=json.dumps(properties),
                )
            ).__fields__("model_id", "target_status", "created_at")
            data = self.sess.perform_op(op)
            log.info(f"Created new deployment: {data}")
            model_id = (op + data).insert_meta_ai_deployment_one.model_id
            self._wait_for_state_change(model_id, field="status", target_status="ONLINE")
            return model_id
        else:
            log.info(f"Deployment already exists with properties: {existing_deployment} ")

    def _set_target_status(
        self, model_id: str, target_status: meta_ai_deployment_status_enum
    ) -> meta_ai_deployment_status_enum:
        op = Operation(mutation_root)
        op.update_meta_ai_deployment_by_pk(
            _set=meta_ai_deployment_set_input(target_status=target_status),
            pk_columns=meta_ai_deployment_pk_columns_input(model_id=model_id),
        ).__fields__("target_status")
        data = self.sess.perform_op(op)
        return (op + data).update_meta_ai_deployment_by_pk.target_status

    def set_deployment_status(self, model_id: str, target_status: meta_ai_deployment_status_enum) -> bool:
        """Change status field of an existing deployment.

        Args:
            model_id:
            target_status: The designated status of the deployment which the backend will fulfill
        """
        current_status = self.get_deployment(model_id)["status"]
        current_target_status = self.get_deployment(model_id)["target_status"]

        if current_status == target_status:
            if current_status != target_status:
                logger.info(f"Deployment status not consistent. Setting field target_status to {target_status}")
                stored_target_status = self._set_target_status(model_id, target_status)
                return stored_target_status == target_status
            return True
        elif current_status != target_status and current_target_status == target_status:
            return self._wait_for_state_change(model_id, field="status", target_status=target_status)
        else:
            stored_target_status = self._set_target_status(model_id, target_status)
            assert stored_target_status == target_status, "Could not set Deployment target_status properly."
            return self._wait_for_state_change(model_id, field="status", target_status=target_status)

    def _wait_for_state_change(self, model_id: str, field: str, target_status, retries=20):
        log.info("Waiting for status change...")
        for t in range(retries):
            backend_status = self.get_deployment(model_id)[field]
            if backend_status == target_status:
                log.info(f"Success: {field} achieved {target_status}")
                return True
            if t % 10 == 0:
                log.info(f"waiting for {field}=={target_status} match retry {t}, time {t * 10} seconds")
            time.sleep(10)
        else:
            log.info(f"{field} did not reach {target_status}")
            return False

    def set_image(self, model_id: str, ecr_image_name: str) -> object:
        """Change image of an existing deployment.

        Args:
            ecr_image_name:
            model_id:
        """
        op = Operation(mutation_root)
        op.update_meta_ai_deployment_by_pk(
            _set=meta_ai_deployment_set_input(image=ecr_image_name),
            pk_columns=meta_ai_deployment_pk_columns_input(model_id=model_id),
        ).__fields__("model_id", "image")
        data = self.sess.perform_op(op)
        return (op + data).update_meta_ai_deployment_by_pk

    def set_deployment_properties(self, model_id: str, properties: dict) -> object:
        """Change properties of a deployment used next time a deployment instance is created.

        Args:
            model_id: str
            properties: dict
        """
        op = Operation(mutation_root)
        op.update_meta_ai_deployment_by_pk(
            _set=meta_ai_deployment_set_input(properties=json.dumps(properties)),
            pk_columns=meta_ai_deployment_pk_columns_input(model_id=model_id),
        ).__fields__("model_id", "properties")
        data = self.sess.perform_op(op)
        return (op + data).update_meta_ai_deployment_by_pk

    def undeploy(self, model_id: str) -> bool:
        """Remove an entry from the deployment table. Action handler should delete the endpoint.
        Return True if deleted successfully.

        Args:
            model_id:
        """
        return self.set_deployment_status(model_id=model_id, target_status=meta_ai_deployment_status_enum.OFFLINE)

    def get_deployment(self, model_id) -> dict:
        """Retrieves deployment entry"""
        opq = Operation(query_root)
        opq.meta_ai_deployment_by_pk(model_id=model_id).__fields__(
            "model_id", "status", "target_status", "created_at", "updated_at", "purpose", "properties"
        )
        data = self.sess.perform_op(opq)
        res = (opq + data).meta_ai_deployment_by_pk
        return res

    def check_endpoint_is_available(self, model_id) -> bool:
        """Query to check if there is an active deployment"""
        deployment = self.get_deployment(model_id=model_id)
        if deployment is not None:
            if deployment["status"] == "ONLINE":
                return True
        return False

    def predict_from_endpoint(self, model_id: str, data_input: dict, parameters: dict = None, timeout: int = 20):
        """Query the endpoint name from deployment table, return prediction (using MetaAI sagemaker configuration)

        Args:
            model_id: id of the model deployed, acts as the primary key of the deployment
            data_input: raw data or reference to stored object
            parameters: parameters for the model inference
            timeout: timeout in seconds to await for a prediction

        """
        request = {"deployment_id": model_id, "data": json.dumps(data_input), "parameters": json.dumps(parameters)}
        opq = Operation(query_root)
        opq.predict_with_deployment(request=request).__fields__("output", "score")
        data = self.sess.perform_op(opq, timeout)
        res = (opq + data).predict_with_deployment
        return res


class TrainApiMixin(ABC):
    _resource = "train"

    def __init__(self):
        self.sess = MetaAISession()

    @property
    def resource(self):
        return self._resource

    def create_training_entry(
        self,
        name,
        version,
        train_data,
        ecr_image_name,
    ):
        """
        Mutation query to create a new entry in the training table, should deploy an endpoint in the action handler
        and store the endpoint name in the table

        Args:
            train_data:
            name:
            version:
            ecr_image_name: Can be queries from the meta_ai_table to populate
        """
        raise NotImplementedError()

    def delete_training_entry(self, name, version) -> Tuple[bool, str]:
        """Remove an entry from the training table. Action handler should delete the endpoint. Return True if deleted
         successfully.

        Args:
            name:
            stage:
            version:
        """
        raise NotImplementedError()
