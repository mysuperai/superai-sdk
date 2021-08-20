import enum
from typing import Optional, List, Union

import jsonpickle


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
    """ParamsSpec to specify range and categorical inputs for yyper-parameter search."""

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
        trainable=Boolean(default=False),
        epochs=Integer(default=10),
        regularization_lambda: Union[ParamsSpec, float] = 0.0,
        learning_rate: Union[ParamsSpec, float] = 0.001,
        # decay:bool=False,
        # decay_rate: Union[ParamsSpec, float]=0.96,
        # decay_steps=10000,
        decay: Optional[ParamsSpec] = None,  # ParamsSpec("decay", ParamsSpec.ParamType.DOUBLE,1, 0.01)
        staircase=Boolean(default=False),
        batch_size: Union[int, ParamsSpec] = 128,
        eval_batch_size: Union[int, ParamsSpec] = 0,
        bucketing_field=None,
        validation_field=String(default="combined"),
        validation_metric=String(default="loss"),
        early_stop=Integer(default=20),
        reduce_learning_rate_on_plateau=Double(default=0),
        reduce_learning_rate_on_plateau_patience=Double(default=5),
        reduce_learning_rate_on_plateau_rate=Double(default=0.5),
        reduce_learning_rate_eval_metric=Tag.LOSS,
        reduce_learning_rate_eval_split=Tag.TRAINING,
        increase_batch_size_on_plateau=Double(default=0),
        increase_batch_size_on_plateau_patience=Double(default=5),
        increase_batch_size_on_plateau_rate=Double(default=2),
        increase_batch_size_on_plateau_max=Double(default=512),
        increase_batch_size_eval_metric=Tag.LOSS,
        increase_batch_size_eval_split=Tag.TRAINING,
        learning_rate_warmup_epochs=Integer(default=1),
        resume=Boolean(default=False),
        skip_save_model=Boolean(default=False),
        skip_save_progress=Boolean(default=False),
        skip_save_log=Boolean(default=False),
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
        self.args = kwargs


class ModelParameters:
    def __init__(
        self,
        conv_layers=Integer(default=None),
        num_conv_layers=Integer(default=None),
        filter_size=Integer(default=3),
        num_filters=Integer(default=32),
        strides: List[Integer] = [Integer(default=1), Integer(default=1)],
        padding=String(default="valid"),
        dilation_rate: List[Integer] = [Integer(default=1), Integer(default=1)],
        conv_use_bias=Boolean(default=True),
        conv_weights_initializer=String(default="glorot_uniform"),
        conv_bias_initializer=String(default="zeros"),
        conv_activation=String(default="relu"),
        conv_dropout=Integer(default=0),
        pool_function=String(default="max"),
        num_fc_layers=Integer(default=1),
        fc_size=Integer(default=128),
        fc_use_bias=Boolean(default=True),
        fc_weights_initializer=String(default="glorot_uniform"),
        fc_bias_initializer=String(default="zeros"),
        fc_activation=String(default="relu"),
        fc_dropout=Integer(value=0),
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
    def from_json(cls, input):
        return jsonpickle.decode(input)

    def __eq__(self, other):
        return self.to_json == other.to_json


if __name__ == "__main__":
    a = Config(default="Something", choice="Something_else")
    print(a.default)
