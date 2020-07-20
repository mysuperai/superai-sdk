from typing import List, Generator, Dict
import names

from abc import ABC, abstractmethod

class TemplateApiMixin(ABC):

    @abstractmethod
    def _request(self, uri, method, body_params=None, query_params=None, required_api_key=False):
        pass



