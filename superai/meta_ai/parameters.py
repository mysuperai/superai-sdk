from __future__ import annotations

import ast
import enum
import json
import logging
from enum import IntEnum
from typing import Any, Callable, Dict, List, Optional, Union

import jsonpickle  # type: ignore
from pydantic import BaseModel, Field, validator

logger = logging.getLogger(__file__)


class Scalar:
    __kind__ = "scalar"

    def converter(self):
        return self

    def __new__(cls, value=None, default=None):
        return default if value is None else cls.converter(value)

    # Add more features for json conversion


class Integer(Scalar):
    converter = int


class Double(Scalar):
    converter = float


class Boolean(Scalar):
    converter = bool


class String(Scalar):
    converter = str


class ParamsSpec:
    """ParamsSpec to specify range and categorical inputs for Hyper-parameter search."""

    class ParamType(str, enum.Enum):
        DOUBLE = "DOUBLE"
        INTEGER = "INTEGER"
        CATEGORICAL = "CATEGORICAL"
        DISCRETE = "DISCRETE"

    def __init__(
        self,
        name: String,
        p_type: ParamType,
        minValue=Double(),
        maxValue=Double(),
        categoricalValues: Optional[List] = None,
        discreteValues: Optional[List] = None,
    ):
        self.name = name
        self.p_type = p_type
        if p_type in [self.ParamType.DOUBLE, self.ParamType.INTEGER]:
            assert (
                minValue is not None and maxValue is not None
            ), "With DOUBLE and INTEGER ParamType, minValue and maxValue cannot be None"
        self.minValue: Double = minValue
        self.maxValue: Double = maxValue
        if p_type == self.ParamType.CATEGORICAL:
            assert categoricalValues is not None, "Need categoricalValues if p_type is CATEGORICAL"
        self.categoricalValues: List = categoricalValues
        if p_type == self.ParamType.DISCRETE:
            assert discreteValues is not None, "Need discreteValues if p_type is DISCRETE"
        self.discreteValues: List = discreteValues

    def value(self):
        pass


