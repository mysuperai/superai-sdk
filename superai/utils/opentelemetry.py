"""Sets up the OpenTelemetry SDK and instruments external libraries.
"""
from contextlib import asynccontextmanager
from typing import Optional, Tuple

from fastapi import FastAPI
from opentelemetry import trace
from opentelemetry.context.context import Context
from opentelemetry.instrumentation.botocore import BotocoreInstrumentor
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.trace import Span
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator

from superai.utils import log

tracer = trace.get_tracer(__name__)


@asynccontextmanager
async def instrumented_lifespan(app: FastAPI):
    """Custom lifespan context manager to initialize OpenTelemetry SDK.
    Is used to make OTLP compatible with forking model of FastAPI server (e.g. uvicorn)."""
    init_otlp()
    yield
    disable_otlp()


def init_otlp():
    """Initializes the OpenTelemetry SDK with the OTLP exporter."""
    RequestsInstrumentor().instrument()
    BotocoreInstrumentor().instrument()


def disable_otlp():
    """Disables the OpenTelemetry SDK."""
    RequestsInstrumentor().uninstrument()
    BotocoreInstrumentor().uninstrument()


def add_fastapi_instrumentation(app: FastAPI):
    """Adds OpenTelemetry FastAPI instrumentation to the app."""
    FastAPIInstrumentor.instrument_app(app)


def _extract_and_activate_span(tags: dict) -> Optional[Tuple[Span, Context]]:
    """Extracts the span context from the tags and activates it as the current span context"""
    try:
        span_context = TraceContextTextMapPropagator().extract(tags)
        # Set the span context as the current context
        span = trace.get_current_span()
        trace.set_span_in_context(span, span_context)
        # Try disabling attach to not clear traceid from global context
        # context.attach(span_context)
        return span, span_context
    except Exception as e:
        log.debug(f"Failed to extract span context from tags: {tags}. Error: {e}")
        return None
