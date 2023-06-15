import json
from pathlib import Path

import pytest

from superai.llm.data_processing.document_preparation import DocumentToString


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
    serialized_doc = extractor.get_document_representation(form_ocr["__ocr_values__"], form_ocr["__key_values__"], None)
    assert len(serialized_doc) != 0
    assert len(serialized_doc) == 1
    assert len(serialized_doc[0]) > 0

    # Even if there are no key value pairs provided it should not fail
    serialized_doc = extractor.get_document_representation(form_ocr["__ocr_values__"], None, None)
    assert len(serialized_doc) != 0
    assert len(serialized_doc) == 1
    assert len(serialized_doc[0]) > 0


def test_document_batching(form_ocr):
    extractor = DocumentToString(True, False, "line", None, 50)
    serialized_doc = extractor.get_document_representation(form_ocr["__ocr_values__"], form_ocr["__key_values__"], None)
    assert len(serialized_doc) != 0
    assert len(serialized_doc) > 1