class HyperParameterSpec:
    class Tag(str, enum.Enum):
        LOSS = "LOSS"
        TRAINING = "TRAINING"

    def __init__(
        self,
        trainable: Union[bool, Boolean] = Boolean(default=False),
        epochs: Union[int, Integer] = Integer(default=10),
        regularization_lambda: Union[ParamsSpec, float] = 0.0,
        learning_rate: Union[ParamsSpec, float] = 0.001,
        decay: Optional[ParamsSpec] = None,  # ParamsSpec("decay", ParamsSpec.ParamType.DOUBLE,1, 0.01)
        staircase: Union[bool, Boolean] = Boolean(default=False),
        batch_size: Union[int, ParamsSpec] = 128,
        eval_batch_size: Union[int, ParamsSpec] = 0,
        bucketing_field: Optional[str] = None,
        validation_field: Union[str, String] = String(default="combined"),
        validation_metric: Union[str, String] = String(default="loss"),
        early_stop: Union[int, Integer] = Integer(default=20),
        reduce_learning_rate_on_plateau: Union[int, Double] = Double(default=0),
        reduce_learning_rate_on_plateau_patience: Union[int, Double] = Double(default=5),
        reduce_learning_rate_on_plateau_rate: Union[int, Double] = Double(default=0.5),
        reduce_learning_rate_eval_metric: str = Tag.LOSS,
        reduce_learning_rate_eval_split: str = Tag.TRAINING,
        increase_batch_size_on_plateau: Union[int, Double] = Double(default=0),
        increase_batch_size_on_plateau_patience: Union[int, Double] = Double(default=5),
        increase_batch_size_on_plateau_rate: Union[int, Double] = Double(default=2),
        increase_batch_size_on_plateau_max: Union[int, Double] = Double(default=512),
        increase_batch_size_eval_metric: str = Tag.LOSS,
        increase_batch_size_eval_split: str = Tag.TRAINING,
        learning_rate_warmup_epochs: Union[int, Integer] = Integer(default=1),
        resume: Union[bool, Boolean] = Boolean(default=False),
        skip_save_model: Union[bool, Boolean] = Boolean(default=False),
        skip_save_progress: Union[bool, Boolean] = Boolean(default=False),
        skip_save_log: Union[bool, Boolean] = Boolean(default=False),
        **kwargs,
    ):
        self.trainable = trainable
        self.epochs = epochs
        self.regularization_lambda = regularization_lambda
        self.learning_rate = learning_rate
        self.decay = decay
        self.staircase = staircase
        self.batch_size = batch_size
        self.eval_batch_size = eval_batch_size
        self.bucketing_field = bucketing_field
        self.validation_field = validation_field
        self.validation_metric = validation_metric
        self.early_stop = early_stop
        self.reduce_learning_rate_on_plateau = reduce_learning_rate_on_plateau
        self.reduce_learning_rate_on_plateau_patience = reduce_learning_rate_on_plateau_patience
        self.reduce_learning_rate_on_plateau_rate = reduce_learning_rate_on_plateau_rate
        self.reduce_learning_rate_eval_metric = reduce_learning_rate_eval_metric
        self.reduce_learning_rate_eval_split = reduce_learning_rate_eval_split
        self.increase_batch_size_on_plateau = increase_batch_size_on_plateau
        self.increase_batch_size_on_plateau_patience = increase_batch_size_on_plateau_patience
        self.increase_batch_size_on_plateau_rate = increase_batch_size_on_plateau_rate
        self.increase_batch_size_on_plateau_max = increase_batch_size_on_plateau_max
        self.increase_batch_size_eval_metric = increase_batch_size_eval_metric
        self.increase_batch_size_eval_split = increase_batch_size_eval_split
        self.learning_rate_warmup_epochs = learning_rate_warmup_epochs
        self.resume = resume
        self.skip_save_model = skip_save_model
        self.skip_save_progress = skip_save_progress
        self.skip_save_log = skip_save_log
        for k in kwargs.keys():
            setattr(self, k, kwargs[k])

    @classmethod
    def load_from_list(cls, parameters: List[str]):
        processed_params = parameter_processor(parameters)
        return HyperParameterSpec(**processed_params)  # type: ignore

    def get(self, key, default=None):
        if hasattr(self, key):
            return getattr(self, key)
        else:
            if default is None:
                raise KeyError(f"Key {key} not found in {self.__class__.__name__} object")
            return default


def parameter_processor(parameters=None):
    if parameters is None:
        parameters = []
    processed_params = {}
    for param in parameters:
        key, value = param.split("=")
        try:
            value = ast.literal_eval(value)
        except Exception as e:
            logger.debug(f"Error parsing value, leaving unchanged: {e}")
        if isinstance(value, list):
            cleaned_values = []
            for val in value:
                try:
                    val = ast.literal_eval(val)
                except Exception as e:
                    logger.debug(f"Error parsing list value, leaving unchanged: {e}")
                if isinstance(val, str):
                    val = val.strip()
                cleaned_values.append(val)
        processed_params[key] = value
    return processed_params


