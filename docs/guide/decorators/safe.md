---
icon: lucide/shield-alert
---

# `@safe`

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

## Options

- `catch`: exception type or tuple of types to catch (default: `Exception`)
- `log_level`: level used when logging a caught exception, or `"NONE"` to
  suppress logging entirely (default: `"ERROR"`)
- `re_raise`: re-raise the exception after handling it (default: `True`)
- `on_error`: callback invoked with the caught exception
- `on_finally`: callback invoked in a `finally` block, regardless of outcome

`@safe` always logs through the `pedros` logger — see the
[logging guide](../logging.md#pedross-own-logging) for how to view or
silence it.

```python
def handle_error(e):
    logger.info(f"Custom error handler caught: {type(e).__name__}")


def cleanup():
    logger.info("Cleanup task executed in finally block")


@safe(catch=KeyError, on_error=handle_error, on_finally=cleanup, re_raise=False)
def specific_fail():
    raise KeyError("Missing key!")
```

## Async functions

```python
import asyncio


@safe(re_raise=False)
async def async_fail():
    await asyncio.sleep(0.1)
    raise ConnectionError("Lost connection")


asyncio.run(async_fail())
```
