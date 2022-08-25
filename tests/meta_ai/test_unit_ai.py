import logging
import os
import shutil
import tarfile
from pathlib import Path
from subprocess import CalledProcessError

import pytest
from docker import DockerClient
from docker.api import APIClient
from docker.models.images import Image

from superai.meta_ai import AI
from superai.meta_ai.ai_template import AITemplate
from superai.meta_ai.image_builder import AiImageBuilder, Orchestrator, kwargs_warning
from superai.meta_ai.parameters import Config
from superai.meta_ai.schema import Schema


@pytest.fixture
def clean():
    if os.path.exists(".AISave"):
        shutil.rmtree(".AISave")


def test_compression():
    compression_method = AI._compress_folder

    folder_path = os.path.join(".AISave", "new_folder")
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    for i in range(1, 5):
        if i == 4:
            os.makedirs(os.path.join(folder_path, "folder"))
            with open(os.path.join(folder_path, "folder", f"{i}_file.txt"), "w") as file:
                file.writelines(["test"] * i)
        with open(os.path.join(folder_path, f"{i}_file.txt"), "w") as file:
            file.writelines(["test"] * i)
    path_to_tarfile = os.path.join(".AISave", "test_tarfile.tar.gz")
    compression_method(path_to_tarfile, folder_path)

    another_folder_path = os.path.join(".AISave", "another_folder")
    os.makedirs(another_folder_path)
    with tarfile.open(path_to_tarfile) as tar:
        tar.extractall(path=another_folder_path)
    for i in range(1, 5):
        assert os.path.exists(os.path.join(another_folder_path, f"{i}_file.txt"))
    shutil.rmtree(folder_path)
    shutil.rmtree(another_folder_path)
    os.remove(path_to_tarfile)


def test_track_changes(caplog, tmp_path, clean):
    caplog.set_level(logging.INFO)
    template = AITemplate(
        input_schema=Schema(),
        output_schema=Schema(),
        configuration=Config(),
        name="My_template",
        description="Template for my new awesome project",
        model_class="MyKerasModel",
        requirements=["tensorflow", "opencv-python-headless"],
    )
    ai = AI(
        ai_template=template,
        input_params=template.input_schema.parameters(),
        output_params=template.output_schema.parameters(choices=map(str, range(0, 10))),
        name="my_mnist_model2",
        version=1,
    )
    pwd = os.getcwd()
    os.chdir(ai._location)
    with open("requirements.txt", "r") as fp:
        backup_content = fp.read()
    with open("requirements.txt", "a") as fp:
        fp.write("\nscipy")
    builder = AiImageBuilder(
        orchestrator=Orchestrator.LOCAL_DOCKER,
        name=ai.name,
        version=ai.version,
        location=ai._location,
        environs=ai.environs,
        entrypoint_class=template.model_class,
        requirements=ai.requirements,
        conda_env=ai.conda_env,
        artifacts=ai.artifacts,
    )
    assert builder._track_changes(cache_root=tmp_path)
    assert not builder._track_changes(cache_root=tmp_path)
    with open("requirements.txt", "w") as fp:
        fp.write(backup_content)
    assert builder._track_changes(cache_root=tmp_path)
    assert not builder._track_changes(cache_root=tmp_path)
    os.chdir(pwd)


def test_conda_pip_dependencies(caplog, clean):
    caplog.set_level(logging.INFO)
    template = AITemplate(
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
    )
    ai = AI(
        ai_template=template,
        input_params=template.input_schema.parameters(),
        output_params=template.output_schema.parameters(choices=map(str, range(0, 10))),
        name="my_mnist_model2",
        version=1,
    )
    pwd = os.getcwd()
    os.chdir(ai._location)
    with open("requirements.txt", "r") as fp:
        requirements = fp.read()
    with open("environment.yml", "r") as fp:
        conda_env_text = fp.read()
    assert "tensorflow" in conda_env_text
    assert "opencv-python-headless" not in conda_env_text
    assert all(requirement in requirements for requirement in ["opencv-python-headless", "imgaug", "scikit-image"])
    os.chdir(pwd)