class ModelParameters:
    def __init__(
        self,
        conv_layers: Union[int, Integer] = Integer(default=None),
        num_conv_layers: Union[int, Integer] = Integer(default=None),
        filter_size: Union[int, Integer] = Integer(default=3),
        num_filters: Union[int, Integer] = Integer(default=32),
        strides: Union[List[int], List[Integer]] = [Integer(default=1), Integer(default=1)],
        padding: Union[str, String] = String(default="valid"),
        dilation_rate: Union[List[int], List[Integer]] = [Integer(default=1), Integer(default=1)],
        conv_use_bias: Union[bool, Boolean] = Boolean(default=True),
        conv_weights_initializer: Union[str, String] = String(default="glorot_uniform"),
        conv_bias_initializer: Union[str, String] = String(default="zeros"),
        conv_activation: Union[str, String] = String(default="relu"),
        conv_dropout: Union[int, Integer] = Integer(default=0),
        pool_function: Union[str, String] = String(default="max"),
        num_fc_layers: Union[int, Integer] = Integer(default=1),
        fc_size: Union[int, Integer] = Integer(default=128),
        fc_use_bias: Union[bool, Boolean] = Boolean(default=True),
        fc_weights_initializer: Union[str, String] = String(default="glorot_uniform"),
        fc_bias_initializer: Union[str, String] = String(default="zeros"),
        fc_activation: Union[str, String] = String(default="relu"),
        fc_dropout: Union[int, Integer] = Integer(value=0),
        **kwargs,
    ):
        self.conv_layers = conv_layers
        self.num_conv_layers = num_conv_layers
        self.filter_size = filter_size
        self.num_filters = num_filters
        self.strides = strides
        self.padding = padding
        self.dilation_rate = dilation_rate
        self.conv_use_bias = conv_use_bias
        self.conv_weights_initializer = conv_weights_initializer
        self.conv_bias_initializer = conv_bias_initializer
        self.conv_activation = conv_activation
        self.conv_dropout = conv_dropout
        self.pool_function = pool_function
        self.num_fc_layers = num_fc_layers
        self.fc_size = fc_size
        self.fc_use_bias = fc_use_bias
        self.fc_weights_initializer = fc_weights_initializer
        self.fc_bias_initializer = fc_bias_initializer
        self.fc_activation = fc_activation
        self.fc_dropout = fc_dropout
        for k in kwargs.keys():
            setattr(self, k, kwargs[k])

    @classmethod
    def load_from_list(cls, parameters: List[str]):
        processed_params = parameter_processor(parameters)
        return ModelParameters(**processed_params)  # type: ignore

    def get(self, key, default=None):
        if hasattr(self, key):
            return getattr(self, key)
        else:
            if default is None:
                raise KeyError(f"Key {key} not found in {self.__class__.__name__} object")
            return default


class Config:
    """Mocked config class to be shared between AI and DP objects."""

    def __init__(self, **kwargs):
        self.kwargs = kwargs
        for k in kwargs.keys():
            setattr(self, k, kwargs[k])

    def __dir__(self):
        return self.kwargs.keys()

    def parametrize(self, **kwargs):
        pass

    @property
    def to_json(self):
        return jsonpickle.encode(self)

    __call__ = parametrize

    @classmethod
    def from_json(cls, inputs):
        return jsonpickle.decode(inputs)

    def __eq__(self, other):
        return self.to_json == other.to_json


class TrainingParameters:
    def __init__(
        self,
        training_data: Optional[str] = None,
        test_data: Optional[str] = None,
        production_data: Optional[str] = None,
        validation_data: Optional[str] = None,
        encoder_trainable: bool = True,
        decoder_trainable: bool = True,
        hyperparameters: Optional[HyperParameterSpec] = None,
        model_parameter: Optional[ModelParameters] = None,
        callbacks: Optional[Callable] = None,
        train_logger: Optional[Any] = None,
    ):
        self.training_data_path = training_data
        self.test_data_path = test_data
        self.production_data_path = production_data
        self.validation_data_path = validation_data
        self.encoder_trainable = encoder_trainable
        self.decoder_trainable = decoder_trainable
        self.hyperparameters = hyperparameters
        self.model_parameter = model_parameter
        self.callbacks = callbacks
        self.train_logger = train_logger
        try:
            self.to_json()
        except Exception:
            logger.exception(
                "Could not JSON serialize the training parameters, please make sure the arguments are JSON serializable"
            )
            raise

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=2)

    def from_dict(self, dictionary: dict):
        for k, v in dictionary.items():
            setattr(self, k, v)


if __name__ == "__main__":
    a = Config(default="Something", choice="Something_else")
    print(a.default)


class GPUVRAM(IntEnum):
    VRAM_8192 = 8192
    VRAM_12288 = 12288
    VRAM_16384 = 16384
    VRAM_24576 = 24576
    VRAM_32768 = 32768
    VRAM_40960 = 40960


