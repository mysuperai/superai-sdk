"""Sets up the OpenTelemetry SDK and instruments external libraries.
"""
from contextlib import asynccontextmanager

from fastapi import FastAPI
from opentelemetry import trace
from opentelemetry.instrumentation.botocore import BotocoreInstrumentor
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor

tracer = trace.get_tracer(__name__)


@asynccontextmanager
async def instrumented_lifespan(app: FastAPI):
    """Custom lifespan context manager to initialize OpenTelemetry SDK.
    Is used to make OTLP compatible with forking model of FastAPI server (e.g. uvicorn)."""
    init_otlp()
    yield


def init_otlp():
    """Initializes the OpenTelemetry SDK with the OTLP exporter."""
    RequestsInstrumentor().instrument()
    BotocoreInstrumentor().instrument()


def add_fastapi_instrumentation(app: FastAPI):
    """Adds OpenTelemetry FastAPI instrumentation to the app."""
    FastAPIInstrumentor.instrument_app(app)
