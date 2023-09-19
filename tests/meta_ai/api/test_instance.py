import uuid
from pathlib import Path
from unittest.mock import MagicMock

import pytest

from superai.apis.meta_ai.instance import AiInstanceApiMixin
from superai.apis.meta_ai.meta_ai_graphql_schema import meta_ai_modelv2
from superai.meta_ai import AI, AIInstance

BASE_FIELDS = AiInstanceApiMixin.BASE_FIELDS
EXTRA_FIELDS = AiInstanceApiMixin.EXTRA_FIELDS


# Fixture for TemplateApiMixin
@pytest.fixture
def instance_api_mixin():
    return AiInstanceApiMixin()


@pytest.fixture(scope="function")
def ai_name():
    """Generate unique name for each test function invocation to prevent collision."""
    return "my_new_super_ai_" + str(uuid.uuid4())[:8]


@pytest.fixture
def template(ai_name):
    model_path = Path(__file__).parent.parent / "fixtures" / "model"
    template = AI(
        name=ai_name,
        model_class="DummyAI",
        model_class_path=str(model_path.absolute()),
        weights_path=model_path / "weights",
    )
    template.id = "1"
    yield template


# Fixture for AI_Template
@pytest.fixture
def instance(template):
    instance = AIInstance(template_id=template.id, name="my_" + template.name)
    yield instance


# Test for _fields method
def test_fields(instance_api_mixin):
    verbose_fields = instance_api_mixin._fields(True)
    assert set(verbose_fields) == set(BASE_FIELDS + EXTRA_FIELDS)

    non_verbose_fields = instance_api_mixin._fields(False)
    assert set(non_verbose_fields) == set(BASE_FIELDS)


# Test for _output_formatter method
def test_output_formatter(instance_api_mixin, instance):
    instance_instance = meta_ai_modelv2(instance.to_dict(only_db_fields=True, exclude_none=True))

    # Test when to_json is False
    assert instance_api_mixin._output_formatter(instance_instance, False) == instance_instance

    # Test when to_json is True
    formatted_output = instance_api_mixin._output_formatter(instance_instance, True)
    assert isinstance(formatted_output, dict)


# Test for get_all_instances method
def test_get_all_instances(instance_api_mixin, instance):
    instance_api_mixin.ai_session = MagicMock()
    instance_api_mixin.ai_session.perform_op.return_value = {"data": {"meta_ai_modelv2": []}}
    result = instance_api_mixin.list_ai_instances(to_json=False, verbose=False)
    assert result == []

    instance_api_mixin.ai_session.perform_op.return_value = {
        "data": {"meta_ai_modelv2": [instance.to_dict(only_db_fields=True, exclude_none=True)]}
    }
    result = instance_api_mixin.list_ai_instances(to_json=True, verbose=True)
    assert isinstance(result[0], dict)


# Test for get_instance method
def test_get_instance(instance_api_mixin, instance):
    instance_api_mixin.ai_session = MagicMock()
    instance_dict = instance.to_dict(only_db_fields=True, exclude_none=True)

    instance_api_mixin.ai_session.perform_op.return_value = {"data": {"meta_ai_modelv2_by_pk": instance_dict}}
    result = instance_api_mixin.get_ai_instance(instance_id="1", to_json=True)
    assert isinstance(result, dict)

    instance_dict["checkpoint"] = {"id": "1", "tag": "LATEST", "source_training_id": "1", "weights_path": "1"}
    instance_dict["checkpoint"]["training_instance"] = {"id": "1", "state": "FINISHED", "dataset_id": "1"}
    instance_api_mixin.ai_session.perform_op.return_value = {"data": {"meta_ai_modelv2_by_pk": instance_dict}}
    result2 = instance_api_mixin.get_ai_instance(instance_id="1", to_json=False, view_checkpoint=True)
    assert result2.checkpoint


# Test for get_instance_by_name method
def test_get_instance_by_name(instance_api_mixin, instance):
    instance_api_mixin.ai_session = MagicMock()
    instance_api_mixin.ai_session.perform_op.return_value = {
        "data": {"meta_ai_modelv2": [instance.to_dict(only_db_fields=True, exclude_none=True)]}
    }
    result = instance_api_mixin.get_ai_instance_by_name(name=instance.name, to_json=True)
    assert isinstance(result, dict)


def test_list_ai_instances(instance_api_mixin, instance):
    # Initialize the mocked session
    instance_api_mixin.ai_session = MagicMock()

    # Check with all arguments as None
    instance_api_mixin.ai_session.perform_op.return_value = {
        "data": {"meta_ai_modelv2": [instance.to_dict(only_db_fields=True, exclude_none=True)]}
    }
    result = instance_api_mixin.list_ai_instances(to_json=True, verbose=True)
    assert isinstance(result[0], dict)

    # Check when name is provided
    instance_api_mixin.list_ai_instances(name="test")
    instance_api_mixin.ai_session.perform_op.assert_called()  # Check if perform_op was called

    # Check when ai_name is provided
    instance_api_mixin.list_ai_instances(ai_name="test")
    instance_api_mixin.ai_session.perform_op.assert_called()  # Check if perform_op was called

    # Check when ai_version is provided
    instance_api_mixin.list_ai_instances(ai_version="1.0")
    instance_api_mixin.ai_session.perform_op.assert_called()  # Check if perform_op was called

    # Check when visibility is provided
    instance_api_mixin.list_ai_instances(visibility="PUBLIC")
    instance_api_mixin.ai_session.perform_op.assert_called()  # Check if perform_op was called

    # Check when checkpoint_tag is provided
    instance_api_mixin.list_ai_instances(checkpoint_tag="LATEST")
    instance_api_mixin.ai_session.perform_op.assert_called()  # Check if perform_op was called

    # Check when to_json is False
    result = instance_api_mixin.list_ai_instances(to_json=False)
    assert isinstance(result[0], meta_ai_modelv2) or isinstance(result[0], dict)

    # Check when verbose is False
    result = instance_api_mixin.list_ai_instances(to_json=True, verbose=False)
    assert isinstance(result[0], dict)


# Test for add_instance method
def test_add_instance(instance_api_mixin, instance):
    instance_api_mixin.ai_session = MagicMock()
    instance_api_mixin.ai_session.perform_op.return_value = {"data": {"insert_meta_ai_modelv2_one": {"id": "1"}}}
    result = instance_api_mixin.create_ai_instance(instance)
    assert result == "1"


# Test for update_instance method
def test_update_instance(instance_api_mixin, instance):
    instance_api_mixin.ai_session = MagicMock()
    instance_api_mixin.ai_session.perform_op.return_value = {"data": {"update_meta_ai_modelv2_by_pk": {"id": "1"}}}
    instance.id = "1"
    result = instance_api_mixin.update_ai_instance(instance)
    assert result == "1"


# Test for delete_instance method
def test_delete_instance(instance_api_mixin):
    instance_api_mixin.ai_session = MagicMock()
    instance_api_mixin.ai_session.perform_op.return_value = {"data": {"delete_meta_ai_modelv2_by_pk": {"id": "1"}}}
    result = instance_api_mixin.delete_ai_instance(instance_id="1")
    assert result == "1"
