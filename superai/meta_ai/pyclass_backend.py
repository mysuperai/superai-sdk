import logging
import os

import subprocess
import posixpath
from .base import BaseBackend

_logger = logging.getLogger(__name__)


class PyClassBackend(BaseBackend):
    """Backend implementation for the generic python models."""

    def __init__(self, config, workers=1, no_conda=False, install_mlflow=False, **kwargs):
        super().__init__(config=config, **kwargs)

    def prepare_env(self, model_uri):
        pass

    def serve(self, model_uri, port, host):
        """Serve pyfunc model locally."""
        pass

    def can_score_model(self):
        pass

    def build_image(self, model_uri, image_name, install_mlflow=False, mlflow_home=None):
        pass
