import json
from abc import ABC
from typing import Tuple

from sgqlc.operation import Operation

from superai.log import logger
from .session import MetaAISession

log = logger.get_logger(__name__)

from superai.apis.meta_ai.meta_ai_graphql_schema import (
    meta_ai_model_insert_input,
    meta_ai_model_pk_columns_input,
    meta_ai_model_set_input,
    meta_ai_visibility_enum,
    mutation_root,
    query_root,
    meta_ai_environment_enum,
)


class ModelApiMixin(ABC):
    _resource = "model"

    def __init__(self):
        self.sess = MetaAISession()

    @property
    def resource(self):
        return self._resource

    def get_all_models(self):
        op = Operation(query_root)
        op.meta_ai_model().__fields__("name", "version", "id", "endpoint")
        data = self.sess.perform_op(op)
        return (op + data).meta_ai_model

    def get_model(self, id):
        op = Operation(query_root)
        op.meta_ai_model_by_pk(id=id).__fields__("name", "version", "id", "endpoint")
        data = self.sess.perform_op(op)
        return (op + data).meta_ai_model_by_pk

    def get_model_by_name(self, name):
        op = Operation(query_root)
        op.meta_ai_model(where={"name": {"_eq": name}}).__fields__(
            "name", "version", "id", "endpoint", "model_save_path"
        )
        data = self.sess.perform_op(op)
        return list(
            map(
                lambda x: {
                    "name": x.name,
                    "version": x.version,
                    "id": x.id,
                    "endpoint": x.endpoint,
                    "modelSavePath": x.model_save_path,
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
        endpoint: str = None,
        visibility: meta_ai_visibility_enum = "PRIVATE",
    ):
        op = Operation(mutation_root)
        op.insert_meta_ai_model_one(
            object=meta_ai_model_insert_input(
                name=name,
                description=description,
                version=version,
                metadata=metadata,
                endpoint=endpoint,
                visibility=visibility,
                stage=stage,
            )
        ).__fields__("name", "version", "id", "stage", "endpoint", "description")
        data = self.sess.perform_op(op)
        log.info(f"Created new model: {data}")
        return (op + data).insert_meta_ai_model_one.id

    def add_model_full_entry(
        self,
        name: str,
        description: str = "",
        version: int = 1,
        stage: str = "LOCAL",
        metadata: str = None,
        endpoint: str = None,
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
            stage:
            metadata:
            endpoint:
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
                metadata=metadata,
                endpoint=endpoint,
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

    def update_model(self, id, **kwargs):
        op = Operation(mutation_root)
        op.update_meta_ai_model_by_pk(
            _set=meta_ai_model_set_input(**kwargs),
            pk_columns=meta_ai_model_pk_columns_input(id=id),
        ).__fields__("name", "version", "id", "endpoint", "description")
        data = self.sess.perform_op(op)
        return (op + data).update_meta_ai_model_by_pk.id

    def update_model_by_name_version(self, name: str, version: int, **kwargs) -> None:
        opq = Operation(query_root)
        opq.meta_ai_model(
            where={"name": {"_eq": name}, "version": {"_eq": version}},
        ).__fields__("name", "version", "id", "stage")
        data = self.sess.perform_op(opq)
        res = (opq + data).meta_ai_model
        if len(res) == 0:
            raise Exception(f"Could not find any matching entries with {name}:{version}")
        else:
            id = res[0].id
            op = Operation(mutation_root)
            op.update_meta_ai_model_by_pk(
                _set=meta_ai_model_set_input(**kwargs),
                pk_columns=meta_ai_model_pk_columns_input(id=id),
            ).__fields__("name", "version", "id", "endpoint", "description")
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

    def delete_model(self, id):
        op = Operation(mutation_root)
        op.delete_meta_ai_model_by_pk(id=id).__fields__("name", "version", "id", "endpoint")
        data = self.sess.perform_op(op)
        return (op + data).delete_meta_ai_model_by_pk.id


class DeploymentApiMixin(ABC):
    _resource = "deployment"

    def __init__(self):
        self.sess = MetaAISession()

    @property
    def resource(self):
        return self._resource

    def deploy(self, name, version, ecr_image_name):
        """Mutation query to create a new entry in the deployment table, should deploy an endpoint in the action handler
        and store the endpoint name in the table.
        
        Args:
            name:
            stage:
            version:
            ecr_image_name: Can be queries from the meta_ai_table to populate.
        """
        raise NotImplementedError()

    def undeploy(self, name, version) -> Tuple[bool, str]:
        """Remove an entry from the deployment table. Action handler should delete the endpoint. Return True if deleted successfully.
        
        Args:
            name:
            stage:
            version:
        """
        raise NotImplementedError()

    def check_endpoint_is_available(self, name, version) -> bool:
        """Query to check if there is an entry in DB
        """
        raise NotImplementedError()

    def predict_from_endpoint(self, name, version, input):
        """Query the endpoint name from deployment table. Return prediction (using MetaAI sagemaker configuration).
        Args:
            name:
            stage:
            version:
            input:
        """
        raise NotImplementedError()


class TrainApiMixin(ABC):
    _resource = "train"

    def __init__(self):
        self.sess = MetaAISession()

    @property
    def resource(self):
        return self._resource

    def create_training_entry(self, name, version, train_data):
        """Mutation query to create a new entry in the training table. Should deploy an endpoint in the action handler
        and store the endpoint name in the table.
        
        Args:
            name:
            stage:
            version:
            ecr_image_name: Can be queries from the meta_ai_table to populate.
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
