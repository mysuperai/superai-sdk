from abc import ABC, abstractmethod
from typing import List

import tiktoken


class Splitter(ABC):
    def __init__(self, split_size: int = 10, overlap: int = 1):
        self.split_size = split_size
        self.overlap = overlap

    @abstractmethod
    def split(self, data):
        pass


class TextSplitter(Splitter):
    def __init__(self, split_size: int = 10, overlap: int = 1, tokenizer_model="gpt-3.5-turbo"):
        super(TextSplitter, self).__init__(split_size, overlap)
        self.tokenizer = tiktoken.encoding_for_model(tokenizer_model)

    def split(self, text: str) -> List[str]:
        token_ids = self.tokenizer.encode(text)
        chunks = []

        for i in range(0, len(token_ids), self.split_size - self.overlap):
            chunk = token_ids[i : i + self.split_size]
            chunk_str = self.tokenizer.decode(chunk)
            chunks.append(chunk_str)

        return chunks


class DictionarySplitter(Splitter):
    def split(self, dictionary: dict) -> List[dict]:
        chunks = []
        items = list(dictionary.items())

        for i in range(0, len(items), self.split_size - self.overlap):
            chunk = items[i : i + self.split_size]
            chunks.append(dict(chunk))

        return chunks


class ListSplitter(Splitter):
    def split(self, input_list: List[int]) -> List[List[int]]:
        chunks = []

        for i in range(0, len(input_list), self.split_size - self.overlap):
            chunk = input_list[i : i + self.split_size]
            chunks.append(chunk)

        return chunks
