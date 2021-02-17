# from superai.apis.meta_ai import ModelApiMixin, ProjectAiApiMixin
# import uuid
# import pytest


# @pytest.fixture()
# def model_api():
#     yield ModelApiMixin()


# @pytest.fixture()
# def ai_api():
#     yield ProjectAiApiMixin()


# @pytest.fixture()
# def existing_app_id():
#     return "" # Requires actual existing app_id, not committed to Repo


# def test_model_creation(model_api):
#     id = uuid.uuid4()
#     a = model_api.add_model(f"TestModel-{id}")
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


# @pytest.fixture()
# def prediction_id(ai_api, existing_app_id, model):
#     test_output = {"score": 1.0, "mask": [0, 1, 1, 0]}
#     prediction_id = ai_api.submit_prelabel(test_output, existing_app_id, 1, model, assignment="PRELABEL")
#     yield prediction_id
#     deleted = ai_api.delete_prelabel(existing_app_id, prediction_id)
#     assert deleted == prediction_id


# def test_model_retrieval(model_api, model):
#     m = model_api.get_model(model)
#     assert "name" in m

#     m = model_api.get_all_models()
#     assert len(m) >= 1


# def test_active_model(ai_api: ProjectAiApiMixin, model: str, existing_app_id):
#     a = ai_api.update_model(app_id=existing_app_id, assignment="PRELABEL", model_id=model)
#     assert a is not None

#     active_models = ai_api.get_models(existing_app_id, "PRELABEL", active=True)
#     assert a.model_id in [act.model.id for act in active_models]

#     a = ai_api.update_model(app_id=existing_app_id, assignment="PRELABEL", model_id=model, active=False)
#     inactive_models = ai_api.get_models(existing_app_id, "PRELABEL", active=False)
#     assert a.model_id in [act.model.id for act in inactive_models]


# def test_view_prelabel(ai_api, existing_app_id, prediction_id):
#     prelabels = ai_api.list_prelabel_instances(existing_app_id, prediction_id)
#     instance_id = prelabels[0].id
#     instance = ai_api.view_prelabel(existing_app_id, prediction_id, instance_id)
#     assert instance is not None


# def test_submit_prelabel(ai_api: ProjectAiApiMixin, model: str, existing_app_id):
#     test_output = {"score": 1.0, "mask": [0, 1, 1, 0]}
#     prediction_id = ai_api.submit_prelabel(test_output, existing_app_id, 1, model, assignment="PRELABEL")
#     assert prediction_id is not None

#     test_output = [
#         {"score": 1.0, "mask": [0, 1, 1, 0]},
#         {"mask": [0, 1, 1, 0]},
#     ]

#     prediction_id = ai_api.submit_prelabel(test_output, existing_app_id, 2, model, assignment="PRELABEL")
#     assert prediction_id is not None
#     prelabels = ai_api.list_prelabel_instances(existing_app_id, prediction_id)
#     assert len(prelabels) == len(test_output)
