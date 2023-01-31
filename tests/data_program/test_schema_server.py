import contextlib
import json
import socket
import time
from multiprocessing import Process
from typing import List

import pytest
import requests
from superai_schema.types import BaseModel, Field, UiWidget

from superai.data_program import Metric
from superai.data_program.dp_server import DPServer
from superai.data_program.types import (
    HandlerOutput,
    PostProcessContext,
    PostProcessRequestModel,
)
from superai.data_program.workflow import WorkflowConfig


def run_server():
    class Parameters(BaseModel):
        choices: List[str] = Field(uniqueItems=True)

    def handler(params: Parameters):
        class JobInput(BaseModel, UiWidget):
            __root__: str

            @classmethod
            def ui_schema(cls):
                return {"ui:help": "Enter the text to label"}

        class JobOutput(BaseModel, UiWidget):
            __root__: str = Field(enum=params.choices)

            @classmethod
            def ui_schema(cls):
                return {"ui:widget": "radio"}

        def metric_func(truths: JobOutput, preds: JobOutput):
            return {"f1_score": {"value": 0.5}}

        def process_job(job_input: JobInput) -> JobOutput:
            index = len(job_input.__root__) % len(params.choices)
            return JobOutput(__root__=params.choices[index])

        def post_process_job(job_output: JobOutput, context: PostProcessContext) -> str:
            return "processed"

        return HandlerOutput(
            input_model=JobInput,
            output_model=JobOutput,
            process_fn=process_job,
            post_process_fn=post_process_job,
            templates=[],
            metrics=[Metric(name="f1_score", metric_fn=metric_func)],
        )

    DPServer(
        params=Parameters(choices=["1", "2"]),
        handler_fn=handler,
        name="Test_Server",
        workflows=[WorkflowConfig("top_heroes", is_default=True), WorkflowConfig("crowd_managers", is_gold=True)],
        template_name="",
        port=8002,
        log_level="critical",
        force_no_tunnel=True,
    ).run()


def local_port_open():
    """Check if there is already a process listening on port 8002
    We use this port for the DP server.
    """
    a_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    location = ("127.0.0.1", 8002)
    result_of_check = a_socket.connect_ex(location)
    return result_of_check == 0


def server_ready(max_wait_secs=10) -> bool:
    """
    Wait until DP Server is ready
    Saves a bit of time compared to a fixed sleep time.
    """
    start = time.time()
    while time.time() - start < max_wait_secs:
        with contextlib.suppress(requests.exceptions.ConnectionError):
            resp = requests.get("http://127.0.0.1:8002/health")
            if resp.status_code == 200:
                return True
        time.sleep(0.2)
    return False


@pytest.fixture(scope="module")
def server():
    if local_port_open():
        raise RuntimeError("Port 8002 is already in use. Is another process running on that port?")
    assert not server_ready()

    proc = Process(target=run_server, args=(), daemon=True)
    proc.start()
    server_ready(max_wait_secs=10)

    yield

    proc.terminate()
    proc.join(timeout=5)


def test_serve_schema_ok(server):
    # assert server is not None
    resp = requests.post("http://127.0.0.1:8002/schema", json={"params": {"choices": ["Dog", "Cat", "UMA"]}})
    expected = json.loads(
        """
        {
            "inputSchema": {
               "title": "JobInput",
               "type": "string"
            },
            "inputUiSchema": {"ui:help": "Enter the text to label"},
            "outputSchema": {
                "enum": ["Dog", "Cat", "UMA"],
                "title": "JobOutput",
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
    resp = requests.post("http://127.0.0.1:8002/schema", json={"params": {"choices": ["Dog", "Dog", "UMA"]}})
    assert resp.json() == expected


def test_metric_names(server):
    expected = json.loads(
        """
       ["f1_score"]
        """
    )
    resp = requests.get("http://127.0.0.1:8002/metrics")
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
        "http://127.0.0.1:8002/metrics/f1_score",
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
        [
            {"methodName": "Test_Server.top_heroes", "role": "normal"},
            {"methodName": "Test_Server.crowd_managers", "role": "normal"},
            {"methodName": "Test_Server.crowd_managers", "role": "gold"}
        ]
        """
    )
    resp = requests.get("http://127.0.0.1:8002/methods")

    assert resp.json() == expected


def test_post_process(server):
    r = PostProcessRequestModel(
        job_uuid="123",
        response={"__root__": "1"},
        app_uuid="123",
        app_params={"params": {"choices": ["Dog", "Cat", "UMA"]}},
    )
    resp = requests.post("http://127.0.0.1:8002/post-process", json=r.dict())

    assert resp.json() == "processed"
