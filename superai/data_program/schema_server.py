from typing import Type, Generic

import fastapi
import uvicorn
from fastapi import HTTPException
from jsonschema import validate, ValidationError
from pydantic import BaseModel
from superai_schema.types import UiWidget
from typing_extensions import Literal

from superai.data_program.types import Handler, Parameters, SchemaServerResponse, Output, Input


class SchemaServer(Generic[Parameters, Input, Output]):
    params_model: Type[Parameters]
    params_schema: dict
    generate: Handler[Parameters, Input, Output]
    log_level: Literal["critical", "error", "warning", "info", "debug", "trace"]

    def __init__(
        self,
        params_model: Type[Parameters],
        generate: Handler[Parameters, Input, Output],
        log_level: Literal["critical", "error", "warning", "info", "debug", "trace"] = "info",
    ):
        self.params_model = params_model
        self.params_schema = self.params_model.schema()
        self.generate = generate
        self.log_level = log_level

    def run(self):
        app = fastapi.FastAPI()
        cls = self.params_model

        class RequestModel(BaseModel):
            params: cls

        @app.post("/schema", response_model=SchemaServerResponse)
        def handle_post(app_params: RequestModel) -> SchemaServerResponse:
            input_model, output_model, _ = self.generate(app_params.params)

            try:
                # FastAPI's request body parser seems to ignore some directives
                # in JSON schema (e.g. `uniqueItems`) so I need to validate again
                validate(app_params.params.dict(), self.params_schema)
            except ValidationError as e:
                raise HTTPException(status_code=422, detail=f"{e.message}")

            return SchemaServerResponse(
                inputSchema=input_model.schema(),
                inputUiSchema=input_model.ui_schema() if issubclass(input_model, UiWidget) else {},
                outputSchema=output_model.schema(),
                outputUiSchema=output_model.ui_schema() if issubclass(output_model, UiWidget) else {},
            )

        uvicorn.run(app, host="0.0.0.0", port=8001, log_level=self.log_level)
