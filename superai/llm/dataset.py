import csv
import json
import sqlite3
from typing import Any, Callable, Dict, List, Optional, Union

import numpy as np
import pandas as pd
import requests
from pydantic import BaseModel, Field, validator

from superai.llm.data_types import DataType


class Data(BaseModel):
    input: Optional[Any] = None
    output: Optional[Any] = None
    metadata: Dict[str, Any] = {}

    def __init__(
        self,
        input: Any = None,
        input_url: str = None,
        input_path: str = None,
        output: Any = None,
        output_url: str = None,
        output_path: str = None,
        metadata: Dict[str, Any] = {},
    ):
        super().__init__(input=None, output=None, metadata=metadata)
        if input is not None or input_url or input_path:
            self.set_input(value=input, url=input_url, path=input_path)
        if output is not None or output_url or output_path:
            self.set_output(value=output, url=output_url, path=output_path)

    def set_input(
        self, value: Any = None, url: str = None, path: str = None, metadata: Optional[Dict[str, Any]] = None
    ):
        if sum(x is not None for x in [value, url, path]) != 1:
            raise ValueError("You must provide only one of input value, url, or path.")

        if value is not None:
            self.input = value
        elif url:
            self.input = self.load_data(url=url)
            self.add_metadata({"input_url": url})
        elif path:
            self.input = self.load_data(path=path)
            self.add_metadata({"input_path": path})

        if metadata:
            self.add_metadata(metadata)

    def set_output(
        self, value: Any = None, url: str = None, path: str = None, metadata: Optional[Dict[str, Any]] = None
    ):
        if sum(x is not None for x in [value, url, path]) != 1:
            raise ValueError("You must provide only one of input value, url, or path.")

        if value is not None:
            self.output = value
        elif url:
            self.output = self.load_data(url=url)
            self.add_metadata({"output_url": url})
        elif path:
            self.output = self.load_data(path=path)
            self.add_metadata({"output_path": path})

        if metadata:
            self.add_metadata(metadata)

    def add_metadata(self, metadata: Dict[str, Any]):
        self.metadata.update(metadata)

    def load_data(self, url: Optional[str] = None, path: Optional[str] = None) -> bytes:
        if url:
            response = requests.get(url)
            if response.status_code == 200:
                return response.content
            else:
                raise ValueError(f"Failed to load data from URL: {url}")
        elif path:
            with open(path, "rb") as file:
                return file.read()
        else:
            raise ValueError("You must provide either a URL or a path to load data from.")

    def __str__(self):
        return f"Data(input={self.input}, output={self.output}, metadata={self.metadata}, input_url={self.metadata.get('input_url')}, output_url={self.metadata.get('output_url')}, input_path={self.metadata.get('input_path')}, output_path={self.metadata.get('output_path')})"

    def __repr__(self):
        return self.__str__()


