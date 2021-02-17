from abc import ABC
from sgqlc.operation import Operation, ArgDict
from sgqlc.types import Arg
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
    meta_ai_app_bool_exp,
    meta_ai_assignment_bool_exp,
    String_comparison_exp,
    Boolean,
    Boolean_comparison_exp,
    mutation_root,
    uuid_comparison_exp,
    query_root,
)


class ProjectAiApiMixin(ABC):
    _resource = "project_ai"

    @property
    def resource(self):
        return self._resource

    def get_models(self, app_id: str, assignment: str = None, active=None):
        sess = MetaAISession(app_id=app_id)
        op = Operation(query_root)
        check = meta_ai_app_bool_exp(
            active=Boolean_comparison_exp(_eq=active),
            id=uuid_comparison_exp(_eq=app_id),
            assignment=meta_ai_assignment_bool_exp(type=String_comparison_exp(_eq=assignment)),
        )
        models = op.meta_ai_app(where=check).model
        models.id()
        models.name()
        data = sess.perform_op(op)
        try:
            output = (op + data).meta_ai_app
            return output
        except AttributeError as e:
            log.info(f"No models for project with id: {app_id} and assigment type {assignment}")

    def update_model(self, app_id: str, assignment: meta_ai_assignment_enum, model_id: str, active: bool = None):
        sess = MetaAISession(app_id=app_id)
        op = Operation(mutation_root)
        input_args = {"id": app_id, "model_id": model_id, "assigned": assignment}
        if active is not None:
            input_args["active"] = active
        insert_input = meta_ai_app_insert_input(input_args)
        conflict_handler = meta_ai_app_on_conflict(
            constraint=meta_ai_app_constraint("app_modelId_id_assigned_key"),
            update_columns=["modelId", "active"],
            where=None,
        )
        op.insert_meta_ai_app_one(object=insert_input, on_conflict=conflict_handler).__fields__(
            "id", "model_id", "assigned", "active"
        )
        data = sess.perform_op(op)
        print(data)
        return (op + data).insert_meta_ai_app_one
