from abc import ABC

from .model import ModelApiMixin, DeploymentApiMixin, TrainApiMixin
from .project_ai import ProjectAiApiMixin


class AiApiMixin(
    ProjectAiApiMixin,
    ModelApiMixin,
    DeploymentApiMixin,
    TrainApiMixin,
):
    _resource = "ai"
