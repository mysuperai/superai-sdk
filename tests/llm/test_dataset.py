from unittest import TestCase

from superai.llm.dataset import Data


class TestData(TestCase):
    def test_data(self):
        data = Data(input="input", output="output")
        self.assertEqual(data.input, "input")
        self.assertEqual(data.output, "output")

        data = Data(input={}, output=[])
        self.assertEqual(data.input, {})
        self.assertEqual(data.output, [])

        data.set_input([])
        self.assertEqual(data.input, [])

        data.set_input({})
        self.assertEqual(data.input, {})
