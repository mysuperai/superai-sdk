import json

from superai.meta_ai.ai import AI


class ModelService:
    initialized = False

    def __init__(self):
        self.ai = None

    def initialize(self):
        self.initialized = True
        self.ai = AI.load_local("/home/model-server/", "/opt/ml/model/")

    def predict(self, context, data):
        data = json.loads(data[0]["body"].decode("utf-8"))
        return self.ai.predict(data)

    def handle(self, data, context):
        if not self.initialized:
            self.initialize()
        if not data:
            return None
        return self.predict(context, data)
