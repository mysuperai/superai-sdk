import pathlib

import pytest
import vcr

from superai.client import Client


def scrub_string(string, replacement=""):
    def before_record_response(response):
        response = str(response).replace(string, replacement)
        response = ast.literal_eval(response)
        return response

    return before_record_response


def my_vcr():
    return vcr.VCR(
        serializer="yaml",
        cassette_library_dir=f"{pathlib.Path(__file__).resolve().parent}/cassettes",
        record_mode="none",
        match_on=["body", "headers", "method", "path"],
        filter_headers=["x-api-key", "x-app-id", "Content-Length", "User-Agent", "API-KEY", "Accept-Encoding"],
        decode_compressed_response=True,
    )


@pytest.fixture(scope="module")
def client():
    with my_vcr().use_cassette("project_api.yaml"):
        yield Client("TEST_API_KEY")


def test_get_project(client: Client):
    # Test case to ensure the method correctly fetches a project based on a provided UUID.
    response = client.get_project("a6a7b101-3c27-417f-964b-6b501977057e")
    assert response["uuid"] == "a6a7b101-3c27-417f-964b-6b501977057e"
    assert response["name"] == "Test Project"


def test_get_project_no_uuid(client: Client):
    # Test case to ensure the method raises a ValueError if no UUID is provided.
    with pytest.raises(ValueError):
        client.get_project(None)


def test_get_project_unexpected_arg(client: Client):
    # Test case to ensure the method raises a TypeError if unexpected keyword arguments are provided.
    with pytest.raises(TypeError):
        client.get_project("test_uuid", unexpected_arg="unexpected_value")


def test_create_project_no_body(client: Client):
    # Test case to ensure the method raises a ValueError if no body is provided.
    with pytest.raises(ValueError):
        client.create_project(None)


def test_create_project_unexpected_arg(client: Client):
    # Test case to ensure the method raises a TypeError if unexpected keyword arguments are provided.
    body = {"name": "New Project"}
    with pytest.raises(TypeError):
        client.create_project(body, unexpected_arg="unexpected_value")


def test_list_projects_default(client: Client):
    client.list_projects()


@pytest.mark.parametrize(
    "param, value",
    [
        ("page", ["pageNumber", 1]),
        ("size", ["pageSize", 10]),
    ],
)
def test_list_projects_parameters(param, value, client: Client):
    response = client.list_projects(**{param: value[1]})
    assert response.get(value[0]) == value[1]


def test_list_projects_combinations(client: Client):
    response = client.list_projects(page=2, size=1, sort_by="created")
    assert response.get("pageNumber") == 2
    assert response.get("pageSize") == 1


def test_list_projects_unexpected_arg(client: Client):
    with pytest.raises(TypeError):
        client.list_projects(unexpected_arg="unexpected_value")
