import importlib
import json
import logging
import os

from superai.meta_ai import BaseModel
from superai.meta_ai.parameters import Config
from superai.meta_ai.schema import Schema

logger = logging.getLogger(__name__)


class ModelService:
    initialized = False

    def __init__(self):
        self.model_name = os.environ["MODEL_NAME"]
        parts = self.model_name.rsplit(".", 1)
        if len(parts) == 1:
            logger.info(f"Importing {self.model_name}")
            interface_file = importlib.import_module(self.model_name)
            user_class = getattr(interface_file, self.model_name)
        else:
            logger.info(f"Importing submodule {parts}")
            interface_file = importlib.import_module(parts[0])
            user_class = getattr(interface_file, parts[1])

        if os.path.exists("AITemplateSaveFile.json"):
            with open("AITemplateSaveFile.json", "r") as template_file:
                template = json.load(template_file)
                input_schema = template["input_schema"]
                output_schema = template["output_schema"]
                configuration = template["configuration"]
        else:
            input_schema, output_schema, configuration = Schema(), Schema(), Config()

        self.user_object: BaseModel = user_class(
            input_schema=input_schema, output_schema=output_schema, configuration=configuration
        )

    def initialize(self):
        self.initialized = True
        logger.info("Initializing service")
        if hasattr(self.user_object, "load_weights"):
            self.user_object.load_weights("/opt/ml/model/")
        else:
            raise AttributeError(f"Missing `load_weights` method in user_object `{self.model_name}`")

    def predict(self, context, data):
        data = json.loads(data[0]["body"].decode("utf-8"))
        if hasattr(self.user_object, "predict"):
            result = self.user_object.predict(data)
            return result
        else:
            raise AttributeError(f"Missing `predict` method in user_object `{self.model_name}`")

    def handle(self, data, context):
        if not self.initialized:
            self.initialize()
        if not data:
            return None
        return self.predict(context, data)
