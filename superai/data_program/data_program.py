import inspect
import json
import os
from typing import Callable, Dict, List, Optional, Type

from pydantic import ValidationError
from superai_schema.generators import dynamic_generator
from superai_schema.types import UiWidget
from superai_schema.universal_schema import task_schema_functions as df

from superai import Client
from superai.data_program import Task, Workflow
from superai.data_program.base import DataProgramBase
from superai.data_program.dp_server import DPServer
from superai.data_program.Exceptions import UnknownTaskStatus
from superai.data_program.protocol.task import task as task
from superai.data_program.router import BasicRouter, Router
from superai.data_program.router.training import Training
from superai.data_program.types import (
    DataProgramDefinition,
    Handler,
    Input,
    JobContext,
    Output,
    Parameters,
    PostProcessContext,
    TaskResponse,
    TaskTemplate,
    WorkflowConfig,
)
from superai.data_program.utils import model_to_task_io_payload, parse_dp_definition
from superai.log import logger
from superai.utils import load_api_key, load_auth_token, load_id_token

log = logger.get_logger(__name__)


class DataProgram(DataProgramBase):
    def __init__(
        self,
        name: str,
        definition: DataProgramDefinition,
        description: str = None,
        add_basic_workflow: bool = True,
        client: Client = None,
        router: Router = None,
        metadata: dict = None,
        auto_generate_metadata: bool = True,
        dataprogram: str = None,
        dataprogram_suffix: str = "router",
        **kwargs,
    ):
        super().__init__(add_basic_workflow=add_basic_workflow)
        assert "input_schema" in definition
        assert "output_schema" in definition
        self.client = (
            client
            if client
            else Client(
                api_key=load_api_key(),
                auth_token=load_auth_token(),
                id_token=load_id_token(),
            )
        )
        # FIXME: Needs to register default_workflow, and workflows... not the router
        self.__dict__.update(definition)
        self.dp_definition = definition
        (
            self.input_schema,
            self.output_schema,
            self.parameter_schema,
            self.default_parameter,
            self.input_ui_schema,
            self.output_ui_schema,
            self.parameter_ui_schema,
        ) = parse_dp_definition(definition)

        self._default_workflow: str = None
        self._gold_workflow: str = None
        self.name = name
        self.__validate_name()

        suffix = "router"
        self.is_training = False
        if dataprogram is not None:
            self.parent_workflow = f"{dataprogram}.{dataprogram_suffix}"
            self.is_training = True
            suffix = "training"
        self.qualified_name = f"{self.name}.{suffix}"
        self.description = description
        self.router = router
        self.task_templates = []
        self.workflows: List[Workflow] = []

        # TODO:
        #  1. Add version support: The current idea is to have a new version when something changes in any of the
        #     schemas (input, output, params)
        #  2. Link to code repository

        self.metadata = (
            dynamic_generator.create_metadata_boilerplate(
                input_schema=self.input_schema,
                output_schema=self.output_schema,
                param_schema=self.parameter_schema,
                name=name,
                description=self.description,
            )
            if metadata == None and auto_generate_metadata
            else metadata
        )

        self.__template_object = self.__create_template()
        if self.is_training:
            self.__update_parent_training_workflow()
        log.info(f"DataProgram created {self.qualified_name}")

    @staticmethod
    def run(
        *,
        default_params: Parameters,
        handler: Handler[Parameters],
        workflows: List[WorkflowConfig],
        metadata: dict = None,
        auto_generate_metadata: bool = True,
    ):
        # TODO: Fix: start the DP without legacy dependencies
        from canotic.hatchery import hatchery_config
        from canotic.qumes_transport import start_threads

        name = os.getenv("WF_PREFIX")
        if len(workflows) == 1 and (workflows[0].is_default != True or workflows[0].is_gold != True):
            log.info("WARNING: The only workflow should be default and gold")
            workflows[0].is_default = True
            workflows[0].is_gold = True
        else:
            assert len(list(filter(lambda w: w.is_default, workflows))) == 1, "There should be one default workflow"
            assert len(list(filter(lambda w: w.is_gold, workflows))) == 1, "There should be one gold workflow"

        # Setting the SERVICE env variable indicates that we are running the Data Program as a service
        service = os.getenv("SERVICE")
        params_cls = default_params.__class__

        if name is None:
            raise Exception("Environment variable 'WF_PREFIX' is missing.")

        if service is None:
            raise Exception(
                """Environment variable 'SERVICE' is missing.
If you are running data program with 'canotic deploy' command,
make sure to pass `--serve-schema` in order to opt-in schema server."""
            )

        if hatchery_config.get_transport_backend_config() != "qumes":
            raise Exception("Non Qumes transport is not supported by this API.")

        if service == "data_program":
            log.info("Starting data_program service...")

            log.info("Setting CANOTIC_AGENT=1 and IN_AGENT=YES")
            os.environ["CANOTIC_AGENT"] = "1"
            os.environ["IN_AGENT"] = "YES"

            training_dataprogram = os.getenv("TRAINING_DATAPROGRAM")
            is_training = training_dataprogram is not None and training_dataprogram != name
            default_definition = DataProgram._get_definition_for_params(default_params, handler)
            dp = DataProgram(
                name=name,
                metadata=metadata,
                add_basic_workflow=False,
                definition=default_definition,
                auto_generate_metadata=auto_generate_metadata,
                dataprogram=training_dataprogram if is_training else None,
            )

            dp.check_workflow_deletion(workflows)
            for workflow_config in workflows:
                dp._add_workflow_by_config(workflow_config, params_cls, handler)

            dp.__init_router()
            start_threads()
            return

        if service == "schema":
            log.info("Starting schema service...")
            DPServer(default_params, handler, name=name, workflows=workflows).run()
            return

        raise Exception(f"{service} is invalid service. 'data_program' or 'schema' is available.")

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

    def check_workflow_deletion(self, new_workflows):
        template = self.client.get_template(template_name=self.name)
        old_workflows_names: List[str] = template.get("dpWorkflows", []) or []

        new_workflows_names = [self.name + "." + new_workflow.name for new_workflow in new_workflows]

        if any(item not in new_workflows_names for item in old_workflows_names):
            # Can't delete workflows!
            raise Exception("DP deployment failed, you're trying to remove workflows, use the CLI for that")

    @default_workflow.setter
    def default_workflow(self, workflow_name):
        # TODO: Verify workflow exists
        # TODO: Verify workflow name doesn't contain prefix
        if not workflow_name:
            self._default_workflow = self.__load_default_workflow()
        else:
            body = {"default_workflow": f"{self.name}.{workflow_name}"}
            updated_template = self.client.update_template(template_name=self.qualified_name, body=body)
            assert updated_template.get("defaultWorkflow")
            self._default_workflow = updated_template.get("defaultWorkflow")

    def __validate_name(self):
        if not self.name:
            raise ValueError("DataProgramTemplate.name can not be None")
        if len(self.name.split(".")) > 1:
            raise ValueError('DataProgramTemplate.name can not contain "." characters')

    def __load_default_workflow(self):
        default_workflow = None
        try:
            default_workflow = self.client.get_template(self.qualified_name).get("default_workflow")
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
            "input_ui_schema": self.input_ui_schema,
            "output_schema": self.output_schema,
            "output_ui_schema": self.output_ui_schema,
        }
        name = self.qualified_name
        if self.parameter_schema is not None:
            body_json["parameter_schema"] = {"params": self.parameter_schema}
        if self.parameter_ui_schema is not None:
            body_json["parameter_ui_schema"] = {"params": self.parameter_ui_schema}
        if self.default_parameter is not None:
            body_json["default_app_params"] = self.default_parameter
        if self.description is not None:
            body_json["description"] = self.description
        if self.metadata is not None:
            body_json["metadata"] = self.metadata

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

    def __update_parent_training_workflow(self) -> Dict:
        """Updates the training workflow in the parent workflow"""
        body_json = {"training_workflow": self.qualified_name}

        response = self.client.update_template(template_name=self.parent_workflow, body=body_json)

        assert "uuid" in response
        return response

    def _add_workflow_obj(self, workflow: Workflow, default: bool = None, gold: bool = None) -> Optional[dict]:
        self.workflows.append(workflow)

        if default:
            self.default_workflow = workflow.name

        if gold:
            self.gold_workflow = workflow.name

        self._register_workflow(workflow)
        # Everything after this line can be ignored once the data program™ is already deployed
        if os.environ.get("IN_AGENT"):
            log.info(f"[DataProgramTemplate.add_workflow] ignoring because IN_AGENT = " f"{os.environ.get('IN_AGENT')}")
            return

        workflow_dict = workflow.put()
        assert workflow_dict.get("name") == workflow.qualified_name

        return workflow_dict

    def add_workflow(
        self,
        workflow: Callable,
        name: str = None,
        description: str = None,
        default: bool = False,
        gold: bool = False,
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

    def _add_workflow_by_config(
        self,
        workflow: WorkflowConfig,
        params_cls: Type[Parameters],
        handler: Handler[Parameters],
    ):
        if self.is_training and not workflow.is_default:
            return

        def workflow_fn(inp, params):
            params_model = params_cls.parse_obj(params)
            handler_output = handler(params_model)
            process_job = handler_output.process_fn
            post_process_job = handler_output.post_process_fn

            # Load raw job input into model with validation
            job_input_model_cls = handler_output.input_model
            job_input_model = job_input_model_cls.parse_obj(inp)

            if not (handler_output.templates or len(handler_output.templates) < 1):

                def send_task(
                    name: str,
                    *,
                    task_template: TaskTemplate,
                    task_input: Input,
                    task_output: Output,
                    max_attempts: int,
                    excluded_ids: List[int] = None,
                ) -> None:
                    raise NotImplementedError("Can't send a task with no templates defined")

            else:

                def send_task(
                    name: str,
                    *,
                    task_template: TaskTemplate,
                    task_input: Input,
                    task_output: Output,
                    max_attempts: int,
                    excluded_ids: List[int] = None,
                ) -> Output:
                    # checks task input type
                    if not isinstance(task_input, task_template.input):
                        raise ValidationError("The input type is not the one in the task template")

                    my_task = Task(name=name, max_attempts=max_attempts)
                    my_task.process(
                        model_to_task_io_payload(task_input),
                        model_to_task_io_payload(task_output),
                        excluded_ids=excluded_ids,
                    )
                    raw_result = my_task.output["values"]["formData"]
                    output = task_output.parse_obj(raw_result)

                    # check task output type
                    if not isinstance(output, task_template.output):
                        raise ValidationError("The output type is not the one in the task template")

                    return TaskResponse[Output](
                        task_output=output,
                        hero_id=my_task.output["hero"]["workerId"],
                    )

            job_context = JobContext[Output](
                workflow,
                send_task,
                use_job_cache=bool(post_process_job),
                is_training=self.is_training,
            )
            job_output = process_job(job_input_model, job_context)

            if post_process_job is not None:
                context = PostProcessContext(job_cache=job_context.job_cache)
                response_data = post_process_job(job_output, context)

                return (
                    json.loads(job_output.json(exclude_unset=True)),
                    response_data,
                    None,
                )

            return json.loads(job_output.json(exclude_unset=True))

        self.add_workflow(
            name=workflow.name,
            description=workflow.description,
            workflow=workflow_fn,
            default=workflow.is_default,
            gold=workflow.is_gold,
        )

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
                # TODO: Handle types recursively
                for k, v in input_schema.get("properties", {}).items():
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
                        log.info(f"TASK_RESULT {task_result.response()}")
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
            self.router = (
                Training(client=self.client, training_dataprogram=self)
                if self.is_training
                else BasicRouter(client=self.client, dataprogram=self)
            )

    def start(self):
        self.__init_router()
        self._run_local()

    def _register_workflow(self, workflow: Workflow):
        template = self.client.get_template(template_name=self.qualified_name)
        workflow_list: List[str] = template.get("dpWorkflows", []) or []
        if workflow.qualified_name in workflow_list:
            return
        else:
            workflow_list.append(workflow.qualified_name)
            body = {"workflows": workflow_list}
            updated_template = self.client.update_template(template_name=self.qualified_name, body=body)
            assert workflow.qualified_name in updated_template.get("dpWorkflows")

    @staticmethod
    def _get_definition_for_params(params: Parameters, handler: Handler[Parameters]) -> DataProgramDefinition:
        param_schema = params.schema()
        handler_output = handler(params)
        input_model, output_model = (
            handler_output.input_model,
            handler_output.output_model,
        )

        return {
            "parameter_schema": param_schema if param_schema else None,
            "parameter_ui_schema": params.ui_schema() if isinstance(params, UiWidget) else {},
            "input_schema": input_model.schema(),
            "input_ui_schema": input_model.ui_schema() if issubclass(input_model, UiWidget) else {},
            "output_schema": output_model.schema(),
            "output_ui_schema": output_model.ui_schema() if issubclass(output_model, UiWidget) else {},
            "default_parameter": json.loads(params.json(exclude_none=True)),
        }
