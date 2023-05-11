import os
import random
import string
import tempfile
from typing import Optional, Union

import requests
from pydantic import validator

from .data_type import DataType


class AnyValueError(Exception):
    """Custom error raised when both value and url are missing."""

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)


class AnyPathError(Exception):
    """Custom error raised when the path does not exist."""

    def __init__(self, path: str, message: str) -> None:
        self.path = path
        self.message = message
        super().__init__(message)


class AnyUrlError(Exception):
    """Custom error raised when the URL is not valid."""

    def __init__(self, url: str, message: str) -> None:
        self.url = url
        self.message = message
        super().__init__(message)


class Any(DataType):
    value: Optional[Union[str, bytes, dict, list, int, float, bool, None]] = None
    path: Optional[str] = None
    url: Optional[str] = None

    @validator("value")
    @classmethod
    def validate_value(cls, value):
        # Since Any accepts any data type, no validation is required
        return value

    @validator("path")
    @classmethod
    def validate_path(cls, path) -> str:
        if path and not os.path.isfile(path):
            raise AnyPathError(path=path, message="File does not exist.")
        return path

    @validator("url")
    @classmethod
    def validate_url(cls, url) -> str:
        if url:
            response = requests.head(url)
            if response.status_code != 200:
                raise AnyUrlError(url=url, message="Failed to fetch data from URL.")
        return url

    def _load_from_path(self):
        self.validate_path()
        with open(self.path, "rb") as f:
            self.value = f.read()

    def _load_from_url(self):
        self.validate_url()
        response = requests.get(self.url)
        self.value = response.content

    def generate_value(self) -> Union[str, bytes, dict, list, int, float, bool, None]:
        # Randomly generate a value of any data type
        random_type = random.choice(["str", "bytes", "dict", "list", "int", "float", "bool", "None"])
        if random_type == "str":
            return "".join(random.choices(string.ascii_letters + string.digits, k=10))
        elif random_type == "bytes":
            return os.urandom(10)
        elif random_type == "dict":
            return {"".join(random.choices(string.ascii_letters, k=3)): random.randint(1, 10) for _ in range(3)}
        elif random_type == "list":
            return [random.randint(1, 10) for _ in range(5)]
        elif random_type == "int":
            return random.randint(1, 100)
        elif random_type == "float":
            return random.uniform(1, 100)
        elif random_type == "bool":
            return random.choice([True, False])
        else:
            return None

    def generate_url(self) -> str:
        # Please note that this is a placeholder URL and not a working one.
        # Replace it with a valid URL containing your desired data.
        return "https://example.com/generated_any_data"

    def generate_path(self) -> str:
        temp_file = tempfile.NamedTemporaryFile(delete=False)
        generated_value = self.generate_value()
        if isinstance(generated_value, (str, bytes)):
            temp_file.write(generated_value)
        else:
            temp_file.write(str(generated_value).encode("utf-8"))
        temp_file.close()
        return temp_file.name

    def to_text(self) -> str:
        if self.value is None:
            raise ValueError("No data available.")
        return str(self.value)

    def __str__(self) -> str:
        return f"Any(value={self.value}, path={self.path}, url={self.url})"

    def __repr__(self) -> str:
        return self.__str__()
