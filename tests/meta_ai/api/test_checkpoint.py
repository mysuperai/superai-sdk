import uuid
from pathlib import Path
from unittest.mock import MagicMock

import pytest

from superai.apis.meta_ai.checkpoint import AiCheckpointApiMixin
from superai.apis.meta_ai.meta_ai_graphql_schema import meta_ai_checkpoint
from superai.meta_ai import AI, AICheckpoint

BASE_FIELDS = AiCheckpointApiMixin.BASE_FIELDS
EXTRA_FIELDS = AiCheckpointApiMixin.EXTRA_FIELDS


# Fixture for CheckpointApiMixin
@pytest.fixture
def checkpoint_api_mixin():
    return AiCheckpointApiMixin()


@pytest.fixture(scope="function")
def ai_name():
    """Generate unique name for each test function invocation to prevent collision."""
    return "my_new_super_ai_" + str(uuid.uuid4())[:8]


# Fixture for AI_Template
@pytest.fixture
def template(ai_name):
    model_path = Path(__file__).parent.parent / "fixtures" / "model"
    template = AI(
        name=ai_name,
        model_class="DummyAI",
        model_class_path=str(model_path.absolute()),
        weights_path=model_path / "weights",
    )
    template.id = 1
    yield template


# Fixture for AI_Checkpoint
@pytest.fixture
def checkpoint(template):
    checkpoint = AICheckpoint(template_id=template.id, weights_path="s3://bucket/weights", id="123")
    yield checkpoint


# Test for _fields method
def test_fields(checkpoint_api_mixin):
    verbose_fields = checkpoint_api_mixin._fields(True)
    assert set(verbose_fields) == set(BASE_FIELDS + EXTRA_FIELDS)

    non_verbose_fields = checkpoint_api_mixin._fields(False)
    assert set(non_verbose_fields) == set(BASE_FIELDS)


# Test for _output_formatter method
def test_output_formatter(checkpoint_api_mixin, checkpoint):
    checkpoint_instance = meta_ai_checkpoint(checkpoint.to_dict(only_db_fields=True))

    # Test when to_json is False
    assert checkpoint_api_mixin._output_formatter(checkpoint_instance, False) == checkpoint_instance

    # Test when to_json is True
    formatted_output = checkpoint_api_mixin._output_formatter(checkpoint_instance, True)
    assert isinstance(formatted_output, dict)


# Test for get_all_checkpoints method
def test_get_all_checkpoints(checkpoint_api_mixin, checkpoint):
    checkpoint_api_mixin.ai_session = MagicMock()
    checkpoint_api_mixin.ai_session.perform_op.return_value = {"data": {"meta_ai_checkpoint": []}}
    result = checkpoint_api_mixin.list_all_checkpoints(to_json=False, verbose=False)
    assert result == []

    checkpoint_api_mixin.ai_session.perform_op.return_value = {
        "data": {"meta_ai_checkpoint": [checkpoint.to_dict(only_db_fields=True)]}
    }
    result = checkpoint_api_mixin.list_all_checkpoints(to_json=True, verbose=True)
    assert isinstance(result[0], dict)


# Test for get_checkpoint method
def test_get_checkpoint(checkpoint_api_mixin, checkpoint):
    checkpoint_api_mixin.ai_session = MagicMock()
    checkpoint_api_mixin.ai_session.perform_op.return_value = {
        "data": {"meta_ai_checkpoint_by_pk": checkpoint.to_dict(only_db_fields=True)}
    }
    result = checkpoint_api_mixin.get_checkpoint(checkpoint_id="1", to_json=True)
    assert isinstance(result, dict)


# Test for add_checkpoint method
def test_add_checkpoint(checkpoint_api_mixin, checkpoint):
    checkpoint_api_mixin.ai_session = MagicMock()
    checkpoint_api_mixin.ai_session.perform_op.return_value = {"data": {"insert_meta_ai_checkpoint_one": {"id": "1"}}}
    result = checkpoint_api_mixin.add_checkpoint(checkpoint)
    assert result == "1"


# Test for update_checkpoint method
def test_update_checkpoint(checkpoint_api_mixin, checkpoint):
    checkpoint_api_mixin.ai_session = MagicMock()
    checkpoint_api_mixin.ai_session.perform_op.return_value = {"data": {"update_meta_ai_checkpoint_by_pk": {"id": "1"}}}
    checkpoint.id = "1"
    result = checkpoint_api_mixin.update_checkpoint(checkpoint)
    assert result == "1"


# Test for delete_checkpoint method
def test_delete_checkpoint(checkpoint_api_mixin):
    checkpoint_api_mixin.ai_session = MagicMock()
    checkpoint_api_mixin.ai_session.perform_op.return_value = {"data": {"delete_meta_ai_checkpoint_by_pk": {"id": "1"}}}
    result = checkpoint_api_mixin.delete_checkpoint(checkpoint_id="1")
    assert result == "1"
