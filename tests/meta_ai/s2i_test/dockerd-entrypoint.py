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
def _start_mms(model_name):
    os.environ["SAGEMAKER_MODEL_SERVER_WORKERS"] = "1"
    os.environ["MODEL_NAME"] = model_name
    path = os.path.dirname(os.path.abspath(__file__))

    model_server.start_model_server(handler_service=f'{os.path.join(path, "handler.py")}:ModelService.handle')


def main():
    if sys.argv[2] == "serve":
        _start_mms(model_name=sys.argv[1])
    else:
        subprocess.check_call(shlex.split(" ".join(sys.argv[1:])))

    # prevent docker exit
    subprocess.call(["tail", "-f", "/dev/null"])


main()
