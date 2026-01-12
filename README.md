# Pedros

[![PyPI](https://img.shields.io/pypi/v/pedros)](https://pypi.org/project/pedros/)  

A small package of reusable Python utilities for Python projects.

## Features

- **Dependency Management**: Smart detection of optional dependencies (rich, tqdm)
- **Logging**: Simplified logging setup with optional Rich support
- **Progress Bars**: Unified progress bar API with multiple backends
- **Decorators**: Robust decorators for timing (`@timed`) and error handling (`@safe`)
- **Type Safe**: Comprehensive type hints and PEP 561 compliance

## Installation

```bash
pip install pedros
```

OR

```bash
uv add pedros
```

## Quickstart

```python
from pedros import setup_logging, get_logger, progbar, timed, safe

# Configure logging
setup_logging()
logger = get_logger()

# Use progress bar (auto-selects backend: rich > tqdm > basic)
for item in progbar(range(10), desc="Processing"):
    pass

# Time function execution
@timed
def process_data():
    return "result"


process_data()  # Logs: "process_data took 1.23 ms to execute."


# Safely handle errors
@safe(re_raise=False)
def risky_operation():
    raise ValueError("Something went wrong")


risky_operation()  # Logs the error but doesn't crash
```

## License

This project is licensed under the MIT [License](LICENSE).

## Contributing

Contributions are welcome! Please open issues or pull requests on GitHub.

## Support

For questions or support, please open a GitHub issue.
