"""Util that calls Wikipedia."""
from typing import Any, Dict, Optional

from pydantic import BaseModel, Extra, root_validator

from superai.llm.actions import BaseAction
from superai.llm.configuration import Configuration

config = Configuration()

WIKIPEDIA_MAX_QUERY_LENGTH = 300


class WikipediaSearchAPI(BaseModel):
    """Wrapper around WikipediaSearchAPI.

    To use, you should have the ``wikipedia`` python package installed.
    This wrapper will use the Wikipedia API to conduct searches and
    fetch page summaries. By default, it will return the page summaries
    of the top-k results of an input search.
    """

    wiki_client: Any  #: :meta private:
    n_results: int = 3
    lang: str = "en"

    class Config:
        """Configuration for this pydantic object."""

        extra = Extra.forbid

    @root_validator()
    def validate_environment(cls, values: Dict) -> Dict:
        """Validate that the python package exists in environment."""
        try:
            import wikipedia

            wikipedia.set_lang(values["lang"])
            values["wiki_client"] = wikipedia
        except ImportError:
            raise ValueError(
                "Could not import wikipedia python package. " "Please install it with `pip install wikipedia`."
            )
        return values

    def run(self, query: str) -> str:
        """Run Wikipedia search and get page summaries."""
        search_results = self.wiki_client.search(query[:WIKIPEDIA_MAX_QUERY_LENGTH])
        summaries = []
        len_search_results = len(search_results)
        if len_search_results == 0:
            return "No good Wikipedia Search Result was found"
        for i in range(min(self.n_results, len_search_results)):
            summary = self.fetch_formatted_page_summary(search_results[i])
            if summary is not None:
                summaries.append(summary)
        return "\n\n".join(summaries)

    def fetch_formatted_page_summary(self, page: str) -> Optional[str]:
        try:
            wiki_page = self.wiki_client.page(title=page, auto_suggest=False)
            return f"Page: {page}\nSummary: {wiki_page.summary}"
        except (
            self.wiki_client.exceptions.PageError,
            self.wiki_client.exceptions.DisambiguationError,
        ):
            return None


class WikipediaSearchAction(BaseAction):
    """Wikipedia search action."""

    name = "Wikipedia search results as JSON"
    description = (
        "Call Wikipedia to search for something and return the results as JSON."
        "Useful for when you need to answer questions about current events"
        "Input should be a search query. Output will be a JSON array of the query results."
    )
    n_results: int = 4
    wiki_client: Any  #: :meta private:
    lang: str = "en"

    def _run(self, query: str) -> str:
        search_api = WikipediaSearchAPI(n_results=self.n_results, wiki_client=self.wiki_client, lang=self.lang)
        return search_api.run(query)
