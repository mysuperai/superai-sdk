from __future__ import annotations

from abc import ABCMeta, abstractmethod
from typing import Optional

from superai.meta_ai.parameters import HyperParameterSpec, ModelParameters
from superai.meta_ai.schema import Schema, SchemaParameters
from superai.meta_ai.tracking import SuperTracker

default_random_seed = 65778


class BaseModel(metaclass=ABCMeta):
    """
    Represents a generic Python model that evaluates inputs and produces Data Program Project compatible outputs.
    By subclassing :class:`~BaseModel`, users can create customized SuperAI models, leveraging custom inference logic and
    artifact dependencies.
    """

    def __init__(self, input_schema: Schema = None, output_schema=None, configuration=None, **kwargs):
        self.input_schema = input_schema
        self.output_schema = output_schema
        self.configuration = configuration
        self.initialized = False
        self.model = None
        self.logger_dir = kwargs.get("log_dir")
        self.tracker = SuperTracker(path=self.logger_dir)

        self.input_parameters = input_schema.parameters()
        self.output_parameters = output_schema.parameters()

    def update_logger_path(self, path):
        self.logger_dir = path
        self.tracker = SuperTracker(path=self.logger_dir)

    def load_context(self, context: BaseModelContext):
        """
        Loads artifacts from the specified :class:`~BaseModelContext` that can be used by
        :func:`~BaseModel.predict` when evaluating inputs. When loading an MLflow model with
        :func:`~load_pyfunc`, this method is called as soon as the :class:`~BaseModel` is
        constructed.

        The same :class:`~BaseModelContext` will also be available during calls to
        :func:`~BaseModel.handle`, but it may be more efficient to override this method
        and load artifacts from the context at model load time.

        :param context: A :class:`~BaseModelContext` instance containing artifacts §that the model
                        can use to perform inference.
        """
        pass

    @classmethod
    @abstractmethod
    def load_weights(cls, weights_path):
        """
        Used to load the model from ``weights_path``. Supports S3 remote artifact URIs and relative filesystem paths.
        Note that paths to outer folder e.g. `../my_outer_dir` are not supported

        :param weights_path: Relative path or remote S3 URI
        :return:
        """
        pass

    def initialize(self, context: "BaseModelContext"):
        """
        Initialize model and loads model artifact using :func:`~BaseModel.load_context`. In the base
        func:`~BaseModel.handle` implementation, this function is called during model loading time.

        Post-condition is to set self.initialized to True

        :param context: Initial context contains model server system properties.
        :return:
        """
        self.load_context(context)
        self.initialized = True

    def preprocess(self, request):
        """
        Transform raw input into model input data.
        :param request: list of raw requests
        :return: list of preprocessed model input data
        """
        return request

    def postprocess(self, inference_output):
        """
        Return predict result in as list.
        :param inference_output: list of inference output
        :return: list of predict results
        """
        return inference_output

    @abstractmethod
    def predict(self, inputs):
        """
        Generate model predictions.

        Enforces the input schema first before calling the model implementation with the sanitized input.

        :param inputs: Model input
        :return: Model predictions as one of pandas.DataFrame, pandas.Series, numpy.ndarray or list.
        """
        pass

    @abstractmethod
    def train(
        self,
        model_save_path,
        training_data,
        validation_data=None,
        test_data=None,
        production_data=None,
        encoder_trainable: bool = True,
        decoder_trainable: bool = True,
        hyperparameters: HyperParameterSpec = None,
        model_parameters: ModelParameters = None,
        callbacks=None,
        random_seed=default_random_seed,
    ):
        """

        :param random_seed:
        :param callbacks:
        :param decoder_trainable:
        :param encoder_trainable:
        :param production_data:
        :param test_data:
        :param validation_data:
        :param training_data:
        :param model_save_path:
        :param hyperparameters:
        :param model_parameters:
        :return: Model URI
        """
        pass

    def handle(self, data, context):
        """
        Call preprocess, inference and post-process functions
        :param data: input data
        :param context: BaseModelContext context
        """
        if not self.initialized:
            self.initialize(context)

        if not data:
            return None

        model_input = self.preprocess(data)
        model_out = self.predict(model_input)
        return self.postprocess(model_out)

    def _encoder(self, input_data, trainable=True):
        pass

    def _decoder(self, input_data, trainable=True):
        pass

    def to_framework(self, framework="tensorflow"):
        pass

    def to_pytorch(self):
        return self.to_framework(framework="pytorch")

    def to_tf(self):
        return self.to_framework(framework="tensorflow")

    def update_parameters(
        self,
        input_parameters: Optional[SchemaParameters] = None,
        output_parameters: Optional[SchemaParameters] = None,
    ):
        if input_parameters is not None:
            self.input_parameters = input_parameters
        if output_parameters is not None:
            self.output_parameters = output_parameters


class BaseModelContext(object):
    """
    A collection of artifacts that a :class:`~BaseModel` can use when performing inference.
    :class:`~BaseModelContext` objects are created *implicitly* by the
    :func:`save_model() <superai.meta_ai.save_ai>` and
    :func:`post_model() <superai.meta_ai.post_ai>` persistence methods, using the contents specified
    by the ``artifacts`` parameter of these methods.
    """

    def __init__(self, artifacts):
        """
        :param artifacts: A dictionary of ``<name, artifact_path>`` entries, where ``artifact_path``
                          is an absolute filesystem path to a given artifact.
        """
        self._artifacts = artifacts

    @property
    def artifacts(self):
        """
        A dictionary containing ``<name, artifact_path>`` entries, where ``artifact_path`` is an
        absolute filesystem path to the artifact.
        """
        return self._artifacts