class AiDeploymentParameters(BaseModel):
    min_replica_count: Optional[int] = Field(0, ge=0, description="Minimum number of replicas", alias="minReplicaCount")
    max_replica_count: Optional[int] = Field(1, ge=1, description="Maximum number of replicas", alias="maxReplicaCount")
    cooldown_period: Optional[int] = Field(
        1800,
        description="Cooldown period (in seconds) after which unused deployments get scaled down.",
        alias="cooldownPeriod",
    )
    target_average_utilization: Optional[float] = Field(
        0.5, gt=0, description="Target average CPU utilization", alias="targetAverageUtilization"
    )
    gpu_target_average_utilization: Optional[float] = Field(
        None, description="[Not implemented] Target average utilization for gpu", alias="gpuTargetAverageUtilization"
    )
    gpu_memory_requirement: Optional[GPUVRAM] = Field(
        None,
        description="Controls the amount of VRAM allocated to the GPU. If set to 0, no GPU is used. Can be one of [8192, 12288, 16384, 24576, 32768, 40960]",
        alias="gpuMemoryRequirement",
    )
    target_memory_requirement: Optional[str] = Field(
        "512Mi", description="Target memory requirement", alias="targetMemoryRequirement"
    )
    target_memory_limit: Optional[str] = Field("4Gi", description="Target memory limit", alias="targetMemoryLimit")
    mount_path: Optional[str] = Field("/shared", description="Mount path", alias="mountPath")
    num_threads: Optional[int] = Field(
        1, description="[Untested] Number of concurrent serving threads", alias="numThreads"
    )
    enable_cuda: Optional[bool] = Field(
        False,
        description="Enable CUDA capable deployment. Is used to build correct image and deploy on Compute nodes with NVIDIA GPU.",
        alias="enableCuda",
    )
    queue_length: Optional[int] = Field(
        20,
        description="""Controls scaling behaviour. 
        Should be the expected throughput per model instance in one minute.
        If the model queue contains 40 items with a queueLength of 20, the deployment will scale up to 2 instances.
        """,
        alias="queueLength",
    )
    model_timeout_seconds: Optional[int] = Field(
        20,
        gt=0,
        le=60,
        description="""The expected time of the model to complete one average prediction.
        Will be used to cancel waiting for overwhelmed models to complete."
        The upper bound is a hard limit given by backend constraints.
        """,
        alias="modelTimeoutSeconds",
    )
    lambda_ai_cache: Optional[int] = Field(32, ge=0, description="Lambda AI cache size", alias="lambdaAICache")
    sagemaker_worker_count: Optional[int] = Field(
        1, ge=1, description="SageMaker worker count in the same endpoint", alias="sagemakerWorkerCount"
    )
    envs: Optional[Dict[str, str]] = Field(
        None,
        description="Pass custom environment variables to the deployment. "
        'Should be a dictionary like {"LOG_LEVEL": "DEBUG", "OTHER": "VARIABLE"}',
    )

    class Config:
        use_enum_values = True
        allow_population_by_field_name = True
        extra = "forbid"

    # Validate that memory is using correct format
    @validator("target_memory_requirement", "target_memory_limit")
    def validate_memory_requirement(cls, v):
        """
        Allowed is Mi and Gi, e.g. 512Mi or 4Gi
        """
        if v is None:
            return v
        if not v.endswith("Mi") and not v.endswith("Gi"):
            raise ValueError("Memory requirement must be in Mi or Gi")
        return v

    def dict_for_db(self) -> dict:
        """
        Method wrapping pydantics dict() method to only contain set fields.
        """
        return self.dict(exclude_unset=True, by_alias=True, exclude_defaults=True)

    def json_for_db(self) -> str:
        """
        Method dumping dict_for_db() method to JSON.
        """
        return json.dumps(self.dict_for_db())

    @classmethod
    def parse_from_optional(
        cls, deployment_parameters: Optional[dict, AiDeploymentParameters]
    ) -> AiDeploymentParameters:
        if isinstance(deployment_parameters, dict):
            deployment_parameters = AiDeploymentParameters.parse_obj(deployment_parameters)
        if deployment_parameters and not isinstance(deployment_parameters, AiDeploymentParameters):
            raise ValueError("deployment_parameters must be of type DeploymentParameters or a compatible dict.")
        if not deployment_parameters:
            deployment_parameters = AiDeploymentParameters()
        return deployment_parameters

    def merge(self, other: AiDeploymentParameters):
        """
        Merge two DeploymentParameters objects.
        """
        for k, v in other.dict().items():
            if k in self.dict():
                self.dict()[k] = v
        return self
