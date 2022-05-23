import logging
import os
import shutil
import tarfile
from subprocess import CalledProcessError

import pytest

from superai.meta_ai import AI
from superai.meta_ai.ai import AITemplate
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


def test_track_changes(caplog):
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
        name="my_mnist_model",
        version=1,
    )
    pwd = os.getcwd()
    os.chdir(ai._location)
    with open("requirements.txt", "r") as fp:
        backup_content = fp.read()
    with open("requirements.txt", "a") as fp:
        fp.write("\nscipy")
    assert ai._track_changes()
    assert not ai._track_changes()
    with open("requirements.txt", "w") as fp:
        fp.write(backup_content)
    assert ai._track_changes()
    assert not ai._track_changes()
    os.chdir(pwd)


def test_system_commands():
    sys_func = AI._system
    command = "python --help"
    output = sys_func(command)
    assert output == 0

    with pytest.raises(CalledProcessError) as e:
        sys_func("python random_file_name.py")


def test_base_name():
    assert AI._get_base_name() == f"superai-model-s2i-python3711-cpu:1"
    assert AI._get_base_name(enable_cuda=True) == f"superai-model-s2i-python3711-gpu:1"
    assert AI._get_base_name(lambda_mode=True) == f"superai-model-s2i-python3711-cpu-lambda:1"
    assert AI._get_base_name(k8s_mode=True) == f"superai-model-s2i-python3711-cpu-seldon:1"
    assert AI._get_base_name(k8s_mode=True, enable_cuda=True) == f"superai-model-s2i-python3711-gpu-seldon:1"
