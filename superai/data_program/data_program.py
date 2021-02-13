####
import inspect
import os
from typing import Callable, Dict, List, Optional

from superai_schema.generators import dynamic_generator
from superai_schema.universal_schema import task_schema_functions as df

from superai import Client
from superai.data_program import Workflow
from superai.data_program.base import DataProgramBase
from superai.data_program.Exceptions import UnknownTaskStatus
from superai.data_program.protocol.task import task as task
from superai.data_program.router import BasicRouter, Router
from superai.data_program.utils import parse_dp_definition
from superai.log import logger
from superai.utils import load_api_key, load_auth_token, load_id_token

log = logger.get_logger(__name__)


class DataProgram(DataProgramBase):
    def __init__(
        self,
        name: str,
        definition: Dict = {},
        description: str = None,
        add_basic_workflow: bool = True,
        client: Client = None,
        router: Router = None,
        **kwargs,
    ):
        super().__init__(add_basic_workflow=add_basic_workflow)
        assert "input_schema" in definition
        assert "output_schema" in definition
        self.client = (
            client if client else Client(api_key=load_api_key(), auth_token=load_auth_token(), id_token=load_id_token())
        )
        # FIXME: Needs to register default_workflow, and workflows... not the router
        self.__dict__.update(definition)
        self.dp_definition = definition
        (
            self.input_schema,
            self.output_schema,
            self.parameter_schema,
        ) = parse_dp_definition(definition)

        self._default_workflow: str = None
        self._gold_workflow: str = None
        self.name, self.template_name = name, name
        self.__validate_name()
        self.qualified_name = f"{self.name}.router"

        self.description = description
        self.router = router
        self.task_templates = []
        self.workflows: List[Workflow] = []

        # TODO:
        #  1. Add version support: The current idea is to have a new version when something changes in any of the
        #     schemas (input, output, params)
        #  2. Link to code repository

        self.__template_object = self.__create_template()
        log.info(f"DataProgram created {self.qualified_name}")

    @property
    def gold_workflow(self) -> str:
        return self._gold_workflow

    @gold_workflow.setter
    def gold_workflow(self, workflow_name: str):
        self._gold_workflow = f"{self.name}.{workflow_name}"

    @property
    def default_workflow(self) -> str:
        if not hasattr(self, "_default_workflow") or not self._default_workflow:
            self._default_workflow = self.__load_default_workflow()

        return self._default_workflow

    @default_workflow.setter
    def default_workflow(self, workflow_name):
        # TODO: Verify workflow exists
        # TODO: Verify workflow name doesn't contain prefix
        if not workflow_name:
            self._default_workflow = self.__load_default_workflow()
        else:
            body = {"default_workflow": f"{self.template_name}.{workflow_name}"}
            template_update = self.client.update_template(template_name=self.template_name, body=body)
            assert template_update.get("defaultWorkflow")
            self._default_workflow = template_update.get("defaultWorkflow")

    def __validate_name(self):
        if not self.name:
            raise ValueError("DataProgramTemplate.name can not be None")
        if len(self.name.split(".")) > 1:
            raise ValueError('DataProgramTemplate.name can not contain "." characters')

    def __load_default_workflow(self):
        default_workflow = None
        try:
            default_workflow = self.client.get_template(self.template_name).get("default_workflow")
        except Exception as e:
            log.error(f"Error retrieving default workflow : {e}")

        return default_workflow

    def __create_template(self) -> Dict:
        """
            TODO: 1.Handle versions: This means that the API should a) Find if a tempalte with the same name exists,
                        b) if the templat exists, check that the input and output schema are the same and if so then
                        simply return the existing dataprogram. If the input or output schema are different, create a new
                        dataprogram with and increase the version
        Create a data program dataprogram
        :param input_schema:
        :param output_schema:
        :param parameter_schema:
        :return:
        """
        body_json = {
            "input_schema": self.input_schema,
            "output_schema": self.output_schema,
        }
        name = self.qualified_name
        if self.parameter_schema is not None:
            body_json["parameter_schema"] = {"params": self.parameter_schema}
        if self.description is not None:
            body_json["description"] = self.description

        body_json["metadata"] = dynamic_generator.create_metadata_boilerplate(
            input_schema=self.input_schema,
            output_schema=self.output_schema,
            param_schema=self.parameter_schema,
            name=name,
            description=self.description,
        )
        # TODO:
        #  1. When duplicated dataprogram exists Nacelle responds with:
        #     requests.exceptions.HTTPError: 400 Client Error: BAD REQUEST for url:
        #     http://0.0.0.0:5000/v1/templates/jennifer_pvf.router
        #     -> Should respond with a meaningful response
        response = self.client.create_template(template_name=name, body=body_json)

        # TODO: Create models/template which takes a template object and validates the respone from nacelle
        assert "uuid" in response
        assert "name" in response and response["name"].split(".")[0] == self.name
        self.template_uuid = response["uuid"]
        return response

    def _add_workflow_obj(self, workflow: Workflow, default: bool = None, gold: bool = None) -> Optional[dict]:
        self.workflows.append(workflow)

        if default:
            self.default_workflow = workflow.name

        if gold:
            self.gold_workflow = workflow.name

        # Everything after this line can be ignored once the data program™ is already deployed
        if os.environ.get("IN_AGENT"):
            log.info(f"[DataProgramTemplate.add_workflow] ignoring because IN_AGENT = " f"{os.environ.get('IN_AGENT')}")
            return

        workflow_dict = workflow.put()
        assert workflow_dict.get("name") == workflow.qualified_name
        self._register_workflow(workflow)

        return workflow_dict

    def add_workflow(
        self, workflow: Callable, name: str = None, description: str = None, default: bool = False, gold: bool = False
    ) -> Dict:
        """
        Assuming that if the _basic workflow is not deployed then the first workflow added will be the default and gold workflow
        :param workflow:
        :param name:
        :param description:
        :return:
        """
        # TODO: Check that the workflow function can take inputs and params arguments
        #          inspect.getfullargspec(workflow).args is one option

        kkwargs = dict()
        if not self.add_basic_workflow and len(self.workflows) < 1:
            default = True
            gold = True

        workflow = Workflow(
            prefix=self.name,
            workflow_fn=workflow,
            name=name,
            description=description,
            dp_definition=self.dp_definition,
            **kkwargs,
        )
        return self._add_workflow_obj(workflow=workflow, default=default, gold=gold)

    def __add_basic_workflow(self):
        exists = next(filter(lambda w: w.name == "_basic", self.workflows), None)
        if not exists and self.add_basic_workflow:

            def _basic(*args, **kwargs):
                log.debug(f"{self.name}._basic:Arguments: *args: {args}, **kwargs: {kwargs} ")
                log.debug(f"{self.name}._basic:inputSchema: {self.__template_object.get('inputSchema')}")
                log.debug(f"{self.name}._basic:outputSchema: {self.__template_object.get('outputSchema')}")
                log.debug(f"{self.name}._basic:appParamsSchema: {self.__template_object.get('appParamsSchema')}")
                """
                Simple workflow generated by schemas
                """
                # TODO: Retry functionality (definition_v1)
                n_tries = 1

                inputs = args[0]

                if len(args) > 1:
                    params = args[1]
                else:
                    params = kwargs.get("params", {})

                # TODO: Introduce support for task schemas (definition_v1, v2)
                #   1. Handle case where the output/param schema is not created with task_schema_functions
                # task_definition = {
                #     "input_schema": self.dp_definition['input_schema'],
                #     "output_schema": self.dp_definition['output_schema']
                # }
                # task1 = Task(task_definition)

                # TODO:
                #  1. <PARTIAL> Traverse input schema and feed task correctly
                #  2. <PARTIAL> Traverse params schema and get instructions
                #  3. What if the expected field doesn't exist? Fail fast on validation

                # FIXME: This implementation is not production ready, won't generalize
                input_schema = self.__template_object.get("inputSchema")
                task_inputs = []

                # Adding instructions
                if params and isinstance(params, dict) and params.get("instructions"):
                    task_inputs.append(df.text(params.get("instructions", "")))

                # Using the schema types to create a function handler from task_schema_functions
                for k, v in input_schema.get("properties", {}).items():  # TODO: Handle types recursively
                    schema_fun = getattr(
                        df, v.get("$ref").replace("-", "_")
                    )  # FIXME: Will throw an exception if the function is not in df
                    task_inputs.append(schema_fun(inputs.get(k)))
                log.info(f"{self.name}._basic:TaskInputs {task_inputs}")
                if None in task_inputs:
                    raise Exception(f"Task inputs could not get generated. Schema={input_schema}," f"Inputs={inputs}")

                # TODO:
                #  1. Support output schemas that were generated using task_schema_functions
                #  2. <SOLVED> Get all properties in output
                #  3. How do we know that the output requires choices?
                # FIXME: This implementation is not production ready, won't generalize
                output_schema = self.__template_object.get("outputSchema")
                task_outputs = []
                job_output_keys = []

                # TODO:
                #  1. Handle types recursively
                for k, v in output_schema.get("properties", {}).items():
                    # FIXME:
                    #  1. Will throw an exception if the function is not in df
                    #  2. <SOLVED> Get rid of "choices" and find if it is required input
                    schema_fun = getattr(df, v.get("$ref").replace("-", "_"))
                    args = inspect.getfullargspec(schema_fun).args
                    log.info(f"{self.name}._basic:schema_fun args {args}")
                    kkwargs = {}
                    for arg in args:
                        if arg in params:
                            kkwargs[arg] = params[arg]

                    log.info(f"{self.name}._basic:TaskSchemaFun kkwargs {kkwargs}")
                    task_outputs.append(schema_fun(**kkwargs))
                    job_output_keys.append(k)

                log.info(f"{self.name}._basic:TaskOutputs {task_outputs}")
                if None in task_outputs:
                    raise Exception(
                        f"Task outputs could not get generated. Schema={output_schema}, " f"Params={params}"
                    )
                task_result = task(
                    input=task_inputs,
                    output=task_outputs,
                    name=f"{self.name}_basic",
                    price="EASY",
                    qualifications=None,
                    groups=None,
                    time_to_expire_secs=1 * 60 * 10,
                    excluded_ids=None,
                    show_reject=False,
                    amount=None,
                ).result()
                log.info(f"task status {task_result.status()} with response: {task_result.response()}")
                if task_result.status() == "COMPLETED":
                    # TODO: Handle task failure cases like in resend_task
                    log.info(f"task succeeded with response: {task_result.response()}")
                    if len(task_result.response()) > 0:
                        log.info(f"ENRIQUE_TASK_RESULT {task_result.response()}")
                        # return task_result
                    else:
                        log.info("WARNING: completed task, but empty task response.")
                        # log.info("resending task, trial no. ", n_tries + 1)
                        # continue
                elif task_result.status() in ["EXPIRED", "REJECTED"]:
                    log.info(f"WARNING: task status is {task_result.status()}")
                    # log.info("resending task, trial no. ", n_tries + 1)
                    # continue
                else:
                    raise UnknownTaskStatus(str(task_result.status()))

                output = {
                    key: task_result.response().get("values", [])[i].get("schema_instance")
                    for i, key in enumerate(job_output_keys)
                }
                log.info(f"{self.name}._basic:JobOutput {output}")
                return output

            workflow = Workflow(
                prefix=self.name,
                name="_basic",
                workflow_fn=_basic,
                description="basic workflow",
                dp_definition=self.dp_definition,
            )
            return self._add_workflow_obj(workflow, default=True, gold=True)

    def __init_router(self):
        self.__add_basic_workflow()

        if not self.router:
            self.router = BasicRouter(client=self.client, dataprorgam=self)

    def start(self):
        self.__init_router()
        self._run_local()

    def _register_workflow(self, workflow):
        template = self.client.get_template(template_name=self.name)
        workflow_list: List[str] = template.get("dpWorkflows", []) or []
        if workflow.qualified_name in workflow_list:
            return
        else:
            workflow_list.append(workflow.qualified_name)
            body = {"workflows": workflow_list}
            template_udpate = self.client.update_template(template_name=self.name, body=body)
            assert workflow.qualified_name in template_udpate.get("dpWorkflows")
