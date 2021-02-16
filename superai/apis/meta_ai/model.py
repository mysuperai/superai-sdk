from sgqlc.operation import Operation
from superai.log import logger

from .session import MetaAISession

log = logger.get_logger(__name__)

from superai.apis.meta_ai.meta_ai_schema import (
    meta_ai_app_constraint,
    meta_ai_app_insert_input,
    meta_ai_app_on_conflict,
    meta_ai_app_update_column,
    meta_ai_assignment_enum,
    meta_ai_model_insert_input,
    meta_ai_model_pk_columns_input,
    meta_ai_model_set_input,
    meta_ai_visibility_enum,
    mutation_root,
    query_root,
)


def get_all_models():
    sess = MetaAISession()
    op = Operation(query_root)
    op.meta_ai_model().__fields__("name", "version", "id", "endpoint")
    data = sess.perform_op(op)
    return (op + data).meta_ai_model


def get_model(id):
    sess = MetaAISession()
    op = Operation(query_root)
    op.meta_ai_model_by_pk(id=id).__fields__("name", "version", "id", "endpoint")
    data = sess.perform_op(op)
    return (op + data).meta_ai_model_by_pk


def add_model(
    name: str,
    description: str = "",
    version: int = 1,
    metadata: str = None,
    endpoint: str = "",
    visibility: meta_ai_visibility_enum = "PRIVATE",
):
    sess = MetaAISession()
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
    data = sess.perform_op(op)
    log.info(f"Created new model: {data}")
    return (op + data).insert_meta_ai_model_one.id


def update_model(id, **kwargs):
    sess = MetaAISession()
    op = Operation(mutation_root)
    op.update_meta_ai_model_by_pk(
        _set=meta_ai_model_set_input(**kwargs), pk_columns=meta_ai_model_pk_columns_input(id=id)
    ).__fields__("name", "version", "id", "endpoint", "description")
    data = sess.perform_op(op)
    return (op + data).update_meta_ai_model_by_pk.id


def delete_model(id):
    sess = MetaAISession()
    op = Operation(mutation_root)
    op.delete_meta_ai_model_by_pk(id=id).__fields__("name", "version", "id", "endpoint")
    data = sess.perform_op(op)
    return (op + data).delete_meta_ai_model_by_pk.id


def get_active_model(app_id, assignment: meta_ai_assignment_enum):
    sess = MetaAISession(app_id=app_id)
    op = Operation(query_root)
    op.meta_ai_app(id=app_id, assigned=assignment, active=True).model.__fields__(
        "name", "version", "id", "endpoint", "description", "active"
    )
    data = sess.perform_op(op)
    try:
        output = (op + data).meta_ai_app.model
        return output
    except AttributeError as e:
        log.info(f"No active model for app_id: {app_id}")


def set_active_model(app_id, model_id):
    sess = MetaAISession(app_id=app_id)
    op = Operation(mutation_root)
    insert_input = meta_ai_app_insert_input(id=app_id, model_id=model_id)
    conflict_handler = meta_ai_app_on_conflict(
        constraint=meta_ai_app_constraint("app_to_model_pkey"), update_columns=["modelId"], where=None
    )
    op.insert_meta_ai_app_one(object=insert_input, on_conflict=conflict_handler).__fields__("id", "model_id")
    data = sess.perform_op(op)
    return (op + data).insert_meta_ai_app_one


def deactivate_app(app_id):
    sess = MetaAISession(app_id=app_id)
    op = Operation(mutation_root)
    op.delete_meta_ai_app_by_pk(id=app_id).__fields__("id")
    data = sess.perform_op(op)
    output = (op + data).delete_meta_ai_app_by_pk.id
    if output == app_id:
        log.info(f"Deactivated model for app_id: {app_id}")
        return output
