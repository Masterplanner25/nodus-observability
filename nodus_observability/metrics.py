"""Prometheus metrics helpers.

The core pattern: always use a dedicated ``CollectorRegistry`` rather than
the default global registry.  This prevents metric registration conflicts
when multiple libraries or tests share the same Python process.

Usage::

    from nodus_observability import create_registry, Counter, Histogram, Gauge

    REGISTRY = create_registry()

    requests_total = Counter(
        "myapp_requests_total",
        "Total HTTP requests",
        ["method", "status"],
        registry=REGISTRY,
    )
"""
from __future__ import annotations

try:
    from prometheus_client import CollectorRegistry, Counter, Gauge, Histogram

    _PROMETHEUS_AVAILABLE = True
except ImportError:
    CollectorRegistry = None  # type: ignore[assignment,misc]
    Counter = None  # type: ignore[assignment,misc]
    Gauge = None  # type: ignore[assignment,misc]
    Histogram = None  # type: ignore[assignment,misc]
    _PROMETHEUS_AVAILABLE = False


def create_registry() -> "CollectorRegistry":
    """Return a fresh Prometheus CollectorRegistry.

    Always prefer a dedicated registry over the default global one to avoid
    metric name conflicts across libraries and test runs.

    Raises:
        ImportError: If ``prometheus-client`` is not installed.  Install with
            ``pip install 'nodus-observability[metrics]'``.
    """
    if not _PROMETHEUS_AVAILABLE:
        raise ImportError(
            "prometheus-client is required for metrics support. "
            "Install with: pip install 'nodus-observability[metrics]'"
        )
    return CollectorRegistry(auto_describe=True)
