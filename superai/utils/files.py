import urllib.request
from pathlib import Path
from typing import Union

from superai.log import logger

log = logger.get_logger(__name__)


def download_file_to_directory(url: str, filename: str, path: Union[Path, str]) -> str:
    """
    Download a file from a url to a path

    Parameters
    ----------
    url : str
        The url of the file to download
    filename : str
        The name of the file to download
    path : Path
        The path to download the file to

    """
    path = Path(path)
    destination = path / filename
    destination.parent.mkdir(exist_ok=True)
    destination.touch()
    urllib.request.urlretrieve(url, destination)
    return str(destination)
