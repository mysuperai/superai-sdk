from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Extra, root_validator

from superai.llm.actions import BaseAction
from superai.llm.configuration import Configuration
from superai.llm.utilities import get_from_dict_or_env

config = Configuration()


class GoogleSearchAPI(BaseModel):
    """Wrapper for Google Search API.

    TODO: DOCS for using it
    1. Install google-api-python-client
    - If you don't already have a Google account, sign up.
    - If you have never created a Google APIs Console project,
    read the Managing Projects page and create a project in the Google API Console.
    - Install the library using pip install google-api-python-client
    The current version of the library is 2.70.0 at this time

    2. To create an API key:
    - Navigate to the APIs & Services→Credentials panel in Cloud Console.
    - Select Create credentials, then select API key from the drop-down menu.
    - The API key created dialog box displays your newly created key.
    - You now have an API_KEY

    3. Setup Custom Search Engine so you can search the entire web
    - Create a custom search engine in this link.
    - In Sites to search, add any valid URL (i.e. www.stackoverflow.com).
    - That’s all you have to fill up, the rest doesn’t matter.
    In the left-side menu, click Edit search engine → {your search engine name}
    → Setup Set Search the entire web to ON. Remove the URL you added from
     the list of Sites to search.
    - Under Search engine ID you’ll find the search-engine-ID.

    4. Enable the Custom Search API
    - Navigate to the APIs & Services→Dashboard panel in Cloud Console.
    - Click Enable APIs and Services.
    - Search for Custom Search API and click on it.
    - Click Enable.
    URL for it: https://console.cloud.google.com/apis/library/customsearch.googleapis
    .com
    """

    search_engine: Any
    google_api_key: Optional[str] = config.google_api_key
    google_cse_id: Optional[str] = config.google_cse_id
    n_results: int = 10
    siterestrict: bool = False

    def run(self, query: str) -> List[Dict]:
        """Run the search"""
        snippets = []
        results = self._search(query=query)
        if len(results) == 0:
            return "No good Google Search Result was found"
        for result in results:
            if "snippet" in result:
                snippets.append(result["snippet"])
        return snippets

    def _search(self, query: str) -> List[Dict]:
        """Search Google for the query"""
        cse = self.search_engine.cse()
        if self.siterestrict:
            cse = cse.siterestrict()
        results = cse.list(q=query, cx=self.google_cse_id, num=self.n_results).execute()
        return results.get("items", [])

    class Config:
        """Pydantic configuration for GoogleSearchAPI"""

        extra = Extra.forbid

    @root_validator
    def check_n_results(cls, values: dict) -> dict:
        """Check that the number of results is valid"""
        if values["n_results"] <= 0:
            raise ValueError("Number of results must be > 0")
        return values

    @root_validator()
    def validate_environment(cls, values: Dict) -> Dict:
        """Validate that api key and python package exists in environment."""
        google_api_key = get_from_dict_or_env(values, "google_api_key", "GOOGLE_API_KEY", default=config.google_api_key)
        values["google_api_key"] = google_api_key

        google_cse_id = get_from_dict_or_env(values, "google_cse_id", "GOOGLE_CSE_ID", default=config.google_cse_id)
        values["google_cse_id"] = google_cse_id

        try:
            from googleapiclient.discovery import build

        except ImportError:
            raise ImportError(
                "google-api-python-client is not installed. "
                "Please install it with `pip install google-api-python-client`"
            )

        service = build("customsearch", "v1", developerKey=google_api_key)
        values["search_engine"] = service

        return values


class GoogleSearchAction(BaseAction):
    """Google search action."""

    name = "Google search results as JSON"
    description = (
        "Call Google to search for something and return the results as JSON."
        "Useful for when you need to answer questions about current events"
        "Input should be a search query. Output will be a JSON array of the query results."
    )
    n_results: int = 4
    siterestrict: bool = False
    search_engine: Any

    def _run(self, query: str) -> str:
        search_api = GoogleSearchAPI(
            n_results=self.n_results, siterestrict=self.siterestrict, search_engine=self.search_engine
        )
        return search_api.run(query)
