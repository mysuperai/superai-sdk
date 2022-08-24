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
