import io
import random
import tempfile
from typing import List

import requests
from PIL import Image as PILImage

from .document import Document


class Image(Document):
    types: List[str] = ["jpg", "jpeg", "png", "gif"]

    # Inherits __init__, validate_value, validate_url, validate_path, validate_constraints, _load_from_path, and _load_from_url from Document.

    # generate methods
    def generate_value(self) -> bytes:
        # For simplicity, generate a blank image in the desired format
        file_type = random.choice(self.types)
        img = PILImage.new("RGB", (100, 100), color="white")

        byte_data = io.BytesIO()
        img.save(byte_data, format=file_type.upper())
        byte_data.seek(0)

        return byte_data.read()

    def generate_url(self) -> str:
        # Please note that this is a placeholder URL and not a working one.
        # Replace it with a valid URL containing your desired image.
        file_type = random.choice(self.types)
        return f"https://example.com/generated_image.{file_type}"

    def generate_path(self) -> str:
        file_type = random.choice(self.types)
        temp_file = tempfile.NamedTemporaryFile(suffix=f".{file_type}", delete=False)

        img = PILImage.new("RGB", (100, 100), color="white")
        img.save(temp_file, format=file_type.upper())

        temp_file.close()

        return temp_file.name

    def to_text(self) -> str:
        if not self.value:
            raise ValueError("No image data available.")
        # TODO: implement summary API
        response = requests.post("https://api.example.com/summarize_image", json={"image_data": self.value})
        return response.json()["summary"]
