---
icon: lucide/rocket
---

# pedros

A small package of reusable Python utilities: zero-setup logging, a
multi-backend progress bar, and sync/async-safe decorators for timing,
error handling, and call tracing.

## Installation

```bash
pip install pedros
```

or

```bash
uv add pedros
```

Requires Python 3.10-3.15. `rich` and `tqdm` are optional and auto-detected
at runtime; install either to get the enhanced logging/progress-bar
backend.

## A quick tour

```python
from pedros import monitor, progbar

@monitor
def process(items):
    for item in progbar(items, desc="Processing"):
        ...

process(range(100))
```

`@monitor` logs the call, times it, and catches/logs/re-raises any
exception; `progbar` shows a progress bar with whatever backend is
installed. Both need zero configuration.

## Where to go next

- [Guide](guide/logging.md) — one page per feature, with runnable examples
  and every configuration option
- [API Reference](reference.md) — every public signature in one place
