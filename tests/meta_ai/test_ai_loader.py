from typing import Dict

import pytest

from superai.meta_ai.ai_uri import AiURI


@pytest.mark.parametrize(
    "uri, expected_components",
    [
        ("ai://user1/my_model/1.0", {"owner_name": "user1", "model_name": "my_model", "version": "1.0"}),
        ("ai://my_model/1.0", {"model_name": "my_model", "version": "1.0", "username": None}),
        ("ai://my_model", {"model_name": "my_model", "version": None, "username": None}),
        ("ai://superai/my_model", {"owner_name": "superai", "model_name": "my_model", "version": None}),
    ],
)
def test_parse_model_uri_valid(uri: str, expected_components: Dict[str, str]) -> None:
    result = AiURI.parse(uri)
    assert result.owner_name == expected_components.get("owner_name")
    assert result.model_name == expected_components.get("model_name")
    assert result.version == expected_components.get("version")


@pytest.mark.parametrize(
    "uri",
    [
        "ai://username//model_name/version",
        "ai://username/model_name/",
        "ai:///",
        "ai://",
    ],
)
def test_parse_model_uri_invalid(uri: str) -> None:
    with pytest.raises(ValueError, match="Invalid model URI format"):
        AiURI.parse(uri)
