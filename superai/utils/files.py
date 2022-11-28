import unicodedata
import urllib.error
import urllib.request
from pathlib import Path
from typing import Union

from rich.progress import (
    BarColumn,
    DownloadColumn,
    Progress,
    TextColumn,
    TimeRemainingColumn,
    TransferSpeedColumn,
)

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
    progress = Progress(
        TextColumn("[bold blue]{task.fields[filename]}", justify="right"),
        BarColumn(bar_width=None),
        "[progress.percentage]{task.percentage:>3.1f}%",
        "•",
        DownloadColumn(),
        "•",
        TransferSpeedColumn(),
        "•",
        TimeRemainingColumn(),
    )

    normalized_filename = unicodedata.normalize("NFC", filename)
    t = progress.add_task("Downloading", filename=normalized_filename, start=False)

    def update(blocknum, bs, size):
        progress.update(t, completed=blocknum * bs, total=size)

    try:
        with progress:
            progress.start_task(t)
            urllib.request.urlretrieve(url, destination, update)
    except urllib.error.HTTPError as e:
        destination.unlink()
        raise RuntimeError(f"Could not download file. Status code {e.code}.")

    return str(destination)
