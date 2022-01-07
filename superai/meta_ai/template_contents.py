runner_script_s2i = """
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
        self.model_name = "{{model_name}}"
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
"""

runner_script = f"""
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
"""

lambda_script = """
import os
import functools

from superai.meta_ai.ai import AI

os.environ["SUPERAI_CONFIG_ROOT"] = "/tmp/.superai"


class ModelService:
    def __init__(self):
        pass

    @functools.lru_cache(maxsize={{ai_cache}})
    def get_ai(self, path: str, weights: str) -> AI:
        return AI.load(path, weights)

    def predict(self, data, context):
        path, weights = data.get("path", "/home/model-server/"), data.get("weights", "/opt/ml/model/")
        ai = self.get_ai(path, weights)
        return ai.predict(data)

    def handle(self, data, context):
        if not data:
            return None
        result = self.predict(data, context)
        return result


service = ModelService()


def processor(input, context):
    global service
    return service.handle(input, context)
"""

server_script = """
import subprocess
import sys
import shlex
import os
from retrying import retry
from subprocess import CalledProcessError
from sagemaker_inference import model_server


def _retry_if_error(exception):
    return isinstance(exception, CalledProcessError or OSError)


@retry(stop_max_delay=1000 * 50, retry_on_exception=_retry_if_error)
def _start_mms():
    os.environ["PATH"] = (
        f"/opt/conda/envs/{os.environ.get('CONDA_ENV_NAME', 'env')}/bin:" + os.environ["PATH"]
    )
    os.environ["SAGEMAKER_MODEL_SERVER_WORKERS"] = "{{worker_count}}"
    path = os.path.dirname(os.path.abspath(__file__))

    model_server.start_model_server(handler_service=f'{os.path.join(path, "handler.py")}:ModelService.handle')


def main():
    if sys.argv[2] == "serve":
        _start_mms()
    else:
        subprocess.check_call(shlex.split(' '.join(sys.argv[1:])))

    # prevent docker exit
    subprocess.call(['tail', '-f', '/dev/null'])

main()
"""

entry_script = """#!/bin/sh

if [ -z "${AWS_LAMBDA_RUNTIME_API}" ]; then
  # shellcheck disable=SC2068
  exec /usr/local/bin/aws-lambda-rie /opt/conda/envs/{{env}}/bin/python -m awslambdaric $1
else
  # shellcheck disable=SC2068
  exec /opt/conda/envs/{{env}}/bin/python -m awslambdaric $1
fi
"""
