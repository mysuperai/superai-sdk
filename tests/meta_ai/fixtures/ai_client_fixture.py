import pathlib

import pytest
import vcr

from superai import AiApiMixin

"""
New shared ai_client fixture module
#TODO:
- Rewrite existing tests to use this fixture
"""

my_vcr = vcr.VCR(
    serializer="yaml",
    cassette_library_dir=f"{pathlib.Path(__file__).resolve().parent}/cassettes",
    record_mode="new",
    match_on=["body", "headers", "method"],
    filter_headers=["x-api-key", "x-app-id", "Content-Length", "User-Agent"],
    decode_compressed_response=True,
)


@pytest.fixture(scope="session")
def ai_client():
    """
    Fixture to provide a shared instance of the AiApiMixin class.
    Calls and responses are recorded in cassettes/ directory using VCR.

    Returns:

    """
    with my_vcr.use_cassette("client.yaml"):
        yield AiApiMixin()
