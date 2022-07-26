import json
from pathlib import Path
from typing import List, Optional

import numpy as np
from pydantic import BaseModel

from superai import logger
from superai.meta_ai.schema import TaskBatchInput, TaskBatchOutput, TaskInput


class Dataset(BaseModel):
    X_train: Optional[TaskBatchInput]
    X_test: Optional[TaskBatchInput]
    y_train: Optional[TaskBatchOutput]
    y_test: Optional[TaskBatchOutput]
    task_ids_train: Optional[List[int]]
    task_ids_test: Optional[List[int]]
    job_ids_train: Optional[List[int]]
    job_ids_test: Optional[List[int]]

    @classmethod
    def from_file(cls, file_path: Path) -> "Dataset":
        if file_path.suffix == ".npz":
            dataset = Dataset.from_npz(file_path)
        else:
            dataset = Dataset.from_json(file_path)
        return dataset

    @classmethod
    def from_npz(cls, npz_file_path: Path) -> "Dataset":
        logger.info(f"Loading data from {npz_file_path}")
        compressed_file = np.load(str(npz_file_path), allow_pickle=True)
        (X_train, X_test, y_train, y_test, task_ids_train, task_ids_test, job_ids_train, job_ids_test,) = (
            compressed_file["X_train"],
            compressed_file["X_test"],
            compressed_file["y_train"],
            compressed_file["y_test"],
            compressed_file["task_ids_train"],
            compressed_file["task_ids_test"],
            compressed_file["job_ids_train"],
            compressed_file["job_ids_test"],
        )
        return cls(
            X_train=X_train.tolist(),
            X_test=X_test.tolist(),
            y_train=y_train.tolist(),
            y_test=y_test.tolist(),
            task_ids_train=task_ids_train.tolist(),
            task_ids_test=task_ids_test.tolist(),
            job_ids_train=job_ids_train.tolist(),
            job_ids_test=job_ids_test.tolist(),
        )

    @classmethod
    def from_json(cls, json_path: Optional[Path] = None, json_input: Optional[str] = None) -> "Dataset":
        logger.info(f"Loading data from {json_path}. ")
        logger.warning(
            "Creating a dataset from a json file is not recommended. Only the dataset.X_train field is supported."
        )
        if json_path and json_path.is_file():
            with open(json_path, "r") as f:
                json_input = f.read()
        decoded_input = json.loads(json_input)
        is_batch = _is_batch(decoded_input)
        if is_batch:
            input = TaskBatchInput.parse_obj(decoded_input)
        else:
            if not _is_single_input(decoded_input):
                decoded_input = [decoded_input]
            i = TaskInput.parse_obj(decoded_input)
            input = TaskBatchInput(__root__=[i])
        return cls(X_train=input)


def _is_batch(input_object: object) -> bool:
    """
    Checks if the input object is a batch.
    A batch is an Iterable[Iterable[...]]
    Args:
        input_object: object

    Returns:
        bool
    """
    is_batch = False
    try:
        _ = input_object[0][0]
        is_batch = True
    except (KeyError, TypeError, IndexError):
        # If it's not a List[List[...]], it's a single input
        pass
    return is_batch


def _is_single_input(input_object: object) -> bool:
    """
    Checks if the input object is a single input.
    A single input is a list of dicts
    Args:
        input_object: object

    Returns:
        bool
    """
    is_single_input = False
    try:
        _ = input_object[0]
        if isinstance(_, dict):
            is_single_input = True
        else:
            is_single_input = False
    except (KeyError, TypeError, IndexError):
        # If it's not a List[...], it's a single input dict {}
        pass
    return is_single_input
