# pedros

`pedros` is a compact utility package for:

- dependency detection (`has_dep`),
- logging setup (`setup_logging`, `get_logger`),
- progress bars with fallback backends (`progbar`),
- resilient decorators (`@timed`, `@safe`).

## Quickstart

```python
from pedros import setup_logging, get_logger, progbar, timed, safe

setup_logging()
logger = get_logger("demo")

for i in progbar(range(3), desc="Processing"):
    logger.info("step=%s", i)

@timed
def work():
    return "ok"

@safe(re_raise=False)
def risky():
    raise ValueError("boom")
```

## Build Docs

```bash
uv sync --group docs
uv run mkdocs build --strict
```
