from typing import Any, Dict, List, Union

from superai.llm.memory.base import Memory


class NoMemory(Memory):
    """
    A class that does not store any data.
    """

    def __init__(self):
        pass

    def add(self, data: str) -> str:
        return ""

    def get(self, data: str) -> Union[List[Any], None]:
        return None

    def clear(self) -> str:
        return ""

    def get_relevant(self, data: str, num_relevant: int = 5) -> Union[List[Any], None]:
        return None

    def get_stats(self) -> Dict[str, Any]:
        return {}
