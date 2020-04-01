
class SuperAIError(Exception):

    def __init__(self, message: str, error_code: int):
        self.error_code = error_code
        self.message = message
        super(Exception, self).__init__(f'super.AI API returned {str(self.error_code)}: {self.message}')

class SuperAIStorageError(Exception):
    def __init__(self, message: str):
        self.message = message
        super(Exception, self).__init__(f'super.AI Storage service failed: {self.message}')