from __future__ import annotations

import json
import os
import shutil
from pathlib import Path
from typing import Dict, List, Optional, Union

import yaml

from superai import Client, settings
from superai.log import logger
from superai.meta_ai.config_parser import TemplateConfig
from superai.meta_ai.environment_file import EnvironmentFileProcessor
from superai.meta_ai.parameters import Config
from superai.meta_ai.schema import Schema
from superai.utils import load_api_key, load_auth_token, load_id_token

log = logger.get_logger(__name__)


class AITemplate:
    def __init__(
        self,
        input_schema: Schema,
        output_schema: Schema,
        configuration: Config,
        name: str,
        description: str,
        model_class: str,
        model_class_path: str = ".",
        requirements: Optional[Union[str, List[str]]] = None,
        code_path: Optional[Union[str, List[str]]] = None,
        conda_env: Optional[Union[str, Dict]] = None,
        artifacts: Optional[Dict] = None,
        client: Client = None,
        bucket_name: str = None,
        parameters=None,
    ):
        """Create an AI template for subsequently creating instances of AI objects

        Args:
            input_schema: Input Schema of the AI Template
            output_schema: Output Schema of the AI Template
            configuration: Configuration of the AI Template
            model_class: Name of instance of a subclass of :class:`~BaseModel`. This file will be moved to the container
                         Any dependencies of the class should be included in one of the following locations:

                            - The SuperAI library.
                            - Package(s) listed in the model's Conda environment, specified by
                              the ``conda_env`` parameter.
                            - One or more of the files specified by the ``code_path`` parameter.

                         Note: If the class is imported from another module, as opposed to being defined in the
                         ``__main__`` scope, the defining module should also be included in code_path parameter.
                         If the name of the instance (Eg. ModelName) is not same as file name of imported module
                         (Eg. some_file.py), please change the passed argument to reflect the correct module path as
                         'some_file.ModelName'
            model_class_path: Path to the location where :param model_class is present
            name: Name of the AI template
            description: Description of the AI template
            requirements: A list of PyPi requirements or the path to a requirements.txt file. If both this
                             parameter and the :param: conda_env is specified an ValueError is raised.
            code_path: A list of local filesystem paths to Python file dependencies (or directories containing file
                          dependencies). These files are *prepended* to the system path before the ai is loaded.
            conda_env: Either a dictionary representation of a Conda environment or the path to a Conda environment
                      yaml file. This describes the environment this AI should be run in. If ``ai_class`` is not
                      ``None``, the Conda environment must at least specify the dependencies contained in
                      :func:`get_default_conda_env()`. If `None`, the default :func:`get_default_conda_env()`
                      environment is added to the AI. The following is an *example* dictionary representation of a
                      Conda environment::

                        {
                            'name': 'superai-env',
                            'channels': ['defaults'],
                            'dependencies': [
                                'python=3.7.2',
                            ]
                        }
            artifacts: A dictionary containing ``<name, artifact_uri>`` entries. Remote artifact URIs are resolved
                      to absolute filesystem paths, producing a dictionary of ``<name, absolute_path>`` entries.
                      ``ai_class`` can reference these resolved entries as the ``artifacts`` property of the
                      ``context`` parameter in
                            - :func:`BaseModel.load_context() <superai.meta_ai.base.BaseModel.load_context>`, and
                            - :func:`BaseModel.predict() <superai.meta_ai.base.BaseModel.predict>`.

                      For example, consider the following ``artifacts`` dictionary::

                        {
                            "my_file": "s3://my-bucket/path/to/my/file"
                        }

                      In this case, the ``"my_file"`` artifact is downloaded from S3. The
                      ``ai_class`` can then refer to ``"my_file"`` as an absolute filesystem
                      path via ``context.artifacts["my_file"]``.

                      If ``None``, no artifacts are added to the model.
            client:
            bucket_name:
            parameters: Optional; Parameters to be passed to the model, could be the model architecture parameters,
                           or training parameters.
                           For example: parameters=MyModel.params_schema.parameters(conv_layers=None,
                                                                    num_conv_layers=None,
                                                                    filter_size=3,
                                                                    num_filters=32,
                                                                    strides=(1, 1),
                                                                    padding='valid',
                                                                    dilation_rate=(1, 1),
                                                                    conv_use_bias=True)
        """
        self.input_schema = input_schema
        self.output_schema = output_schema
        self.configuration = configuration
        self.requirements = requirements
        self.name = name
        self.description = description
        self.code_path = code_path
        self.conda_env = conda_env
        self.artifacts = artifacts
        self.client = (
            client
            if client
            else Client(
                api_key=load_api_key(),
                auth_token=load_auth_token(),
                id_token=load_id_token(),
            )
        )
        self.bucket_name = bucket_name or settings["meta_ai_bucket"]
        self.parameters = parameters
        if model_class is None:
            raise NotImplementedError(
                "Ludwig like implicit model creation is not implemented yet, please provide a model_class"
            )
        self.model_class = model_class
        self.model_class_path = model_class_path
        self.environs: Optional[EnvironmentFileProcessor] = None
        self.template_id = None

    @classmethod
    def load_local(cls, load_path: str) -> "AITemplate":
        with open(os.path.join(load_path, "AITemplateSaveFile.json"), "r") as json_file:
            details = json.load(json_file)
        requirements = os.path.join(load_path, "requirements.txt") if details.get("requirements") is not None else None
        conda_env = os.path.join(load_path, "conda.yml") if details.get("conda_env") is not None else None
        code_path = details.get("code_path")
        artifacts = details.get("artifacts")
        model_class = details["model_class"]
        name = details["name"]
        description = details["description"]
        input_schema = Schema.from_json(details["input_schema"])
        output_schema = Schema.from_json(details["output_schema"])
        configuration = Config.from_json(details["configuration"])
        template = AITemplate(
            input_schema=input_schema,
            output_schema=output_schema,
            configuration=configuration,
            name=name,
            description=description,
            model_class=model_class,
            model_class_path=load_path,
            requirements=requirements,
            code_path=code_path,
            conda_env=conda_env,
            artifacts=artifacts,
        )
        environs = EnvironmentFileProcessor(os.path.abspath(load_path))
        environs.from_dict(details["environs"])
        template.environs = environs
        return template

    def save(self, version_save_path):
        if os.path.exists(f"{self.model_class}.py"):
            shutil.copy(f"{self.model_class}.py", os.path.join(version_save_path, f"{self.model_class}.py"))
        # copy requirements file and conda_env
        if self.conda_env is not None:
            if type(self.conda_env) == dict:
                with open(os.path.join(version_save_path, "environment.yml"), "w") as conda_file:
                    yaml.dump(self.conda_env, conda_file, default_flow_style=False)
            elif (
                type(self.conda_env) == str
                and os.path.exists(os.path.abspath(self.conda_env))
                and (self.conda_env.endswith(".yml") or self.conda_env.endswith(".yaml"))
            ):
                shutil.copy(os.path.abspath(self.conda_env), os.path.join(version_save_path, "environment.yml"))
            else:
                raise ValueError("Make sure conda_env is a valid path to a .yml file or a dictionary.")
        log.info("Copying all code_path content")
        if self.code_path is not None:
            if isinstance(self.code_path, str):
                assert Path(self.code_path).is_dir(), "code_path should point to a directory when passing a string."
                self.code_path = [self.code_path]
            elif isinstance(self.code_path, list):
                assert all(
                    isinstance(path, str) for path in self.code_path
                ), "Types don't match for code_path, please pass a list of strings."
            else:
                raise ValueError("Make sure code_path is a valid path to a directory or a list of files/directories.")
        if self.model_class_path != ".":
            self.code_path = (
                [self.model_class_path] + self.code_path if self.code_path is not None else [self.model_class_path]
            )
        if self.code_path is not None:
            for path in self.code_path:
                if Path(path).is_dir():
                    shutil.copytree(path, os.path.join(version_save_path, os.path.basename(path)))
                elif Path(path).is_file():
                    shutil.copyfile(path, os.path.join(version_save_path, os.path.basename(path)))
                else:
                    raise ValueError(f"{path} does not represent a valid path to a local directory or file.")
        if self.requirements is not None:
            if type(self.requirements) == str and os.path.exists(os.path.abspath(self.requirements)):
                shutil.copy(os.path.abspath(self.requirements), os.path.join(version_save_path, "requirements.txt"))
            elif type(self.requirements) == list:
                with open(os.path.join(version_save_path, "requirements.txt"), "w") as requirements_file:
                    requirements_file.write("\n".join(self.requirements))
            else:
                raise ValueError(
                    "Make sure requirements is a list of requirements or valid path to requirements.txt file"
                )
        if self.artifacts is not None and "run" in self.artifacts:
            shutil.copy(os.path.abspath(self.artifacts["run"]), os.path.join(version_save_path, "setup.sh"))
        # create the environment file
        self.environs = EnvironmentFileProcessor(os.path.abspath(version_save_path), filename="environment")
        self.environs.add_or_update("MODEL_NAME", self.model_class)
        if os.path.exists(os.path.join(version_save_path, "environment.yml")):
            with open(os.path.join(version_save_path, "environment.yml"), "r") as env_yaml:
                try:
                    conda_env_yaml = yaml.safe_load(env_yaml)
                    self.environs.add_or_update("CONDA_ENV_NAME", conda_env_yaml.get("name", "env"))
                except yaml.YAMLError as exc:
                    log.error(exc)
        with open(os.path.join(version_save_path, "AITemplateSaveFile.json"), "w") as ai_template_writer:
            content = {
                "description": self.description,
                "input_schema": self.input_schema.to_json,
                "output_schema": self.output_schema.to_json,
                "configuration": self.configuration.to_json,
                "name": self.name,
                "requirements": os.path.join(version_save_path, "requirements.txt")
                if self.requirements is not None
                else None,
                "code_path": self.code_path,
                "conda_env": os.path.join(version_save_path, "conda.yml") if self.conda_env is not None else None,
                "model_class": self.model_class,
                "model_class_path": self.model_class_path,
                "artifacts": self.artifacts,
                "environs": self.environs.to_dict(),
            }
            json.dump(content, ai_template_writer, indent=1)

    def get_or_create_training_entry(self, model_id: str, app_id: str = None, properties: dict = {}):
        existing_template_id = self.client.get_training_templates(model_id=model_id, app_id=app_id)
        if len(existing_template_id):
            log.info(f"Found existing template {existing_template_id}")
            self.template_id = existing_template_id[0].id
        else:
            template_id = self.client.create_training_template_entry(
                model_id=model_id, properties=properties, app_id=app_id
            )
            log.info(f"Created template : {template_id}")
            self.template_id = template_id
        return self.template_id

    @classmethod
    def from_settings(cls, template: TemplateConfig) -> AITemplate:
        if template.input_schema is None:
            input_schema = Schema()
        elif isinstance(template.input_schema, str):
            input_schema = Schema.from_json(json.loads(template.input_schema))
        else:
            input_schema = Schema.from_json(template.input_schema)

        if template.output_schema is None:
            output_schema = Schema()
        elif isinstance(template.output_schema, str):
            output_schema = Schema.from_json(json.loads(template.output_schema))
        else:
            output_schema = Schema.from_json(template.output_schema)

        if template.configuration is None:
            configuration = Config()
        elif isinstance(template.configuration, str):
            configuration = Config.from_json(json.loads(template.configuration))
        else:
            configuration = Config.from_json(template.configuration)

        return AITemplate(
            input_schema=input_schema,
            output_schema=output_schema,
            configuration=configuration,
            name=template.name,
            description=template.description,
            model_class=template.model_class,
            model_class_path=template.model_class_path,
            requirements=template.requirements,
            code_path=template.code_path,
            conda_env=template.conda_env,
            artifacts=template.artifacts,
            bucket_name=template.bucket_name,
            parameters=template.parameters,
        )
