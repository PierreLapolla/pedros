---
icon: lucide/timer
---

# Decorators

Both `@timed` and `@safe` work on sync and async functions transparently, and
can be used bare (`@timed`) or configured (`@timed(...)`).

## `@timed`

Logs how long a function took to run.

```python
import time
from pedros import timed


@timed
def long_running_func(sleep_time: float):
    time.sleep(sleep_time)


long_running_func(0.001)
# Logs (INFO): "long_running_func took 1.23 ms to execute."
```

The duration is formatted with an appropriate unit — nanoseconds,
microseconds, milliseconds, seconds, or `hh:mm:ss` for anything over a
minute.

Configure the log level or target a specific logger:

```python
@timed(log_level="DEBUG", logger="my_package")
def process_data():
    return "result"
```

Set `log_level="NONE"` to time silently without logging.

## `@safe`

Wraps a function in a try/except, with logging, error callbacks, and
optional re-raising.

```python
from pedros import safe, get_logger

logger = get_logger("safe_demo")


@safe(re_raise=False)
def risky_operation():
    logger.info("Executing risky_operation...")
    raise ValueError("Something went wrong")


risky_operation()  # Logs the error (ERROR level) but doesn't crash
```

### Options

- `catch`: exception type or tuple of types to catch (default: `Exception`)
- `log_level`: level used when logging a caught exception, or `"NONE"` to
  suppress logging entirely (default: `"ERROR"`)
- `re_raise`: re-raise the exception after handling it (default: `True`)
- `on_error`: callback invoked with the caught exception
- `on_finally`: callback invoked in a `finally` block, regardless of outcome
- `logger`: logger instance or name to log through

```python
def handle_error(e):
    logger.info(f"Custom error handler caught: {type(e).__name__}")


def cleanup():
    logger.info("Cleanup task executed in finally block")


@safe(catch=KeyError, on_error=handle_error, on_finally=cleanup, re_raise=False)
def specific_fail():
    raise KeyError("Missing key!")
```

### Async functions

```python
import asyncio


@safe(re_raise=False)
async def async_fail():
    await asyncio.sleep(0.1)
    raise ConnectionError("Lost connection")


asyncio.run(async_fail())
```

`@timed` supports the same async usage.
