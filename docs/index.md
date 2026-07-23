---
icon: lucide/rocket
---

# pedros

A small package of reusable Python utilities for Python projects.

## Features

- **Dependency Management**: smart detection of optional dependencies ([`has_dep`](guide/has-dep.md))
- **Logging**: simplified logging setup with optional Rich support ([logging guide](guide/logging.md))
- **Progress Bars**: unified progress bar API with multiple backends ([progress bars guide](guide/progress-bars.md))
- **Decorators**: robust decorators for timing and error handling ([decorators section](guide/decorators/index.md))
- **Type Safe**: comprehensive type hints and PEP 561 compliance

## Installation

```bash
pip install pedros
```

or

```bash
uv add pedros
```

`rich` and `tqdm` are optional and auto-detected at runtime — install either
yourself to get the enhanced logging/progress-bar backend.

See the guide pages in the sidebar for usage examples of every feature.
