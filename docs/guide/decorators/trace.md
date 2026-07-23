---
icon: lucide/scan-search
---

# `@trace`

Logs a function's arguments and return value, or the exception it raised.
Purely observational: it never catches or suppresses exceptions, they
always propagate exactly as they would without the decorator.

```python
from pedros import trace


@trace
def add(x, y):
    return x + y


add(1, 2)
# Logs (DEBUG): "Calling add(args=(1, 2), kwargs={})"
# Logs (DEBUG): "add returned 3"
```

On an exception, it logs the exception instead of the return value, then
re-raises:

```python
@trace
def risky():
    raise ValueError("boom")


risky()
# Logs (DEBUG): "Calling risky(args=(), kwargs={})"
# Logs (DEBUG): "risky raised ValueError: boom"
# ... then ValueError propagates normally
```

Configure the log level:

```python
@trace(log_level="INFO")
def process_data():
    return "result"
```

Set `log_level="NONE"` to disable tracing entirely.

`@trace` always logs through the `pedros` logger, see the
[logging guide](../logging.md#pedross-own-logging) for how to view or
silence it.

## Async functions

```python
@trace
async def fetch_data():
    ...


await fetch_data()
```

## Combining with `@safe`

`@trace` never suppresses exceptions, so it composes cleanly with `@safe`
when you want both a full call/return/error trace and error handling:

```python
from pedros import trace, safe


@trace
@safe(re_raise=False)
def risky_operation():
    raise ValueError("Something went wrong")
```
