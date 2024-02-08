from __future__ import annotations


class AIException(Exception):
    """Exceptions related to the operations of the AI object"""


class ModelNotFoundError(AIException):
    def __init__(self, message: str):
        self.message = message
        super(ModelNotFoundError, self).__init__(f"super.AI Model Not Found Error: {self.message}")


class DockerImageNotFoundError(AIException):
    def __init__(self, message: str):
        self.message = message
        super(DockerImageNotFoundError, self).__init__(f"Docker Image Not Found Error: {self.message}")


class ModelDeploymentError(AIException):
    def __init__(self, message: str):
        self.message = message
        super(ModelDeploymentError, self).__init__(f"super.AI Model Deployment Error: {self.message}")


class MetricException(Exception):
    def __init__(self, message: str):
        self.message = message
        super(MetricException, self).__init__(f"super.AI Metric Error: {self.message}")


class ModelAlreadyExistsError(AIException):
    def __init__(self, message: str):
        self.message = message
        super(ModelAlreadyExistsError, self).__init__(f"super.AI Model Already Exists Error: {self.message}")


class ModelUploadError(AIException):
    def __init__(self, message: str):
        self.message = message
        super(ModelUploadError, self).__init__(f"super.AI Model not uploaded Error: {self.message}")


class ExpiredTokenException(Exception):
    def __init__(self, message: str):
        self.message = message
        super(ExpiredTokenException, self).__init__(f"super.AI Token Expired Error: {self.message}")


class AIDeploymentException(AIException):
    def __init__(self, message: str):
        self.message = message
        super(AIDeploymentException, self).__init__(f"super.AI Deployment Error: {self.message}")
