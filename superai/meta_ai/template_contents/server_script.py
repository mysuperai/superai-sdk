import os
import shlex
import subprocess
import sys
from subprocess import CalledProcessError

from retrying import retry
from sagemaker_inference import model_server


def _retry_if_error(exception):
    return isinstance(exception, CalledProcessError or OSError)


@retry(stop_max_delay=1000 * 50, retry_on_exception=_retry_if_error)
def _start_mms():
    os.environ["PATH"] = f"/opt/conda/envs/{os.environ.get('CONDA_ENV_NAME', 'env')}/bin:" + os.environ["PATH"]
    os.environ["SAGEMAKER_MODEL_SERVER_WORKERS"] = "{{worker_count}}"
    path = os.path.dirname(os.path.abspath(__file__))

    model_server.start_model_server(handler_service=f'{os.path.join(path, "handler.py")}:ModelService.handle')


def main():
    if sys.argv[2] == "serve":
        _start_mms()
    else:
        subprocess.check_call(shlex.split(" ".join(sys.argv[1:])))

    # prevent docker exit
    subprocess.call(["tail", "-f", "/dev/null"])


main()