@pytest.mark.parametrize("enable_cuda", [True, False])
@pytest.mark.parametrize("skip_build", [True, False])
@pytest.mark.parametrize("build_all_layers", [True, False])
@pytest.mark.parametrize("download_base", [True, False])
def test_builder(caplog, capsys, mocker, enable_cuda, skip_build, build_all_layers, download_base):
    caplog.set_level(logging.DEBUG)
    template = AITemplate(
        input_schema=Schema(),
        output_schema=Schema(),
        configuration=Config(),
        name="My_template",
        description="Template for my new awesome project",
        model_class="DummyModel",
        model_class_path=Path(__file__).parent / "fixtures" / "model",
        requirements=["sklearn"],
    )
    ai = AI(
        ai_template=template,
        input_params=template.input_schema.parameters(),
        output_params=template.output_schema.parameters(choices=map(str, range(0, 10))),
        name="my_dummy_model",
        version=1,
    )
    builder = AiImageBuilder(
        orchestrator=Orchestrator.LOCAL_DOCKER,
        name=ai.name,
        version=ai.version,
        location=ai._location,
        environs=ai.environs,
        entrypoint_class=template.model_class,
        requirements=ai.requirements,
        conda_env=ai.conda_env,
        artifacts=ai.artifacts,
    )
    # Disable actual S2I call until we have efficient way to test it
    mocker.patch("superai.meta_ai.image_builder.system", return_value=0)
    # Mock Docker client and API client
    mock_docker_client = mocker.Mock(spec=DockerClient)
    mock_docker_client.api = mocker.Mock(spec=APIClient)
    mock_image = mocker.Mock(spec=Image)
    mock_image._id = "test_image_id"
    mock_docker_client.images.get.return_value = mock_image
    mock_docker_client.images.pull.return_value = mock_image
    mock_docker_client.api.reload_config.return_value = None
    mocker.patch("superai.meta_ai.image_builder.get_docker_client", return_value=mock_docker_client)
    # Mock s2i availability
    mocker.patch("superai.meta_ai.image_builder.shutil.which", return_value="s2i")
    # Mock ecr login
    mocker.patch("superai.meta_ai.image_builder.aws_ecr_login", return_value=0)
    # Mock ecr registry call
    mocker.patch(
        "superai.meta_ai.image_builder.AiImageBuilder._get_docker_registry",
        return_value="123.dkr.ecr.us-east-1.amazonaws.com",
    )

    image_name = builder.build_image(
        skip_build=skip_build, build_all_layers=build_all_layers, download_base=download_base
    )
    assert image_name == f"{ai.name}:{ai.version}"


def test_system_commands():
    from superai.utils import system

    command = "python --help"
    output = system(command)
    assert output == 0

    with pytest.raises(CalledProcessError) as e:
        system("python random_file_name.py")


def test_base_name():
    assert AiImageBuilder._get_base_name() == f"superai-model-s2i-python3711-cpu:1"
    assert AiImageBuilder._get_base_name(enable_cuda=True) == f"superai-model-s2i-python3711-gpu:1"
    assert AiImageBuilder._get_base_name(lambda_mode=True) == f"superai-model-s2i-python3711-cpu-lambda:1"
    assert AiImageBuilder._get_base_name(k8s_mode=True) == f"superai-model-s2i-python3711-cpu-seldon:1"
    assert (
        AiImageBuilder._get_base_name(k8s_mode=True, enable_cuda=True) == f"superai-model-s2i-python3711-gpu-seldon:1"
    )
    assert (
        AiImageBuilder._get_base_name(k8s_mode=True, enable_cuda=True, use_internal=True)
        == f"superai-model-s2i-python3711-gpu-internal-seldon:1"
    )


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
