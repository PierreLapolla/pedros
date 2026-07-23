---
icon: lucide/gauge
---

# `@monitor`

Combines [`@trace`](trace.md), [`@timed`](timed.md), and [`@safe`](safe.md)
with their default settings. No configuration of its own, if you need to
tune any of the three, stack them individually instead.

```python
from pedros import monitor


@monitor
def process_data():
    return "result"


process_data()
# Logs (DEBUG): "calling process_data(args=(), kwargs={})"
# Logs (DEBUG): "process_data took 1.23 ms to execute."
# Logs (DEBUG): "process_data returned 'result'"
```

The `DEBUG`-level lines above stay silent unless you've raised `pedros`'s
verbosity, see the [logging guide](../logging.md#pedross-own-logging).
`@safe`'s `ERROR`-level line always shows at the default configuration.

On an exception, `@safe`'s error log fires (ERROR by default) in addition
to `@timed`'s duration and `@trace`'s own exception trace, then it
re-raises:

```python
@monitor
def risky():
    raise ValueError("boom")


risky()
# Logs (DEBUG): "calling risky(args=(), kwargs={})"
# Logs (ERROR): "Error in risky: boom"
# Logs (DEBUG): "risky took 45.00 µs to execute."
# Logs (DEBUG): "risky raised ValueError: boom"
# ... then ValueError propagates normally
```

Equivalent to:

```python
@trace
@timed
@safe
def f(): ...
```

`@trace` is outermost so it logs the call before anything else runs;
`@safe` is innermost so it catches errors closest to the source; `@timed`
sits between them so it measures the actual work.

## Async functions

```python
@monitor
async def fetch_data():
    ...


await fetch_data()
```
