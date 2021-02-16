from superai.apis.meta_ai import ModelApiMixin
import uuid
import pytest


@pytest.fixture()
def api():
    yield ModelApiMixin()

def test_model_creation(api):
    id = uuid.uuid4()
    a = api.add_model(f"TestModel-{id}" )
    assert a is not None
    b = api.update_model(a, name=f"ChangedTestModel-{id}", version=2)
    assert a == b
    c = api.delete_model(a)
    assert a == c


@pytest.fixture()
def model(api):
    id = uuid.uuid4()
    a = api.add_model(f"TestModel-{id}")
    assert a is not None
    yield a
    c = api.delete_model(a)
    assert a == c


def test_model_retrieval(api, model):
    m = api.get_model(model)
    assert "name" in m

    m = api.get_all_models()
    assert len(m) >= 1