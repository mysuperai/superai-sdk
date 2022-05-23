import ast
import pathlib

import pytest
import vcr  # type: ignore

import superai.apis.meta_ai.model
from superai import Client
from superai.apis.meta_ai import ProjectAiApiMixin

# To record new cassette, use real app_id and run pytest against running endpoint
from superai.apis.meta_ai.meta_ai_graphql_schema import (
    meta_ai_instance,
    meta_ai_prediction,
)

APP_ID = "1e266751-4f5e-4bdd-9709-c381c72ded6d"


def scrub_string(string, replacement=""):
    def before_record_response(response):
        response = str(response).replace(string, replacement)
        response = ast.literal_eval(response)
        return response

    return before_record_response


def before_record_cb(request):
    request.body = scrub_string(APP_ID, "FAKE_APP_ID")(request.body)
    return request


@pytest.fixture(scope="module")
def my_vcr():
    return vcr.VCR(
        serializer="yaml",
        cassette_library_dir=f"{pathlib.Path(__file__).resolve().parent}/cassettes",
        record_mode="new",
        match_on=["body", "headers", "method", "host", "path", "query"],
        filter_headers=["x-api-key", "x-app-id", "Content-Length", "User-Agent"],
        before_record_response=scrub_string(APP_ID, "FAKE_APP_ID"),
        before_record_request=before_record_cb,
        decode_compressed_response=True,
    )


@pytest.fixture(scope="module")
def model_api(my_vcr) -> Client:
    with my_vcr.use_cassette("model_api.yaml"):
        yield Client()


@pytest.fixture(scope="function")
def existing_app_id():
    return APP_ID


@pytest.fixture(scope="function")
def model(model_api):
    a = model_api.add_model(f"TestModel")
    assert a is not None
    yield a
    c = model_api.delete_model(a)
    assert a == c


def test_model(model_api, model):

    m = model_api.get_model_by_name("TestModel")
    assert "name" in m[0]
    assert m[0]["name"] == "TestModel"

    m = model_api.get_model(model)
    assert "name" in m

    m = model_api.get_all_models()
    assert len(m) >= 1

    new_name = "ChangedTestModel"
    b = model_api.update_model(model, name=new_name)
    assert model == b
    assert new_name == model_api.get_model(model).name


@pytest.fixture()
def prediction_id(model_api, existing_app_id, model):
    test_output = {"score": 1.0, "mask": [0, 1, 1, 0]}
    prediction_id = model_api.submit_prelabel(test_output, existing_app_id, 1, model, assignment="PRELABEL")

    yield prediction_id

    # Teardown
    deleted = model_api.delete_prelabel(existing_app_id, prediction_id)
    assert deleted == prediction_id


def test_view_prediction(model_api, existing_app_id, prediction_id):
    object: meta_ai_prediction = model_api.view_prediction(app_id=existing_app_id, prediction_id=prediction_id)
    assert "id" in object
    assert "state" in object


def test_get_prediction(model_api: Client, prediction_id):
    p = model_api.get_prediction_with_data(prediction_id=prediction_id)
    assert p.created_at is not None
    assert p.started_at is None
    assert p.error_message is None


def test_request_prediction_of_job(model_api, existing_app_id):
    with pytest.raises(Exception):
        ids = model_api.request_prediction_of_job(app_id=existing_app_id, job_id=1, assignment="PRELABEL")


def test_update_model_by_name_version(model_api):
    a = model_api.add_model(f"TestModel2", version=1)
    assert a is not None
    model_api.update_model_by_name_version("TestModel2", version=1, description="TestModel_Something")
    c = model_api.get_model(a)
    assert "name" in c
    assert c["name"] == "TestModel2"
    d = model_api.delete_model(a)
    assert d == a


def test_add_model_full_entry(model_api):
    a = model_api.add_model(
        "TestModel3",
        "some description",
        1,
        input_schema={"some": "input"},
        output_schema={"Some": "output"},
        model_save_path="s3://some_s3_location",
        weights_path="s3://should_be_some_s3_location",
    )
    assert a is not None
    b = model_api.delete_model(a)
    assert a == b


def test_get_latest_version_of_model_by_name(model_api):
    a = model_api.add_model("TestModel5", version=1)
    b = model_api.add_model("TestModel5", version=2, root_id=a)
    assert a is not None and b is not None
    c = model_api.get_latest_version_of_model_by_name("TestModel5")
    assert c == 2
    with pytest.raises(Exception):
        _ = model_api.get_latest_version_of_model_by_name("SomeOtherName")
    # First delete root model
    e = model_api.delete_model(b)
    # Then delete child model, otherwise foreign key constraint fails
    d = model_api.delete_model(a)
    assert d == a and e == b


