import json
import time
from multiprocessing import Process
from typing import List

import pytest
import requests
from superai_schema.types import BaseModel, Field, UiWidget

from superai.data_program.schema_server import SchemaServer


def run_server():
    class Parameters(BaseModel):
        choices: List[str] = Field(uniqueItems=True)

    def handler(params: Parameters):
        class MyInput(BaseModel, UiWidget):
            __root__: str

            @classmethod
            def ui_schema(cls):
                return {"ui:help": "Enter the text to label"}

        class MyOutput(BaseModel, UiWidget):
            __root__: str = Field(enum=params.choices)

            @classmethod
            def ui_schema(cls):
                return {"ui:widget": "radio"}

        def process_job(job_input: MyInput) -> MyOutput:
            index = len(job_input.__root__) % len(params.choices)
            return MyOutput(__root__=params.choices[index])

        return MyInput, MyOutput, process_job

    SchemaServer(params_model=Parameters, generate=handler, log_level="critical").run()


@pytest.fixture(scope="module")
def server():
    proc = Process(target=run_server, args=(), daemon=True)
    proc.start()
    time.sleep(2)  # time for the server to start
    yield
    proc.terminate()


def test_serve_schema_ok(server):
    resp = requests.post("http://127.0.0.1:8001/schema", json={"params": {"choices": ["Dog", "Cat", "UMA"]}})
    expected = json.loads(
        """
        {
            "inputSchema": {
               "title": "MyInput",
               "type": "string"
            },
            "inputUiSchema": {"ui:help": "Enter the text to label"},
            "outputSchema": {
                "enum": ["Dog", "Cat", "UMA"],
                "title": "MyOutput",
                "type": "string"
            },
            "outputUiSchema": {"ui:widget": "radio"}
        }
        """
    )
    assert resp.json() == expected


def test_serve_schema_invalid(server):
    expected = json.loads(
        """
        {"detail": "['Dog', 'Dog', 'UMA'] has non-unique elements"}
        """
    )
    resp = requests.post("http://127.0.0.1:8001/schema", json={"params": {"choices": ["Dog", "Dog", "UMA"]}})
    assert resp.json() == expected
