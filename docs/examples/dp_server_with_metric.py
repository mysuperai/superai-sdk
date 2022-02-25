from typing import List

from superai_schema.types import BaseModel, Field, UiWidget

from superai.data_program.dp_server import DPServer, Metric, WorkflowConfig


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
        assert len(truths) == len(preds), "Length of truths and preds should be same"
        for t, p in zip(truths, preds):
            MyOutput.validate(t)
            MyOutput.validate(p)

        return {"f1_score": {"value": 0.5}}

    def process_job(job_input: MyInput) -> MyOutput:
        index = len(job_input.__root__) % len(params.choices)
        return MyOutput(__root__=params.choices[index])

    return MyInput, MyOutput, process_job, [], [Metric(name="f1_score", metric_fn=metric_func)]


DPServer(
    params=Parameters(choices=["1", "2"]),
    name="Test_Server",
    generate=handler,
    workflows=[WorkflowConfig("top_heroes", is_default=True), WorkflowConfig("crowd_managers", is_gold=True)],
).run()
