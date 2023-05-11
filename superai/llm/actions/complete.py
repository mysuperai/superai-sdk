from superai.llm.actions import BaseAction


class CompleteAction(BaseAction):
    """Complete action."""

    name = "Complete"
    description = (
        "Call Complete action when you think you have generated the desired output and have acheived all goals and constraints."
        "Useful for when you are done with your assigned goal and want to end the program,"
        "Input should be a reason to end, output will be a message that the program has ended."
    )

    def _run(self, end_reason: str) -> str:
        return f"Agent complete for reason: {end_reason}"
