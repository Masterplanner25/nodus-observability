"""nodus-observability — OTel tracing, Prometheus metrics, structured logging, trace context.

Trace context (ContextVars — zero dependencies):
    get_trace_id / set_trace_id / reset_trace_id / ensure_trace_id
    get_parent_event_id / set_parent_event_id / reset_parent_event_id
    is_pipeline_active / set_pipeline_active / reset_pipeline_active
    get_current_request / set_current_request / reset_current_request
    get_current_execution_context / set_current_execution_context / reset_current_execution_context

OTel tracing (optional — install with [otel] extra):
    init_otel(service_name)        — bootstrap TracerProvider + OTLP exporter
    get_tracer(name)               — retrieve tracer (noop when OTEL absent)
    span_context_from_trace_id     — convert hex trace ID to SpanContext

Prometheus metrics (optional — install with [metrics] extra):
    create_registry()              — fresh CollectorRegistry (never use the global one)
    Counter, Histogram, Gauge      — re-exported from prometheus_client

Structured logging:
    configure_logging(...)         — set up root logger with JSON + correlation fields
"""
from .context import (
    ensure_trace_id,
    get_current_execution_context,
    get_current_request,
    get_current_trace_id,
    get_parent_event_id,
    get_trace_id,
    is_pipeline_active,
    reset_current_execution_context,
    reset_current_request,
    reset_current_trace_id,
    reset_parent_event_id,
    reset_pipeline_active,
    reset_trace_id,
    set_current_execution_context,
    set_current_request,
    set_current_trace_id,
    set_parent_event_id,
    set_pipeline_active,
    set_trace_id,
)
from .logging import configure_logging
from .metrics import Counter, Gauge, Histogram, create_registry
from .otel import _NoopSpan, _NoopTracer, get_tracer, init_otel, span_context_from_trace_id

__all__ = [
    # Context
    "ensure_trace_id",
    "get_current_execution_context",
    "get_current_request",
    "get_current_trace_id",
    "get_parent_event_id",
    "get_trace_id",
    "is_pipeline_active",
    "reset_current_execution_context",
    "reset_current_request",
    "reset_current_trace_id",
    "reset_parent_event_id",
    "reset_pipeline_active",
    "reset_trace_id",
    "set_current_execution_context",
    "set_current_request",
    "set_current_trace_id",
    "set_parent_event_id",
    "set_pipeline_active",
    "set_trace_id",
    # Logging
    "configure_logging",
    # Metrics
    "Counter",
    "Gauge",
    "Histogram",
    "create_registry",
    # OTel
    "_NoopSpan",
    "_NoopTracer",
    "get_tracer",
    "init_otel",
    "span_context_from_trace_id",
]
