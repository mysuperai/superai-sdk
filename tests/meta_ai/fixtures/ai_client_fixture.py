import pathlib
from typing import Optional

import pytest

from superai import settings
from superai.apis.meta_ai import MetaAiApiMixin

"""
New shared ai_client fixture module
#TODO:
- Rewrite existing tests to use this fixture
"""


@pytest.fixture(scope="module")
def vcr(vcr):
    vcr.serializer = "yaml"
    vcr.cassette_library_dir = f"{pathlib.Path(__file__).resolve().parent}/cassettes"
    vcr.record_mode = "new"
    vcr.match_on = ["body", "headers", "method"]
    vcr.filter_headers = [
        "x-api-key",
        "x-app-id",
        "Content-Length",
        "User-Agent",
        "Authorization",
        "X-Amz-Security-Token",
        "Accept-Encoding",
    ]
    vcr.decode_compressed_response = True
    return vcr


@pytest.fixture(scope="module")
def monkeysession(request):
    """Enables monkeypatching of session scoped fixtures"""

    from _pytest.monkeypatch import MonkeyPatch

    mpatch = MonkeyPatch()
    yield mpatch
    mpatch.undo()


def _get_host_port_for_container(container_name: str, container_port: int = "8080") -> Optional[int]:
    """
    Get the host port for a container in cases where the port is dynamically assigned and not static.
    Args:
        container_name: (Sub)string of the container name
        container_port: Port the container (service) is listening on.
    Returns:
        The host port for the container if it exists.
    """
    import docker

    client = docker.from_env()
    containers = client.containers.list(filters={"name": container_name}, limit=2)
    if len(containers) != 1:
        raise Exception(f"Multiple containers with name {container_name} found")
    # get port
    hasura = containers[0]
    port = hasura.attrs["NetworkSettings"]["Ports"][f"{container_port}/tcp"][0]["HostPort"]
    return int(port)


@pytest.fixture(scope="module")
def ai_client(local_endpoint, monkeysession, vcr):
    """
    Fixture to provide a shared instance of the AiApiMixin class.
    Calls and responses are recorded in cassettes/ directory using VCR.

    Returns:

    """
    if local_endpoint:
        # Set URL in config so new MetaAISession instances can use it
        port = _get_host_port_for_container("hasura")
        base_url = f"localhost:{port}/v1/graphql"
        monkeysession.setattr(settings, "meta_ai_request_protocol", "http")
        monkeysession.setattr(settings, "meta_ai_base", base_url)

    with vcr.use_cassette("client.yaml"):
        yield MetaAiApiMixin()


def pytest_addoption(parser):
    parser.addoption(
        "--local-endpoint",
        "-L",
        action="store_true",
        default=False,
        help="Runs tests with local AI endpoint.",
    )


@pytest.fixture(scope="module")
def local_endpoint(request):
    return request.config.option.local_endpoint
