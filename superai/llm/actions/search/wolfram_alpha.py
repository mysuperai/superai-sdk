"""Util that calls WolframAlpha."""
from typing import Any, Dict, Optional

from pydantic import BaseModel, Extra, root_validator

from superai.llm.actions import BaseAction
from superai.llm.configuration import Configuration
from superai.llm.utilities import get_from_dict_or_env

config = Configuration()


class WolframAlphaAPI(BaseModel):
    """Wrapper for Wolfram Alpha.

    Docs for using:

    1. Go to wolfram alpha and sign up for a developer account
    2. Create an app and get your APP ID
    3. Save your APP ID into WOLFRAM_ALPHA_APPID env variable
    4. pip install wolframalpha

    """

    wolfram_client: Any
    wolfram_alpha_appid: Optional[str] = config.wolfram_alpha_appid

    class Config:
        """Configuration for this pydantic object."""

        extra = Extra.forbid

    @root_validator()
    def validate_environment(cls, values: Dict) -> Dict:
        """Validate that api key and python package exists in environment."""
        wolfram_alpha_appid = get_from_dict_or_env(
            values, "wolfram_alpha_appid", "WOLFRAM_ALPHA_APPID", default=config.wolfram_alpha_appid
        )
        values["wolfram_alpha_appid"] = wolfram_alpha_appid

        try:
            import wolframalpha

        except ImportError:
            raise ImportError("wolframalpha is not installed. " "Please install it with `pip install wolframalpha`")
        client = wolframalpha.Client(wolfram_alpha_appid)
        values["wolfram_client"] = client

        return values

    def run(self, query: str) -> str:
        """Run query through WolframAlpha and parse result."""
        res = self.wolfram_client.query(query)

        try:
            assumption = next(res.pods).text
            answer = next(res.results).text
        except StopIteration:
            return "Wolfram Alpha wasn't able to answer it"

        if answer is None or answer == "":
            # We don't want to return the assumption alone if answer is empty
            return "No good Wolfram Alpha Result was found"
        else:
            return f"Assumption: {assumption} \nAnswer: {answer}"


class WolframAlphaAction(BaseAction):
    """Google search action."""

    name = "Google search results as JSON"
    description = (
        "Call Google to search for something and return the results as JSON."
        "Useful for when you need to answer questions about current events"
        "Input should be a search query. Output will be a JSON array of the query results."
    )
    wolfram_client: Any
    wolfram_alpha_appid: Optional[str] = None

    def _run(self, query: str) -> str:
        search_api = WolframAlphaAPI(wolfram_client=self.wolfram_client, wolfram_alpha_appid=self.wolfram_alpha_appid)
        return search_api.run(query)
