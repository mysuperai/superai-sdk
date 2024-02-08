from __future__ import annotations

import json
import os
import re
import shutil
import tarfile
import tempfile
import uuid
from copy import deepcopy
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING, List, Optional, Union
from urllib.parse import urlparse

import boto3
import yaml
from superai_builder.ai.image_build import AIImageBuilder

from superai.log import logger
from superai.meta_ai.ai_helper import _compress_folder
from superai.meta_ai.ai_uri import AiURI
from superai.meta_ai.base.utils import pull_weights
from superai.meta_ai.environment_file import EnvironmentFileProcessor

if TYPE_CHECKING:
    from superai.meta_ai import AI


MODEL_WORKDIR = "AISavedModel"
MODEL_ZIPFILE = f"{MODEL_WORKDIR}.tar.gz"

ENV_VAR_FILENAME = "environment"
CONDA_ENV_FILE_NAME = "environment.yml"
REQUIREMENTS_FILE_NAME = "requirements.txt"
ARTIFACT_SETUP_SCRIPT_NAME = "setup.sh"
TEMPLATE_SAVE_FILE_NAME = "AISaveFile.yaml"

# Prefix path for the model directory on storage backend
MODEL_ARTIFACT_PREFIX_S3 = "meta_ai_models"

log = logger.get_logger(__name__)

AI_URI_PREFIX = "ai://"
AI_S3_PREFIX = "s3://"


