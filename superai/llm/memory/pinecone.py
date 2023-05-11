import re
from typing import Any, Dict, List, Optional, Union

import pinecone
from colorama import Fore, Style
from pydantic import Field, root_validator

from superai.llm.configuration import Configuration
from superai.llm.foundation_models import OpenAIEmbedding
from superai.llm.logger import logger
from superai.llm.memory.base import Memory

config = Configuration()


class PineconeMemory(Memory):
    table_name: str = Field("super-llm")
    metric: str = Field("cosine")
    pod_type: str = Field("p1")
    embedding_dimension: int = Field(config.embedding_dimension)
    embedding_model: OpenAIEmbedding = Field(default_factory=OpenAIEmbedding)
    vec_num: int = Field(0)
    index: Optional[Any] = None

    @root_validator
    def initialize_and_validate(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        pinecone_api_key = config.pinecone_api_key
        pinecone_region = config.pinecone_region
        pinecone.init(api_key=pinecone_api_key, environment=pinecone_region)

        try:
            pinecone.whoami()
        except Exception as e:
            logger.log(
                "FAILED TO CONNECT TO PINECONE",
                Fore.RED,
                Style.BRIGHT + str(e) + Style.RESET_ALL,
            )
            logger.log(
                "Please ensure you have setup and configured Pinecone properly for use."
                + f"You can check out {Fore.CYAN + Style.BRIGHT}"
                "https://github.com/Torantulino/Auto-GPT#-pinecone-api-key-setup"
                f"{Style.RESET_ALL} to ensure you've set up everything correctly."
            )
            exit(1)

        table_name = values.get("table_name")
        if not re.match(r"^[a-z0-9]+(?:-[a-z0-9]+)*$", table_name.lower()):
            raise ValueError(
                "Invalid table_name. Must consist of lower case alphanumeric characters or '-', and must start and end with an alphanumeric character."
            )

        table_name = table_name.lower()
        if table_name not in pinecone.list_indexes():
            pinecone.create_index(
                table_name,
                dimension=int(values.get("embedding_dimension")),
                metric=values.get("metric"),
                pod_type=values.get("pod_type"),
            )
        values["index"] = pinecone.Index(table_name)
        return values

    def add(self, data: Any) -> str:
        vector = self.embedding_model.predict(data)
        # no metadata here. We may wish to change that long term.
        self.index.upsert([(str(self.vec_num), vector, {"raw_text": data})])
        _text = f"Inserting data into memory at index: {self.vec_num}:\n data: {data}"
        self.vec_num += 1
        return _text

    def get(self, data: Any) -> Union[List[Any], None]:
        return self.get_relevant(data, 1)

    def clear(self) -> str:
        self.index.delete(deleteAll=True)
        return "Obliviated"

    def get_relevant(self, data: Any, num_relevant: int = 5) -> Union[List[Any], None]:
        """
        Returns all the data in the memory that is relevant to the given data.
        :param data: The data to compare to.
        :param num_relevant: The number of relevant data to return. Defaults to 5
        """
        query_embedding = self.embedding_model.predict(data)
        results = self.index.query(query_embedding, top_k=num_relevant, include_metadata=True)
        sorted_results = sorted(results.matches, key=lambda x: x.score)
        return [str(item["metadata"]["raw_text"]) for item in sorted_results]

    def get_stats(self) -> Dict[str, Any]:
        return self.index.describe_index_stats()
