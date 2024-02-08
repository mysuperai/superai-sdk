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
        "organization_id",
        "output_schema",
        "owner_id",
        "updated_at",
    ]

    # Updated _build_query to support all parameters
    def _build_ai_template_query(
        self,
        name: Optional[str] = None,
        version: Optional[str] = None,
        owner_id: Optional[int] = None,
        organization_id: Optional[int] = None,
        fuzzy: bool = True,
    ) -> Dict:
        """Build filter query for listing AIs."""
        comparison = "_ilike" if fuzzy else "_eq"
        if fuzzy:
            # Add wildcards to the name and version
            name = f"%{name}%" if name else None
            version = f"%{version}%" if version else None
        where = {}
        if name:
            where["name"] = {comparison: name}
        if version:
            where["version"] = {comparison: version}
        if owner_id:
            where["owner_id"] = {"_eq": owner_id}
        if organization_id:
            where["organization_id"] = {"_eq": organization_id}
        return where

    def list_ai(
        self,
        name: Optional[str] = None,
        version: Optional[str] = None,
        owner_id: Optional[int] = None,
        organization_id: Optional[int] = None,
        to_json: bool = False,
        verbose: bool = False,
        fuzzy: bool = False,
    ) -> List[Union[meta_ai_template, Dict]]:
        """List AI templates, filtered by optional parameters."""
        where = self._build_ai_template_query(
            name=name, version=version, owner_id=owner_id, organization_id=organization_id, fuzzy=fuzzy
        )
        return self._perform_ai_template_query(where, to_json, verbose)

    def _perform_ai_template_query(
        self, where: Dict, to_json: bool, verbose: bool
    ) -> List[Union[meta_ai_template, Dict]]:
        op = Operation(query_root)
        op.meta_ai_template(where=where).__fields__(*AiApiMixin._fields(verbose))
        data = self.ai_session.perform_op(op)
        return self._output_formatter((op + data).meta_ai_template, to_json)

    def get_ai(self, template_id: str, to_json: bool = False) -> Optional[Union[meta_ai_template, Dict]]:
        op = Operation(query_root)
        op.meta_ai_template_by_pk(id=template_id).__fields__(*AiApiMixin._fields(verbose=True))
        data = self.ai_session.perform_op(op)
        return self._output_formatter((op + data).meta_ai_template_by_pk, to_json)

    def create_ai(self, template: AI) -> str:
        op = Operation(mutation_root)
        template_dict = template.to_dict(only_db_fields=True)
        template_dict = self.__filter_inferred_fields(template_dict)
        op.insert_meta_ai_template_one(object=meta_ai_template_insert_input(**template_dict)).__fields__("id")
        data = self.ai_session.perform_op(op)
        log.info(f"Created new template: {data}")
        return (op + data).insert_meta_ai_template_one.id

    def __filter_inferred_fields(self, template_dict):
        """Filter fields that are handled by the backend"""
        template_dict.pop("id", None)
        # Ownership IDs are inferred from the session tokens in the backend
        template_dict.pop("owner_id", None)
        template_dict.pop("organization_id", None)
        return template_dict

    def update_ai(self, template_id: str, **fields) -> str:
        op = Operation(mutation_root)
        op.update_meta_ai_template_by_pk(
            _set=meta_ai_template_set_input(**fields),
            pk_columns=meta_ai_template_pk_columns_input(id=template_id),
        ).__fields__("id")
        data = self.ai_session.perform_op(op)
        return (op + data).update_meta_ai_template_by_pk.id

    def update_ai_by_object(self, template: AI) -> str:
        op = Operation(mutation_root)
        template_dict = template.to_dict(only_db_fields=True, not_null=True)
        template_dict = self.__filter_inferred_fields(template_dict)
        op.update_meta_ai_template_by_pk(
            _set=meta_ai_template_set_input(**template_dict),
            pk_columns=meta_ai_template_pk_columns_input(id=template.id),
        ).__fields__("id")
        data = self.ai_session.perform_op(op)
        return (op + data).update_meta_ai_template_by_pk.id

    def delete_ai(self, template_id: str) -> str:
        op = Operation(mutation_root)
        op.delete_meta_ai_template_by_pk(id=template_id).__fields__("id")
        data = self.ai_session.perform_op(op)
        return (op + data).delete_meta_ai_template_by_pk.id