class AILoader:
    """Class to load and store an AI Template from/to a local or S3 path."""

    builder = AIImageBuilder(
        environment_file_name=CONDA_ENV_FILE_NAME,
        requirements_file_name=REQUIREMENTS_FILE_NAME,
        setup_script_name=ARTIFACT_SETUP_SCRIPT_NAME,
    )

    @classmethod
    def load_ai(
        cls, identifier: Union[Path, str], weights_path: Optional[Union[Path, str]] = None, pull_db_data=True
    ) -> AI:
        """Loads an AI from a local or S3 path.

        If the path is a valid local path, the AI model will be loaded from the local path. If the path is a valid S3 path,
        the model will be downloaded from S3. Manage S3 access using your AWS credentials. If the path is a valid model path
        (i.e., prefix is `ai://some_name/version` or `ai://some_name/stage`), the database will be queried to find the
        relevant model and loaded.

        Args:
            identifier: The path to the AI model.
            weights_path: The path to the model weights file (if any).
            pull_db_data: If True, will pull the latest data from the database and overwrite the local model config.

        Returns:
            An AI object

        Raises:
            ValueError: If the path is not valid.
        """
        # Test if path is local
        weights_path = str(weights_path) if weights_path else None
        identifier_string = str(identifier)
        identifier_path = Path(identifier)
        if identifier_string.startswith(AI_S3_PREFIX):
            return cls.load_from_s3(identifier_string, weights_path, pull_db_data=pull_db_data)
        elif identifier_string.startswith(AI_URI_PREFIX):
            ai_dict = cls._get_ai_by_uri(identifier_string)
            s3_path = cls._get_s3_path_from_ai_dict(ai_dict)
            return cls.load_from_s3(s3_path, weights_path, pull_db_data=pull_db_data)
        elif _is_uuid(identifier_string):
            ai_dict = cls._get_ai_dict_by_id(identifier_string)
            s3_path = cls._get_s3_path_from_ai_dict(ai_dict)
            return cls.load_from_s3(s3_path, weights_path, pull_db_data=pull_db_data)
        elif identifier_path.exists():
            return cls.load_local(identifier_path, weights_path, pull_db_data=pull_db_data)
        else:
            raise ValueError("Invalid path, please ensure the path exists")

    @classmethod
    def load_essential(cls, identifier: Union[Path, str]) -> AI:
        """Loads only the AI database data, skipping S3 downloads.

        Args:
            identifier: The path or ID of the AI model.

        Returns:
            An AI object with only database data loaded.

        Raises:
            ValueError: If the identifier is not valid.
        """
        identifier_string = str(identifier)
        if identifier_string.startswith(AI_URI_PREFIX):
            ai_dict = cls._get_ai_by_uri(identifier_string)
        elif _is_uuid(identifier_string):
            ai_dict = cls._get_ai_dict_by_id(identifier_string)
        else:
            raise ValueError("Invalid identifier, please ensure it's either a URI or UUID")
        from superai.meta_ai.ai import AI

        return AI.from_dict(ai_dict)

    @classmethod
    def _get_ai_by_uri(cls, raw_uri: str) -> dict:
        """Find the AI model in the backend via API via its URI and return its S3 save path.

        Args:
            raw_uri: The URI of the AI model.

        Returns:
            The dict of an AI from database.

        """
        uri = AiURI.parse(raw_uri)
        from superai import Client

        if uri.owner_name and uri.owner_name != "superai":
            # TODO: Resolve the namespace to an ID ( owner / organization )
            raise NotImplementedError(
                "Namespace resolution is not implemented yet. We only support loading ai://superai/... URIs"
            )

        client = Client.from_credentials(organization_name=uri.owner_name)
        if uri.version:
            ai_list = client.list_ai(name=uri.model_name, version=uri.version, verbose=True, to_json=True)
        else:
            ai_list = client.list_ai(name=uri.model_name, verbose=True, to_json=True)

        if len(ai_list) == 0:
            raise ValueError(f"AI for URI {uri} not found. Make sure you have access to load.")
        elif len(ai_list) > 1:
            # Fallback to the latest version
            # Iterate over the list and find the one with the latest creation date
            log.warning(f"Multiple AIs found for URI {uri}. Loading the latest version.")
            ai_list = cls.sort_ai_by_timestamp(ai_list)

            # TODO: add check for owner name so that we can infer if the caller wants the user or organization model
            # e.g.  if client.get_current_user() == ai.owner_name

        return ai_list[0]

    @staticmethod
    def sort_ai_by_timestamp(ai_list: list, date_format: str = "%Y-%m-%dT%H:%M:%S.%f%z") -> list:
        """Sort a list of AI dictionaries by the 'created_at' field.

        Args:
            ai_list: List of AI dictionaries.
            date_format: The format of the 'created_at' field.

        Returns:
            The sorted list of AI dictionaries.
        """
        return sorted(ai_list, key=lambda x: datetime.strptime(x["created_at"], date_format), reverse=True)

    @classmethod
    def _get_ai_dict_by_id(cls, ai_id: str) -> dict:
        """Find the AI model in the backend via API via its ID and return its data.

        Args:
            ai_id: The ID of the AI model.

        Returns:
            The dict of an AI from database.

        """
        from superai import Client

        client = Client.from_credentials()
        return client.get_ai(ai_id, to_json=True)

    @staticmethod
    def _get_s3_path_from_ai_dict(ai: dict) -> str:
        s3_path = ai["model_save_path"]
        if not s3_path:
            from superai.meta_ai.exceptions import AIException

            raise AIException("AI model was not uploaded to the backend yet. Try ai.save() first before loading.")
        return s3_path

    @classmethod
    def load_from_s3(cls, path: str, weights_path: Optional[str] = None, pull_db_data=False) -> "AI":
        """Load an AI Template from an S3 path.

        The AI Template is downloaded from S3, unpacked, and then loaded using the `load_local` method.

        Args:
            path: The S3 path of the AI model. The path should start with `s3` and end with `AISavedModel.tar.gz`.
            weights_path: The path to the model weights file (if any).
            pull_db_data: Update the AI object with data from the database.

        Returns:
            An instance of the `AI` class.

        Raises:
            AssertionError: If the path is invalid.
        """
        cls._validate_s3_path(path)
        log.info(f"Loading from '{path}' with weights in '{weights_path}'")

        download_folder = cls._create_temp_folder()
        log.info(f"Storing temporary files in {download_folder}")

        cls._download_and_extract_model(path, download_folder)

        return cls.load_local(
            load_path=download_folder / MODEL_WORKDIR,
            weights_path=weights_path,
            download_folder=download_folder,
            pull_db_data=pull_db_data,
        )

    @staticmethod
    def _validate_s3_path(path: str) -> None:
        assert path.startswith("s3") and path.endswith(
            MODEL_ZIPFILE
        ), f"Invalid path provided, should start with s3 and end with {MODEL_ZIPFILE}"

    @staticmethod
    def _create_temp_folder() -> Path:
        temp_folder = tempfile.mkdtemp(prefix="ai_contents_")
        return Path(temp_folder)

    @classmethod
    def _download_and_extract_model(cls, path: str, download_folder: Path) -> None:
        parsed_url = urlparse(path, allow_fragments=False)
        bucket_name = parsed_url.netloc
        path_to_object = parsed_url.path[1:] if parsed_url.path.startswith("/") else parsed_url.path
        log.info(f"Downloading and unpacking AI object from bucket `{bucket_name}` and path `{path_to_object}`")

        cls._download_model(bucket_name, path_to_object, download_folder)
        cls._extract_model(download_folder)

    @staticmethod
    def _download_model(bucket_name: str, path_to_object: str, download_folder: Path) -> None:
        s3 = boto3.client("s3")
        s3.download_file(bucket_name, path_to_object, str(download_folder / MODEL_ZIPFILE))

    @staticmethod
    def _extract_model(download_folder: Path) -> None:
        with tarfile.open(str(download_folder / MODEL_ZIPFILE)) as tar:
            tar.extractall(path=str(download_folder / MODEL_WORKDIR))

    @classmethod
    def load_local(
        cls,
        load_path: Union[Path, str],
        weights_path: Optional[str] = None,
        download_folder: Optional[Union[Path, str]] = None,
        pull_db_data: bool = False,
    ) -> AI:
        """Loads AI model stored locally.

        Args:
            weights_path: Location of weights.
            load_path: The location of the AISave or any other matching folder.
            download_folder: The folder where the downloaded files are stored.

        """
        load_path = Path(load_path)
        log.info(f"Attempting to load model from {load_path}...")
        save_file = load_path / TEMPLATE_SAVE_FILE_NAME
        from superai.meta_ai.ai import AI

        loaded_ai = AI.from_yaml(save_file, pull_db_data=pull_db_data, override_weights_path=weights_path)
        loaded_ai._location = load_path
        log.info(f"Loaded model {loaded_ai}")
        cls._load_weights(weights_path, str(download_folder))
        return loaded_ai

    @classmethod
    def save_local(cls, ai: AI, path: Union[Path, str] = ".AISave", overwrite: bool = False) -> Path:
        """Packages and saves the model locally for later uploading/loading.

        Args:
            ai: The AI model to save.
            path: The path to save the model to.
            overwrite: Whether to overwrite existing files in the path.
        """
        version_save_path = Path(path)  # Disabled subdirectories as part of path for now

        if not version_save_path.exists():
            version_save_path.mkdir(parents=True)
        elif overwrite:
            log.info(f"Removing existing content from path: {version_save_path}")

            shutil.rmtree(version_save_path)
            version_save_path.mkdir(parents=True)

        cls.export_all(ai, version_save_path)
        log.info(f"Saved model in {version_save_path}")
        return version_save_path

    @classmethod
    def _load_weights(cls, weights_path: str, download_folder: Optional[str] = None) -> Optional[str]:
        """Load weights from a given path.

        Supports:
        - Local paths
        - S3 paths to folders
        - S3 paths to tar.gz files

        Args:
            weights_path (str): Path to the weights file in local filesystem or S3.
            download_folder (Optional[str], optional): Folder to download S3 files to.
                    By default will use subfolder in /tmp.

        Raises:
            ValueError: If an unsupported or non-existent weights path is provided.

        Returns:
            str: Path to the downloaded or local weights.
        """
        if not weights_path:
            log.info("No weights path provided, skipping weights loading")
            return

        log.info(f"Loading weights from {weights_path}")
        if weights_path.startswith("s3"):
            weights_path = cls._download_s3_weights(weights_path, download_folder)
        elif not os.path.exists(weights_path):
            raise ValueError(
                f"Unexpected weights path provided {weights_path}. " "Please ensure it's an S3 path or a local folder."
            )
        return weights_path

    @staticmethod
    def _download_s3_weights(weights_s3_key: str, download_folder: Optional[str] = None, prefix="local_weights") -> str:
        """Download weights from S3 into specified folder.
        If download_folder is not specified, will use a temporary folder."""
        log.info(f"Downloading weights from S3 {weights_s3_key}")

        # Extract bucket and object key
        parsed_url = urlparse(weights_s3_key, allow_fragments=False)
        path_to_object = parsed_url.path.lstrip("/")

        # Prepare download folder
        download_folder = download_folder or os.path.join(tempfile.gettempdir(), prefix, path_to_object)
        os.makedirs(download_folder, exist_ok=True)
        log.info(f"Using local folder for weights: {download_folder}")

        # Download weights
        path = pull_weights(weights_uri=weights_s3_key, output_path=download_folder)

        return path

    @classmethod
    def export_all(cls, ai, target_directory: Union[str, Path]):
        """Save the AI to a given path.
        This will copy the code, requirements, conda environment and also dump the ai metadata to a json file.
        """
        # Copy the ai to avoid side effects when changing fields
        ai_clone = deepcopy(ai)
        target_directory = Path(target_directory)

        conda_target = cls._dump_conda_env(ai_clone, target_directory)

        cls._copy_dockerfile(ai_clone, target_directory)

        cls._copy_source(ai_clone, target_directory)

        cls._copy_requirements(ai_clone, conda_target, target_directory)

        cls._copy_setup_script(ai_clone, target_directory)

        cls._create_environment_file(ai_clone, conda_target, target_directory)

        # Save json
        save_file_path = target_directory / TEMPLATE_SAVE_FILE_NAME
        with open(save_file_path, "w") as ai_ai_writer:
            content = ai_clone.to_dict()
            json.dump(content, ai_ai_writer, indent=1)

    @staticmethod
    def _create_environment_file(ai: AI, conda_target: Path, version_save_path: Union[Path, str]):
        """
        Create and save the environment file for the project AI. It creates an 'EnvironmentFileProcessor' object
        for the specified version save path and sets the 'MODEL_NAME', 'MODEL_CLASS_PATH', and 'CONDA_ENV_NAME' environment
        variables for the project AI. If the 'conda_target' file exists, it extracts the 'name' key from the '.yml'
        file and sets it as the value for 'CONDA_ENV_NAME' environment variable.

        Args:
            conda_target (Path): The path to the 'environment.yml' file.
            version_save_path (str): The path to the save directory.

        Raises:
            yaml.YAMLError: If there is an error in the formatting of the 'environment.yml' file.
        """
        ai._environs = EnvironmentFileProcessor(os.path.abspath(version_save_path), filename=ENV_VAR_FILENAME)
        ai._environs.add_or_update("MODEL_NAME", ai.model_class)
        model_module_path = ai.model_class_path
        if model_module_path != Path("."):
            log.debug("Copying model_class_path")
            ai._environs.add_or_update("MODEL_CLASS_PATH", str(model_module_path).replace("/", "."))
        if conda_target.exists():
            with open(conda_target, "r") as env_yaml:
                try:
                    conda_env_yaml = yaml.safe_load(env_yaml)
                    ai._environs.add_or_update("CONDA_ENV_NAME", conda_env_yaml.get("name", "env"))
                except yaml.YAMLError as exc:
                    log.error(exc)

    @classmethod
    def _copy_setup_script(cls, ai: AI, target: Path):
        # Save setup script
        if ai.artifacts is not None and "run" in ai.artifacts:
            shutil.copy(Path(ai.artifacts["run"]), target / ARTIFACT_SETUP_SCRIPT_NAME)
        cls.builder.ensure_setup_script(target)

    @staticmethod
    def copy_requirements_txt(ai: AI, requirements_target_file: Path):
        """Copy the requirements.txt file to the target directory"""
        if ai.requirements is not None:
            log.debug("Copying all requirements")
            if type(ai.requirements) == str:
                requirements_file = Path(ai.requirements)
                whl_file_folder = requirements_file.parent
                if requirements_file.exists():
                    shutil.copy(requirements_file, requirements_target_file)
            elif type(ai.requirements) == list:
                with open(requirements_target_file, "w") as f:
                    f.write("\n".join(ai.requirements))
                whl_file_folder = ai.artifacts.get("whl_file_folder", None) if ai.artifacts is not None else None
            else:
                raise ValueError(
                    "Make sure requirements is a list of requirements or valid path to requirements.txt file"
                )
            if whl_file_folder is not None:
                for filename in whl_file_folder.iterdir():
                    if filename.suffix == ".whl":
                        log.info(f"Copying whl file {filename.name}")
                        shutil.copy(filename, requirements_target_file.parent / filename.name)

    @staticmethod
    def extract_pip_from_conda(conda_target_file: Path):
        """We only install Python dependencies from conda environment file.
        In case there are pip dependencies, we extract them and install them with conda later"""
        conda_pip_packages = None
        if conda_target_file.exists():
            conda_env_text = conda_target_file.read_text()
            if "pip:" in conda_env_text:
                # Extract pip dependencies from conda environment file
                conda_env_dict = yaml.safe_load(conda_env_text)
                conda_dependencies = conda_env_dict.get("dependencies", {})
                for package in conda_dependencies:
                    if isinstance(package, dict) and "pip" in package:
                        conda_pip_packages = package.pop("pip")

                if conda_pip_packages is not None:
                    # Write the environment file without the pip dependencies
                    # pip dependencies will be installed separately from conda dependencies
                    with open(conda_target_file, "w") as f:
                        yaml.dump(conda_env_dict, f, sort_keys=False)

        return conda_pip_packages

    @classmethod
    def _copy_requirements(cls, ai: AI, conda_target_file: Path, target_folder: Path):
        """Copy all pip and conda requirements to the target folder.
        If there are pip dependencies in the conda environment file, they will be extracted and merged with conda dependencies.
        """
        requirements_target_file = target_folder / REQUIREMENTS_FILE_NAME
        cls.copy_requirements_txt(ai, requirements_target_file)

        conda_pip_packages = cls.extract_pip_from_conda(conda_target_file)

        if conda_pip_packages is not None:
            # Append pip packages extracted from conda env to the requirements file
            initial_line = "\n" if ai.requirements is not None else ""
            with open(requirements_target_file, "a") as f:
                f.write(initial_line + "\n".join(conda_pip_packages))

        ai.requirements = str(requirements_target_file) if requirements_target_file.exists() else None
        cls.builder.ensure_requirements(target_folder)
        return requirements_target_file

    @classmethod
    def _copy_dockerfile(cls, ai: AI, target: Path):
        """Copy Dockerfile if it exists, otherwise create one from builder"""
        dockerfile_target = cls.builder.get_dockerfile_path(target)

        if ai.dockerfile is not None:
            log.debug("Copying Dockerfile")
            dockerfile = Path(ai.dockerfile)
            if dockerfile.is_file() and dockerfile.name == "Dockerfile":
                shutil.copy(dockerfile, dockerfile_target)
            else:
                logger.warning("dockerfile is not a valid path, copying the default Dockerfile")
                cls.builder.copy_docker_file(target)
        else:
            cls.builder.copy_docker_file(target)
        return dockerfile_target

    @classmethod
    def _copy_source(cls, ai: AI, target: Path):
        """
        Copy the code directories and files of the AI ai to the specified target folder. The function first
        appends the 'model_class_path' attribute to the 'code_path' attribute of the project ai, and validates the
        code paths. Then it copies each code path from the AI ai to the target folder using 'shutil.copytree' or
        'shutil.copy', depending on whether the path represents a directory or a file. If 'model_class_path' is not a valid
        python module, the function creates an empty '__init__.py' file in the target folder.

        Args:
            target (Path): The path to the target folder.

        Raises:
            ValueError: If any path in the 'code_path' attribute of the project ai is not a valid path to a local
            directory or file.
        """
        cwd = Path(os.getcwd())
        if ai.model_class_path in ai.code_path:
            log.warning("model_class_path already matches one entry in code_path. This is most likely redundant.")
        ai.model_class_path = Path(ai.model_class_path).absolute().relative_to(cwd)
        ai.code_path.append(ai.model_class_path)

        cls._validate_code_paths(ai.code_path)

        log.info(f"Copying over: {', '.join(map(str, ai.code_path))}")
        ignore_ai_save = shutil.ignore_patterns(target.name)
        new_relative_code_paths = []
        for p in ai.code_path:
            path = p.absolute().relative_to(cwd)
            if path.is_dir():
                shutil.copytree(path, target / path, dirs_exist_ok=True, ignore=ignore_ai_save)
            elif path.is_file():
                shutil.copy(path, target / path)
            else:
                raise ValueError(f"{path} does not represent a valid path to a local directory or file.")
            new_relative_code_paths.append(Path(path))
        ai.code_path = new_relative_code_paths

        # Ensure that model_class_path is python module with __init__.py for correct import
        model_module = target / ai.model_class_path / "__init__.py"
        if not model_module.is_file():
            model_module.touch()

    @staticmethod
    def _validate_code_paths(code_path: List[Path]):
        if code_path is not None:
            cwd = Path(os.getcwd())
            for path in code_path:
                path_object = path.absolute()
                log.info(f"Validating {path_object} with working directory {cwd}")
                if cwd == path_object:
                    log.warning(
                        "code_path or model_class_path is pointing to the current working directory."
                        " This can be the case when `./` or `.` is used in the code_path or model_class_path."
                        " This is not recommended since all project files will be copied."
                        " We recommend putting source files in sub-directories."
                    )

    @classmethod
    def _dump_conda_env(cls, ai: AI, target: Path):
        """
        Save the conda environment file of the AI ai to the specified target folder. If the project ai
        has a 'conda_env' attribute, it will either write the dictionary to the 'environment.yml' file or copy the
        specified '.yml' or '.yaml' file to the target folder. The path to the 'environment.yml' file is returned at the
        end of the function.

        Args:
            target (Path): The path to the target folder.

        Returns:
            Path: The path to the 'environment.yml' file.

        Raises:
            ValueError: If 'conda_env' is not a valid path to a '.yml' or '.yaml' file, or a dictionary.
        """
        conda_target = target / CONDA_ENV_FILE_NAME
        if ai.conda_env is not None:
            log.debug("Copying conda env")
            if type(ai.conda_env) == dict:
                with open(conda_target, "w") as f:
                    yaml.dump(ai.conda_env, f, default_flow_style=False)
            elif type(ai.conda_env) == str:
                conda_file = Path(ai.conda_env)
                if conda_file.is_file() and conda_file.suffix in [".yml", ".yaml"]:
                    shutil.copy(conda_file, conda_target)
                else:
                    raise ValueError("Make sure conda_env is a valid path to a .yml or .yaml file.")
            else:
                raise ValueError("Make sure conda_env is a valid path to a .yml file or a dictionary.")
            ai.conda_env = str(conda_target)
        cls.builder.ensure_environment(target)
        return conda_target

    @classmethod
    def upload_model_folder(
        cls, location: Union[str, Path], model_id: str, name: str, version: str, bucket_name: str
    ) -> str:
        """
        Uploads a compressed model folder to an S3 bucket.

        Parameters:
        -----------
        location : str
            The path to the folder containing the model files to be uploaded.
        model_id : str
            A unique identifier for the model.
        name : str
            The name of the model.
        version : int
            The version number of the model.
        bucket_name : str
            The name of the S3 bucket where the model files will be uploaded.

        Returns:
        --------
        str
            The S3 path where the model files were uploaded.

        Raises:
        -------
        Any exceptions raised by boto3.client or _compress_folder functions.

        """
        assert bucket_name, "Bucket name cannot be empty"
        location = Path(location)
        s3_client = boto3.client("s3")
        path_to_tarfile = location / MODEL_ZIPFILE

        log.info(f"Compressing AI folder at {location}")
        _compress_folder(path_to_tarfile, location)

        object_name = os.path.join(MODEL_ARTIFACT_PREFIX_S3, model_id, name, version, MODEL_ZIPFILE)
        log.info(f"Uploading AI object to '{object_name}' in bucket '{bucket_name}'")
        with open(path_to_tarfile, "rb") as f:
            s3_client.upload_fileobj(f, bucket_name, object_name)

        model_save_path = os.path.join("s3://", bucket_name, object_name)
        log.info(f"Uploaded AI object to '{model_save_path}'")
        return model_save_path

    @classmethod
    def parse_model_uri(cls, uri: str):
        """
        Parse a model URI and return its components.

        Args:
            uri (str): The model URI in the format ai://<username>/modelname/version,
                       ai://modelname/version or ai://modelname

        Returns:
            dict: A dictionary containing the components 'username', 'modelname', and 'version'
        """
        components = {}

        # Define the regular expression for parsing the URI
        # fmt: off
        pattern = r"^ai://" \
                  r"(?:(?P<username>[\w-]+)/)?" \
                  r"(?P<modelname>[\w\-_]+)" \
                  r"(?:(?:/)(?P<version>\d+\.\d+))?$"
        # fmt: on

        # Try to match URI with the pattern
        match = re.match(pattern, uri)
        if match:
            components = match.groupdict()

        # If no match is found, raise an exception
        if not components:
            raise ValueError(f"Invalid model URI format: {uri}")

        return components


def _extract_tar_gz_weights(target_folder: str, weights_path: str) -> str:
    """Extracts a tar.gz file and returns the path to the extracted folder.

    Args:
        target_folder (str): The path to the folder where the tar.gz file should be extracted.
        weights_path (str): The path to the tar.gz file to extract.

    Returns:
        str: The path to the folder where the tar.gz file was extracted.

    Raises:
        FileNotFoundError: If the tar.gz file specified by `weights_path` does not exist.

    """
    weights_folder_name = os.path.basename(weights_path).split(".tar.gz")[0]
    extracted_weights_path = os.path.join(target_folder, weights_folder_name)
    with tarfile.open(os.path.join(target_folder, os.path.basename(weights_path))) as tar_weights:
        tar_weights.extractall(path=target_folder)
    log.info(f"New weights path {extracted_weights_path}")
    shutil.rmtree(os.path.join(target_folder, os.path.basename(weights_path)))
    return extracted_weights_path


def _is_uuid(string: str) -> bool:
    """Checks if a string is a valid UUID.

    Args:
        string (str): The string to check.

    Returns:
        bool: True if the string is a valid UUID, False otherwise.

    """
    try:
        uuid.UUID(string)
        return True
    except ValueError:
        return False
