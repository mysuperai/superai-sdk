import uuid
from pathlib import Path
from unittest.mock import MagicMock

import pytest

from superai.apis.meta_ai.ai import AiApiMixin
from superai.apis.meta_ai.meta_ai_graphql_schema import meta_ai_template
from superai.meta_ai import AI

BASE_FIELDS = AiApiMixin.BASE_FIELDS
EXTRA_FIELDS = AiApiMixin.EXTRA_FIELDS


# Fixture for TemplateApiMixin
@pytest.fixture
def template_api_mixin():
    return AiApiMixin()


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
    yield template


# Test for _fields method
def test_fields(template_api_mixin):
    verbose_fields = template_api_mixin._fields(True)
    assert set(verbose_fields) == set(BASE_FIELDS + EXTRA_FIELDS)

    non_verbose_fields = template_api_mixin._fields(False)
    assert set(non_verbose_fields) == set(BASE_FIELDS)


# Test for _output_formatter method
def test_output_formatter(template_api_mixin, template):
    template_instance = meta_ai_template(template.to_dict(only_db_fields=True, not_null=True))

    # Test when to_json is False
    assert template_api_mixin._output_formatter(template_instance, False) == template_instance

    # Test when to_json is True
    formatted_output = template_api_mixin._output_formatter(template_instance, True)
    assert isinstance(formatted_output, dict)


# Test for get_all_templates method
def test_get_all_templates(template_api_mixin, template):
    template_api_mixin.ai_session = MagicMock()
    template_api_mixin.ai_session.perform_op.return_value = {"data": {"meta_ai_template": []}}
    result = template_api_mixin.list_ai(to_json=False, verbose=False)
    assert result == []

    template_api_mixin.ai_session.perform_op.return_value = {
        "data": {"meta_ai_template": [template.to_dict(only_db_fields=True, not_null=True)]}
    }
    result = template_api_mixin.list_ai(to_json=True, verbose=True)
    assert isinstance(result[0], dict)


# Test for get_template method
def test_get_template(template_api_mixin, template):
    template_api_mixin.ai_session = MagicMock()
    template_api_mixin.ai_session.perform_op.return_value = {
        "data": {"meta_ai_template_by_pk": template.to_dict(only_db_fields=True, not_null=True)}
    }
    result = template_api_mixin.get_ai(template_id="1", to_json=True)
    assert isinstance(result, dict)


# Test for get_template_by_name method
def test_get_template_by_name(template_api_mixin, template):
    template_api_mixin.ai_session = MagicMock()
    template_api_mixin.ai_session.perform_op.return_value = {
        "data": {"meta_ai_template": [template.to_dict(only_db_fields=True, not_null=True)]}
    }
    result = template_api_mixin.list_ai(name="test_template", to_json=True, verbose=True)
    assert isinstance(result[0], dict)


# Test for get_template_by_name_version method
def test_get_template_by_name_version(template_api_mixin, template):
    template_api_mixin.ai_session = MagicMock()
    template_api_mixin.ai_session.perform_op.return_value = {
        "data": {"meta_ai_template": [template.to_dict(only_db_fields=True, not_null=True)]}
    }
    result = template_api_mixin.list_ai(name="test_template", version="1.0", to_json=True, verbose=True)
    assert isinstance(result[0], dict)


# Test for add_template method
def test_add_template(template_api_mixin, template):
    template_api_mixin.ai_session = MagicMock()
    template_api_mixin.ai_session.perform_op.return_value = {"data": {"insert_meta_ai_template_one": {"id": "1"}}}
    result = template_api_mixin.create_ai(template)
    assert result == "1"


# Test for update_template method
def test_update_template(template_api_mixin, template):
    template_api_mixin.ai_session = MagicMock()
    template_api_mixin.ai_session.perform_op.return_value = {"data": {"update_meta_ai_template_by_pk": {"id": "1"}}}
    template.id = "1"
    result = template_api_mixin.update_ai(template.id, name="test_template", version="1.0")
    assert result == "1"


# Test for delete_template method
def test_delete_template(template_api_mixin):
    template_api_mixin.ai_session = MagicMock()
    template_api_mixin.ai_session.perform_op.return_value = {"data": {"delete_meta_ai_template_by_pk": {"id": "1"}}}
    result = template_api_mixin.delete_ai(template_id="1")
    assert result == "1"
