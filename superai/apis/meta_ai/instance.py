from __future__ import annotations

from typing import TYPE_CHECKING, Dict, List, Optional, Union

from sgqlc.operation import Operation

from superai.apis.meta_ai.meta_ai_graphql_schema import (
    meta_ai_modelv2,
    meta_ai_modelv2_pk_columns_input,
    meta_ai_modelv2_set_input,
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
    from superai.meta_ai import AIInstance

log = logger.get_logger(__name__)


class AiInstanceApiMixin(AiApiBase):
    """Instance API"""

    _resource = "aiInstance"
    BASE_FIELDS = ["name", "id", "template_id", "checkpoint_tag", "visibility"]
    EXTRA_FIELDS = [
        "created_at",
        "description",
        "editor_id",
        "owner_id",
        "organisation_id",
        "updated_at",
        "deployment_parameters",
        "ai_worker_id",
        "ai_worker_username",
        "served_by",
    ]

    def list_ai_instances(
        self,
        to_json: bool = False,
        name: Optional[str] = None,
        ai_name: Optional[str] = None,
        ai_version: Optional[str] = None,
        visibility: Optional[str] = None,
        checkpoint_tag=Optional[str],
        verbose: bool = True,
    ) -> List[Union[meta_ai_modelv2, Dict]]:
        op = Operation(query_root)
        where = {}
        if name:
            where["name"] = {"_ilike": f"%{name}%"}
        if ai_name:
            where["template"] = {"name": {"_ilike": f"%{ai_name}%"}}
        if ai_version:
            where["template"] = {"version": {"_ilike": f"%{ai_version}%"}}
        if visibility:
            where["visibility"] = {"_eq": visibility}
        if checkpoint_tag:
            where["checkpoint_tag"] = {"_eq": checkpoint_tag}

        instance = op.meta_ai_modelv2(where=where)
        instance.__fields__(*AiInstanceApiMixin._fields(verbose))
        instance.template.__fields__("name", "version", "visibility")

        data = self.sess.perform_op(op)
        return self._output_formatter((op + data).meta_ai_modelv2, to_json)

    def get_ai_instance_by_name(
        self, name: str, template_id: Optional[str] = None, to_json: bool = False
    ) -> Optional[Union[meta_ai_modelv2, Dict]]:
        """
        Get AI instance by name and template_id
        Args:
            name: name of the instance
            template_id: template_id of the instance
            to_json: return json

        Returns:

        """
        op = Operation(query_root)
        fields = AiInstanceApiMixin._fields(True)
        where = {"name": {"_eq": name}}
        if template_id:
            where["template_id"] = {"_eq": template_id}
        op.meta_ai_modelv2(where=where).__fields__(*fields)
        data = self.sess.perform_op(op)
        instance = self._output_formatter((op + data).meta_ai_modelv2, to_json)
        return instance[0] if instance else None

    def get_ai_instance(self, instance_id: str, to_json: bool = False) -> Optional[Union[meta_ai_modelv2, Dict]]:
        op = Operation(query_root)
        fields = AiInstanceApiMixin._fields(True)
        op.meta_ai_modelv2_by_pk(id=instance_id).__fields__(*fields)
        data = self.sess.perform_op(op)
        instance = self._output_formatter((op + data).meta_ai_modelv2_by_pk, to_json)
        return instance if instance else None

    def get_ai_instance_by_template_version(
        self,
        name: str,
        version: str,
        owner_id: Optional[int] = None,
        visibility: str = "PRIVATE",
        to_json: bool = False,
    ) -> Optional[Union[meta_ai_modelv2, Dict]]:
        op = Operation(query_root)
        fields = AiInstanceApiMixin._fields(True)

        where = {
            "template": {"version": {"_eq": version}},
            "name": {"_eq": name},
            "visibility": {"_eq": visibility},
        }
        if owner_id:
            where["ownerId"] = {"_eq": owner_id}

        op.meta_ai_modelv2(where=where).__fields__(*fields)
        data = self.sess.perform_op(op)
        instance = self._output_formatter((op + data).meta_ai_modelv2, to_json)
        return instance[0] if instance else None

    def create_ai_instance(self, instance: AIInstance) -> str:
        op = Operation(mutation_root)
        op.insert_meta_ai_modelv2_one(object=instance.to_dict(exclude_none=True, only_db_fields=True)).__fields__("id")
        data = self.sess.perform_op(op)
        log.info(f"Created new instance: {data}")
        return (op + data).insert_meta_ai_modelv2_one.id

    def update_ai_instance(self, instance_id: str, **fields) -> str:
        op = Operation(mutation_root)

        if "checkpoint_tag" in fields:
            tag = fields["checkpoint_tag"]
            from ...meta_ai.ai_checkpoint import CheckpointTag

            if isinstance(tag, CheckpointTag):
                fields["checkpoint_tag"] = tag.value

        op.update_meta_ai_modelv2_by_pk(
            _set=meta_ai_modelv2_set_input(**fields),
            pk_columns=meta_ai_modelv2_pk_columns_input(id=instance_id),
        ).__fields__("id")
        data = self.sess.perform_op(op)
        return (op + data).update_meta_ai_modelv2_by_pk.id

    def delete_ai_instance(self, instance_id: str) -> str:
        op = Operation(mutation_root)
        op.delete_meta_ai_modelv2_by_pk(id=instance_id).__fields__("id")
        data = self.sess.perform_op(op)
        return (op + data).delete_meta_ai_modelv2_by_pk.id
