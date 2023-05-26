from unittest import TestCase

from superai.llm.prompts import Prompt
from superai.llm.prompts.base import PromptExample


class TestDecorators(TestCase):
    def test_prompt(self):
        prompt = Prompt.from_components(
            name="Test", examples=["test 1", PromptExample(input="Input2", output="Output2")]
        )
        self.assertNotEqual(prompt.prompt.find("Input2"), -1)
        self.assertNotEqual(prompt.prompt.find("test 1"), -1)
