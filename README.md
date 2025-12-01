# Decorpack

[![PyPI](https://img.shields.io/pypi/v/pedros)](https://pypi.org/project/pedros/)  

A small collection of reusable Python decorators and utilities.

## Features
 
- `logger`: pre-configured Python logger ready to use

## Installation

```bash
  pip install pedros
```

## Quickstart

```python
from pedros.logger import setup_logging, get_logger

setup_logging()
logger = get_logger(__name__)

logger.info("This is an info message")
```

## License

This project is licensed under the MIT [License](LICENSE).
