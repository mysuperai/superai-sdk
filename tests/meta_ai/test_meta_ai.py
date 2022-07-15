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
def vcr():
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


@pytest.fixture(scope="function")
def existing_app_id():
    return APP_ID


@pytest.fixture(scope="function")
def model(ai_client):
    a = ai_client.add_model(f"TestModel")
    assert a is not None
    yield a
    c = ai_client.delete_model(a)
    assert a == c


def test_model(ai_client, model):

    m = ai_client.get_model_by_name("TestModel")
    assert "name" in m[0]
    assert m[0]["name"] == "TestModel"

    m = ai_client.get_model(model)
    assert "name" in m

    m = ai_client.get_all_models()
    assert len(m) >= 1

    new_name = "ChangedTestModel"
    b = ai_client.update_model(model, name=new_name)
    assert model == b
    assert new_name == ai_client.get_model(model).name


@pytest.fixture()
def prediction_id(ai_client, existing_app_id, model):
    test_output = {"score": 1.0, "mask": [0, 1, 1, 0]}
    prediction_id = ai_client.submit_prelabel(test_output, existing_app_id, 1, model, assignment="PRELABEL")

    yield prediction_id

    # Teardown
    deleted = ai_client.delete_prelabel(existing_app_id, prediction_id)
    assert deleted == prediction_id


def test_view_prediction(ai_client, existing_app_id, prediction_id):
    object: meta_ai_prediction = ai_client.view_prediction(app_id=existing_app_id, prediction_id=prediction_id)
    assert "id" in object
    assert "state" in object


def test_get_prediction(ai_client: Client, prediction_id):
    p = ai_client.get_prediction_with_data(prediction_id=prediction_id)
    assert p.created_at is not None
    assert p.started_at is None
    assert p.error_message is None


def test_request_prediction_of_job(ai_client, existing_app_id):
    with pytest.raises(Exception):
        ids = ai_client.request_prediction_of_job(app_id=existing_app_id, job_id=1, assignment="PRELABEL")


def test_update_model_by_name_version(ai_client):
    a = ai_client.add_model(f"TestModel2", version=1)
    assert a is not None
    ai_client.update_model_by_name_version("TestModel2", version=1, description="TestModel_Something")
    c = ai_client.get_model(a)
    assert "name" in c
    assert c["name"] == "TestModel2"
    d = ai_client.delete_model(a)
    assert d == a


def test_add_model_full_entry(ai_client):
    a = ai_client.add_model(
        "TestModel3",
        "some description",
        1,
        input_schema={"some": "input"},
        output_schema={"Some": "output"},
        model_save_path="s3://some_s3_location",
        weights_path="s3://should_be_some_s3_location",
    )
    assert a is not None
    b = ai_client.delete_model(a)
    assert a == b


def test_get_latest_version_of_model_by_name(ai_client):
    a = ai_client.add_model("TestModel5", version=1)
    b = ai_client.add_model("TestModel5", version=2, root_id=a)
    assert a is not None and b is not None
    c = ai_client.get_latest_version_of_model_by_name("TestModel5")
    assert c == 2
    with pytest.raises(Exception):
        _ = ai_client.get_latest_version_of_model_by_name("SomeOtherName")
    # First delete root model
    e = ai_client.delete_model(b)
    # Then delete child model, otherwise foreign key constraint fails
    d = ai_client.delete_model(a)
    assert d == a and e == b


def test_active_model(ai_client: ProjectAiApiMixin, model: str, existing_app_id):
    a = ai_client.project_set_model(app_id=existing_app_id, assignment="PRELABEL", model_id=model, threshold=0.5)
    assert a is not None

    active_models = ai_client.get_models(existing_app_id, "PRELABEL", active=True)
    assert a.model_id in [act.model.id for act in active_models]
    assert active_models[0].threshold == 0.5

    a = ai_client.project_set_model(app_id=existing_app_id, assignment="PRELABEL", model_id=model, active=False)
    inactive_models = ai_client.get_models(existing_app_id, "PRELABEL", active=False)
    assert a.model_id in [act.model.id for act in inactive_models]


def test_view_prediction_instance(ai_client, existing_app_id, prediction_id):
    prelabels = ai_client.list_prediction_instances(existing_app_id, prediction_id)
    instance_id = prelabels[0].id
    instance = ai_client.view_prediction_instance(existing_app_id, prediction_id, instance_id)
    assert instance is not None


def test_submit_prelabel(ai_client: Client, model: str, existing_app_id):
    test_output = {"score": 1.0, "mask": [0, 1, 1, 0]}
    prediction_id = ai_client.submit_prelabel(test_output, existing_app_id, 1, model, assignment="PRELABEL")
    assert prediction_id is not None

    test_output = [
        {"score": 1.0, "mask": [0, 1, 1, 0]},
        {"mask": [0, 1, 1, 0]},
    ]

    prediction_id = ai_client.submit_prelabel(test_output, existing_app_id, 2, model, assignment="PRELABEL")
    assert prediction_id is not None
    prelabels = ai_client.list_prediction_instances(existing_app_id, prediction_id)
    assert len(prelabels) == len(test_output)


@pytest.mark.skip
def test_submit_prediction_request(ai_client: Client, model: str):
    input_data = {
        "test_key": "test_value",
    }
    prediction_id = ai_client.submit_prediction_request(model_id=model, input_data=input_data)
    assert prediction_id is not None

    params = {"param1": "value1", "param2": "value2"}
    prediction_id = ai_client.submit_prediction_request(model_id=model, input_data=input_data, parameters=params)
    assert prediction_id is not None


@pytest.mark.skip
def test_resolve_data_reference(ai_client: ProjectAiApiMixin):
    url = ai_client.resolve_data_reference(
        prediction_id="7bb07cdc-cbfa-4d26-a996-d4c48eca903f",
        instance_id=0,
        reference="data://ai/7bb07cdc-cbfa-4d26-a996-d4c48eca903f/0/mask0.png",
    )
    assert url is not None
    assert "https" in url


def test_predictions(ai_client, mocker):

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

    p = ai_client.predict_from_endpoint(
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
def test_training(ai_client, model, existing_app_id):
    training_template = ai_client.create_training_template_entry(model, {}, existing_app_id)
    assert training_template
    training_instance = ai_client.create_training_entry(model, existing_app_id, {})
    assert training_instance

    templates = ai_client.get_training_templates(model, existing_app_id)
    assert templates[0]["id"] == training_template
    trainings = ai_client.get_trainings(existing_app_id, model)
    assert trainings[0]["id"] == training_instance

    assert ai_client.delete_training(training_instance, existing_app_id)
    assert ai_client.delete_training_template(training_template, existing_app_id)
