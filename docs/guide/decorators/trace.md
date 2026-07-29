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
# Logs (DEBUG): "calling add(args=(1, 2), kwargs={})"
# Logs (DEBUG): "add returned 3"
```

`@trace` logs at `DEBUG` by default, which stays silent unless you've
raised `pedros`'s verbosity, see the
[logging guide](../logging.md#pedross-own-logging).

On an exception, it logs the exception instead of the return value, then
re-raises:

```python
@trace
def risky():
    raise ValueError("boom")


risky()
# Logs (DEBUG): "calling risky(args=(), kwargs={})"
# Logs (DEBUG): "risky raised ValueError: boom"
# ... then ValueError propagates normally
```

## Options

- `log_level`: level used for the call/return/error trace, or `"NONE"` to
  disable tracing entirely (default: `"DEBUG"`)

```python
@trace(log_level="INFO")
def process_data():
    return "result"
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
