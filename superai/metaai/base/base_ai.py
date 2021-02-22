from __future__ import annotations

from abc import ABCMeta, abstractmethod


class BaseAI(metaclass=ABCMeta):
    """
    Represents a generic Python model that evaluates inputs and produces Data Program Project compatible outputs.
    By subclassing :class:`~AIModel`, users can create customized SuperAI models, leveraging custom inference logic and
    artifact dependencies.
    """

    def __init__(self):
        self.initialized = False
        self.model = None

    def load_context(self, context: AIModelContext):
        """
        Loads artifacts from the specified :class:`~AIModelContext` that can be used by
        :func:`~AIModel.predict` when evaluating inputs. When loading an MLflow model with
        :func:`~load_pyfunc`, this method is called as soon as the :class:`~AIModel` is
        constructed.

        The same :class:`~AIModelContext` will also be available during calls to
        :func:`~AIModel.handle`, but it may be more efficient to override this method
        and load artifacts from the context at model load time.

        :param context: A :class:`~AIModelContext` instance containing artifacts §that the model
                        can use to perform inference.
        """
        pass

    @classmethod
    @abstractmethod
    def load_weights(cls, weights_path):
        """
        Used to load the model from ``weights_path``

        :param weights_path:
        :return:
        """
        pass

    def initialize(self, context: "AIModelContext"):
        """
        Initialize model and loads model artifact using :func:`~AIModel.load_context`. In the base
        func:`~AIModel.handle` implementation, this function is called during model loading time.

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
    def predict(self, input):
        """
        Generate model predictions.

        Enforces the input schema first before calling the model implementation with the sanitized input.

        :param input: Model input
        :return: Model predictions as one of pandas.DataFrame, pandas.Series, numpy.ndarray or list.
        """
        pass

    @abstractmethod
    def train(self, input_data_path, model_save_path, hyperparams_path=None):
        """

        :param input_data_path:
        :param model_save_path:
        :param hyperparams_path:
        :return: Model URI
        """
        pass

    def _handle(self, data, context):
        """
        Call preprocess, inference and post-process functions
        :param data: input data
        :param context: AIModelContext context
        """
        if not self.initialized:
            self.initialize()

        if not data:
            return None

        model_input = self.preprocess(data)
        model_out = self.predict(model_input)
        return self.postprocess(model_out)


class AIModelContext(object):
    """
    A collection of artifacts that a :class:`~AIModel` can use when performing inference.
    :class:`~AIModelContext` objects are created *implicitly* by the
    :func:`save_model() <superai.metaai.save_model>` and
    :func:`post_model() <superai.metaai.post_model>` persistence methods, using the contents specified
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
