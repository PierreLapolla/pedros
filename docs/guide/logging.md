---
icon: lucide/scroll-text
---

# Logging

`setup_logging` configures a single logger without touching Python's root
logging configuration. It attaches a [Rich](https://pypi.org/project/rich/)
handler when `rich` is installed, and falls back to a plain
`logging.StreamHandler` otherwise.

## Basic usage

```python
import logging
from pedros import setup_logging, get_logger

setup_logging(level=logging.DEBUG)
logger = get_logger()

logger.debug("This is a debug message.")
logger.info("This is an info message.")
logger.warning("This is a warning message.")
logger.error("This is an error message.")
logger.critical("This is a critical message.")
```

`level` also accepts a level name instead of the `logging` constant:

```python
setup_logging(level="DEBUG")
```

If `rich` is not installed, `setup_logging` silently falls back to a
timestamped, plain-text formatter — no code changes needed.

## Configuring another logger

By default, `setup_logging` and `get_logger` target the `pedros` logger. Pass
`logger_name` / a name to target any logger, e.g. your own package's, without
affecting root logging or other loggers:

```python
setup_logging(logger_name="my_package")
logger = get_logger("my_package")
```

## Handler and propagation control

`add_handler` and `propagate` are inferred by default:

- a handler is attached only if neither root logging nor the target logger
  already has one
- propagation to ancestor loggers is enabled only when the target logger
  ends up without its own handler (i.e. root logging is doing the handling)

Override either explicitly if you need different behavior:

```python
setup_logging(logger_name="my_package", add_handler=True, propagate=False)
```
