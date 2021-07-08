import os
import shutil
import tarfile

import pytest

from superai.meta_ai import AI, BaseModel
from superai.meta_ai.ai import AITemplate
from superai.meta_ai.parameters import Config
from superai.meta_ai.schema import Schema, SchemaParameters


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


def test_create_dockerfile_cuda_check(clean):
    class SomeClass(BaseModel):
        pass

    mock_template = AITemplate(
        input_schema=Schema(),
        output_schema=Schema(),
        configuration=Config(),
        model_class=SomeClass,
        name="MockTemplate",
        description="Some mocked template",
    )
    mock_ai = AI(
        mock_template, input_params=SchemaParameters(), output_params=SchemaParameters(), name="Mock_AI_instance"
    )

    content_cpu = mock_ai._create_dockerfile(lambda_mode=False, enable_cuda=False)
    content_gpu = mock_ai._create_dockerfile(lambda_mode=False, enable_cuda=True)

    assert content_cpu[1] != content_gpu[1], "Different Base images should be present"
    assert content_cpu[2:] == content_gpu[2:], "Rest of the content should be the same"
