"""Action for getting human feedback"""

from typing import Callable

from pydantic import Field

from superai.llm.actions import BaseAction


def _print_func(text: str) -> None:
    print("\n")
    print(text)


class HumanFeedbackAction(BaseAction):
    """Action that adds the capability to ask user for input."""

    name = "Ask human for feedback"
    description = (
        "You can ask a human for guidance when you think you "
        "got stuck or you are not sure what to do next. "
        "The input should be a question for the human."
    )
    prompt_func: Callable[[str], None] = Field(default_factory=lambda: _print_func)
    input_func: Callable = Field(default_factory=lambda: input)

    def _run(self, query: str) -> str:
        self.prompt_func(query)
        return self.input_func()
