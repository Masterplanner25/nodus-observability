# Changelog

Format: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
Versioning: [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

---

## [0.1.0] — 2026-05-31

Initial release.

### Added

- **Trace ContextVars (zero dependencies)** — async-safe context propagation:
  `get_trace_id` / `set_trace_id` / `reset_trace_id` / `ensure_trace_id`
  (auto-generates UUID v4 if unset).
  `get_parent_event_id` / `set_parent_event_id` / `reset_parent_event_id`.
  `is_pipeline_active` / `set_pipeline_active` / `reset_pipeline_active`.
  `get_current_request` / `set_current_request` / `reset_current_request`.
  `get_current_execution_context` / `set_current_execution_context` /
  `reset_current_execution_context`.

- **`configure_logging(env, service, level, json_logs)`** — sets up the root
  logger with JSON formatting (via `pythonjsonlogger`) when `json_logs=True`.
  Falls back to plain text when `python-json-logger` is not installed.
  Correlation fields (`trace_id`, `user_id`, `env`) injected from ContextVars.
  Requires `[logging]` extra for JSON output.

- **`init_otel(service_name)`** — bootstraps `TracerProvider` with OTLP gRPC
  exporter. Reads `OTEL_EXPORTER_OTLP_ENDPOINT` from environment. No-op when
  `[otel]` extra not installed. Requires `[otel]` extra.

- **`get_tracer(name)`** — returns a tracer (noop `_NoopTracer` when OTel
  not installed).

- **`span_context_from_trace_id(hex_trace_id)`** — converts a hex trace ID
  to an OTel `SpanContext` for distributed trace propagation.

- **`create_registry()`** — creates a fresh `CollectorRegistry` (never uses
  the global default — avoids metric pollution between tests/instances).
  `Counter`, `Gauge`, `Histogram` re-exported from `prometheus_client`.
  Requires `[metrics]` extra.

- **27 tests** across three test files (context, logging, otel).

- **No required dependencies** — all extras optional. Core ContextVars are
  pure stdlib. JSON logging requires `[logging]`, OTel requires `[otel]`,
  Prometheus requires `[metrics]`.

[0.1.0]: https://github.com/Masterplanner25/nodus-observability/releases/tag/v0.1.0
