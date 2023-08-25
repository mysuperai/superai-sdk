from .ai import AiApiMixin
from .checkpoint import AiCheckpointApiMixin
from .instance import AiInstanceApiMixin
from .model import DeploymentApiMixin, TrainApiMixin
from .project_ai import ProjectAiApiMixin


class AiApiMixin(
    ProjectAiApiMixin,
    DeploymentApiMixin,
    TrainApiMixin,
    AiApiMixin,
    AiInstanceApiMixin,
    AiCheckpointApiMixin,
):
    _resource = "ai"
