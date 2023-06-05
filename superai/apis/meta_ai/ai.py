from __future__ import annotations

from typing import TYPE_CHECKING, Dict, List, Optional, Union

from sgqlc.operation import Operation

from superai.apis.meta_ai.meta_ai_graphql_schema import (
    meta_ai_template,
    meta_ai_template_insert_input,
    meta_ai_template_pk_columns_input,
    meta_ai_template_set_input,
    mutation_root,
    query_root,
)
from superai.log import logger

from .base import AiApiBase
from .session import (  # type: ignore
    GraphQlException,
    MetaAISession,
    MetaAIWebsocketSession,
)

if TYPE_CHECKING:
    from superai.meta_ai import AI
log = logger.get_logger(__name__)


class AiTemplateError(Exception):
    """Template Error"""


class AiApiMixin(AiApiBase):
    """AI API"""

    _resource = "ai"
    BASE_FIELDS = ["name", "version", "id", "trainable", "visibility"]
    EXTRA_FIELDS = [
        "created_at",
        "default_checkpoint",
        "default_training_parameters",
        "default_deployment_parameters",
        "description",
        "image",
        "input_schema",
        "model_save_path",
        # "organisation_id",
        "output_schema",
        # "owner_id",
        "updated_at",
    ]

    def list_ai(self, to_json: bool = False, verbose: bool = False) -> List[Union[meta_ai_template, Dict]]:
        op = Operation(query_root)
        op.meta_ai_template().__fields__(*AiApiMixin._fields(verbose))
        data = self.sess.perform_op(op)
        return self._output_formatter((op + data).meta_ai_template, to_json)

    def get_ai(self, template_id: str, to_json: bool = False) -> Optional[Union[meta_ai_template, Dict]]:
        op = Operation(query_root)
        op.meta_ai_template_by_pk(id=template_id).__fields__(*AiApiMixin._fields(verbose=True))
        data = self.sess.perform_op(op)
        return self._output_formatter((op + data).meta_ai_template_by_pk, to_json)

    def list_ai_by_name(
        self, name: str, to_json: bool = False, verbose: bool = False
    ) -> List[Union[meta_ai_template, Dict]]:
        op = Operation(query_root)
        op.meta_ai_template(where={"name": {"_eq": name}}).__fields__(*AiApiMixin._fields(verbose))
        data = self.sess.perform_op(op)
        return self._output_formatter((op + data).meta_ai_template, to_json)

    def list_ai_by_name_version(
        self, name: str, version: str, owner_id: int = None, to_json: bool = False, verbose: bool = False
    ) -> List[Union[meta_ai_template, Dict]]:
        """
        List all ai templates by name and version and optionally owner_id
        """
        op = Operation(query_root)
        where = {"name": {"_eq": name}, "version": {"_eq": version}}

        if owner_id:
            where["owner_id"] = {"_eq": owner_id}

        op.meta_ai_template(where=where).__fields__(*AiApiMixin._fields(verbose))
        data = self.sess.perform_op(op)
        return self._output_formatter((op + data).meta_ai_template, to_json)

    def list_ai(self, to_json: bool = False, verbose: bool = False) -> List[Union[meta_ai_template, Dict]]:
        op = Operation(query_root)
        op.meta_ai_template().__fields__(*AiApiMixin._fields(verbose))
        data = self.sess.perform_op(op)
        return self._output_formatter((op + data).meta_ai_template, to_json)

    def create_ai(self, template: AI) -> str:
        op = Operation(mutation_root)
        template_dict = template.to_dict(only_db_fields=True)
        template_dict.pop("id", None)
        op.insert_meta_ai_template_one(object=meta_ai_template_insert_input(**template_dict)).__fields__("id")
        data = self.sess.perform_op(op)
        log.info(f"Created new template: {data}")
        return (op + data).insert_meta_ai_template_one.id

    def update_ai(self, template_id: str, **fields) -> str:
        op = Operation(mutation_root)
        op.update_meta_ai_template_by_pk(
            _set=meta_ai_template_set_input(**fields),
            pk_columns=meta_ai_template_pk_columns_input(id=template_id),
        ).__fields__("id")
        data = self.sess.perform_op(op)
        return (op + data).update_meta_ai_template_by_pk.id

    def update_ai_by_object(self, template: AI) -> str:
        op = Operation(mutation_root)
        template_dict = template.to_dict(only_db_fields=True, not_null=True)
        template_dict.pop("id", None)
        op.update_meta_ai_template_by_pk(
            _set=meta_ai_template_set_input(**template_dict),
            pk_columns=meta_ai_template_pk_columns_input(id=template.id),
        ).__fields__("id")
        data = self.sess.perform_op(op)
        return (op + data).update_meta_ai_template_by_pk.id

    def delete_ai(self, template_id: str) -> str:
        op = Operation(mutation_root)
        op.delete_meta_ai_template_by_pk(id=template_id).__fields__("id")
        data = self.sess.perform_op(op)
        return (op + data).delete_meta_ai_template_by_pk.id
