from __future__ import annotations

from nodus_observability import get_tracer, init_otel, span_context_from_trace_id
from nodus_observability.otel import _NoopTracer, _initialized


def test_init_otel_is_idempotent():
    # May already be initialized from a previous test run in the process
    init_otel(service_name="test")
    init_otel(service_name="test")  # second call must not raise


def test_get_tracer_returns_something():
    tracer = get_tracer("test-tracer")
    assert tracer is not None


def test_noop_tracer_context_manager():
    tracer = _NoopTracer()
    with tracer.start_as_current_span("test-span") as span:
        span.set_status("ok")
        span.record_exception(ValueError("test"))


def test_span_context_from_trace_id_valid_hex():
    hex_id = "a" * 32
    # Returns a SpanContext when OTEL is available, None otherwise — both are valid
    result = span_context_from_trace_id(hex_id)
    # Just verify it doesn't raise


def test_span_context_from_trace_id_none():
    result = span_context_from_trace_id(None)
    assert result is None


def test_span_context_from_trace_id_empty():
    result = span_context_from_trace_id("")
    assert result is None


def test_span_context_from_uuid_style():
    import uuid
    uid = str(uuid.uuid4())
    result = span_context_from_trace_id(uid)
    # Should not raise regardless of OTEL availability
