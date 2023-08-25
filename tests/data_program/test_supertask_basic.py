from unittest.mock import patch

import pytest

from superai.data_program.task.basic import Task, WorkerType

sample_task = Task()


def test_create_task_future_bots():
    task_name = "custom_name"
    with patch("superai.data_program.task.basic.task") as mock_task:
        sample_task._create_task_future(name=task_name, worker_type=WorkerType.bots)
        # bots are mapped to CROWD
        mock_task.assert_called_once_with(name=task_name, worker_type="CROWD", groups=["BOTS"], explicit_id=None)


def test_create_task_future_ai_valid():
    task_name = "custom_name"
    with patch("superai.data_program.task.basic.task") as mock_task:
        included_ids = ["model_id"]
        sample_task._create_task_future(name=task_name, worker_type=WorkerType.ai, included_ids=included_ids)
        mock_task.assert_called_once_with(name=task_name, worker_type="AI", groups=None, explicit_id="model_id")


def test_create_task_future_ai_invalid():
    included_ids = ["model1", "model2"]
    with pytest.raises(ValueError, match="Invalid configuration. AI worker requires one and only one model ID"):
        sample_task._create_task_future(worker_type=WorkerType.ai, included_ids=included_ids)


def test_create_task_future_custom_name():
    with patch("superai.data_program.task.basic.task") as mock_task:
        task_name = "custom_name"
        sample_task._create_task_future(name=task_name)
        mock_task.assert_called_once_with(name=task_name, worker_type=None, groups=None, explicit_id=None)
