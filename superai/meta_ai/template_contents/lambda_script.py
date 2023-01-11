import functools

from superai.meta_ai.ai import AI


class ModelService:
    @functools.lru_cache(maxsize={{ai_cache}})
    def get_ai(self, path: str, weights: str) -> AI:
        return AI.load(path, weights)

    def predict(self, data, context):
        path, weights = data.get("path", "/home/model-server/"), data.get("weights", "/opt/ml/model/")
        ai = self.get_ai(path, weights)
        return ai.predict(data)

    def handle(self, data, context):
        return self.predict(data, context) if data else None


service = ModelService()


def processor(input, context):
    global service
    return service.handle(input, context)
