from __future__ import annotations

import json
import logging
import os
import tarfile
from abc import ABCMeta, abstractmethod
from pathlib import Path
from typing import Optional
from urllib.parse import urlparse

import boto3

from superai.meta_ai.parameters import Config, HyperParameterSpec, ModelParameters
from superai.meta_ai.schema import Schema, SchemaParameters
from superai.meta_ai.tracking import SuperTracker

default_random_seed = 65778

log = logging.getLogger()


class BaseModel(metaclass=ABCMeta):
    """Represents a generic Python model that evaluates inputs and produces Data Program Project compatible outputs.
    By subclassing :class:`~BaseModel`, users can create customized SuperAI models, leveraging custom inference logic and
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
        self.default_seldon_load_path = os.environ.get("MNT_PATH", "/shared")

    def __init_subclass__(cls, **kwargs):
        cls.predict = cls._process_json_func(cls.predict)
        super().__init_subclass__(**kwargs)

    @staticmethod
    def _process_json_func(pred_func):
        """This method json encodes a dictionary and returns the same dictionary, avoiding JSON encoding failures."""

        def __inner__(*args, **kwargs):
            prediction_result = pred_func(*args, **kwargs)
            json_string = json.dumps(prediction_result)
            json_dict = json.loads(json_string)
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
        pod. The loading will be done with a default path, but we are passing some options to parametrize this"""

        if os.environ.get("WEIGHTS_PATH"):
            weights_path = os.environ.get("WEIGHTS_PATH")
            if weights_path.startswith("s3://"):
                path = self._pull_weights(weights_path, self.default_seldon_load_path)
                log.info(f"Loading weights from `{path}`")
                return self.load_weights(path)

        return self.load_weights(self.default_seldon_load_path)

    @staticmethod
    def _pull_weights(weights_uri: str, output_path: str) -> str:
        """Helper function to pull weights from S3 bucket
        Supports loading tar.gz files or whole directories

        Args:
            weights_uri: S3 URI of the weights to be loaded
            output_path: Path to the output directory

        Returns:
            Name of the folder where weights where downloded / extracted to
        """
        log.info(f"Downloading weights from {weights_uri} to {output_path}")
        s3 = boto3.client("s3")
        parsed_url = urlparse(weights_uri, allow_fragments=False)
        bucket_name = parsed_url.netloc
        path_to_object = parsed_url.path if not parsed_url.path.startswith("/") else parsed_url.path[1:]
        object_name = os.path.basename(path_to_object)
        log.debug("Bucket name: {}, path to object: {}, tar name: {}".format(bucket_name, path_to_object, object_name))
        OUTPUT_DIR_NAME = "weights"
        full_path = os.path.join(output_path, OUTPUT_DIR_NAME)

        if "tar.gz" in object_name:
            log.info(f"Downloading and unpacking AI object from bucket `{bucket_name}` and path `{path_to_object}`")
            s3.download_file(bucket_name, path_to_object, os.path.join(output_path, object_name))
            with tarfile.open(os.path.join(output_path, object_name)) as tar:
                tar.extractall(path=full_path)
            log.info(f"Successfully downloaded and unpacked weights to path `{full_path}`")
        else:
            BaseModel._pull_s3_folder(weights_uri, full_path)
            log.info(f"Successfully downloaded weights folder to path `{full_path}`")
        return full_path

    @staticmethod
    def _pull_s3_folder(s3_uri, local_dir):
        s3 = boto3.resource("s3")
        bucket = s3.Bucket(urlparse(s3_uri).hostname)
        s3_path = urlparse(s3_uri).path.lstrip("/")
        local_dir = Path(local_dir)
        for obj in bucket.objects.filter(Prefix=s3_path):
            target = obj.key if local_dir is None else local_dir / Path(obj.key).relative_to(s3_path)
            target.parent.mkdir(parents=True, exist_ok=True)
            if obj.key[-1] == "/":
                continue
            bucket.download_file(obj.key, str(target))

    def predict_raw(self, inputs):
        """Seldon uses this method to return raw predictions back to invoker. Seldon uses the predict method to
        process numpy arrays. If you want to process numpy arrays differently from raw prediction requests,
        you can define both

        Args:
            inputs: Model input

        Returns
            Model predictions as one of pandas.DataFrame, pandas.Series, numpy.ndarray or list."""
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
    def predict(self, inputs, context=None):
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
    ):
        """
        Args:
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
            Model URI.
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
        """
        Args:
            artifacts: A dictionary of ``<name, artifact_path>`` entries, where ``artifact_path`` is an absolute
            filesystem path to a given artifact.
        """
        self._artifacts = artifacts

    @property
    def artifacts(self):
        """A dictionary containing ``<name, artifact_path>`` entries, where ``artifact_path`` is an absolute
        filesystem path to the artifact."""
        return self._artifacts
