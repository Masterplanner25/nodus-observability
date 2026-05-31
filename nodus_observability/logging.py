"""Structured JSON logging with pluggable correlation context."""
from __future__ import annotations

import logging
import os
from typing import Any, Callable, Optional

_HANDLER_MARKER = "_nodus_structured_logging_handler"


class _CorrelationFilter(logging.Filter):
    """Inject trace_id, user_id, and env into every log record.

    Fields added (all strings):
      ``trace_id`` — from ``get_trace_id_fn()`` or empty string
      ``user_id``  — from ``get_request_fn()`` / ``get_context_fn()`` or empty string
      ``env``      — deployment environment label
    """

    def __init__(
        self,
        env: str = "development",
        *,
        get_trace_id_fn: Optional[Callable[[], Optional[str]]] = None,
        get_request_fn: Optional[Callable[[], Any]] = None,
        get_context_fn: Optional[Callable[[], Any]] = None,
    ) -> None:
        super().__init__()
        self._env = env
        self._get_trace_id = get_trace_id_fn or (lambda: None)
        self._get_request = get_request_fn or (lambda: None)
        self._get_context = get_context_fn or (lambda: None)

    def filter(self, record: logging.LogRecord) -> bool:
        try:
            record.trace_id = self._get_trace_id() or ""
            request = self._get_request()
            request_state = getattr(request, "state", None)
            record.user_id = ""
            if request_state is not None:
                record.user_id = str(getattr(request_state, "user_id", "") or "")
            if not record.user_id:
                execution_context = self._get_context()
                if isinstance(execution_context, dict):
                    record.user_id = str(execution_context.get("user_id", "") or "")
                elif execution_context is not None:
                    record.user_id = str(getattr(execution_context, "user_id", "") or "")
        except Exception:
            record.trace_id = ""
            record.user_id = ""
        record.env = self._env
        return True


def configure_logging(
    *,
    env: str = "development",
    log_level: str = "INFO",
    json_logs: Optional[bool] = None,
    force: bool = False,
    get_trace_id_fn: Optional[Callable[[], Optional[str]]] = None,
    get_request_fn: Optional[Callable[[], Any]] = None,
    get_context_fn: Optional[Callable[[], Any]] = None,
) -> None:
    """Configure the root logger with structured correlation output.

    ``json_logs`` defaults to True in production/staging, False in dev/test.
    Override via the ``LOG_FORMAT`` environment variable (``json`` or ``text``).

    Args:
        env: Deployment environment name (``"development"``, ``"production"``, etc.).
        log_level: Root log level string (``"DEBUG"``, ``"INFO"``, etc.).
        json_logs: Force JSON (True) or plain text (False).  Auto-detected when None.
        force: Replace existing handlers even when one already exists.
        get_trace_id_fn: Callable returning the current trace ID string or None.
        get_request_fn: Callable returning the current HTTP request object or None.
        get_context_fn: Callable returning the current execution context or None.

    Usage with nodus-observability's own context module::

        from nodus_observability import configure_logging, get_trace_id
        configure_logging(env="development", get_trace_id_fn=get_trace_id)

    Usage with AINDY trace_context::

        from nodus_observability import configure_logging
        from AINDY.platform_layer.trace_context import get_current_trace_id, get_current_request, get_current_execution_context
        configure_logging(
            env="production",
            get_trace_id_fn=get_current_trace_id,
            get_request_fn=get_current_request,
            get_context_fn=get_current_execution_context,
        )
    """
    if json_logs is None:
        fmt_env = os.getenv("LOG_FORMAT", "").lower()
        if fmt_env == "json":
            json_logs = True
        elif fmt_env == "text":
            json_logs = False
        else:
            json_logs = env.lower() in {"production", "prod", "staging"}

    correlation_filter = _CorrelationFilter(
        env=env,
        get_trace_id_fn=get_trace_id_fn,
        get_request_fn=get_request_fn,
        get_context_fn=get_context_fn,
    )

    if json_logs:
        try:
            from pythonjsonlogger import jsonlogger

            formatter = jsonlogger.JsonFormatter(
                fmt="%(asctime)s %(levelname)s %(name)s %(message)s %(trace_id)s %(user_id)s %(env)s",
                datefmt="%Y-%m-%dT%H:%M:%S",
                rename_fields={
                    "asctime": "timestamp",
                    "levelname": "level",
                    "name": "logger",
                },
            )
        except ImportError:
            formatter = logging.Formatter(
                "%(asctime)s %(levelname)s %(name)s [trace_id=%(trace_id)s user_id=%(user_id)s env=%(env)s] %(message)s",
                datefmt="%Y-%m-%dT%H:%M:%S",
            )
    else:
        formatter = logging.Formatter(
            "%(asctime)s %(levelname)s %(name)s [trace_id=%(trace_id)s user_id=%(user_id)s env=%(env)s] %(message)s",
            datefmt="%Y-%m-%dT%H:%M:%S",
        )

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    handler.addFilter(correlation_filter)
    setattr(handler, _HANDLER_MARKER, True)

    root = logging.getLogger()
    current_handler = next(
        (
            candidate
            for candidate in root.handlers
            if getattr(candidate, _HANDLER_MARKER, False)
        ),
        None,
    )
    should_replace = force or current_handler is None or len(root.handlers) != 1

    if should_replace:
        root.handlers.clear()
        root.addHandler(handler)
    else:
        current_handler.setFormatter(formatter)
        for existing_filter in list(current_handler.filters):
            current_handler.removeFilter(existing_filter)
        current_handler.addFilter(correlation_filter)

    root.setLevel(getattr(logging, log_level.upper(), logging.INFO))

    if env.lower() in {"production", "prod"}:
        logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
        logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
        logging.getLogger("apscheduler").setLevel(logging.WARNING)
