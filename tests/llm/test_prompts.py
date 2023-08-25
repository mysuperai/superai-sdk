from unittest import TestCase

from superai.llm.prompts import Prompt
from superai.llm.prompts.base import PromptExample


class TestPrompt(TestCase):
    def test_prompt(self):
        prompt = Prompt.from_components(
            name="name1",
            role="role1",
            advice=["advice1"],
            constraints=["constraint1"],
            prompt_prefix="prefix1",
            prompt_suffix="suffix1",
            output_constraints=["outputConstraint1"],
            output_format=["format1"],
            examples=["example 1", PromptExample(input="Input2", output="Output2")],
        )
        self.assertIn("name1", prompt.prompt)
        self.assertIn("role1", prompt.prompt)
        self.assertIn("advice1", prompt.prompt)
        self.assertIn("constraint1", prompt.prompt)
        self.assertIn("prefix1", prompt.prompt)
        self.assertIn("suffix1", prompt.prompt)
        self.assertIn("outputConstraint1", prompt.prompt)
        self.assertIn("format1", prompt.prompt)
        self.assertIn("example 1", prompt.prompt)
        self.assertIn("Input2", prompt.prompt)
        self.assertIn("Output2", prompt.prompt)