class Dataset(BaseModel):
    input_schema: DataType
    output_schema: DataType
    data: List[Data] = Field(default_factory=list)
    splits_indices: Dict[str, List[int]] = Field(default_factory=dict)
    splits: Optional[Dict[str, float]] = None
    metadata: Dict[str, Any] = {}

    @validator("data", pre=True)
    def validate_data(cls, data_list):
        if not all(isinstance(item, Data) for item in data_list):
            raise ValueError("Data list must contain only instances of Data class.")
        return data_list

    def _parse_single_split(self, split_str: str):
        if "[" in split_str:
            split_name, indices = split_str.split("[")
            start, end = indices[:-1].split(":")
            start = int(float(start.strip("%")) / 100 * len(self.data)) if "%" in start else int(start)
            end = int(float(end.strip("%")) / 100 * len(self.data)) if "%" in end else int(end)
            self.splits[split_str] = self.data[start:end]
        else:
            self.splits[split_str] = self.get_split(split_str)

    def __str__(self):
        return f"Dataset(data_length=[{len(self.data)}], input_schema={self.input_schema}, output_schema={self.output_schema}, splits={self.splits})"

    def __repr__(self):
        return self.__str__()

    def __len__(self):
        return len(self.data)

    def __getitem__(self, index):
        return self.data[index]

    def __getattr__(self, attr):
        if self.splits is not None and attr in self.splits:
            return self.get_split(attr)
        else:
            raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{attr}'")

    def split_data(self, splits: Dict[str, float]):
        total_percentage = sum(splits.values())
        if not (0.999 <= total_percentage <= 1.001):
            raise ValueError("The sum of the split percentages should be equal to 1.0.")
        data_indices = np.arange(len(self.data))
        np.random.shuffle(data_indices)
        train_split = int(len(data_indices) * self.splits["train"])
        validation_split = int(len(data_indices) * self.splits["validation"])

        self.splits_indices = {
            "train": data_indices[:train_split],
            "validation": data_indices[train_split : train_split + validation_split],
            "test": data_indices[train_split + validation_split :],
        }

    def get_split(self, split: str):
        if split in self.splits_indices:
            split_data = [self.data[i] for i in self.splits_indices[split]]
            return Dataset.parse_obj(
                {"input_schema": self.input_schema, "output_schema": self.output_schema, "data": split_data}
            )
        else:
            raise ValueError(f"Invalid split name: {split}")

    def _get_data_slice(self, split: str):
        data = self.splits.get(split, self.data)
        if "[" in split:
            split_name, indices = split.split("[")
            start, end = indices[:-1].split(":")
            start = int(float(start.strip("%")) / 100 * len(data)) if "%" in start else int(start)
            end = int(float(end.strip("%")) / 100 * len(data)) if "%" in end else int(end)
            return data[start:end]
        else:
            return data

    def create_splits(
        self,
        test_size: Optional[float] = 0.2,
        train_size: Optional[float] = 0.7,
        validation_size: Optional[float] = 0.1,
        stratify_by_column: Optional[str] = None,
        seed: Optional[int] = 42,
    ):
        if seed is not None:
            np.random.seed(seed)

        total_percentage = test_size + train_size + validation_size
        if not (0.999 <= total_percentage <= 1.001):
            raise ValueError("The sum of the split percentages should be equal to 1.0.")
        data_indices = np.arange(len(self.data))
        np.random.shuffle(data_indices)

        if stratify_by_column is not None:
            sorted_indices = sorted(data_indices, key=lambda x: self.data[x].metadata[stratify_by_column])
            data_indices = np.array(sorted_indices)

        train_split = int(len(data_indices) * train_size)
        validation_split = int(len(data_indices) * validation_size)

        self.splits = {"train": train_size, "validation": validation_size, "test": test_size}

        self.splits_indices = {
            "train": data_indices[:train_split],
            "validation": data_indices[train_split : train_split + validation_split],
            "test": data_indices[train_split + validation_split :],
        }

    def add_data(
        self,
        input: Any = None,
        input_url: str = None,
        input_path: str = None,
        output: Any = None,
        output_url: str = None,
        output_path: str = None,
        metadata: Dict[str, Any] = {},
        split: Optional[str] = None,
    ):
        data_point = Data()
        data_point.set_input(value=input, url=input_url, path=input_path, metadata=metadata)
        if output is not None:
            data_point.set_output(value=output, url=output_url, path=output_path, metadata=metadata)

        if metadata is not None:
            data_point.add_metadata(metadata)

        if split and split in self.splits:
            self.splits[split].append(data_point)

        self.data.append(data_point)

    def update_data(
        self,
        index: int,
        input: Any = None,
        input_url: str = None,
        input_path: str = None,
        output: Any = None,
        output_url: str = None,
        output_path: str = None,
        metadata: Dict[str, Any] = {},
        split: Optional[str] = None,
    ):
        data_point = self.data[index]

        if input or input_url or input_path:
            data_point.set_input(value=input, url=input_url, path=input_path, metadata=metadata)

        if output or output_url or output_path:
            data_point.set_output(value=output, url=output_url, path=output_path, metadata=metadata)

        if metadata:
            data_point.add_metadata(metadata)

    def delete_data(self, index: int):
        del self.data[index]

    def from_json(self, data_files: Union[str, Dict[str, str]], field: str = None) -> "Dataset":
        if isinstance(data_files, str):
            data_files = {"": data_files}

        for key, file_path in data_files.items():
            with open(file_path, "r") as f:
                data = json.load(f)
                if field:
                    data = data[field]
                self.data.extend(data)
        return self

    def from_csv(self, data_files: Union[str, Dict[str, str]]) -> "Dataset":
        if isinstance(data_files, str):
            data_files = {"": data_files}

        for key, file_path in data_files.items():
            with open(file_path, newline="") as f:
                reader = csv.reader(f)
                data = list(reader)
                self.data.extend(data)
        return self

    def from_pandas(self, df: pd.DataFrame) -> "Dataset":
        self.data = list(df.to_records(index=False))
        return self

    def from_dict(self, dictionary: Dict[str, List[Any]]) -> "Dataset":
        keys = list(dictionary.keys())
        for values in zip(*dictionary.values()):
            row = {key: value for key, value in zip(keys, values)}
            self.add_data(input=row)
        return self

    def from_list(self, data_list: List[Dict[str, Any]]) -> "Dataset":
        for row in data_list:
            self.add_data(input=row)
        return self

    def from_generator(self, generator: Callable[[], Any]) -> "Dataset":
        for row in generator():
            self.add_data(input=row)
        return self

    def from_sql(self, query: str, con: Union[str, sqlite3.Connection]) -> "Dataset":
        if isinstance(con, str):
            con = sqlite3.connect(con)
        df = pd.read_sql_query(query, con)
        return self.from_pandas(df)

    def save_to_json(self, file_path: str, field: Optional[str] = None):
        with open(file_path, "w") as f:
            if field:
                json.dump({field: self.data}, f)
            else:
                json.dump(self.data, f)

    def save_to_csv(self, file_path: str):
        with open(file_path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerows(self.data)

    def to_pandas(self) -> pd.DataFrame:
        return pd.DataFrame(self.data)

    def to_dict(self) -> Dict[str, List[Any]]:
        result = {}
        for key in self.data[0].keys():
            result[key] = [dic[key] for dic in self.data]
        return result


def to_list(self) -> List[Dict[str, Any]]:
    return self.data


def to_generator(self) -> Callable[[], Any]:
    def generator():
        for item in self.data:
            yield item

    return generator


def save_to_sql(self, table_name: str, con: Union[str, sqlite3.Connection], if_exists: str = "fail"):
    if isinstance(con, str):
        con = sqlite3.connect(con)
    df = self.to_pandas()
    df.to_sql(table_name, con, if_exists=if_exists, index=False)
