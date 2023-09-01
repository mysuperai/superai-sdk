from __future__ import annotations

from typing import TYPE_CHECKING, Dict, List, Optional, Union

from sgqlc.operation import Operation

from superai.apis.meta_ai.meta_ai_graphql_schema import (
    meta_ai_checkpoint,
    meta_ai_checkpoint_bool_exp,
    meta_ai_checkpoint_insert_input,
    meta_ai_checkpoint_pk_columns_input,
    meta_ai_checkpoint_set_input,
    meta_ai_checkpoint_tag_enum_comparison_exp,
    mutation_root,
    query_root,
    uuid_comparison_exp,
)
from superai.log import logger

from .base import AiApiBase
from .session import (  # type: ignore
    GraphQlException,
    MetaAISession,
    MetaAIWebsocketSession,
)

if TYPE_CHECKING:
    from superai.meta_ai import AICheckpoint


log = logger.get_logger(__name__)


class AiCheckpointError(Exception):
    """Checkpoint Error"""


class AiCheckpointApiMixin(AiApiBase):
    """Checkpoint API"""

    _resource = "checkpoint"
    BASE_FIELDS = ["id", "tag", "modelv2_id", "template_id", "created_at", "description"]
    EXTRA_FIELDS = [
        "metadata",
        "parent_version",
        "source_training_id",
        "updated_at",
        "version",
        "weights_path",
    ]

    def list_all_checkpoints(
        self, to_json: bool = False, verbose: bool = False
    ) -> List[Union[meta_ai_checkpoint, Dict]]:
        op = Operation(query_root)
        op.meta_ai_checkpoint().__fields__(*AiCheckpointApiMixin._fields(verbose))
        data = self.ai_session.perform_op(op)
        return self._output_formatter((op + data).meta_ai_checkpoint, to_json)

    def get_checkpoint(self, checkpoint_id: str, to_json: bool = False) -> Optional[Union[meta_ai_checkpoint, Dict]]:
        op = Operation(query_root)
        op.meta_ai_checkpoint_by_pk(id=checkpoint_id).__fields__(*AiCheckpointApiMixin._fields(verbose=True))
        data = self.ai_session.perform_op(op)
        mapped: meta_ai_checkpoint = (op + data).meta_ai_checkpoint_by_pk
        return self._output_formatter(mapped, to_json)

    def get_checkpoint_by_version(
        self, version: str, to_json: bool = False, verbose: bool = False
    ) -> List[Union[meta_ai_checkpoint, Dict]]:
        op = Operation(query_root)
        op.meta_ai_checkpoint(where={"version": {"_eq": version}}).__fields__(*AiCheckpointApiMixin._fields(verbose))
        data = self.ai_session.perform_op(op)
        return self._output_formatter((op + data).meta_ai_checkpoint, to_json)

    def get_checkpoint_for_instance(
        self, instance_id: str, tag: str = "LATEST", to_json: bool = False, verbose: bool = False
    ) -> Optional[Union[meta_ai_checkpoint, Dict]]:
        op = Operation(query_root)
        check = meta_ai_checkpoint_bool_exp(
            modelv2_id=uuid_comparison_exp(_eq=instance_id), tag=meta_ai_checkpoint_tag_enum_comparison_exp(_eq=tag)
        )
        op.meta_ai_checkpoint(where=check).__fields__(*AiCheckpointApiMixin._fields(verbose))
        data = self.ai_session.perform_op(op)
        output = self._output_formatter((op + data).meta_ai_checkpoint, to_json)
        if len(output) > 1:
            raise AiCheckpointError(f"More than one checkpoint found for instance {instance_id} with tag {tag}")
        return output[0] if output else None

    def get_checkpoint_for_template(
        self, template_id: str, tag: str = "LATEST", to_json: bool = False, verbose: bool = False
    ) -> Optional[Union[meta_ai_checkpoint, Dict]]:
        op = Operation(query_root)
        check = meta_ai_checkpoint_bool_exp(
            template_id=uuid_comparison_exp(_eq=template_id),
            tag=meta_ai_checkpoint_tag_enum_comparison_exp(_eq=tag),
            modelv2_id=uuid_comparison_exp(_is_null=True),
        )
        op.meta_ai_checkpoint(where=check).__fields__(*AiCheckpointApiMixin._fields(verbose))
        data = self.ai_session.perform_op(op)
        output = self._output_formatter((op + data).meta_ai_checkpoint, to_json)
        if len(output) > 1:
            raise AiCheckpointError(f"More than one checkpoint found for template {template_id} with tag {tag}")
        return output[0] if output else None

    def list_checkpoints_for_instance(
        self, instance_id: str, with_tag=False, to_json: bool = False, verbose: bool = False
    ) -> List[Union[meta_ai_checkpoint, Dict]]:
        op = Operation(query_root)
        check = meta_ai_checkpoint_bool_exp(
            modelv2_id=uuid_comparison_exp(_eq=instance_id),
            tag=meta_ai_checkpoint_tag_enum_comparison_exp(_is_null=not with_tag),
        )
        op.meta_ai_checkpoint(where=check).__fields__(*AiCheckpointApiMixin._fields(verbose))
        data = self.ai_session.perform_op(op)
        return self._output_formatter((op + data).meta_ai_checkpoint, to_json)

    def get_default_checkpoint_for_template(
        self, template_id: str, to_json: bool = False
    ) -> Optional[Union[meta_ai_checkpoint, Dict]]:
        op = Operation(query_root)
        op.meta_ai_template_by_pk(id=template_id).default_checkpoint()
        data = self.ai_session.perform_op(op)
        mapped = (op + data).meta_ai_template_by_pk
        if mapped and mapped.default_checkpoint:
            return self.get_checkpoint(mapped.default_checkpoint, to_json)
        else:
            return None

    def list_checkpoints_for_template(
        self, template_id: str, with_tag=False, to_json: bool = False, verbose: bool = False
    ) -> List[Union[meta_ai_checkpoint, Dict]]:
        op = Operation(query_root)
        check = meta_ai_checkpoint_bool_exp(
            template_id=uuid_comparison_exp(_eq=template_id),
            tag=meta_ai_checkpoint_tag_enum_comparison_exp(_is_null=not with_tag),
        )
        op.meta_ai_checkpoint(where=check).__fields__(*AiCheckpointApiMixin._fields(verbose))
        data = self.ai_session.perform_op(op)
        return self._output_formatter((op + data).meta_ai_checkpoint, to_json)

    def add_checkpoint(self, checkpoint: AICheckpoint) -> str:
        op = Operation(mutation_root)

        # Translate enum to string if needed
        from superai.meta_ai.ai_checkpoint import CheckpointTag

        tag = CheckpointTag(checkpoint.tag).value if checkpoint.tag else None

        op.insert_meta_ai_checkpoint_one(
            object=meta_ai_checkpoint_insert_input(
                template_id=checkpoint.template_id,
                weights_path=checkpoint.weights_path,
                metadata=checkpoint.metadata,
                description=checkpoint.description,
                tag=tag,
                modelv2_id=checkpoint.ai_instance_id,
            )
        ).__fields__("id")
        data = self.ai_session.perform_op(op)
        log.info(f"Created new checkpoint: {data}")
        return (op + data).insert_meta_ai_checkpoint_one.id

    def update_checkpoint(self, checkpoint_id: str, **fields) -> str:
        op = Operation(mutation_root)

        # Translate ai_instance_id to modelv2_id
        if "ai_instance_id" in fields:
            fields["modelv2_id"] = fields.pop("ai_instance_id")

        op.update_meta_ai_checkpoint_by_pk(
            _set=meta_ai_checkpoint_set_input(**fields),
            pk_columns=meta_ai_checkpoint_pk_columns_input(id=checkpoint_id),
        ).__fields__("id")
        data = self.ai_session.perform_op(op)
        return (op + data).update_meta_ai_checkpoint_by_pk.id

    def delete_checkpoint(self, checkpoint_id: str) -> str:
        op = Operation(mutation_root)
        op.delete_meta_ai_checkpoint_by_pk(id=checkpoint_id).__fields__("id")
        data = self.ai_session.perform_op(op)
        return (op + data).delete_meta_ai_checkpoint_by_pk.id

    def list_available_checkpoint_tags(self) -> List[str]:
        op = Operation(query_root)
        op.meta_ai_checkpoint_tag().__fields__("tag")
        data = self.ai_session.perform_op(op)
        output = (op + data).meta_ai_checkpoint_tag
        return [o.tag for o in output]
