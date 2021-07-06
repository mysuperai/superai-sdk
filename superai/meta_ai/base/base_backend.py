from abc import ABCMeta, abstractmethod


class BaseBackend(object):
    """
    Abstract class for Base Backend.
    This class defines the API interface for local model deployment of AIs.
    """

    __metaclass__ = ABCMeta

    def __init__(self, config, **kwargs):  # pylint: disable=unused-argument
        self._config = config

    @abstractmethod
    def serve(self, model_uri, port, host):
        """Serve the specified ai locally.

        Args:
            model_uri: URI pointing to the AI to be used for scoring.
            port: Port to use for the AI deployment.
            host: Host to use for the AI deployment. Defaults to ``localhost``.
        """
        pass

    def prepare_env(self, model_uri):
        """Performs any preparation necessary to predict or serve the AI, for example downloading dependencies or
        initializing a conda environment. After preparation, calling predict or serve should be fast.
        """
        pass

    @abstractmethod
    def can_score_ai(self):
        """Check whether this backend can be deployed in the current environment and used to score models.

        Returns:
            True if this flavor backend can be applied in the current environment.
        """
        pass

    def can_build_image(self):
        """
        Returns:
            True if this backend has a `build_image` method defined for building a docker container capable of serving the model. Otherwise, false.
        """
        return callable(getattr(self.__class__, "build_image", None))
