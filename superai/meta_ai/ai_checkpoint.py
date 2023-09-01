from __future__ import annotations

import datetime
import os
from enum import Enum
from pathlib import Path
from typing import List, Optional, Union

import attr

from superai.apis.meta_ai.meta_ai_graphql_schema import meta_ai_checkpoint
from superai.config import get_ai_bucket
from superai.log import logger
from superai.meta_ai.ai_helper import upload_dir
from superai.meta_ai.ai_loader import MODEL_ARTIFACT_PREFIX_S3

MODEL_WEIGHT_INFIX_S3 = "saved_models"  # Part of s3 path for model weights

log = logger.get_logger(__name__)


class CheckpointTag(str, Enum):
    LATEST = "LATEST"
    STABLE = "STABLE"
    EXPERIMENTAL = "EXPERIMENTAL"


@attr.define()
class AICheckpoint:
    """Contains data about AI checkpoints.
    Checkpoints are snapshots of the weights of an AI model.
    They are used to save the progress of training and to deploy models.
    """

    template_id: str
    weights_path: str
    id: Optional[str] = None
    metadata: Optional[dict] = {}
    description: Optional[str] = ""
    tag: Optional[CheckpointTag] = CheckpointTag.LATEST
    ai_instance_id: Optional[str] = attr.field(default=None, repr=False)
    _created_at: Optional[datetime.datetime] = None
    _updated_at: Optional[datetime.datetime] = attr.field(default=None, repr=False)
    _parent_version: Optional[str] = attr.field(default=None, repr=False)
    _source_training_id: Optional[str] = attr.field(default=None, repr=False)
    _version: Optional[int] = attr.field(default=None, repr=False)
    _local_path: Optional[Path] = attr.field(default=None, repr=False)
    _client: Optional["Client"] = attr.field(default=None, repr=False)

    @property
    def is_local(self):
        return Path(self.weights_path).exists()

    @property
    def client(self):
        from superai import Client

        if self._client is None:
            self._client = Client.from_credentials()
        return self._client

    @classmethod
    def load(cls, id):
        # Load the checkpoint from the backend data
        from superai import Client

        client = Client.from_credentials()
        backend_data = client.get_checkpoint(id, to_json=True)
        assert backend_data, f"Checkpoint with id {id} not accessible."
        return cls.from_dict(backend_data)

    def save(self, overwrite: bool = False, weights_path: Optional[Union[Path, str]] = None):
        if self.id is None:
            self.id = self.client.add_checkpoint(self)
        else:
            if not overwrite:
                logger.warning("Overwrite disabled, weights will not be uploaded.")

        # Check for weights path
        weights_path = weights_path or self.weights_path
        if Path(weights_path).exists():
            logger.info("Uploading weights...")
            s3_path = self.upload_weights(
                weights_path=weights_path,
            )
            self.client.update_checkpoint(self.id, weights_path=s3_path)
            # In case of local path, save the local path
            self._local_path = Path(weights_path)
            self.weights_path = s3_path
        elif weights_path.startswith("s3"):
            logger.info(f"Weights path {weights_path} is already an s3 path, skipping upload.")
        else:
            raise ValueError(f"Invalid weights path: {weights_path}. Must be either a local path or an s3 path.")

        return self

    def upload_weights(self, weights_path: Optional[str]) -> str:
        """Upload weights to s3 and return the s3 path"""

        if weights_path.startswith("s3"):
            raise ValueError("weights_path must be a local path")

        s3_key = os.path.join(MODEL_ARTIFACT_PREFIX_S3, MODEL_WEIGHT_INFIX_S3, self.id)
        weights_path = Path(weights_path)

        def _upload_weights_to_s3(weights_path: Path) -> str:
            log.info("Uploading weights...")
            bucket = get_ai_bucket()
            upload_dir(weights_path, s3_key, bucket, prefix="/")
            uploaded_weights = f"s3://{os.path.join(bucket, s3_key)}"
            log.info(f"Uploaded weights to '{uploaded_weights}'")
            return uploaded_weights

        if weights_path.exists() and weights_path.is_dir():
            return _upload_weights_to_s3(weights_path)
        else:
            raise ValueError(f"Invalid weights path: {weights_path}. Must be existing directory.")

    def change_description(self, new_description):
        self.description = new_description
        self.client.update_checkpoint(self.id, description=new_description)

    def change_tag(self, new_tag: Optional[Union[CheckpointTag, str]] = None):
        # List available checkpoint tags first
        if new_tag:
            new_tag = CheckpointTag(new_tag)
            self.validate_checkpoint_tag(new_tag)
            self.tag = new_tag.value

            previous_checkpoint = self._find_relative_with_tag(new_tag)
            if previous_checkpoint:
                self._transfer_tag(previous_checkpoint, self)
            else:
                self.client.update_checkpoint(self.id, tag=new_tag.value)
        else:
            # Reset the tag to None
            self.client.update_checkpoint(self.id, tag=None)
            self.tag = None

    def _find_relative_with_tag(self, new_tag) -> Optional["AICheckpoint"]:
        """Find checkpoints with the same tag as the new tag."""
        if self.ai_instance_id:
            checkpoint = self.client.get_checkpoint_for_instance(self.ai_instance_id, tag=new_tag.value)
        else:
            checkpoint = self.client.get_checkpoint_for_template(self.template_id, tag=new_tag.value)
        if checkpoint:
            return AICheckpoint.load(checkpoint.id)

    def validate_checkpoint_tag(self, new_tag: str):
        available_tags = self.client.list_available_checkpoint_tags()
        if new_tag not in available_tags:
            raise ValueError(f"Invalid tag: {new_tag.value}. Available tags: {available_tags}")

    def delete(self):
        self.client.delete_checkpoint(self.id)

    @classmethod
    def load_by_instance_and_tag(cls, ai_instance_id: str, tag: Union[CheckpointTag, str]) -> Optional["AICheckpoint"]:
        from superai import Client

        tag = CheckpointTag(tag)
        client = Client.from_credentials()
        checkpoint = client.get_checkpoint_for_instance(ai_instance_id, tag.value)
        if checkpoint:
            return cls.load(checkpoint.id)

        log.debug(f"No checkpoint found for instance {ai_instance_id} with tag {tag.value}")

    @classmethod
    def get_default_template_checkpoint(cls, template_id: str) -> Optional["AICheckpoint"]:
        from superai import Client

        client = Client.from_credentials()
        ck = client.get_default_checkpoint_for_template(template_id)
        return cls.load(ck.id) if ck else None

    @classmethod
    def list_checkpoints(cls, ai_instance_id: str) -> List["AICheckpoint"]:
        from superai import Client

        client = Client.from_credentials()
        cklist = client.get_checkpoint_for_instance(ai_instance_id, to_json=True, verbose=True)
        return [cls.from_dict(ck) for ck in cklist]

    def create_descendant(self, weights_path: str) -> "AICheckpoint":
        """Create a new checkpoint that is a descendant of this one."""

        descendant = AICheckpoint(
            template_id=self.template_id,
            weights_path=weights_path,
            parent_version=self.id,
            ai_instance_id=self.ai_instance_id,
            tag=None,
        )
        descendant.save()

        if self.tag == CheckpointTag.LATEST:
            self._transfer_tag(self, descendant)
        return descendant

    @classmethod
    def _transfer_tag(
        cls, source: "AICheckpoint", target: "AICheckpoint", new_tag: Optional[Union[CheckpointTag, str]] = None
    ):
        """Method to transfer tag from source to target Checkpoint.
        The database schema only allows one checkpoint to have a tag at a time.
        We need to remove the tag from the source checkpoint before assigning it to the target checkpoint.

        Args:
            source (AICheckpoint): Source checkpoint
            target (AICheckpoint): Target checkpoint
            new_tag (Optional[Union[CheckpointTag, str]], optional): New tag to assign to the target checkpoint.
                Defaults to source tag.
        """
        from superai import Client

        client = Client.from_credentials()
        new_tag = new_tag or source.tag
        new_tag = CheckpointTag(new_tag)

        client.update_checkpoint(source.id, tag=None)
        client.update_checkpoint(target.id, tag=new_tag.value)
        source.tag = None
        target.tag = new_tag

    def create_clone(self, ai_instance_id: str, tag=None) -> "AICheckpoint":
        """Create a new checkpoint that is a clone of this one."""
        clone = AICheckpoint(
            template_id=self.template_id, weights_path=self.weights_path, ai_instance_id=ai_instance_id, tag=tag
        )
        clone.save()
        return clone

    def to_dict(self, only_db_fields=False):
        """Converts the object to a json string."""

        def filter_fn(attr, value):
            name = attr.name
            if name.startswith("_"):
                # Ignore private fields
                return False
            if only_db_fields and name not in meta_ai_checkpoint.__field_names__:
                # Ignore non-db fields
                return False

            return True

        json_data = attr.asdict(self, filter=filter_fn)
        return json_data

    @classmethod
    def from_dict(cls, data: dict):
        """Creates a Checkpoint object from a dict."""
        if "modelv2_id" in data:
            data["ai_instance_id"] = data.pop("modelv2_id")
        return cls(**data)
