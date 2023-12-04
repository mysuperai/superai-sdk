from abc import ABC, abstractmethod

from pydantic import BaseModel, Extra
from tiktoken.model import MODEL_TO_ENCODING

# TODO: remove when tiktoken model registry will be updated
MODEL_TO_ENCODING.setdefault("gpt-35-turbo", "cl100k_base")
MODEL_TO_ENCODING.setdefault("gpt-35-turbo-16k", "cl100k_base")


class FoundationModel(ABC, BaseModel):
    class Config:
        """Configuration for this pydantic object."""

        extra = Extra.allow
        arbitrary_types_allowed = True

    @abstractmethod
    def check_api_key(self, api_key):
        raise NotImplementedError

    @abstractmethod
    def predict(self, prompt_instance):
        raise NotImplementedError