def test_active_model(model_api: ProjectAiApiMixin, model: str, existing_app_id):
    a = model_api.project_set_model(app_id=existing_app_id, assignment="PRELABEL", model_id=model, threshold=0.5)
    assert a is not None

    active_models = model_api.get_models(existing_app_id, "PRELABEL", active=True)
    assert a.model_id in [act.model.id for act in active_models]
    assert active_models[0].threshold == 0.5

    a = model_api.project_set_model(app_id=existing_app_id, assignment="PRELABEL", model_id=model, active=False)
    inactive_models = model_api.get_models(existing_app_id, "PRELABEL", active=False)
    assert a.model_id in [act.model.id for act in inactive_models]


def test_view_prediction_instance(model_api, existing_app_id, prediction_id):
    prelabels = model_api.list_prediction_instances(existing_app_id, prediction_id)
    instance_id = prelabels[0].id
    instance = model_api.view_prediction_instance(existing_app_id, prediction_id, instance_id)
    assert instance is not None


def test_submit_prelabel(model_api: Client, model: str, existing_app_id):
    test_output = {"score": 1.0, "mask": [0, 1, 1, 0]}
    prediction_id = model_api.submit_prelabel(test_output, existing_app_id, 1, model, assignment="PRELABEL")
    assert prediction_id is not None

    test_output = [
        {"score": 1.0, "mask": [0, 1, 1, 0]},
        {"mask": [0, 1, 1, 0]},
    ]

    prediction_id = model_api.submit_prelabel(test_output, existing_app_id, 2, model, assignment="PRELABEL")
    assert prediction_id is not None
    prelabels = model_api.list_prediction_instances(existing_app_id, prediction_id)
    assert len(prelabels) == len(test_output)


@pytest.mark.skip
def test_submit_prediction_request(model_api: Client, model: str):
    input_data = {
        "test_key": "test_value",
    }
    prediction_id = model_api.submit_prediction_request(model_id=model, input_data=input_data)
    assert prediction_id is not None

    params = {"param1": "value1", "param2": "value2"}
    prediction_id = model_api.submit_prediction_request(model_id=model, input_data=input_data, parameters=params)
    assert prediction_id is not None


@pytest.mark.skip
def test_resolve_data_reference(model_api: ProjectAiApiMixin):
    url = model_api.resolve_data_reference(
        prediction_id="7bb07cdc-cbfa-4d26-a996-d4c48eca903f",
        instance_id=0,
        reference="data://ai/7bb07cdc-cbfa-4d26-a996-d4c48eca903f/0/mask0.png",
    )
    assert url is not None
    assert "https" in url


def test_predictions(model_api, mocker):

    prediction_id = "396337dc-53a7-48ac-87c4-4a472bf52b41"
    # Mock model api return values
    mocker.patch.object(
        superai.apis.meta_ai.model.DeploymentApiMixin, "submit_prediction_request", return_value=prediction_id
    )
    mocker.patch.object(
        superai.apis.meta_ai.model.DeploymentApiMixin, "wait_for_prediction_completion", return_value="COMPLETED"
    )

    # Create prediction object mock
    test_score = 1.0
    instance = meta_ai_instance(json_data={"id": 0, "output": "test", "score": test_score})
    prediction = meta_ai_prediction(json_data={"id": prediction_id, "instances": [instance]})
    mocker.patch.object(
        superai.apis.meta_ai.model.DeploymentApiMixin, "get_prediction_with_data", return_value=prediction
    )

    p = model_api.predict_from_endpoint(
        model_id="9680e0e7-504e-4a94-a631-861bcb40e1ed",
        input_data={
            "merchant_name": "Test Merchant 123",
            "line_of_business": "Test Line of Business",
        },
    )
    assert p is not None
    assert len(p) == 1
    assert p[0].score == test_score


@pytest.mark.skip
def test_training(model_api, model, existing_app_id):
    training_template = model_api.create_training_template_entry(existing_app_id, model, {})
    assert training_template
    training_instance = model_api.create_training_entry(model, existing_app_id, {})
    assert training_instance

    templates = model_api.get_training_templates(existing_app_id, model)
    assert templates[0]["id"] == training_template
    trainings = model_api.get_trainings(existing_app_id, model)
    assert trainings[0]["id"] == training_instance

    assert model_api.delete_training(training_instance, existing_app_id)
    assert model_api.delete_training_template(training_template, existing_app_id)
