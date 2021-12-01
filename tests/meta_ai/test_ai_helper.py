import pytest

from superai.meta_ai.ai_helper import create_model_entrypoint, create_model_handler


@pytest.mark.parametrize("worker_count", [pytest.param(0, marks=pytest.mark.xfail), 1, 2])
def test_create_model_entrypoint(worker_count):
    script = create_model_entrypoint(worker_count=worker_count)
    assert script is not None


@pytest.mark.parametrize("is_lambda", [True, False])
@pytest.mark.parametrize("model_name", ["test_name", pytest.param(None, marks=pytest.mark.xfail)])
def test_create_model_handler(is_lambda, model_name):
    script = create_model_handler(model_name=model_name, lambda_mode=is_lambda, ai_cache=1)
    assert script is not None
