import logging
import shlex
import subprocess

logger = logging.getLogger(__name__)


def system(command: str) -> int:
    """
    An alternative of `os.system`, with error catching and failure on bash commands
    Args:
        command: String command
    Returns:
        Return code of the command
    """
    logger.info(f"Running '{command}'")
    process = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE)
    (out, _) = process.communicate()
    if process.returncode != 0:
        raise subprocess.CalledProcessError(process.returncode, command, output=out)
    return process.returncode
