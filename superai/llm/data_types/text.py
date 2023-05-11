import os
import string
from random import random
from typing import Optional

import requests
from pydantic import ValidationError

from .data_type import DataType


class Text(DataType):
    value: Optional[str] = None
    path: Optional[str] = None
    url: Optional[str] = None
    min_characters: Optional[int] = None
    max_characters: Optional[int] = None

    def __init__(self, **data):
        super().__init__(**data)
        if self.path:
            self._load_from_path()
        elif self.url:
            self._load_from_url()

    def validate_value(self):
        if not self.value:
            return

        if self.min_characters and len(self.value) < self.min_characters:
            raise ValidationError(f"Text length is below the minimum of {self.min_characters} characters.")
        if self.max_characters and len(self.value) > self.max_characters:
            raise ValidationError(f"Text length exceeds the maximum of {self.max_characters} characters.")

    def validate_url(self):
        if not self.url:
            return

        response = requests.head(self.url)
        if response.status_code != 200:
            raise ValidationError(f"Failed to fetch text from URL {self.url}.")

    def validate_path(self):
        if not self.path:
            return

        if not os.path.isfile(self.path):
            raise ValidationError(f"File {self.path} does not exist.")

    def validate_constraints(self):
        # Call the validate_value() function since it already validates the constraints for the Text class
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
        length = random.randint(self.min_characters or 10, self.max_characters or 100)
        return "".join(random.choices(string.ascii_letters + string.digits + string.punctuation + " ", k=length))

    def generate_url(self) -> str:
        # Please note that this is a placeholder URL and not a working one.
        # Replace it with a valid URL containing your desired text.
        return "https://example.com/generated_text.txt"

    def generate_path(self) -> str:
        temp_file = tempfile.NamedTemporaryFile(mode="w+", delete=False)
        temp_file.write(self.generate_value())
        temp_file.close()
        return temp_file.name

    def to_text(self) -> str:
        if not self.value:
            raise ValueError("No text data available.")
        return self.value
