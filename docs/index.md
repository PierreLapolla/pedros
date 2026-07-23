---
icon: lucide/rocket
---

# pedros

A small package of reusable Python utilities for Python projects.

## Features

- **Dependency Management**: smart detection of optional dependencies ([`has_dep`](guide/has-dep.md))
- **Logging**: simplified logging setup with optional Rich support ([logging guide](guide/logging.md))
- **Progress Bars**: unified progress bar API with multiple backends ([progress bars guide](guide/progress-bars.md))
- **Decorators**: robust decorators for timing and error handling ([decorators guide](guide/decorators.md))
- **Type Safe**: comprehensive type hints and PEP 561 compliance

## Installation

```bash
pip install pedros
```

or

```bash
uv add pedros
```

Optional backends:

```bash
pip install "pedros[rich]"   # Rich logging/progress backend
pip install "pedros[all]"    # all optional backends
```

## Quickstart

```python
from pedros import setup_logging, get_logger, progbar, timed, safe

# Configure logging for pedros
setup_logging()
logger = get_logger()

# Or configure another package logger without touching root logging
setup_logging(logger_name="my_package")
logger = get_logger("my_package")

# Use progress bar (auto-selects backend: rich > tqdm > basic)
for item in progbar(range(10), desc="Processing"):
    pass

# Time function execution
@timed(logger="my_package")
def process_data():
    return "result"


process_data()  # Logs: "process_data took 1.23 ms to execute."


# Safely handle errors
@safe(re_raise=False, logger="my_package")
def risky_operation():
    raise ValueError("Something went wrong")


risky_operation()  # Logs the error but doesn't crash
```

See the guide pages in the sidebar for details and more examples on every feature.
