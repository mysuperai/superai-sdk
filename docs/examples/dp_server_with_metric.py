from typing import List

from superai_schema.types import BaseModel, Field, UiWidget

from superai.data_program.dp_server import DPServer
from superai.data_program.types import HandlerOutput, Metric, WorkflowConfig


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

    def metric_func(truths: List[JobOutput], preds: List[JobOutput]):
        assert len(truths) == len(preds), "Length of truths and preds should be the same"
        for t, p in zip(truths, preds):
            JobOutput.validate(t)
            JobOutput.validate(p)

        return {"f1_score": {"value": 0.5}}

    def process_job(job_input: JobInput) -> JobOutput:
        index = len(job_input.__root__) % len(params.choices)
        return JobOutput(__root__=params.choices[index])

    return HandlerOutput(
        input_model=JobInput,
        output_model=JobOutput,
        process_fn=process_job,
        templates=[],
        metrics=[Metric(name="f1_score", metric_fn=metric_func)],
    )


DPServer(
    params=Parameters(choices=["1", "2"]),
    name="Test_Server",
    generate=handler,
    workflows=[WorkflowConfig("top_heroes", is_default=True), WorkflowConfig("crowd_managers", is_gold=True)],
    template_name="",  # template name should be empty, we don't want the reverse proxy
    port=8002,
    log_level="critical",
).run()
