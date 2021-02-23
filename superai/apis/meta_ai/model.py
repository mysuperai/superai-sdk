from abc import ABC

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

    def add_model(
        self,
        name: str,
        description: str = "",
        version: int = 1,
        metadata: str = None,
        endpoint: str = "",
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
            )
        ).__fields__("name", "version", "id", "endpoint", "description")
        data = self.sess.perform_op(op)
        log.info(f"Created new model: {data}")
        return (op + data).insert_meta_ai_model_one.id

    def update_model(self, id, **kwargs):
        op = Operation(mutation_root)
        op.update_meta_ai_model_by_pk(
            _set=meta_ai_model_set_input(**kwargs), pk_columns=meta_ai_model_pk_columns_input(id=id)
        ).__fields__("name", "version", "id", "endpoint", "description")
        data = self.sess.perform_op(op)
        return (op + data).update_meta_ai_model_by_pk.id

    def delete_model(self, id):
        op = Operation(mutation_root)
        op.delete_meta_ai_model_by_pk(id=id).__fields__("name", "version", "id", "endpoint")
        data = self.sess.perform_op(op)
        return (op + data).delete_meta_ai_model_by_pk.id
