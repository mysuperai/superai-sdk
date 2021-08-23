import os
import shutil
import tarfile

import pytest
from superai.meta_ai import AI


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


def test_system_commands():
    sys_func = AI._system
    command = "python --help"
    output = sys_func(command)
    assert "python [option]" in output
