import json
import os
from typing import Any, Dict, List, Union

import numpy as np
import orjson
from pydantic import BaseModel, Field, root_validator, validator

import superai.llm
from superai.llm.configuration import Configuration
from superai.llm.foundation_models import FoundationModel, OpenAIEmbedding
from superai.llm.logger import logger
from superai.llm.memory.base import Memory

config = Configuration()

SAVE_OPTIONS = orjson.OPT_SERIALIZE_NUMPY | orjson.OPT_SERIALIZE_DATACLASS


def create_default_embeddings():
    return np.zeros((0, int(config.embedding_dimension))).astype(np.float32)


class CacheContentConfig:
    arbitrary_types_allowed = True

    @staticmethod
    def ndarray_validator(v):
        if not isinstance(v, np.ndarray):
            raise ValueError("Value must be a numpy ndarray")
        return v


class CacheContent(BaseModel):
    datas: List[str] = Field(default_factory=list)
    embeddings: np.ndarray = Field(default_factory=create_default_embeddings)

    class Config(CacheContentConfig):
        pass

    @validator("embeddings")
    def validate_embeddings(cls, v):
        return cls.Config.ndarray_validator(v)


class LocalMemory(Memory):
    """A class that stores the memory in a local file"""

    embedding_model: FoundationModel = Field(default_factory=OpenAIEmbedding)
    memory_name: str = Field("super_llm_memory")
    folder_name: str = Field("db")
    filename: str = Field()
    data: CacheContent = Field()

    @root_validator(pre=True)
    def initialize_memory(cls, values):
        memory_name = values.get("memory_name") or "super_llm_memory"
        folder_name = values.get("folder_name") or "db"

        module_dir = os.path.dirname(superai.llm.__file__)
        parent_dir = os.path.abspath(os.path.join(module_dir, os.pardir))
        db_dir = os.path.join(parent_dir, folder_name)

        if not os.path.exists(db_dir):
            os.makedirs(db_dir)

        filename = os.path.join(db_dir, f"{memory_name}.json")
        data = cls.initialize_cache_content(filename, overwrite=True)

        values["filename"] = filename
        values["data"] = data
        return values

    @staticmethod
    def initialize_cache_content(filename, overwrite):
        if os.path.exists(filename) and not overwrite:
            try:
                with open(filename, "rb") as f:
                    file_content = f.read()
                    if not file_content.strip():
                        file_content = b"{}"
                        with open(filename, "wb") as f:
                            f.write(file_content)

                    loaded = orjson.loads(file_content)
                    return CacheContent(**loaded)
            except orjson.JSONDecodeError:
                print(f"Error: The file '{filename}' is not in JSON format.")
                return CacheContent()
        else:
            if os.path.exists(filename) and overwrite:
                if config.debug:
                    logger.debug(f"Warning: The file '{filename}' already exists. " f"Overwriting {filename} ")
            else:
                if config.debug:
                    logger.debug(f"Warning: The file '{filename}' does not exist. " f"Creating {filename} ")
            with open(filename, "wb") as f:
                f.write(b"{}")
            return CacheContent()

    def add(self, data: str):
        if not isinstance(data, str):
            data = str(data)
        self.data.datas.append(data)

        embedding = self.embedding_model.predict(data)

        vector = np.array(embedding).astype(np.float32)
        vector = vector[np.newaxis, :]
        self.data.embeddings = np.concatenate(
            [
                self.data.embeddings,
                vector,
            ],
            axis=0,
        )

        with open(self.filename, "w") as f:
            out = json.dumps(self.data.dict(), default=str)
            f.write(out)
        return data

    def clear(self) -> str:
        """
        Clears the redis server.

        Returns: A message indicating that the memory has been cleared.
        """
        self.data = CacheContent()
        return "Obliviated"

    def get(self, data: str) -> Union[List[Any], None]:
        """
        Gets the data from the memory that is most relevant to the given data.

        Args:
            data: The data to compare to.

        Returns: The most relevant data.
        """
        return self.get_relevant(data, 1)

    def get_relevant(self, data: str, n: int) -> Union[List[Any], None]:
        """ "
        matrix-vector mult to find score-for-each-row-of-matrix
         get indices for top-n winning scores
         return datas for those indices
        Args:
            data: str
            n: int

        Returns: List[str]
        """
        embedding = self.embedding_model.predict(data)

        scores = np.dot(self.data.embeddings, embedding)

        top_n_indices = np.argsort(scores)[-n:][::-1]

        return [self.data.datas[i] for i in top_n_indices]

    def get_stats(self) -> Dict[str, Any]:
        """
        Returns: The stats of the local cache.
        """
        return {
            "num_texts": len(self.data.texts),
            "embeddings_shape": self.data.embeddings.shape,
        }
