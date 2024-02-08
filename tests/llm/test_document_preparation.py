import json
from pathlib import Path

import pytest
import tiktoken

from superai.llm.data_processing.document_preparation import (
    DocumentToString,
    _replace_checkbox_kv_pairs,
)


@pytest.fixture
def invoice_ocr():
    with open(Path(__file__).parent.joinpath("ocr_outputs/invoice_ocr_output.json"), "r") as f:
        invoice_ocr = json.load(f)
    return invoice_ocr


@pytest.fixture
def form_ocr():
    with open(Path(__file__).parent.joinpath("ocr_outputs/gewa_ocr_output.json"), "r") as f:
        form_ocr = json.load(f)
    return form_ocr


@pytest.fixture
def table_ocr():
    with open(Path(__file__).parent.joinpath("ocr_outputs/table_ocr_output.json"), "r") as f:
        table_ocr = json.load(f)
    return table_ocr


def test_whitespace_extractor(invoice_ocr):
    extractor = DocumentToString(False, False, "whitespace", None, 4000)
    serialized_doc = extractor.get_document_representation(invoice_ocr["__ocr_values__"], None, None)
    assert len(serialized_doc) != 0
    assert len(serialized_doc) == 1
    assert len(serialized_doc[0]) != 0


def test_line_extractor(invoice_ocr):
    extractor = DocumentToString(False, False, "line", None, 4000)
    serialized_doc = extractor.get_document_representation(invoice_ocr["__ocr_values__"], None, None)
    assert len(serialized_doc) != 0
    assert len(serialized_doc) == 1
    assert len(serialized_doc[0]) > 0


def test_line_extractor_kv(form_ocr):
    extractor = DocumentToString(True, False, "line", None, 40000)
    serialized_doc = extractor.get_document_representation(form_ocr["__ocr_values__"], form_ocr["__key_values__"], None)
    assert len(serialized_doc) != 0
    assert len(serialized_doc) == 1
    assert len(serialized_doc[0]) > 0

    # Even if there are no key value pairs provided it should not fail
    serialized_doc = extractor.get_document_representation(form_ocr["__ocr_values__"], None, None)
    assert len(serialized_doc) != 0
    assert len(serialized_doc[0]) > 0


def test_whitespace_extractor_kv(form_ocr):
    extractor = DocumentToString(True, False, "whitespace", None, 4000)
    encoder = tiktoken.encoding_for_model(extractor.tokenizer_model)
    serialized_doc = extractor.get_document_representation(form_ocr["__ocr_values__"], form_ocr["__key_values__"], None)
    assert all(len(encoder.encode(chunk)) < 4000 for chunk in serialized_doc)
    assert len(serialized_doc) == 2
    assert len(serialized_doc[0]) > 0

    # Even if there are no key value pairs provided it should not fail
    serialized_doc = extractor.get_document_representation(form_ocr["__ocr_values__"], None, None)
    assert all(len(encoder.encode(chunk)) < 4000 for chunk in serialized_doc)
    assert len(serialized_doc) == 2
    assert len(serialized_doc[0]) > 0


def test_whitespace_extractor_table(table_ocr):
    extractor = DocumentToString(False, True, "whitespace", None, 4000)
    serialized_doc = extractor.get_document_representation(
        table_ocr["__ocr_values__"], None, table_ocr["__general_tables__"]
    )
    assert serialized_doc[0].count("Table") == 2
    assert len(serialized_doc) == 1


def test_document_batching(form_ocr):
    extractor = DocumentToString(True, False, "line", None, 100)
    serialized_doc = extractor.get_document_representation(form_ocr["__ocr_values__"], form_ocr["__key_values__"], None)
    encoder = tiktoken.encoding_for_model(extractor.tokenizer_model)
    assert all(len(encoder.encode(chunk)) < 100 for chunk in serialized_doc)
    assert len(serialized_doc) > 1


def test_line_numbers(form_ocr):
    extractor = DocumentToString(True, False, "whitespace", None, 4000, include_line_number=True)
    serialized_doc = extractor.get_document_representation(form_ocr["__ocr_values__"], form_ocr["__key_values__"], None)
    assert serialized_doc[0][0:2] == "0:"
    assert serialized_doc[0].split("\n")[3][0] == "3"


def test_get_white_space_line_dict(invoice_ocr):
    extractor = DocumentToString(False, False, "whitespace", None, 4000, include_line_number=True)
    serialized_doc = extractor.get_document_representation(invoice_ocr["__ocr_values__"], None, None)
    line_dict = extractor.get_white_space_line_dict(invoice_ocr["__ocr_values__"])

    split_doc = serialized_doc[0].split("\n")
    assert line_dict[int(split_doc[7][0])][0]["content"] in split_doc[7]
    assert line_dict[int(split_doc[26][0:2])][1]["content"] in split_doc[26]
    assert line_dict[int(split_doc[103][0:3])][0]["content"] in split_doc[103]


def test_replace_checkbox_kv_pairs(form_ocr):
    # Test dummy removal
    ocr_values = [
        {"content": "Box", "pageNumber": 1, "boundingBox": {"top": 0, "left": 10, "height": 5, "width": 5}},
        {"content": "|X", "pageNumber": 1, "boundingBox": {"top": 0, "left": 0, "height": 5, "width": 5}},
    ]
    ocr_key_values = [
        {
            "key": {"content": "Box", "pageNumber": 1, "boundingBox": {"top": 0, "left": 10, "height": 5, "width": 5}},
            "value": {
                "content": ":selected:",
                "pageNumber": 1,
                "boundingBox": {"top": 0, "left": 0, "height": 5, "width": 5},
            },
        }
    ]
    ocr_values = _replace_checkbox_kv_pairs(ocr_values, ocr_key_values)
    assert ocr_values[0]["content"] == "Box-[X]"
