import atexit
import inspect
import os
import threading
from pathlib import Path

from colorama import Fore, Style

from superai.config import settings
from superai.data_program.hatchery import BuildConfig, run, RuntimeConfig
from superai.data_program.router import Router
from superai.data_program.utils import IgnoreInAgent
from superai.log import logger

BASE_URL = settings.base_url
log = logger.get_logger(__name__)


class DataProgramBase:
    # TODO: A nicer design is to inherit from thread.
    _thread: threading.Thread = None

    def __init__(
        self,
        router: Router = None,
        add_basic_workflow: bool = True,
    ):
        self._router = router
        self._add_basic_workflow = add_basic_workflow
        self._caller_info = self.__caller_info()
        self._threadLocal = threading.local()

    @property
    def insideThread(self):
        return getattr(self._threadLocal, "initialized", False)

    @property
    def add_basic_workflow(self):
        return self._add_basic_workflow

    @add_basic_workflow.setter
    def add_basic_workflow(self):
        return self._add_basic_workflow

    @property
    def router(self):
        return self._router

    @router.setter
    def router(self, router: Router):
        self._router = router

    def run_thread(self):
        if DataProgramBase._thread and not DataProgramBase._thread.is_alive():
            log.info(f"[DataProgramBase.run] - Starting thread")
            DataProgramBase._thread.start()
            DataProgramBase._thread.join()

    @IgnoreInAgent
    def _run_local(self, name: str = None, **kwargs):
        if DataProgramBase._thread:
            log.debug(Fore.RED + "_run_local tried to run but DataProgramBase._thread is already set" + Style.RESET_ALL)
            return

        name = name if name else self.name
        if not name:
            raise Exception("DataProgram can not be deployed without a name")

        build_config = BuildConfig()
        runtime_config = RuntimeConfig(name=name, environment=[{"name": "IN_AGENT", "value": "YES"}])
        filepath = self._caller_info.get("filepath")
        DataProgramBase._thread = threading.Thread(
            name=f"DP-{name}",
            target=run,
            args=[build_config.as_dict(), runtime_config.as_dict()],
            kwargs={"filepath": filepath},
            daemon=True,
        )
        log.info(f"[DataProgramBase._deploy] - Thread created")
        atexit.register(DataProgramBase.run_thread, self)
        log.info(f"[DataProgramBase._deploy] - Thread registered to run join before the data program closes")

    def __caller_info(self):
        index = -1
        frm = inspect.stack()[index]
        # Filters PyCharm frames to support debugging mode. TODO: Filter also libraries like pytest
        while "PyCharm" in frm.filename:
            index = index - 1
            frm = inspect.stack()[index]
        mod = inspect.getmodule(frm[0])
        dir = os.path.dirname(mod.__file__) if os.path.dirname(mod.__file__) else os.path.abspath(os.path.curdir)
        file_name = os.path.basename(mod.__file__)
        info = {
            "dir": dir,
            "file_name": file_name,
            "filepath": Path(dir) / file_name,
            "object": mod,
        }
        return info
