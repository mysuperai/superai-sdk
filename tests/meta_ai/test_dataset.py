from pathlib import Path

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
