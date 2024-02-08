from superai.meta_ai.base.tags import _handle_tags


def test_handle_tags():
    meta = {}
    tags = None
    span, span_context, tags = _handle_tags(meta, tags)
    assert span is None
    assert span_context is None
    # Assure we always have a tags object
    assert tags is not None

    meta = {
        "tags": {
            "traceparent": {"string_value": "test_traceparent"},
            "superai.job.id": {"string_value": "123"},
            "superai.task.id": {"string_value": "456"},
        }
    }
    span, span_context, tags = _handle_tags(meta, tags)
    assert span is not None
    assert span_context is not None
    assert tags is not None
    assert tags.job_id == "123"
    assert tags.task_id == "456"
