# Contributing to nodus-observability

## Setup

```bash
git clone https://github.com/Masterplanner25/nodus-observability.git
cd nodus-observability
pip install -e ".[dev]"
```

The `dev` extra includes `python-json-logger` so JSON logging tests pass.

## Running tests

```bash
pytest tests/ -q
```

## Code style

- Python 3.11+
- All four subsystems (context, logging, otel, metrics) must degrade
  gracefully when their optional dep is absent — use `try/except ImportError`
- `create_registry()` must never use the global Prometheus registry
- ContextVars must be async-safe and reset-safe (always return a token for reset)

## Submitting changes

1. Fork the repo and create a branch from `main`
2. Add tests for any new behaviour
3. Ensure `pytest tests/ -q` passes
4. Open a pull request with a description of what changes and why
