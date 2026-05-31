from __future__ import annotations

import logging

from nodus_observability import configure_logging, get_trace_id, set_trace_id, reset_trace_id


def test_configure_logging_runs_without_error():
    configure_logging(env="development", force=True)


def test_configure_logging_sets_log_level():
    configure_logging(env="development", log_level="DEBUG", force=True)
    assert logging.getLogger().level == logging.DEBUG
    configure_logging(env="development", log_level="INFO", force=True)


def test_configure_logging_with_trace_id_fn():
    tok = set_trace_id("test-trace-123")
    configure_logging(
        env="development",
        force=True,
        get_trace_id_fn=get_trace_id,
    )
    logger = logging.getLogger("test_logging")
    # Verify the filter injects trace_id — exercise the filter manually
    root = logging.getLogger()
    handler = next(
        (h for h in root.handlers if hasattr(h, "_nodus_structured_logging_handler")),
        None,
    )
    if handler:
        record = logging.LogRecord(
            name="test", level=logging.INFO, pathname="", lineno=0,
            msg="test", args=(), exc_info=None,
        )
        for f in handler.filters:
            f.filter(record)
        assert record.trace_id == "test-trace-123"
    reset_trace_id(tok)


def test_configure_logging_no_callbacks_does_not_raise():
    configure_logging(env="development", force=True)
    root = logging.getLogger()
    handler = next(
        (h for h in root.handlers if hasattr(h, "_nodus_structured_logging_handler")),
        None,
    )
    if handler:
        record = logging.LogRecord(
            name="test", level=logging.INFO, pathname="", lineno=0,
            msg="test", args=(), exc_info=None,
        )
        for f in handler.filters:
            f.filter(record)
        assert record.trace_id == ""
        assert record.user_id == ""


def test_configure_logging_idempotent():
    configure_logging(env="development", force=True)
    configure_logging(env="development")  # should not add duplicate handlers
    root = logging.getLogger()
    nodus_handlers = [
        h for h in root.handlers if hasattr(h, "_nodus_structured_logging_handler")
    ]
    assert len(nodus_handlers) == 1
