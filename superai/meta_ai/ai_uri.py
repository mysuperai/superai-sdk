import re
from typing import Optional

import attr

from superai.meta_ai.ai_helper import _ai_name_validator, _ai_version_validator


@attr.s(auto_attribs=True)
class AiURI:
    """
    Dataclass for storing and parsing the components of a model URI.
    Args:
        model_name (str): The name of the model.
        version (Optional[str]): The version of the model (optional).
        owner_name (Optional[str]): The name of the owner of the model. Can either be a single user or organisation (optional).

    Raises:
        ValueError: If the model name is invalid (as determined by the _ai_name_validator function).
        ValueError: If the version is invalid (as determined by the _ai_version_validator function).

    """

    model_name: str = attr.field(validator=_ai_name_validator)
    version: Optional[str] = attr.field(validator=attr.validators.optional(_ai_version_validator))
    owner_name: Optional[str] = None

    @classmethod
    def parse(cls, uri: str) -> "AiURI":
        """
        Parse a model URI and return its components.

        Args:
            uri (str): The model URI in the format ai://<owner_name>/model_name/version,
                       ai://model_name/version or ai://model_name
                       Owner name can be either a username or an organization name.

        Returns:
            AiURI: An instance of the AIURL dataclass containing the parsed components
        """
        # Define the regular expression for parsing the URI
        # fmt: off
        pattern = r"^ai://" \
                  r"(?:(?P<owner_name>[\w-]+)/)?" \
                  r"(?P<model_name>[\w\-_]+)" \
                  r"(?:(?:/)(?P<version>\d+\.\d+))?$"
        # fmt: on

        # Try to match URI with the pattern
        match = re.match(pattern, uri)
        if not match:
            raise ValueError(f"Invalid model URI format: {uri}")

        # Extract the components from the match object
        components = match.groupdict()

        # Create and return an instance of the AIURL dataclass
        return cls(**components)

    def __str__(self) -> str:
        base_str = f"ai://{self.model_name}"
        if self.owner_name:
            base_str = f"ai://{self.owner_name}/{self.model_name}"
        if self.version:
            base_str += f"/{self.version}"
        return base_str
