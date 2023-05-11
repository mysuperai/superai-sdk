from abc import ABC, abstractmethod
from typing import Any, Dict, List, Union

from pydantic import BaseModel, Extra


class Memory(BaseModel, ABC):
    """Base interface for all memory classes."""

    class Config:
        """Configuration for this pydantic object."""

        extra = Extra.forbid
        arbitrary_types_allowed = True

    @abstractmethod
    def add(self, data: Any) -> str:
        """Add data to memory."""
        raise NotImplementedError

    @abstractmethod
    def get(self, data: Any) -> Union[List[Any], None]:
        """Get data from memory."""
        raise NotImplementedError

    @abstractmethod
    def clear(self) -> str:
        """Clear memory."""
        raise NotImplementedError

    @abstractmethod
    def get_relevant(self, data: Any, num_relevant: int = 5) -> Union[List[Any], None]:
        """Get relevant data from memory."""
        raise NotImplementedError

    @abstractmethod
    def get_stats(self) -> Dict[str, Any]:
        """Get stats about memory."""
        raise NotImplementedError
