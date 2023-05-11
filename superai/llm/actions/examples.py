from typing import Any, List

from superai.llm.actions import BaseAction


class ChooseExamplesAction(BaseAction):
    """Choose best example from a list of examples."""

    name = "Choose best examples"
    description = (
        "Call Choose Examples when you need to find the best examples for a prompt."
        "Useful for when there is too many examples to fit into a single prompt."
        "Input should be a list of examples. Output will be a list of the best examples."
    )
    n_examples: int = 4

    def _run(self, examples: Any) -> List[str]:
        return 'examples["examples"][:self.n_examples]'
