import pytest

from superai.apis.meta_ai import AiApiMixin
from superai.apis.meta_ai.session import GraphQlException
from superai.meta_ai.ai_helper import find_root_model


def test_client(ai_client: AiApiMixin):
    models = ai_client.get_all_models()
    assert models is not None


def test_create_child_model(ai_client):
    parent_id = ai_client.add_model(name="model_2", version=1)
    assert parent_id

    model = ai_client.get_model(parent_id)
    assert model
    assert model.name == "model_2"
    assert model.root_id == parent_id

    siblings = ai_client.list_model_versions(parent_id)
    assert len(siblings) == 1

    child_id = ai_client.add_model(name="model_2", version=2, root_id=parent_id)
    assert child_id

    child_model = ai_client.get_model(child_id)
    assert child_model
    assert child_model.name == "model_2"
    assert child_model.root_id == parent_id

    found_root_id = find_root_model(child_model.name, ai_client)
    assert found_root_id == parent_id

    with pytest.raises(GraphQlException):
        child_without_root_id = ai_client.add_model(name="model_3", version=2)

    # Siblings by root model
    siblings_by_root = ai_client.list_model_versions(parent_id, sort_by_version=True)
    assert len(siblings_by_root) == 2
    # Siblings by child model
    siblings_by_child = ai_client.list_model_versions(child_id, sort_by_version=True)
    assert len(siblings_by_child) == 2
    # Assert same order
    for c1, c2 in zip(siblings_by_root, siblings_by_child):
        assert c1.id == c2.id

    # Assert that both return lists have root model as first element
    first_version = siblings_by_root[0]
    assert first_version.id == parent_id

    second_version = siblings_by_root[1]
    assert second_version.id == child_id

    root_model = ai_client.get_root_model(child_id)
    assert root_model.id == siblings_by_root[0].id

    latest_model = ai_client.get_latest_model(parent_id)
    assert latest_model.id == child_id
