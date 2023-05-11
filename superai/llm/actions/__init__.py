# super_llm/actions/__init__.py
import json
from typing import List

from superai.llm.actions.base import BaseAction
from superai.llm.actions.complete import CompleteAction
from superai.llm.actions.examples import ChooseExamplesAction
from superai.llm.actions.human import HumanFeedbackAction
from superai.llm.actions.search.bing import BingSearchAction
from superai.llm.actions.search.duck_duck_go import DuckDuckGoSearchAction
from superai.llm.actions.search.google import GoogleSearchAction
from superai.llm.actions.search.serp import SerpSearchAction
from superai.llm.actions.search.serper import SerperSearchAction
from superai.llm.actions.search.wikipedia import WikipediaSearchAction
from superai.llm.actions.search.wolfram_alpha import WolframAlphaAction

_all_actions = [
    ChooseExamplesAction,
    HumanFeedbackAction,
    BingSearchAction,
    DuckDuckGoSearchAction,
    GoogleSearchAction,
    SerpSearchAction,
    SerperSearchAction,
    WikipediaSearchAction,
    WolframAlphaAction,
    CompleteAction,
]

name_to_action_map = {action().name: action for action in _all_actions}
action_to_dict_map = {action().name: action for action in _all_actions}


def get_action_dict(action: BaseAction) -> dict:
    action_dict = {
        "name": action.name,
        "description": action.description,
        "params": action.params,
    }
    return action_dict


def list_actions():
    all_actions = []
    for action in _all_actions:
        action = action()
        params = {k: action.params[k]["type"] for k in action.params.keys()}
        all_actions.append({"name": action.name, "description": action.description, "params": params})
    return all_actions


__all__ = [
    "BaseAction",
    "list_actions",
    "get_action_dict",
]

__all__.extend(_all_actions)
