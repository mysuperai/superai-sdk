import logging
import os
import shutil
import tarfile
from pathlib import Path
from subprocess import CalledProcessError

import boto3
import pytest
from docker import DockerClient
from docker.api import APIClient
from docker.models.images import Image
from moto import mock_aws

from superai import settings
from superai.meta_ai import AI, Orchestrator
from superai.meta_ai.ai_helper import _compress_folder
from superai.meta_ai.image_builder import AiImageBuilder, kwargs_warning
from superai.meta_ai.parameters import Config
from superai.meta_ai.schema import Schema


@pytest.fixture
def clean():
    if os.path.exists(".AISave"):
        shutil.rmtree(".AISave")


@pytest.fixture(scope="function")
def aws_credentials(monkeypatch):
    """Mocked AWS Credentials for moto."""
    monkeypatch.setenv("AWS_ACCESS_KEY_ID", "testing")
    monkeypatch.setenv("AWS_SECRET_ACCESS_KEY", "testing")
    monkeypatch.setenv("AWS_SECURITY_TOKEN", "testing")
    monkeypatch.setenv("AWS_SESSION_TOKEN", "testing")


@pytest.fixture(scope="function")
def s3(aws_credentials):
    with mock_aws():
        yield boto3.client("s3", region_name="us-east-1")


@pytest.fixture
def bucket(s3: boto3.client):
    s3.create_bucket(
        Bucket=settings["meta_ai_bucket"],
    )


def test_compression(tmp_path_factory):
    compression_method = _compress_folder
    folder_path = tmp_path_factory.mktemp("test_folder")
    another_folder_path = tmp_path_factory.mktemp("test_folder2")
    destination_folder = tmp_path_factory.mktemp("destination")

    for i in range(1, 5):
        if i == 4:
            os.makedirs(os.path.join(folder_path, "folder"))
            with open(os.path.join(folder_path, "folder", f"{i}_file.txt"), "w") as file:
                file.writelines(["test"] * i)
        with open(os.path.join(folder_path, f"{i}_file.txt"), "w") as file:
            file.writelines(["test"] * i)

    path_to_tarfile = os.path.join(destination_folder, "test_tarfile.tar.gz")
    compression_method(path_to_tarfile, folder_path)

    with tarfile.open(path_to_tarfile) as tar:
        tar.extractall(path=another_folder_path)
    for i in range(1, 5):
        assert os.path.exists(os.path.join(another_folder_path, f"{i}_file.txt"))


def test_conda_pip_dependencies(caplog, clean, bucket, tmp_path):
    caplog.set_level(logging.INFO)
    ai = AI(
        input_schema=Schema(),
        output_schema=Schema(),
        configuration=Config(),
        name="My_template",
        description="Template for my new awesome project",
        model_class="MyKerasModel",
        conda_env={
            "name": "keras-model",
            "dependencies": ["pip", "tensorflow", {"pip": ["opencv-python-headless"]}],
        },
        requirements=["imgaug", "scikit-image"],
        version="1.0",
    )
    # Export the AI (as we do for deployment)
    output_path = ai._save_local(tmp_path)
    with open(output_path / "requirements.txt", "r") as fp:
        requirements = fp.read()
    with open(output_path / "environment.yml", "r") as fp:
        conda_env_text = fp.read()
    assert "tensorflow" in conda_env_text
    assert "opencv-python-headless" not in conda_env_text
    assert all(requirement in requirements for requirement in ["opencv-python-headless", "imgaug", "scikit-image"])


@pytest.mark.parametrize("enable_cuda", [True, False])
@pytest.mark.parametrize("skip_build", [True, False])
@pytest.mark.parametrize("build_all_layers", [True, False])
@pytest.mark.parametrize("download_base", [True, False])
def test_builder(caplog, capsys, mocker, enable_cuda, skip_build, build_all_layers, download_base, bucket, tmp_path):
    caplog.set_level(logging.DEBUG)
    ai = AI(
        input_schema=Schema(),
        output_schema=Schema(),
        configuration=Config(),
        description="Template for my new awesome project",
        model_class="DummyAI",
        model_class_path=Path(__file__).parent / "fixtures" / "model",
        requirements=["sklearn"],
        name="my_dummy_model",
        version="1.0",
    )
    builder = AiImageBuilder(orchestrator=Orchestrator.LOCAL_DOCKER_K8S, ai=ai)
    # Mock Docker client and API client
    mock_docker_client = mocker.Mock(spec=DockerClient)
    mock_docker_client.api = mocker.Mock(spec=APIClient)
    mock_image = mocker.Mock(spec=Image)
    mock_image.id = "test_image_id"
    mock_docker_client.images.get.return_value = mock_image
    mock_docker_client.images.pull.return_value = mock_image
    mock_docker_client.api.reload_config.return_value = None
    mocker.patch("superai_builder.docker.client.get_docker_client", return_value=mock_docker_client)
    # Mock ecr registry call
    mocker.patch(
        "superai.meta_ai.image_builder.AiImageBuilder._get_docker_registry",
        return_value="123.dkr.ecr.us-east-1.amazonaws.com",
    )
    mocker.patch("superai_builder.ai.image_build.os.path.expanduser", return_value=str(tmp_path))
    Path(tmp_path / ".aws").mkdir(parents=True, exist_ok=True)
    Path(tmp_path / ".superai").mkdir(parents=True, exist_ok=True)
    Path(tmp_path / ".canotic").mkdir(parents=True, exist_ok=True)

    mocker.patch("superai_builder.ai.image_build.AIImageBuilder.run", return_value=None)

    image_name = builder.build_image(skip_build=skip_build)
    assert image_name == f"{ai.name}:{ai.version}"


def test_system_commands():
    from superai.utils import system

    command = "python --help"
    output = system(command)
    assert output == 0

    with pytest.raises(CalledProcessError) as e:
        system("python random_file_name.py")


def test_kwargs_warning(monkeypatch):
    from superai.meta_ai.ai import log

    def warn_method(*_, **__):
        assert False, "Should not be called"

    def dummy_method(some_argument: bool = False, other_argument: bool = True, **kwargs):
        assert "some_argument" not in list(kwargs.keys())
        assert "other_argument" not in list(kwargs.keys())
        assert "random_arg" in list(kwargs.keys())
        kwargs_warning(allowed_kwargs=["random_arg"], **kwargs)

    monkeypatch.setattr(log, "warn", warn_method)
    dummy_method(random_arg="bla")
