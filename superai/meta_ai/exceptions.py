class ModelNotFoundError(Exception):
    def __init__(self, message: str):
        self.message = message
        super(ModelNotFoundError, self).__init__(f"super.AI Model Not Found Error: {self.message}")


class ModelDeploymentError(Exception):
    def __init__(self, message: str):
        self.message = message
        super(ModelDeploymentError, self).__init__(f"super.AI Model Deployment Error: {self.message}")


class MetricException(Exception):
    def __init__(self, message: str):
        self.message = message
        super(MetricException, self).__init__(f"super.AI Metric Error: {self.message}")


class ModelAlreadyExistsError(Exception):
    def __init__(self, message: str):
        self.message = message
        super(ModelAlreadyExistsError, self).__init__(f"super.AI Model Already Exists Error: {self.message}")


class ModelUploadError(Exception):
    def __init__(self, message: str):
        self.message = message
        super(ModelUploadError, self).__init__(f"super.AI Model not uploaded Error: {self.message}")


class ExpiredTokenException(Exception):
    def __init__(self, message: str):
        self.message = message
        super(ExpiredTokenException, self).__init__(f"super.AI Token Expired Error: {self.message}")
