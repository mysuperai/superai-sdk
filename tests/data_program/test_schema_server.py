from typing import List

import pytest
from superai_schema.types import BaseModel, Field, UiWidget

from superai.data_program import Metric
from superai.data_program.dp_server import DPServer
from superai.data_program.types import (
    HandlerOutput,
    PostProcessContext,
    SuperTaskGraphRequestModel,
)
from superai.data_program.workflow import WorkflowConfig

sample_graph = {
    "nodes": [
        {"id": "start", "active": True, "reason": ""},
        {"id": "end", "active": True, "reason": ""},
    ],
    "edges": [{"source": "start", "target": "end", "weight": 1}],
}


@pytest.fixture(scope="module")
def dp_server():
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

        def supertask_graph_fn(super_task_config, app_params):
            return sample_graph

        return HandlerOutput(
            input_model=JobInput,
            output_model=JobOutput,
            process_fn=process_job,
            post_process_fn=post_process_job,
            templates=[],
            metrics=[Metric(name="f1_score", metric_fn=metric_func)],
            super_tasks_graph_fn=supertask_graph_fn,
        )

    yield DPServer(
        params=Parameters(choices=["1", "2"]),
        handler_fn=handler,
        name="Test_Server",
        workflows=[WorkflowConfig("top_heroes", is_default=True), WorkflowConfig("crowd_managers", is_gold=True)],
        template_name="",
        port=8002,
        log_level="critical",
        force_no_tunnel=True,
    )


@pytest.fixture(scope="module")
def test_client(dp_server):
    # Defines fastapi testclient
    from fastapi.testclient import TestClient

    app = dp_server.define_app()
    with TestClient(app) as client:
        yield client


def test_serve_schema_ok(test_client):
    data = {"params": {"choices": ["Dog", "Cat", "UMA"]}}
    response = test_client.post("/schema", json=data)
    expected = {
        "inputSchema": {"title": "JobInput", "type": "string"},
        "inputUiSchema": {"ui:help": "Enter the text to label"},
        "outputSchema": {"enum": ["Dog", "Cat", "UMA"], "title": "JobOutput", "type": "string"},
        "outputUiSchema": {"ui:widget": "radio"},
    }
    assert response.json() == expected


def test_serve_schema_invalid(test_client):
    data = {"params": {"choices": ["Dog", "Dog", "UMA"]}}
    response = test_client.post("/schema", json=data)
    expected = {"detail": "['Dog', 'Dog', 'UMA'] has non-unique elements"}
    assert response.json() == expected


def test_metric_names(test_client):
    response = test_client.get("/metrics")
    expected = ["f1_score"]
    assert response.json() == expected


def test_metric_calculate(test_client):
    data = {
        "truths": [
            {
                "url": "https://farm1.static.flickr.com/22/30133265_5d1a4d6b1e.jpg",
                "annotations": [{"top": 126.49, "left": 56.55, "width": 367.56, "height": 209.82, "selection": "1"}],
            }
        ],
        "preds": [
            {
                "url": "https://farm1.static.flickr.com/22/30133265_5d1a4d6b1e.jpg",
                "annotations": [{"top": 26.49, "left": 51.55, "width": 234.56, "height": 21.82, "selection": "1"}],
            }
        ],
    }
    response = test_client.post("/metrics/f1_score", json=data)
    expected = {"f1_score": {"value": 0.5}}
    assert response.json() == expected


def test_method_names(test_client):
    response = test_client.get("/methods")
    expected = [
        {"methodName": "Test_Server.top_heroes", "role": "normal"},
        {"methodName": "Test_Server.crowd_managers", "role": "normal"},
        {"methodName": "Test_Server.crowd_managers", "role": "gold"},
    ]
    assert response.json() == expected


def test_post_process(test_client):
    data = {
        "job_uuid": "123",
        "response": {"__root__": "1"},
        "app_uuid": "123",
        "app_params": {"params": {"choices": ["Dog", "Cat", "UMA"]}},
    }
    response = test_client.post("/post-process", json=data)
    assert response.json() == "processed"


def test_supertask_graph_error(test_client):
    resp = test_client.post("/super_tasks-graph", params={})
    assert resp.status_code == 422  # missing params


def test_supertask_graph(test_client):
    r = SuperTaskGraphRequestModel(
        app_params={"params": {"choices": ["Dog", "Cat", "UMA"]}},
        super_task_params={"fancy_supertask_mock": "parameters"},
    )
    resp = test_client.post("/super_tasks-graph", json=r.dict())
    assert resp.status_code == 200
    assert resp.json() == sample_graph
