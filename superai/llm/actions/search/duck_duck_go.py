"""Util that calls DuckDuckGo Search.

No setup required. Free.
https://pypi.org/project/duckduckgo-search/
"""
from typing import Dict, List, Optional

from pydantic import BaseModel, Extra
from pydantic.class_validators import root_validator

from superai.llm.actions import BaseAction
from superai.llm.configuration import Configuration

config = Configuration()


class DuckDuckGoSearchAPI(BaseModel):
    """Wrapper for DuckDuckGo Search API.

    Free and does not require any setup
    """

    region: Optional[str] = "wt-wt"
    time: Optional[str] = "y"
    n_results: int = 5

    class Config:
        """Configuration for this pydantic object."""

        extra = Extra.forbid

    @root_validator()
    def validate_environment(cls, values: Dict) -> Dict:
        """Validate that python package exists in environment."""
        try:
            from duckduckgo_search import ddg  # noqa: F401
        except ImportError:
            raise ValueError(
                "Could not import duckduckgo-search python package. "
                "Please install it with `pip install duckduckgo-search`."
            )
        return values

    def run(self, query: str) -> str:
        from duckduckgo_search import ddg

        """Run query through DuckDuckGo and return concatenated results."""
        results = ddg(
            query,
            region=self.region,
            time=self.time,
            max_results=self.n_results,
        )
        if results is None or len(results) == 0:
            return "No good DuckDuckGo Search Result was found"
        snippets = [result["body"] for result in results]
        return " ".join(snippets)

    def results(self, query: str, n_results: int) -> List[Dict[str, str]]:
        """Run query through DuckDuckGo and return metadata.

        Args:
            query: The query to search for.
            n_results: The number of results to return.

        Returns:
            A list of dictionaries with the following keys:
                snippet - The description of the result.
                title - The title of the result.
                link - The link to the result.
        """
        from duckduckgo_search import ddg

        results = ddg(
            query,
            region=self.region,
            time=self.time,
            max_results=n_results,
        )

        if results is None or len(results) == 0:
            return [{"Result": "No good DuckDuckGo Search Result was found"}]

        def to_metadata(result: Dict) -> Dict[str, str]:
            return {
                "snippet": result["body"],
                "title": result["title"],
                "link": result["href"],
            }

        return [to_metadata(result) for result in results]


class DuckDuckGoSearchAction(BaseAction):
    """Duck Duck Go search action."""

    name = "Duck Duck Go search results as JSON"
    description = (
        "Call Duck Duck Go to search for something and return the results as JSON."
        "Useful for when you need to answer questions about current events"
        "Input should be a search query. Output will be a JSON array of the query results."
    )
    n_results: int = 4
    region: Optional[str] = "wt-wt"
    time: Optional[str] = "y"

    def _run(self, query: str) -> str:
        search_api = DuckDuckGoSearchAPI(n_results=self.n_results, region=self.region, time=self.time)
        return search_api.run(query)
