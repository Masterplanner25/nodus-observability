# nodus-observability

OpenTelemetry bootstrap, Prometheus registry, structured JSON logging, and async-safe trace ContextVars. Zero required dependencies beyond `python-json-logger` — OTel and Prometheus are optional extras.

> **Status:** v0.1.0 — published on [PyPI](https://pypi.org/project/nodus-observability/).

## Install

```bash
pip install nodus-observability                    # core only
pip install "nodus-observability[metrics]"         # + prometheus-client
pip install "nodus-observability[otel]"            # + opentelemetry stack
pip install "nodus-observability[all]"             # everything
```

## Trace context

```python
from nodus_observability import set_trace_id, get_trace_id, reset_trace_id, ensure_trace_id

tok = set_trace_id("req-abc-123")
print(get_trace_id())    # "req-abc-123"
reset_trace_id(tok)
```

## Structured logging

```python
from nodus_observability import configure_logging, get_trace_id

configure_logging(
    env="production",
    log_level="INFO",
    get_trace_id_fn=get_trace_id,   # inject trace_id from ContextVar
)
```

## OTel tracing

```python
from nodus_observability import init_otel, get_tracer

init_otel(service_name="my-service")   # reads OTEL_EXPORTER_OTLP_ENDPOINT
tracer = get_tracer("my-module")

with tracer.start_as_current_span("my-operation") as span:
    span.set_status("ok")
```

## Prometheus metrics

```python
from nodus_observability import create_registry, Counter

REGISTRY = create_registry()   # never use the default global registry

requests_total = Counter(
    "myapp_requests_total",
    "Total requests",
    ["method", "status"],
    registry=REGISTRY,
)
requests_total.labels(method="GET", status="200").inc()
```

## Extracted from

`AINDY/platform_layer/trace_context.py`, `otel.py`, `metrics.py`, and `log_config.py` in the A.I.N.D.Y. runtime.
