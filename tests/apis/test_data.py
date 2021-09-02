import ast

import pytest
import vcr
import json
import os

from superai.client import Client

# To record new cassette, use real app_id and run pytest against runnig endpoint


def scrub_string(string, replacement=""):
    def before_record_response(response):
        response = str(response).replace(string, replacement)
        response = ast.literal_eval(response)
        return response

    return before_record_response


my_vcr = vcr.VCR(
    serializer="yaml",
    cassette_library_dir="fixtures/cassettes",
    record_mode="none",
    match_on=["body", "headers", "method", "path"],
    filter_headers=["x-api-key", "x-app-id", "Content-Length", "User-Agent", "API-KEY"],
    decode_compressed_response=True,
)


@pytest.fixture(scope="module")
def client():
    with my_vcr.use_cassette("data_api.yaml"):
        yield Client("TEST_API_KEY")


def test_list_data_unsigned(client: Client):
    data = client.list_data(signedUrl=False, page=1, size=1)
    assert len(data.get("content", [])) == 1
    entity = data.get("content", []).pop()
    assert entity.get("path") is not None
    assert entity.get("signedUrl") is None


def test_list_data_signed(client: Client):
    data = client.list_data(signedUrl=True, page=1, size=1)
    assert len(data.get("content", [])) == 1
    entity = data.get("content", []).pop()
    assert entity.get("path") is not None
    assert entity.get("signedUrl", None) is not None


def test_get_signed_url(client: Client):
    signed_url = client.get_signed_url(path="default/test1.json")
    assert signed_url.get("ownerId")
    assert signed_url.get("path")
    assert signed_url.get("signedUrl")


def test_download_data_with_relative_path(client: Client):
    downloaded = client.download_data(path="default/test1.json")
    expected = {"test1": True}
    assert downloaded == expected


def test_download_data_with_full_path(client: Client):
    downloaded = client.download_data(path="data://2341234132513251/default/test1.json")
    expected = {"test1": True}
    assert downloaded == expected


def test_download_data_public(client: Client):
    with pytest.raises(Exception) as excinfo:
        downloaded = client.download_data(path="https://filesamples.com/samples/code/json/sample1.json")
    assert str(excinfo.value) == "Forbidden"


def test_delete_data(client: Client):
    a = client.delete_data(path="default/test1.json")
    print(a)
