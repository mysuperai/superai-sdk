import os
from typing import Optional

import requests
from pydantic import ValidationError

from .data_type import DataType


class Webpage(DataType):
    value: Optional[str] = None
    path: Optional[str] = None
    url: Optional[str] = None
    max_file_size: Optional[int] = None

    def __init__(self, **data):
        super().__init__(**data)
        if self.path:
            self._load_from_path()
        elif self.url:
            self._load_from_url()

    def validate_value(self):
        if not self.value:
            return

        if self.max_file_size and len(self.value) > self.max_file_size:
            raise ValidationError(f"Webpage content exceeds the maximum file size of {self.max_file_size} bytes.")

    def validate_url(self):
        if not self.url:
            return

        response = requests.head(self.url)
        if response.status_code != 200:
            raise ValidationError(f"Failed to fetch webpage from URL {self.url}.")

    def validate_path(self):
        if not self.path:
            return

        if not os.path.isfile(self.path):
            raise ValidationError(f"File {self.path} does not exist.")

    def validate_constraints(self):
        # Call the validate_value() function since it already validates the constraints for the Webpage class
        self.validate_value()

    def _load_from_path(self):
        self.validate_path()
        with open(self.path, "r") as f:
            self.value = f.read()

    def _load_from_url(self):
        self.validate_url()
        response = requests.get(self.url)
        self.value = response.text

    def generate_value(self) -> str:
        # Generate a random string to simulate a webpage value
        content = "".join(random.choices(string.ascii_letters + string.digits, k=100))
        return content

    def generate_url(self) -> str:
        domain = "".join(random.choices(string.ascii_letters, k=10))
        return f"http://{domain}.com"

    def generate_path(self) -> str:
        filename = "".join(random.choices(string.ascii_letters, k=10)) + ".html"
        return os.path.join("webpages", filename)

    def to_text(self) -> str:
        if not self.value:
            raise ValueError("No webpage data available.")
        return self.value
