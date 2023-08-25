from __future__ import annotations

import json
import os
import sys
import traceback
from abc import ABCMeta, abstractmethod
from typing import List, Optional, Union

from superai.log import get_logger
from superai.meta_ai.base.utils import pull_weights
from superai.meta_ai.parameters import Config, HyperParameterSpec, ModelParameters
from superai.meta_ai.schema import Schema, SchemaParameters, TaskInput, TrainerOutput
from superai.meta_ai.tracking import SuperTracker

default_random_seed = 65778

log = get_logger(__name__)


class BaseAI(metaclass=ABCMeta):
    """Represents a generic AI that evaluates inputs and produces Data Program Project compatible outputs.
    By subclassing :class:`~BaseAI`, users can create customized SuperAI AIs, leveraging custom inference logic and
    artifact dependencies.
    """

    def __init__(
        self,
        input_schema: Optional[Schema] = None,
        output_schema: Optional[Schema] = None,
        configuration: Optional[Config] = None,
        **kwargs,
    ):
        self.input_schema = input_schema
        self.output_schema = output_schema
        self.configuration = configuration
        self.initialized = False
        self.model = None
        self.logger_dir = kwargs.get("log_dir")
        self.tracker = SuperTracker(path=self.logger_dir)

        self.input_parameters = input_schema.parameters() if input_schema is not None else SchemaParameters()
        self.output_parameters = output_schema.parameters() if output_schema is not None else SchemaParameters()

        # Seldon default weights loading path in the container. You can override this by passing MNT_PATH in the
        # environment file or CRD
        self.default_seldon_load_path = os.environ.get("MNT_PATH", "/mnt/models")

    def __init_subclass__(cls, **kwargs):
        cls.predict = cls._wrapped_prediction(cls.predict)
        super().__init_subclass__(**kwargs)

    @staticmethod
    def _wrapped_prediction(pred_func):
        """Wraps the prediction function to add functionality and hide complex implementation details.

        Currently, does:
        - logs the prediction_uuid and tags if present in the metadata
        -  json encodes a dictionary and returns the same dictionary, avoiding JSON encoding failures.
        - passthrough meta header for routing and logging

        """

        def __inner__(self, inputs: dict, meta: dict = None):
            """
            Args:
                data: Input data to the model
                meta: Metadata about the input data, used in the backend transport and for observability
            """
            if isinstance(inputs, dict) and "data" in inputs and "meta" in inputs:
                meta = inputs["meta"]
                inputs = inputs["data"]
            elif meta is None:
                log.warning(f"Received inputs without meta header. Type of inputs: {type(inputs)}")

            if meta:
                if "puid" in meta:
                    log.info(f"Received prediction request for prediction_uuid={meta['puid']}")
                if "tags" in meta:
                    # TODO: add tracking of tags for jaeger here
                    log.info(f"Received tags={meta['tags']}")

            # Main function
            exception = None
            json_dict = None
            try:
                prediction_result = pred_func(self, inputs)
                json_string = json.dumps(prediction_result)
                json_dict = json.loads(json_string)
            except Exception:
                if meta:
                    # Catch exceptions and return them in the response
                    # This enables us to return our own payload instead of the seldon default
                    log.exception("Exception occurred during prediction")

                    exc_type, exc_value, exc_tb = sys.exc_info()
                    exception = str(traceback.format_exception(exc_type, exc_value, exc_tb, limit=3))
                else:
                    # backwards compatibility
                    # our old behaviour was based on the seldon default
                    raise

            if meta:
                if exception:
                    # Return the exception in the response as `exception`
                    return dict(exception=exception, meta=meta)
                else:
                    # Return the prediction in the response as `data`
                    return dict(data=json_dict, meta=meta)
            else:
                # Backwards compatibility
                return json_dict

        return __inner__

    def update_logger_path(self, path):
        self.logger_dir = path
        self.tracker = SuperTracker(path=self.logger_dir)

    def load_context(self, context: BaseModelContext):
        """Loads artifacts from the specified :class:`~BaseModelContext` that can be used by
        :func:`~BaseModel.predict` when evaluating inputs. When loading an MLflow model with
        :func:`~load_pyfunc`, this method is called as soon as the :class:`~BaseModel` is
        constructed.

        The same :class:`~BaseModelContext` will also be available during calls to
        :func:`~BaseModel.handle`, but it may be more efficient to override this method
        and load artifacts from the context at model load time.

        Args:
            context: A :class:`~BaseModelContext` instance containing artifacts §that the model
                        can use to perform inference.
        """

    @abstractmethod
    def load_weights(self, weights_path: str):
        """Used to load the model from ``weights_path``. Supports S3 remote artifact URIs and relative filesystem paths.
        Note that paths to outer folder e.g. `../my_outer_dir` are not supported

        Args:
            weights_path: Relative path or remote S3 URI.
        """

    def load(self):
        """Seldon helper function to call the load_weights method. Seldon runs this method during the provision of
        pod. The loading will be done with a default path, but we are passing some options to parametrize this
        """

        if os.environ.get("WEIGHTS_PATH"):
            weights_path = os.environ.get("WEIGHTS_PATH")
            if weights_path.startswith("s3://"):
                output_path = os.path.join(self.default_seldon_load_path, "weights")
                path = pull_weights(weights_path, output_path)
                log.info(f"Loading weights from `{path}`")
                return self.load_weights(path)

        return self.load_weights(self.default_seldon_load_path)

    def predict_raw(self, inputs):
        """Seldon uses this method to return raw predictions back to invoker. Seldon uses the predict method to
        process numpy arrays. If you want to process numpy arrays differently from raw prediction requests,
        you can define both

        Args:
            inputs: Model input

        Returns
            Model predictions as one of pandas.DataFrame, pandas.Series, numpy.ndarray or list.
        """
        return self.predict(inputs)

    def initialize(self, context: "BaseModelContext"):
        """Initialize model and loads model artifact using :func:`~BaseModel.load_context`. In the base
        func:`~BaseModel.handle` implementation, this function is called during model loading time.

        Post-condition is to set self.initialized to True.

        Args:
            context: Initial context contains model server system properties.
        """
        self.load_context(context)
        self.initialized = True

    def preprocess(self, request):
        """Transform raw input into model input data.

        Args:
            request: list of raw requests

        Returns:
            List of preprocessed model input data.
        """
        return request

    def postprocess(self, inference_output):
        """Return predict result in as list.

        Args:
            inference_output: list of inference output

        Returns:
            List of predict results.
        """
        return inference_output

    @abstractmethod
    def predict(self, inputs: Union[TaskInput, List[dict]], context=None):
        """Generate model predictions.

        Enforces the input schema first before calling the model implementation with the sanitized input.

        Note: Seldon expects only a numpy.ndarray as an input for this method. If you are not processing numpy.ndarray,
        you can override predict_raw method instead of predict.

        Args:
            inputs: Model input
            context: Support for seldon predict calls

        Returns
            Model predictions as one of pandas.DataFrame, pandas.Series, numpy.ndarray or list.
        """

    def predict_batch(self, input_batch: List[Union[TaskInput, List[dict]]], context=None):
        """Generate model predictions for a batch of inputs.
        Can be overridden to support more efficient batch predictions inside the model.

        Args:
            input_batch: List of model input
            context: Support for seldon predict calls

        Returns:
            List of model predictions.
        """
        log.warning("predict_batch() is not implemented. Falling back to loop predict method.")
        return [self.predict(input, context) for input in input_batch]

    @abstractmethod
    def train(
        self,
        model_save_path,
        training_data,
        validation_data=None,
        test_data=None,
        production_data=None,
        weights_path=None,
        encoder_trainable: bool = True,
        decoder_trainable: bool = True,
        hyperparameters: HyperParameterSpec = None,
        model_parameters: ModelParameters = None,
        callbacks=None,
        random_seed=default_random_seed,
    ) -> TrainerOutput:
        """Args:
            random_seed:
            callbacks:
            decoder_trainable:
            encoder_trainable:
            production_data:
            test_data:
            validation_data:
            training_data:
            model_save_path:
            hyperparameters:
            model_parameters:
            weights_path:

        Returns:
            Dictionary of metrics to be tracked. Eg: `{"eval_accuracy": accuracy}` where `accuracy` is obtained from
            the keras train function. These metrics will be tracked by polyaxon training run
        """

    def handle(self, data, context):
        """Call preprocess, inference, and post-process functions.

        Args:
            data: input data
            context: BaseModelContext context
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

    def metrics(self):
        """Helper function to return metrics used by prometheus"""


class BaseModelContext(object):
    """A collection of artifacts that a :class:`~BaseModel` can use when performing inference.
    :class:`~BaseModelContext` objects are created *implicitly* by the :func:`save_model() <superai.meta_ai.save_ai>`
    and :func:`post_model() <superai.meta_ai.post_ai>` persistence methods, using the contents specified by the
    ``artifacts`` parameter of these methods.
    """

    def __init__(self, artifacts):
        """Args:
        artifacts: A dictionary of ``<name, artifact_path>`` entries, where ``artifact_path`` is an absolute
        filesystem path to a given artifact.
        """
        self._artifacts = artifacts

    @property
    def artifacts(self):
        """A dictionary containing ``<name, artifact_path>`` entries, where ``artifact_path`` is an absolute
        filesystem path to the artifact.
        """
        return self._artifacts


def add_default_tracking(training_method):
    """Decorator to add tracking to the training method which performs basic metrics tracking that are returned by the
    training function. Note that the metrics signature should match the arguments of the `tracking.log_metrics` method

    Args:
        training_method: `train` method of the Base class.
    """
    from polyaxon import tracking

    def inner(*args, **kwargs):
        tracking.init()
        metrics: TrainerOutput = training_method(*args, **kwargs)
        if metrics.metric is not None:
            tracking.log_metrics(**metrics.metric)
        elif metrics.metrics is not None:
            for m in metrics.metrics:
                tracking.log_metric(name=m.name, value=m.value, step=m.step, timestamp=m.timestamp)
        elif metrics.collection is not None:
            for m in metrics.collection:
                tracking.log_metrics(step=m.step, timestamp=m.timestamp, **dict(m.metrics))
        else:
            raise ValueError("One of the metrics should be available")

    return inner
