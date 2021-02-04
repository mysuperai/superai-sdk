from typing import List

from superai.utils import load_api_key
from superai.config import settings


class BuildConfig(object):
    def __init__(
        self,
        args: str = "",
        build: bool = False,
        build_folder: str = ".hatchery",
        clean_build: bool = False,
        agent: dict = settings.agent,
        api_key: str = None,
        version: str = "0.1",
    ):
        self._excluded_keys = []
        self.args = [] if args == "" else [arg.strip() for arg in args.split(",")]
        self.build = build
        self.build_folder = build_folder
        self.clean_build = clean_build
        self.agent = agent
        self.api_key = api_key or load_api_key()
        self.version = version
        self.validate()

    def validate(self):
        required = ["agent", "api_key", "version"]
        missing = missing_attrs(self, required)
        if missing:
            raise ValueError(f"BuildConfig: Attributes {missing} are required")

    def as_dict(self):
        return dict((key, value) for (key, value) in self.__dict__.items() if key not in self._excluded_keys)


class RuntimeConfig(object):
    def __init__(
        self,
        name: str,
        container: bool = False,
        concurrency: int = 100,
        force_schema: bool = False,
        py3: bool = True,
        local: bool = True,
        serve: bool = True,
        simulation: bool = None,
        environment: List[dict] = [],
    ):
        self.container = container
        self.concurrency = concurrency
        self.force_schema = force_schema
        self.py3 = py3
        self.local = local
        self.serve = serve
        self.name = name
        self.simulation = simulation
        self.environment = environment
        self.validate()

    def validate(self):
        required = ["concurrency"]
        missing = missing_attrs(self, required)
        if missing:
            raise ValueError(f"RuntimeConfig: Attributes {missing} are required")

        if self.container:
            raise NotImplementedError("RuntimeConfig: Running in container is no supported")

        if not self.container and not self.local:
            raise ValueError("RuntimeConfig: Data program has to run either in container or local mode")

    def as_dict(self):
        self._excluded_keys = []
        return dict((key, value) for (key, value) in self.__dict__.items() if key not in self._excluded_keys)


def missing_attrs(obj: object, attr_list: List[str]) -> List[str]:
    missing = []
    for param in attr_list:
        if getattr(obj, param, None) is None:
            missing.append(param)
    return missing
