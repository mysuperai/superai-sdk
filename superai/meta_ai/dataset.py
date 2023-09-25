import contextlib
import json
import math
from pathlib import Path
from typing import List, Optional

import numpy as np
from pydantic import BaseModel, Field, root_validator

from superai.log import logger
from superai.meta_ai.schema import TaskBatchInput, TaskBatchOutput, TaskInput


class DatasetMetadata(BaseModel):
    """Model to store dataset metadata.
    The metadata is used during dataset creation and specifies the split of the dataset.
    """

    test_fraction: float = Field(0.2, alias="test_fraction", ge=0.0, lt=1.0)
    training_fraction: float = Field(0.7, alias="training_fraction", gt=0.0, le=1.0)
    validation_fraction: float = Field(0.1, alias="validation_fraction", ge=0.0, lt=1.0)

    @root_validator
    def check_fractions_sum(cls, values):
        test_fraction = values.get("test_fraction", 0)
        training_fraction = values.get("training_fraction", 0)
        validation_fraction = values.get("validation_fraction", 0)

        total = test_fraction + training_fraction + validation_fraction

        if not math.isclose(total, 1.0):
            raise ValueError("Fractions must sum up to 1.0")

        return values


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
        return Dataset.from_npz(file_path) if file_path.suffix == ".npz" else Dataset.from_json(file_path)

    @classmethod
    def from_npz(cls, npz_file_path: Path) -> "Dataset":
        logger.info(f"Loading data from {npz_file_path}")
        compressed_file = np.load(str(npz_file_path), allow_pickle=True)
        return cls(**{name: compressed_file[name].tolist() for name in cls.__fields__})

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

    def __str__(self) -> str:
        """Represent dataset by length of its arrays.
        Returns:

        """
        array_sizes = [
            len(getattr(self, array_name)) if getattr(self, array_name) else None for array_name in self.__fields__
        ]
        len_strings = ", ".join([f"{array_name}={size}" for array_name, size in zip(self.__fields__, array_sizes)])
        return f"Dataset(lengths: ({len_strings}) )"


def _is_batch(input_object: object) -> bool:
    """Checks if the input object is a batch.
    A batch is an Iterable[Iterable[...]]
    Args:
        input_object: object

    Returns:
        bool
    """
    with contextlib.suppress(KeyError, TypeError, IndexError):
        _ = input_object[0][0]
        return True
    return False


def _is_single_input(input_object: object) -> bool:
    """Checks if the input object is a single input.
    A single input is a list of dicts
    Args:
        input_object: object

    Returns:
        bool
    """
    with contextlib.suppress(KeyError, TypeError, IndexError):
        _ = input_object[0]
        return isinstance(_, dict)
    return False
