"""Handles unpacking tags from the prediction payloads and using them in the logger and sentry context."""
from __future__ import annotations

from typing import Optional, Tuple

import sentry_sdk
import structlog
from attr import define
from opentelemetry.trace import Context, Span
from superai_logging import get_logger

from superai.utils.opentelemetry import _extract_and_activate_span

log = get_logger(__name__)


@define(auto_attribs=True)
class PredictionTags:
    """Tags which are passed to the model during prediction."""

    prediction_id: Optional[str] = None
    retries: Optional[int] = None
    deployment_id: Optional[str] = None
    app_id: Optional[str] = None
    model_id: Optional[str] = None
    task_id: Optional[int] = None
    job_id: Optional[int] = None
    traceparent: Optional[str] = None
    raw_tags: Optional[dict] = None

    def dict(self):
        return self.raw_tags


def _parse_prediction_tags(tags: dict) -> PredictionTags:
    """Maps protobuf compatible dictionary used in Seldon tags to normal dictionary"""
    tags = {k: v["string_value"] for k, v in tags.items()}

    return PredictionTags(
        prediction_id=tags.get("superai.prediction.uuid"),
        retries=tags.get("superai.prediction.retries"),
        deployment_id=tags.get("superai.deployment.uuid"),
        app_id=tags.get("superai.app.uuid"),
        model_id=tags.get("superai.model.uuid"),
        task_id=tags.get("superai.task.id"),
        job_id=tags.get("superai.job.id"),
        traceparent=tags.get("traceparent"),
        raw_tags=tags,
    )


def _unpack_meta(inputs: dict, meta: Optional[dict] = None) -> Tuple[dict, Optional[dict]]:
    """Unpacks meta header from inputs if present in a backwards compatible way."""
    if isinstance(inputs, dict) and "data" in inputs and "meta" in inputs:
        meta = inputs["meta"]
        inputs = inputs["data"]
    elif meta is None:
        log.warning(f"Received inputs without meta header. Type of inputs: {type(inputs)}")
    return inputs, meta


def _handle_tags(
    meta: Optional[dict] = None, tags: Optional[PredictionTags] = None
) -> Tuple[Optional[Span], Optional[Context], PredictionTags]:
    """Handles tags from meta header and returns span, span_context and tags.

    Args:
        meta: Meta header from the request. Contains tags in protobuf dictionary format.

        - Sets tags in the logger context
        - Sets tags in the sentry context
        - Extracts span and span_context from the traceparent header
    """
    span, span_context = None, None
    if meta:
        if "puid" in meta:
            log.info(f"Received prediction request for prediction_uuid={meta['puid']}")
        if "tags" in meta:
            # Convert Protobuf dictionary to python dictionary
            tags = _parse_prediction_tags(meta["tags"])

            # Add tags to the logger context
            structlog.contextvars.bind_contextvars(**tags.dict())

            # Add tags to sentry context
            for k, v in tags.dict().items():
                sentry_sdk.set_tag(k, v)

            span, span_context = _extract_and_activate_span(tags.dict())
            if span:
                tags.traceparent = None
            log.info(f"Received tags={tags}")

    tags = tags or PredictionTags()
    return span, span_context, tags
