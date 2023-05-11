"""Chain that calls SerpAPI.

Heavily borrowed from https://github.com/ofirpress/self-ask
"""
import os
import sys
from typing import Any, Dict, Optional, Tuple

import aiohttp
from pydantic import BaseModel, Extra, Field, root_validator

from superai.llm.actions import BaseAction
from superai.llm.configuration import Configuration
from superai.llm.utilities import get_from_dict_or_env

config = Configuration()


class HiddenPrints:
    """Context manager to hide prints."""

    def __enter__(self) -> None:
        """Open file to pipe stdout to."""
        self._original_stdout = sys.stdout
        sys.stdout = open(os.devnull, "w")

    def __exit__(self, *_: Any) -> None:
        """Close file that stdout was piped to."""
        sys.stdout.close()
        sys.stdout = self._original_stdout


class SerpSearchAPI(BaseModel):
    """Wrapper around SerpAPI."""

    search_engine: Any  #: :meta private:
    search_params: dict = Field(
        default={
            "engine": "google",
            "google_domain": "google.com",
            "gl": "us",
            "hl": "en",
        }
    )
    serp_api_key: Optional[str] = config.serp_api_key
    aiosession: Optional[aiohttp.ClientSession] = None

    class Config:
        """Configuration for this pydantic object."""

        extra = Extra.forbid
        arbitrary_types_allowed = True

    @root_validator()
    def validate_environment(cls, values: Dict) -> Dict:
        """Validate that api key and python package exists in environment."""
        serp_api_key = get_from_dict_or_env(values, "serp_api_key", "SERPAPI_API_KEY", default=config.serp_api_key)
        values["serp_api_key"] = serp_api_key
        try:
            from serpapi import GoogleSearch

            values["search_engine"] = GoogleSearch
        except ImportError:
            raise ValueError(
                "Could not import serpapi python package. "
                "Please install it with `pip install google-search-results`."
            )
        return values

    async def arun(self, query: str, **kwargs: Any) -> str:
        """Run query through SerpAPI and parse result async."""
        return self._process_response(await self.aresults(query))

    def run(self, query: str, **kwargs: Any) -> str:
        """Run query through SerpAPI and parse result."""
        return self._process_response(self.results(query))

    def results(self, query: str) -> dict:
        """Run query through SerpAPI and return the raw result."""
        search_params = self.get_search_params(query)
        with HiddenPrints():
            search = self.search_engine(search_params)
            res = search.get_dict()
        return res

    async def aresults(self, query: str) -> dict:
        """Use aiohttp to run query through SerpAPI and return the results async."""

        def construct_url_and_search_params() -> Tuple[str, Dict[str, str]]:
            search_params = self.get_search_params(query)
            search_params["source"] = "python"
            if self.serp_api_key:
                search_params["serp_api_key"] = self.serp_api_key
            search_params["output"] = "json"
            url = "https://serpapi.com/search"
            return url, search_params

        url, search_params = construct_url_and_search_params()
        if not self.aiosession:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, search_params=search_params) as response:
                    res = await response.json()
        else:
            async with self.aiosession.get(url, search_params=search_params) as response:
                res = await response.json()

        return res

    def get_search_params(self, query: str) -> Dict[str, str]:
        """Get parameters for SerpAPI."""
        _search_params = {
            "api_key": self.serp_api_key,
            "q": query,
        }
        search_params = {**self.search_params, **_search_params}
        return search_params

    @staticmethod
    def _process_response(res: dict) -> str:
        """Process response from SerpAPI."""
        if "error" in res.keys():
            raise ValueError(f"Got error from SerpAPI: {res['error']}")
        if "answer_box" in res.keys() and "answer" in res["answer_box"].keys():
            toret = res["answer_box"]["answer"]
        elif "answer_box" in res.keys() and "snippet" in res["answer_box"].keys():
            toret = res["answer_box"]["snippet"]
        elif "answer_box" in res.keys() and "snippet_highlighted_words" in res["answer_box"].keys():
            toret = res["answer_box"]["snippet_highlighted_words"][0]
        elif "sports_results" in res.keys() and "game_spotlight" in res["sports_results"].keys():
            toret = res["sports_results"]["game_spotlight"]
        elif "knowledge_graph" in res.keys() and "description" in res["knowledge_graph"].keys():
            toret = res["knowledge_graph"]["description"]
        elif "snippet" in res["organic_results"][0].keys():
            toret = res["organic_results"][0]["snippet"]

        else:
            toret = "No good search result found"
        return toret


class SerpSearchAction(BaseAction):
    """Sert search action."""

    name = "Serp search results as JSON"
    description = (
        "Call Serp to search for something and return the results as JSON."
        "Useful for when you need to answer questions about current events"
        "Input should be a search query. Output will be a JSON array of the query results."
    )
    search_engine: Any  #: :meta private:
    search_params: dict = Field(
        default={
            "engine": "google",
            "google_domain": "google.com",
            "gl": "us",
            "hl": "en",
        }
    )

    def _run(self, query: str) -> str:
        search_api = SerpSearchAPI(search_engine=self.search_engine, search_params=self.search_params)
        return search_api.run(query)
