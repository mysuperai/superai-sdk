import io
import os
import random
import tempfile
from typing import List, Optional, Union

import PyPDF2
import pytesseract
import requests
from PIL import Image as PILImage
from pydantic import ValidationError, validator

from .data_type import DataType

pytesseract.pytesseract.tesseract_cmd = "/usr/local/Cellar/tesseract/3.05.02/bin/tesseract"


class Document(DataType):
    value: Optional[Union[str, bytes]] = None
    types: List[str] = ["pdf", "jpg", "png"]
    path: Optional[str] = None
    url: Optional[str] = None
    max_file_size: Optional[int] = None
    max_pages: Optional[int] = None

    def __init__(self, **data):
        super().__init__(**data)
        if self.path:
            self._load_from_path()
        elif self.url:
            self._load_from_url()

    @validator("value", always=True)
    def validate_value(cls, value, values, **kwargs):
        if "path" in values or "url" in values:
            return value

        if value is None:
            return value

        file_type = value.split(".")[-1]
        if "types" in values and file_type not in values["types"]:
            raise ValidationError(f"Invalid file type {file_type}. Supported types are {values['types']}")

        if not os.path.isfile(value):
            raise ValidationError(f"File {value} does not exist.")
        return value

    def validate_url(self):
        if not self.url:
            return

        file_type = self.url.split(".")[-1]
        if file_type not in self.types:
            raise ValidationError(f"Invalid file type {file_type}. Supported types are {self.types}")

        response = requests.head(self.url)
        if response.status_code != 200:
            raise ValidationError(f"Failed to fetch document from URL {self.url}.")

        if self.max_file_size:
            file_size = int(response.headers.get("Content-Length", 0))
            if file_size > self.max_file_size:
                raise ValidationError(f"Document exceeds the maximum file size of {self.max_file_size} bytes.")

    def validate_path(self):
        if not self.path:
            return

        if not os.path.isfile(self.path):
            raise ValidationError(f"File {self.path} does not exist.")

        file_type = self.path.split(".")[-1]
        if file_type not in self.types:
            raise ValidationError(f"Invalid file type {file_type}. Supported types are {self.types}")

        if self.max_file_size:
            file_size = os.path.getsize(self.path)
            if file_size > self.max_file_size:
                raise ValidationError(f"Document exceeds the maximum file size of {self.max_file_size} bytes.")

    def validate_constraints(self):
        if not self.value:
            return

        if isinstance(self.value, str):
            with open(self.value, "rb") as f:
                content = f.read()
        else:
            content = self.value

        file_type = self.value.split(".")[-1] if isinstance(self.value, str) else "pdf"  # Default to pdf
        if file_type == "pdf":
            try:
                with io.BytesIO(content) as f:
                    reader = PyPDF2.PdfFileReader(f)
            except PyPDF2.utils.PdfReadError:
                raise ValidationError("Invalid PDF file.")
            if self.max_pages and reader.getNumPages() > self.max_pages:
                raise ValidationError(f"PDF document exceeds the maximum number of pages {self.max_pages}.")
        elif file_type in ["jpg", "png"]:
            try:
                PILImage.open(io.BytesIO(content))
            except IOError:
                raise ValidationError("Invalid image file.")
        else:
            raise ValidationError(f"Unsupported file type {file_type} for constraint validation.")

    def _load_from_path(self):
        self.validate_path()
        self.value = self.path

    def _load_from_url(self):
        self.validate_url()
        response = requests.get(self.url)
        self.value = response.content

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
        # Replace it with a valid URL containing your desired document.
        file_type = random.choice(self.types)
        return f"https://example.com/generated_document.{file_type}"

    def generate_path(self) -> str:
        file_type = random.choice(self.types)
        temp_file = tempfile.NamedTemporaryFile(suffix=f".{file_type}", delete=False)
        if file_type in ["jpg", "png"]:
            img = PILImage.new("RGB", (100, 100), color="white")
            img.save(temp_file, format=file_type.upper())
        else:  # pdf
            # For simplicity, generate a blank PDF with one page
            from reportlab.lib.pagesizes import letter
            from reportlab.pdfgen import canvas

            c = canvas.Canvas(temp_file, pagesize=letter)
            c.showPage()
            c.save()

        temp_file.close()

        return temp_file.name

    def to_text(self) -> str:
        if not self.value:
            raise ValueError("No document data available.")
        if isinstance(self.value, str):
            with open(self.value, "rb") as f:
                image_data = f.read()
        else:
            image_data = self.value
        img = PILImage.open(io.BytesIO(image_data))
        return pytesseract.image_to_string(img)
