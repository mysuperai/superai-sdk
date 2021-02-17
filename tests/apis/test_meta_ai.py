# from superai.apis.meta_ai.meta_ai_schema import meta_ai_app
# from superai.apis.meta_ai import ModelApiMixin, ProjectAiApiMixin
# import uuid
# import pytest

# @pytest.fixture()
# def model_api():
#     yield ModelApiMixin()

# @pytest.fixture()
# def ai_api():
#     yield ProjectAiApiMixin()

# def test_model_creation(model_api):
#     id = uuid.uuid4()
#     a = model_api.add_model(f"TestModel-{id}" )
#     assert a is not None
#     b = model_api.update_model(a, name=f"ChangedTestModel-{id}", version=2)
#     assert a == b
#     c = model_api.delete_model(a)
#     assert a == c


# @pytest.fixture()
# def model(model_api):
#     id = uuid.uuid4()
#     a = model_api.add_model(f"TestModel-{id}")
#     assert a is not None
#     yield a
#     c = model_api.delete_model(a)
#     assert a == c


# def test_model_retrieval(model_api, model):
#     m = model_api.get_model(model)
#     assert "name" in m

#     m = model_api.get_all_models()
#     assert len(m) >= 1

# def test_active_model(model_api:ModelApiMixin, ai_api:ProjectAiApiMixin, model:str ):
#     existing_app_id = uuid.uuid4() # Does only work with real uuid, otherwise no Authorization
#     a = ai_api.update_model(app_id=existing_app_id, assignment="PRELABEL", model_id=model)
#     assert a is not None

#     active_models = ai_api.get_models(existing_app_id,"PRELABEL", active=True)
#     print(active_models)
#     assert a.model_id in [act.model.id for act in active_models]

#     a = ai_api.update_model(app_id=existing_app_id, assignment="PRELABEL", model_id=model, active=False)
#     inactive_models = ai_api.get_models(existing_app_id,"PRELABEL", active=False)
#     print(inactive_models)
#     assert a.model_id in [act.model.id for act in inactive_models]
