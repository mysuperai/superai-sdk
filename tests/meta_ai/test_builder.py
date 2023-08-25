import pytest

from superai.meta_ai import AiImageBuilder
from superai.meta_ai.parameters import AiDeploymentParameters


def test_get_base_image():
    # Test with CUDA
    parameters = AiDeploymentParameters(enable_cuda=True)
    base_image = AiImageBuilder._get_base_image(parameters, python_version="3.10", user_base_image=None)
    assert "cuda" in base_image

    # Test without CUDA, the fallback is the default python image
    parameters = AiDeploymentParameters(enable_cuda=False)
    base_image = AiImageBuilder._get_base_image(parameters, python_version="3.10", user_base_image=None)
    assert "cuda" not in base_image
    assert "python" in base_image
    assert "3.10" in base_image

    # Test with user provided base image
    parameters = AiDeploymentParameters(enable_cuda=False)
    base_image = AiImageBuilder._get_base_image(parameters, python_version="3.10", user_base_image="user/base:1.0")
    assert base_image == "user/base:1.0"

    # Check that a wrong formatted python version raises an error
    with pytest.raises(ValueError):
        AiImageBuilder._get_base_image(parameters, python_version="3.10.1", user_base_image=None)
    with pytest.raises(ValueError):
        AiImageBuilder._get_base_image(parameters, python_version="3", user_base_image=None)
