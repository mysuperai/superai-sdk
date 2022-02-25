import json
import socket
import time
from multiprocessing import Process
from typing import List

import pytest
import requests
from superai_schema.types import BaseModel, Field, UiWidget

from superai.data_program.dp_server import DPServer
from superai.data_program.types import HandlerOutput, Metric, WorkflowConfig


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

        def metric_func(truths: MyOutput, preds: MyOutput):
            return {"f1_score": {"value": 0.5}}

        def process_job(job_input: MyInput) -> MyOutput:
            index = len(job_input.__root__) % len(params.choices)
            return MyOutput(__root__=params.choices[index])

        return HandlerOutput(
            input_model=MyInput,
            output_model=MyOutput,
            process_fn=process_job,
            templates=[],
            metrics=[Metric(name="f1_score", metric_fn=metric_func)],
        )

    DPServer(
        params=Parameters(choices=["1", "2"]),
        name="Test_Server",
        generate=handler,
        workflows=[WorkflowConfig("top_heroes", is_default=True), WorkflowConfig("crowd_managers", is_gold=True)],
        log_level="critical",
    ).run()


def local_port_open():
    """Check if there is already a process listening on port 8001
    We use this for the DP server.
    Kubectl Dashboard is often listening on the same port.
    """
    a_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    location = ("127.0.0.1", 8001)
    result_of_check = a_socket.connect_ex(location)
    return result_of_check == 0


@pytest.fixture(scope="module")
def server():
    if local_port_open():
        raise RuntimeError("Port 8001 is already in use. Is Kubectl Dashboard running?")
    proc = Process(target=run_server, args=(), daemon=True)
    proc.start()
    time.sleep(5)  # time for the server to start
    yield
    proc.terminate()


def test_serve_schema_ok(server):
    # assert server is not None
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


def test_metric_names(server):
    expected = json.loads(
        """
       ["f1_score"]
        """
    )
    resp = requests.get("http://127.0.0.1:8001/metrics")
    assert resp.json() == expected


def test_metric_calculate(server):
    expected = json.loads(
        """
       {"f1_score": {
            "value": 0.5
            }
        }
        
        """
    )
    resp = requests.post(
        "http://127.0.0.1:8001/metrics/f1_score",
        json={
            "truths": [
                {
                    "url": "https://farm1.static.flickr.com/22/30133265_5d1a4d6b1e.jpg",
                    "annotations": [
                        {"top": 126.49, "left": 56.55, "width": 367.56, "height": 209.82, "selection": "1"}
                    ],
                }
            ],
            "preds": [
                {
                    "url": "https://farm1.static.flickr.com/22/30133265_5d1a4d6b1e.jpg",
                    "annotations": [{"top": 26.49, "left": 51.55, "width": 234.56, "height": 21.82, "selection": "1"}],
                }
            ],
        },
    )
    assert resp.json() == expected


def test_method_names(server):
    expected = json.loads(
        """
       [{"method_name": "Test_Server.top_heroes",  "role": "normal"}, {"method_name": "Test_Server.crowd_managers",  "role": "normal"}, {"method_name": "Test_Server.crowd_managers",  "role": "gold"}]
        """
    )
    resp = requests.get("http://127.0.0.1:8001/methods")

    assert resp.json() == expected
