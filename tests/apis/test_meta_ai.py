from superai.apis.meta_ai import ModelApiMixin, ProjectAiApiMixin
import pytest
import vcr
import ast

# To record new cassette, use real app_id and run pytest against runnig endpoint
APP_ID = "FAKE_APP_ID"


def scrub_string(string, replacement=""):
    def before_record_response(response):
        response = str(response).replace(string, replacement)
        response = ast.literal_eval(response)
        return response

    return before_record_response


def before_record_cb(request):
    request.body = scrub_string(APP_ID, "FAKE_APP_ID")(request.body)
    return request


my_vcr = vcr.VCR(
    serializer="yaml",
    cassette_library_dir="fixtures/cassettes",
    record_mode="none",
    match_on=["body", "headers", "method"],
    filter_headers=["x-api-key", "x-app-id", "Content-Length", "User-Agent"],
    before_record_response=scrub_string(APP_ID, "FAKE_APP_ID"),
    before_record_request=before_record_cb,
    decode_compressed_response=True,
)


@pytest.fixture(scope="module")
def model_api():
    with my_vcr.use_cassette("model_api.yaml"):
        yield ModelApiMixin()


@pytest.fixture(scope="module")
def ai_api():
    with my_vcr.use_cassette(
        "ai_api.yaml",
    ):
        yield ProjectAiApiMixin()


@pytest.fixture()
def existing_app_id():
    return APP_ID


def test_model_update(model_api, model):
    new_name = "ChangedTestModel"
    b = model_api.update_model(model, name=new_name)
    assert model == b
    assert new_name == model_api.get_model(model).name


@pytest.fixture()
def model(model_api):
    a = model_api.add_model(f"TestModel")
    assert a is not None
    yield a
    c = model_api.delete_model(a)
    assert a == c


@pytest.fixture()
def prediction_id(ai_api, existing_app_id, model):
    test_output = {"score": 1.0, "mask": [0, 1, 1, 0]}
    prediction_id = ai_api.submit_prelabel(test_output, existing_app_id, 1, model, assignment="PRELABEL")
    yield prediction_id
    deleted = ai_api.delete_prelabel(existing_app_id, prediction_id)
    assert deleted == prediction_id


def test_model_retrieval(model_api, model):
    m = model_api.get_model(model)
    assert "name" in m

    m = model_api.get_all_models()
    assert len(m) >= 1


def test_active_model(ai_api: ProjectAiApiMixin, model: str, existing_app_id):
    a = ai_api.update_model(app_id=existing_app_id, assignment="PRELABEL", model_id=model)
    assert a is not None

    active_models = ai_api.get_models(existing_app_id, "PRELABEL", active=True)
    assert a.model_id in [act.model.id for act in active_models]

    a = ai_api.update_model(app_id=existing_app_id, assignment="PRELABEL", model_id=model, active=False)
    inactive_models = ai_api.get_models(existing_app_id, "PRELABEL", active=False)
    assert a.model_id in [act.model.id for act in inactive_models]


def test_view_prelabel(ai_api, existing_app_id, prediction_id):
    prelabels = ai_api.list_prelabel_instances(existing_app_id, prediction_id)
    instance_id = prelabels[0].id
    instance = ai_api.view_prelabel(existing_app_id, prediction_id, instance_id)
    assert instance is not None


def test_submit_prelabel(ai_api: ProjectAiApiMixin, model: str, existing_app_id):
    test_output = {"score": 1.0, "mask": [0, 1, 1, 0]}
    prediction_id = ai_api.submit_prelabel(test_output, existing_app_id, 1, model, assignment="PRELABEL")
    assert prediction_id is not None

    test_output = [
        {"score": 1.0, "mask": [0, 1, 1, 0]},
        {"mask": [0, 1, 1, 0]},
    ]

    prediction_id = ai_api.submit_prelabel(test_output, existing_app_id, 2, model, assignment="PRELABEL")
    assert prediction_id is not None
    prelabels = ai_api.list_prelabel_instances(existing_app_id, prediction_id)
    assert len(prelabels) == len(test_output)
