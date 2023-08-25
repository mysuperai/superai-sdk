import os
from typing import Callable, Dict, Optional

from attr import define

from superai import Client
from superai.data_program.protocol.task import (
    WorkflowType,
    input_schema,
    output_schema,
    param_schema,
    workflow,
)
from superai.utils import load_api_key, load_auth_token, load_id_token


class Workflow:
    def __init__(
        self,
        workflow_fn: Callable,
        client: Client = None,
        prefix: str = os.getenv("WF_PREFIX"),
        name: str = None,
        description: str = None,
        dp_definition: "DataProgramDefinition" = None,
        on_init_put: bool = True,
        workflow_type: WorkflowType = WorkflowType.WORKFLOW,
        use_new_schema: bool = False,
        **kwargs,
    ):
        """Args:
        workflow_fn:
        name:
        description:
        dp_definition: A data class that can contain the following attributes: 'input_schema', 'output_schema', 'parameter_schema'.
        prefix: Workflow name prefix which is the Data Program name.
        measure: Should this workflow be measured # TODO: Do we want to expose this here?
        is_gold: Is this the gold workflow? DEFAULT false. If a data program has no gold
        workflow specified, then the _basic method is chosen as gold worfklow. If the _basic is not available, then
         a random workflow is chosen. # TODO: Do we want to expose this here?
        is_default: Is this the default method. DEFAULT: _basic method
        use_new_schema: The workflow uses the new schema format
        """
        self._workflow_fn = workflow_fn
        self._name = name
        self._workflow_type = workflow_type
        self._description = description
        from superai.data_program.types import DataProgramDefinition

        self._dp_definition: DataProgramDefinition = dp_definition
        self._prefix = prefix
        self._client = client or Client(
            api_key=load_api_key(),
            auth_token=load_auth_token(),
            id_token=load_id_token(),
        )
        self.kwargs = kwargs

        self._input_ui_schema = self._dp_definition.input_ui_schema
        self._output_ui_schema = self._dp_definition.output_ui_schema
        self._parameter_ui_schema = self._dp_definition.parameter_ui_schema

        # Some workflow validation and task creation logic relies on knowing if we use the new schema or not
        self._uses_new_schema = use_new_schema or any(
            [self._input_ui_schema, self._output_ui_schema, self._parameter_ui_schema]
        )

        (
            self._input_schema,
            self._output_schema,
            self._parameter_schema,
            self._default_parameter,
        ) = self._dp_definition.parse_args(uses_new_schema=self._uses_new_schema)

        # Adding this to kwargs because the Router will do the schema formatting using the task functions.
        # TODO: Simplify behaviour
        kwargs["input_schema_val"] = self._dp_definition.input_schema
        kwargs["output_schema_val"] = self._dp_definition.output_schema
        if self._dp_definition.parameter_schema:
            kwargs["param_schema_val"] = self._dp_definition.parameter_schema

        if on_init_put:
            self.put()

        if os.environ.get("IN_AGENT"):
            self.subscribe_wf()

    @property
    def input_schema(self):
        return self._input_schema

    @property
    def output_schema(self):
        return self._output_schema

    @property
    def parameter_schema(self):
        return self._parameter_schema

    @property
    def default_parameter(self):
        return self._default_parameter

    @property
    def workflow_fn(self):
        return self._workflow_fn

    @property
    def name(self):
        return self._name

    @property
    def prefix(self):
        return self._prefix or os.environ["WF_PREFIX"]

    @property
    def qualified_name(self):
        return f"{self.prefix}.{self._name}"

    @property
    def description(self):
        return self._description

    def subscribe_wf(self):
        @workflow(
            self.name, prefix=self.prefix, workflow_type=self._workflow_type, uses_new_schema=self._uses_new_schema
        )
        @input_schema(name="inp", schema=self.input_schema, uses_new_schema=self._uses_new_schema)
        @param_schema(
            name="params",
            schema=self.parameter_schema,
            default=self.default_parameter,
            uses_new_schema=self._uses_new_schema,
        )
        @output_schema(schema=self.output_schema, uses_new_schema=self._uses_new_schema)
        def method(inp, params, super_task_params=None):
            if super_task_params:
                return self.workflow_fn(inp, params, super_task_params=super_task_params)
            else:
                return self.workflow_fn(inp, params)

    def put(self) -> Dict:
        """Creates a new workflow entry in the database when the workflow doesn't exist. If the workflow entry
        "<prefix>.<name>" exists, it will be replaced.
        """

        body = {
            "input_schema": self.input_schema,
            "output_schema": self.output_schema,
        }
        if self._dp_definition.parameter_schema:
            body["parameter_schema"] = {"params": self.parameter_schema}

        name = self.name or self.workflow_fn.__name__

        # TODO: Description not supported by nacelle
        # if description is not None:
        #     body_json["description"] = description
        qualified_name = f"{self.prefix}.{name}"

        # TODO: Parse response fields: uuid, created, protocol, defaultAppParams, defaultAppMetrics
        response = self._client.update_workflow(workflow_name=qualified_name, body=body)
        assert "uuid" in response

        return response


@define
class WorkflowConfig:
    name: str
    is_default: bool = False
    is_gold: bool = False
    description: Optional[str] = None
    measure: bool = True
    func: Optional[Callable] = None
