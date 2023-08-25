from unittest import TestCase

from superai.llm.splitters import DictionarySplitter, ListSplitter, TextSplitter


class TestSplitters(TestCase):
    def test_text_splitter(self):
        splitter = TextSplitter()
        chunks = splitter.split("Test text test text test text test text Test text test text test text test text")
        self.assertEqual(len(chunks), 2)

    def test_dictionary_splitter(self):
        splitter = DictionarySplitter(split_size=2, overlap=0)
        chunks = splitter.split({"a": 1, "b": 2, "c": 3})
        self.assertEqual(len(chunks), 2)

    def test_list_splitter(self):
        splitter = ListSplitter(split_size=2, overlap=0)
        chunks = splitter.split(["a", "b", "c"])
        self.assertEqual(len(chunks), 2)
