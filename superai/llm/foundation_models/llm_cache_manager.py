"""
LLM Cache Manager is responsible for caching LLM requests. It's not used in production, but helpful in local exvironments, such as LEF.
By default, it doesn't cache anything, one must implement interface LLMCacheManager and call set_cache_manager() function.
LLM foundation models are responsible for serialization and deserialization of their input and outputs into Python dictionaries.

In runner (e.g. in LEF):
```
class MyLLMCacheManager(LLMCacheManager):
  ...

my_cache_manager = MyLLMCacheManager()
set_cache_manager(my_cache_manager)
```

In SDK's LLM foundation models:
```
def predict(input_params: dict):
    ...
    cached_response = check_cache(input_params)
    # use it, don't call LLM
    if cached_response:
        response = ResponseLLM(response) # deserialization
    ...
    new_response_dict = new_response.dict() # serialization
    store_in_cache(input_params, new_response)
    ...
```
"""
from abc import ABC, abstractmethod
from typing import Optional


class LLMCacheManager(ABC):
    @abstractmethod
    def check_cache(self, input: dict) -> Optional[dict]:
        pass

    @abstractmethod
    def store_in_cache(self, input: dict, output: dict) -> None:
        pass


_cache_manager: Optional[LLMCacheManager] = None


def set_cache_manager(manager: Optional[LLMCacheManager]):
    global _cache_manager
    _cache_manager = manager


def check_cache(input: dict) -> Optional[dict]:
    if _cache_manager:
        return _cache_manager.check_cache(input)


def store_in_cache(input: dict, output: dict) -> None:
    if _cache_manager:
        return _cache_manager.store_in_cache(input, output)
