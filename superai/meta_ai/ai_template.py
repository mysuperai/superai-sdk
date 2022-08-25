from __future__ import annotations

import json
import os
from pathlib import Path
from shutil import copy, copytree, ignore_patterns
from typing import Dict, List, Optional, Union

import yaml

from superai import Client, settings
from superai.log import logger
from superai.meta_ai.config_parser import TemplateConfig
from superai.meta_ai.environment_file import EnvironmentFileProcessor
from superai.meta_ai.parameters import AiDeploymentParameters, Config
from superai.meta_ai.schema import Schema
from superai.utils import load_api_key, load_auth_token, load_id_token

ENV_VAR_FILENAME = "environment"
CONDA_ENV_FILE_NAME = "environment.yml"
REQUIREMENTS_FILE_NAME = "requirements.txt"
ARTIFACT_SETUP_SCRIPT_NAME = "setup.sh"
TEMPLATE_SAVE_FILE_NAME = "AITemplateSaveFile.json"

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
        model_class_path: Union[str, Path] = ".",
        requirements: Optional[Union[str, List[str]]] = None,
        code_path: Optional[Union[str, List[str], Path, List[Path]]] = None,
        conda_env: Optional[Union[str, Dict]] = None,
        artifacts: Optional[Dict] = None,
        client: Client = None,
        bucket_name: str = None,
        parameters=None,
        deployment_parameters: Optional[Union[AiDeploymentParameters, dict]] = None,
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
            requirements: A list of PyPI requirements or the path to a requirements.txt file. If both this
                             parameter and the :param: conda_env are specified then conda dependencies will
                             be installed first followed by pip dependencies.
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
            deployment_parameters: Optional; Specification for the hardware (e.g. GPU) and
                                    scaling configuration (e.g. throughput) of the model.

        """
        self.input_schema = input_schema
        self.output_schema = output_schema
        self.configuration = configuration
        self.requirements = requirements
        self.name = name
        self.description = description

        self.code_path = code_path or []
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
        self.model_class_path = Path(model_class_path)
        self.environs: Optional[EnvironmentFileProcessor] = None

        self.deployment_parameters = AiDeploymentParameters.parse_from_optional(deployment_parameters)

    @property
    def model_class_path(self) -> Path:
        return self._model_class_path

    @model_class_path.setter
    def model_class_path(self, value):
        self._model_class_path = Path(value)

    @property
    def code_path(self) -> List[Path]:
        return self._code_path

    @code_path.setter
    def code_path(self, value):
        if isinstance(value, str):
            value = [value]
        # Always store code_path as a list of Path objects
        self._code_path = [Path(p) for p in value]

    @classmethod
    def load_local(cls, load_path: str) -> "AITemplate":
        with open(os.path.join(load_path, "AITemplateSaveFile.json"), "r") as json_file:
            details = json.load(json_file)
        requirements = os.path.join(load_path, "requirements.txt") if details.get("requirements") is not None else None
        conda_env = os.path.join(load_path, "conda.yml") if details.get("conda_env") is not None else None
        code_path = details.get("code_path")
        artifacts = details.get("artifacts")
        model_class = details["model_class"]
        model_class_path = details["model_class_path"]
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
            model_class_path=model_class_path,
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
        target = Path(version_save_path)

        # Save conda env file
        conda_target = target / CONDA_ENV_FILE_NAME
        if self.conda_env is not None:
            log.debug("Copying conda env")
            if type(self.conda_env) == dict:
                with open(conda_target, "w") as f:
                    yaml.dump(self.conda_env, f, default_flow_style=False)
            elif type(self.conda_env) == str:
                conda_file = Path(self.conda_env)
                if conda_file.is_file() and conda_file.suffix in [".yml", ".yaml"]:
                    copy(conda_file, conda_target)
                else:
                    raise ValueError("Make sure conda_env is a valid path to a .yml or .yaml file.")
            else:
                raise ValueError("Make sure conda_env is a valid path to a .yml file or a dictionary.")

        # Copy code directories and files
        if self.model_class_path in self.code_path:
            log.warning("model_class_path already matches one entry in code_path. This is most likely redundant.")
        self.code_path.append(self.model_class_path)

        self._validate_code_paths()
        log.info(f"Copying over: {', '.join(map(str, self.code_path))}")
        ignore_ai_save = ignore_patterns(target.name)
        cwd = Path(os.getcwd())
        for p in self.code_path:
            path = p.absolute().relative_to(cwd)
            if path.is_dir():
                copytree(path, target / path, dirs_exist_ok=True, ignore=ignore_ai_save)
            elif path.is_file():
                copy(path, target / path)
            else:
                raise ValueError(f"{path} does not represent a valid path to a local directory or file.")
        # Ensure that model_class_path is python module with __init__.py for correct import
        model_module = target / self.model_class_path / "__init__.py"
        if not model_module.is_file():
            model_module.touch()

        # Save requirements file
        requirements_target = target / REQUIREMENTS_FILE_NAME
        if self.requirements is not None:
            log.debug("Copying all requirements")
            if type(self.requirements) == str:
                requirements_file = Path(self.requirements)
                if requirements_file.exists():
                    copy(requirements_file, requirements_target)
            elif type(self.requirements) == list:
                with open(requirements_target, "w") as f:
                    f.write("\n".join(self.requirements))
            else:
                raise ValueError(
                    "Make sure requirements is a list of requirements or valid path to requirements.txt file"
                )

        if conda_target.exists():
            conda_env_text = conda_target.read_text()
            if "pip:" in conda_env_text:
                conda_pip_packages = None
                # Extract pip dependencies from conda environment file
                conda_env_dict = yaml.safe_load(conda_env_text)
                conda_dependencies = conda_env_dict.get("dependencies", {})
                for package in conda_dependencies:
                    if isinstance(package, dict) and "pip" in package:
                        conda_pip_packages = package.pop("pip")

                if conda_pip_packages is not None:
                    # Write the environment file without the pip dependencies
                    # pip dependencies will be installed separately from conda dependencies
                    with open(conda_target, "w") as f:
                        yaml.dump(conda_env_dict, f, sort_keys=False)
                    # Append pip packages extracted from conda env to the requirements file
                    initial_line = "\n" if self.requirements is not None else ""
                    with open(requirements_target, "a") as f:
                        f.write(initial_line + "\n".join(conda_pip_packages))

        # Save setup script
        if self.artifacts is not None and "run" in self.artifacts:
            copy(Path(self.artifacts["run"]), target / ARTIFACT_SETUP_SCRIPT_NAME)

        # Create and save the environment file
        self.environs = EnvironmentFileProcessor(os.path.abspath(version_save_path), filename=ENV_VAR_FILENAME)
        self.environs.add_or_update("MODEL_NAME", self.model_class)
        model_module_path = self.model_class_path
        if model_module_path != Path("."):
            log.debug("Copying model_class_path")
            self.environs.add_or_update("MODEL_CLASS_PATH", str(model_module_path).replace("/", "."))
        if conda_target.exists():
            with open(conda_target, "r") as env_yaml:
                try:
                    conda_env_yaml = yaml.safe_load(env_yaml)
                    self.environs.add_or_update("CONDA_ENV_NAME", conda_env_yaml.get("name", "env"))
                except yaml.YAMLError as exc:
                    log.error(exc)

        # Save json
        save_file_path = target / TEMPLATE_SAVE_FILE_NAME
        with open(save_file_path, "w") as ai_template_writer:
            content = {
                "description": self.description,
                "input_schema": self.input_schema.to_json,
                "output_schema": self.output_schema.to_json,
                "configuration": self.configuration.to_json,
                "name": self.name,
                "requirements": str(requirements_target) if requirements_target.exists() else None,
                "code_path": [str(cp) for cp in self.code_path],
                "conda_env": str(conda_target) if conda_target.exists() else None,
                "model_class": self.model_class,
                "model_class_path": str(self.model_class_path),
                "artifacts": self.artifacts,
                "environs": self.environs.to_dict(),
            }
            json.dump(content, ai_template_writer, indent=1)

    def _validate_code_paths(self):
        if self.code_path is not None:
            cwd = Path(os.getcwd())
            for path in self.code_path:
                path_object = path.absolute()
                log.info(f"Validating {path_object} with working directory {cwd}")
                if cwd == path_object:
                    log.warning(
                        "code_path or model_class_path is pointing to the current working directory."
                        "This can be the case when `./` or `.` is used in the code_path or model_class_path."
                        "  This is not recommended since all project files will be copied."
                        " We recommend putting source files in sub-directories."
                    )

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
            deployment_parameters=template.deployment_parameters,
        )
