class SuperAIError(Exception):
    def __init__(self, message: str, error_code: int):
        self.error_code = error_code
        self.message = message
        super(Exception, self).__init__(f"super.AI API returned {str(self.error_code)}: {self.message}")


class SuperAIAuthorizationError(Exception):
    def __init__(self, message: str, error_code: int, endpoint: str = None):
        self.error_code = error_code
        self.message = message
        super(Exception, self).__init__(
            f"User not authorized on endpoint: {endpoint}. API returned {str(self.error_code)}: {self.message}"
        )


class SuperAIEntityDuplicatedError(Exception):
    def __init__(self, message: str, error_code: int, base_url: str = None, endpoint: str = None):
        self.error_code = error_code
        self.message = message
        super(Exception, self).__init__(
            f"Entity duplicated on resource: {endpoint}. API returned {str(self.error_code)} on endpoint: {base_url}/{endpoint}: {self.message}"
        )


class SuperAIStorageError(Exception):
    def __init__(self, message: str):
        self.message = message
        super(Exception, self).__init__(f"super.AI Storage service failed: {self.message}")


class SuperAIAuthenticationError(Exception):
    def __init__(self, message: str):
        self.message = message
        super(Exception, self).__init__(f"super.AI Api Key not found: {self.message}")


class SuperAIConfigurationError(Exception):
    def __init__(self, message: str):
        self.message = message
        super(Exception, self).__init__(f"super.AI Configuration error: {self.message}")


class ModelNotFoundError(Exception):
    def __init__(self, message: str):
        self.message = message
        super(ModelNotFoundError, self).__init__(f"super.AI Model Not Found Error: {self.message}")
