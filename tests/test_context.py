from __future__ import annotations

import uuid

from nodus_observability import (
    ensure_trace_id,
    get_parent_event_id,
    get_trace_id,
    is_pipeline_active,
    reset_parent_event_id,
    reset_pipeline_active,
    reset_trace_id,
    set_parent_event_id,
    set_pipeline_active,
    set_trace_id,
)
from nodus_observability.context import (
    get_current_execution_context,
    get_current_request,
    reset_current_execution_context,
    reset_current_request,
    set_current_execution_context,
    set_current_request,
)


# ── Trace ID ──────────────────────────────────────────────────────────────────

def test_get_trace_id_default_is_none():
    # Reset to default state via a fresh set/reset cycle
    tok = set_trace_id("-")
    assert get_trace_id() is None
    reset_trace_id(tok)


def test_set_and_get_trace_id():
    tok = set_trace_id("trace-abc")
    assert get_trace_id() == "trace-abc"
    reset_trace_id(tok)


def test_reset_trace_id_restores_previous():
    tok1 = set_trace_id("first")
    tok2 = set_trace_id("second")
    assert get_trace_id() == "second"
    reset_trace_id(tok2)
    assert get_trace_id() == "first"
    reset_trace_id(tok1)


def test_ensure_trace_id_generates_uuid_when_empty():
    tok = set_trace_id("-")
    result = ensure_trace_id()
    assert result  # non-empty
    uuid.UUID(result)  # valid UUID
    reset_trace_id(tok)


def test_ensure_trace_id_returns_existing():
    tok = set_trace_id("existing-id")
    result = ensure_trace_id()
    assert result == "existing-id"
    reset_trace_id(tok)


def test_get_trace_id_with_default():
    tok = set_trace_id("-")
    assert get_trace_id(default="fallback") == "fallback"
    reset_trace_id(tok)


# ── Parent event ID ───────────────────────────────────────────────────────────

def test_get_parent_event_id_default_is_none():
    tok = set_parent_event_id(None)
    assert get_parent_event_id() is None
    reset_parent_event_id(tok)


def test_set_and_get_parent_event_id():
    tok = set_parent_event_id("event-123")
    assert get_parent_event_id() == "event-123"
    reset_parent_event_id(tok)


def test_set_parent_event_id_none_clears():
    tok1 = set_parent_event_id("event-abc")
    tok2 = set_parent_event_id(None)
    assert get_parent_event_id() is None
    reset_parent_event_id(tok2)
    reset_parent_event_id(tok1)


# ── Pipeline active flag ──────────────────────────────────────────────────────

def test_pipeline_active_default_false():
    assert is_pipeline_active() is False


def test_set_pipeline_active():
    tok = set_pipeline_active(True)
    assert is_pipeline_active() is True
    reset_pipeline_active(tok)
    assert is_pipeline_active() is False


# ── Current request ───────────────────────────────────────────────────────────

def test_get_current_request_default_none():
    assert get_current_request() is None


def test_set_and_get_current_request():
    request = object()
    tok = set_current_request(request)
    assert get_current_request() is request
    reset_current_request(tok)


# ── Execution context ─────────────────────────────────────────────────────────

def test_get_execution_context_default_none():
    assert get_current_execution_context() is None


def test_set_and_get_execution_context():
    ctx = {"user_id": "u1", "run_id": "r1"}
    tok = set_current_execution_context(ctx)
    assert get_current_execution_context() is ctx
    reset_current_execution_context(tok)
