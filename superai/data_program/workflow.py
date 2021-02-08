import os
from typing import Callable, Dict

from superai import Client
from superai.data_program.protocol.task import (
    input_schema,
    output_schema,
    param_schema,
    workflow,
)
from superai.data_program.utils import parse_dp_definition
from superai.utils import load_api_key, load_auth_token, load_id_token


class Workflow:
    def __init__(
        self,
        workflow_fn: Callable,
        client: Client = None,
        prefix: str = os.getenv("WF_PREFIX"),
        name: str = None,
        description: str = None,
        dp_definition: dict = None,
        on_init_put: bool = True,
        **kwargs,
    ):
        """

        :param Callable workflow_fn:
        :param string name:
        :param string description:
        :param dict dp_definition: A dictionary that can contain the following keys:
            'input_schema', 'output_schema', 'parameter_schema'

        :param string prefix: Workflow name prefix which is the data program name
        :param boolean measure: Should this workflow be measured # TODO: Do we want to expose this here?
        :param boolean is_gold: Is this the gold workflow? DEFAULT false. If a data program has no gold
            workflow specified then the _basic method is chosen as gold worfklow. If the _basic is not available then
             a random workflow is chosen. # TODO: Do we want to expose this here?
        :param boolean is_default: Is this the default method. DEFAULT: _basic method
        """
        self._workflow_fn = workflow_fn
        self._name = name
        self._description = description
        self._dp_definition = dp_definition
        self._prefix = prefix
        self._client = (
            client if client else Client(api_key=load_api_key(), auth_token=load_auth_token(), id_token=load_id_token())
        )
        self.kwargs = kwargs
        (
            self._input_schema,
            self._output_schema,
            self._parameter_schema,
        ) = parse_dp_definition(dp_definition)

        # Adding this to kwargs because the Router will do the schema formatting using the task functions.
        # TODO: Simplify behaviour
        kwargs["input_schema_val"] = dp_definition.get("input_schema")
        kwargs["output_schema_val"] = dp_definition.get("output_schema")
        if dp_definition.get("parameter_schema"):
            kwargs["param_schema_val"] = dp_definition.get("parameter_schema")

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
    def workflow_fn(self):
        return self._workflow_fn

    @property
    def name(self):
        return self._name

    @property
    def prefix(self):
        return self._prefix

    @property
    def qualified_name(self):
        return f"{self.prefix}.{self._name}"

    @property
    def description(self):
        return self._description

    def subscribe_wf(self):
        @workflow(self.name, prefix=self.prefix)
        @input_schema(name="inp", schema=self.input_schema)
        @param_schema(name="params", schema=self.parameter_schema)
        @output_schema(schema=self.output_schema)
        def method(inp, params):
            return self.workflow_fn(inp, params)

    def put(self) -> Dict:
        """
        Creates a new workflow entry in the database if the workflow didn't exist. If the workflow entry
        "<prefix>.<name>" exists, it will be replaced.

        :return:
        """

        body = {
            "input_schema": self.input_schema,
            "output_schema": self.output_schema,
        }
        if self._dp_definition.get("parameter_schema"):
            body["parameter_schema"] = {"params": self.parameter_schema}

        name = self.name if self.name else self.workflow_fn.__name__

        # TODO: Description not supported by nacelle
        # if description is not None:
        #     body_json["description"] = description
        qualified_name = f"{self.prefix}.{name}"

        # TODO: Parse response fields: uuid, created, protocol, defaultAppParams, defaultAppMetrics
        response = self._client.update_workflow(workflow_name=qualified_name, body=body)
        assert "uuid" in response

        return response
