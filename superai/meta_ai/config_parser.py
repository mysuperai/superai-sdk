import logging
import os.path
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

import yaml
from pydantic import BaseModel, BaseSettings, Field, root_validator, validator
from pydantic.env_settings import SettingsSourceCallable

from superai.meta_ai.parameters import AiDeploymentParameters

logger = logging.getLogger(__name__)


class TemplateConfig(BaseModel):
    name: str
    description: str
    model_class: str
    model_class_path: str = "."
    requirements: Optional[Union[str, List[str]]] = None
    input_schema: Optional[Union[str, dict]] = None
    output_schema: Optional[Union[str, dict]] = None
    configuration: Optional[Union[str, dict]] = None
    code_path: Optional[Union[str, List[str]]] = None
    conda_env: Optional[Union[str, dict]] = None
    artifacts: Optional[dict] = None
    bucket_name: Optional[str] = None
    parameters: Optional[dict] = None
    deployment_parameters: Optional[AiDeploymentParameters] = None

    @validator("name")
    def name_must_not_contain_space(cls, v: str) -> str:
        assert " " not in v, "must not contain space"
        return v

    @validator("requirements")
    def check_requirements(cls, v: Optional[Union[str, List[str]]]) -> Optional[Union[str, List[str]]]:
        if v is not None:
            if isinstance(v, str):
                requirements_file_path = Path(v)
                assert requirements_file_path.exists(), "Should exist"
                assert requirements_file_path.is_file(), "Should point to a valid requirements file"
                assert ".txt" in os.path.splitext(v), "Should be a text file"
        return v

    @validator("conda_env")
    def check_conda_env(cls, v: Optional[Union[str, dict]]) -> Optional[Union[str, dict]]:
        if v is not None:
            if isinstance(v, str):
                conda_env_path = Path(v)
                assert conda_env_path.exists(), "Should exist"
                assert conda_env_path.is_file(), "Should point to a valid conda env file"
                assert ".yml" in os.path.splitext(v) or ".yaml" in os.path.splitext(v), "Should be a YAML file"
        return v

    @validator("model_class_path")
    def check_model_class_path(cls, v: str) -> str:
        path = Path(v)
        assert path.exists(), "Should exist"
        assert path.is_dir(), "Should be a directory"
        return v

    @validator("code_path")
    def check_code_path(cls, v: Optional[Union[str, List[str]]]) -> Optional[Union[str, List[str]]]:
        if v is not None:
            if isinstance(v, str):
                path = Path(v)
                assert path.exists(), "Should exist"
                assert path.is_dir(), "Should be a directory"
            else:
                for vs in v:
                    path = Path(vs)
                    assert path.exists(), "Should exist"
        return v


class InstanceConfig(BaseModel):
    name: str
    input_params: Optional[Union[str, dict]] = None
    output_params: Optional[Union[str, dict]] = None
    configuration: Optional[Union[str, dict]] = None
    version: Optional[int] = None
    description: Optional[str] = None
    weights_path: Optional[str] = None
    overwrite: bool = False

    @validator("name")
    def check_name(cls, v: str) -> str:
        assert v.islower(), "Should be lowercase"
        assert " " not in v, "Should not have space"
        return v

    @validator("weights_path")
    def check_weights(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            weights_path_object = Path(v)
            assert weights_path_object.exists(), "Should exist"
            assert weights_path_object.is_dir(), "Should point to an existing directory"
        return v


class DeployConfig(BaseModel):
    orchestrator: str
    skip_build: bool = False
    properties: Optional[Union[AiDeploymentParameters, str, dict]] = {}
    enable_eia: bool = False
    cuda_devel: bool = False
    redeploy: bool = False
    build_all_layers: bool = False
    download_base: bool = False

    push: bool = False
    update_weights: bool = False
    overwrite: bool = False

    @validator("orchestrator")
    def check_orchestrator(cls, v: str) -> str:
        from superai.meta_ai.image_builder import Orchestrator

        assert v in Orchestrator.__members__.values(), f"Should be in {Orchestrator.__members__.values()}"
        return v

    @root_validator()
    def check_push(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        if not values.get("push", False):
            if values.get("update_weights", False) or values.get("overwrite", False):
                logger.warning("`update_weights` and `overwrite` will be ignored as `push` is set to False")
        return values


def yml_config_setting(settings: BaseSettings) -> Dict[str, Any]:
    filename = settings.__config__.env_file
    with open(filename) as f:
        return yaml.safe_load(f)


class TrainingDeployConfig(BaseModel):
    orchestrator: str
    training_data_dir: Optional[str] = None
    skip_build: bool = False
    properties: Optional[Union[AiDeploymentParameters, Dict[str, Any]]] = None
    enable_cuda: bool = False
    training_parameters: Optional[Dict[str, Any]] = None
    envs: Dict[str, Any] = {}
    build_all_layers: bool = False
    download_base: bool = False

    push: bool = False
    update_weights: bool = False
    overwrite: bool = False

    @validator("orchestrator")
    def check_orchestrator(cls, v: str) -> str:
        from superai.meta_ai.image_builder import TrainingOrchestrator

        assert (
            v in TrainingOrchestrator.__members__.values()
        ), f"Should be in {TrainingOrchestrator.__members__.values()}"
        return v

    @validator("training_data_dir")
    def check_training_data_dir(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            tp = Path(v)
            assert tp.exists(), "Should exist"
            assert tp.is_dir(), "Should be a directory"
        return v

    @root_validator()
    def check_push(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        if not values.get("push", False):
            if values.get("update_weights", False) or values.get("overwrite", False):
                logger.warning("`update_weights` and `overwrite` will be ignored as `push` is set to False")
        return values


class TrainingDeploymentFromApp(BaseModel):
    app_id: str
    task_name: str
    current_properties: Union[AiDeploymentParameters, dict] = {}
    metadata: dict = {}
    skip_build: bool = False
    enable_cuda: bool = False
    build_all_layers: bool = False
    envs: Dict[str, Any] = {}
    download_base: bool = False

    push: bool = False
    update_weights: bool = False
    overwrite: bool = False

    @root_validator()
    def check_push(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        if not values.get("push", False):
            if values.get("update_weights", False) or values.get("overwrite", False):
                logger.warning("`update_weights` and `overwrite` will be ignored as `push` is set to False")
        return values


class AIConfig(BaseSettings):
    template: TemplateConfig
    instance: InstanceConfig
    deploy: Optional[DeployConfig] = None
    training_deploy: Optional[TrainingDeployConfig] = None
    training_deploy_from_app: Optional[TrainingDeploymentFromApp] = None

    # define global variables with the Field class
    ENV_STATE: str = Field("test", env="ENV_STATE")

    class Config:
        env_file: str = "config.yaml"

        @classmethod
        def customise_sources(
            cls,
            init_settings: SettingsSourceCallable,
            env_settings: SettingsSourceCallable,
            file_secret_settings: SettingsSourceCallable,
        ) -> Tuple[SettingsSourceCallable, ...]:
            cls.env_file = env_settings.env_file
            return (
                yml_config_setting,
                init_settings,
                file_secret_settings,
            )

    @root_validator()
    def validate(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        if (
            values.get("deploy") is None
            and values.get("training_deploy") is None
            and values.get("training_deploy_from_app") is None
        ):
            raise ValueError("One of `deploy`, `training_deploy` or `training_deploy_from_app` should be present")
        return values
