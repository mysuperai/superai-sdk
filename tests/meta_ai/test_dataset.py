import tarfile
from pathlib import Path
from typing import Dict, List

import jsonlines
import pytest

from superai.meta_ai.base.utils import load_job_dataset
from superai.meta_ai.dataset import Dataset, _is_batch, _is_single_input


def test_dataset_load():
    # open npz file in fixtures subfolder
    npz_file_path = Path(__file__).parent / "fixtures" / "dataset.npz"
    # load dataset
    dataset = Dataset.from_npz(npz_file_path)
    assert dataset.X_train is not None
    assert len(dataset.X_train) == 4


def test__is_batch():
    assert _is_batch([{"a": 1}, {"b": 2}]) == False
    assert _is_batch([{"a": 1}, {"b": 2}, {"c": 3}]) == False
    assert _is_batch(None) == False
    assert _is_batch(1) == False
    assert _is_batch(1.0) == False
    assert _is_batch("") == False
    assert _is_batch([]) == False
    assert _is_batch([[]]) == False

    assert _is_batch([[{"a": 1}, {"b": 2}], [{"c": 3}, {"d": 4}]]) == True
    assert _is_batch([[{}], [{}]]) == True


def test__is_single_input():
    assert _is_single_input(None) == False
    assert _is_single_input(1) == False
    assert _is_single_input(1.0) == False
    assert _is_single_input("") == False
    assert _is_single_input([]) == False
    assert _is_single_input([[]]) == False
    assert _is_single_input({}) == False

    assert _is_single_input([{"a": 1}, {"b": 2}]) == True
    assert _is_single_input([{"a": 1}, {"b": 2}, {"c": 3}]) == True


@pytest.fixture
def create_tar_gz_file(tmp_path):
    def _create_tar_gz_file(content: Dict[str, List[Dict]]) -> Path:
        filepath = tmp_path / "temp.tar.gz"
        with tarfile.open(filepath, mode="w:gz") as tar:
            for key, value in content.items():
                jsonl_file_path = tmp_path / f"{key}.jsonl"
                with jsonl_file_path.open(mode="w") as jsonl_file:
                    writer = jsonlines.Writer(jsonl_file)
                    writer.write_all(value)
                    writer.close()
                tar.add(jsonl_file_path, arcname=f"{key}.jsonl")
        return filepath

    return _create_tar_gz_file


def test_load_job_dataset(create_tar_gz_file):
    # Arrange
    content = {"training": [{"a": 1}, {"b": 2}], "testing": [{"c": 3}], "validation": [{"d": 4}, {"e": 5}]}
    filepath = create_tar_gz_file(content)

    # Act
    result = load_job_dataset(filepath)

    # Assert
    assert len(result) == 3
    assert result["training"] == content["training"]
    assert result["testing"] == content["testing"]
    assert result["validation"] == content["validation"]
