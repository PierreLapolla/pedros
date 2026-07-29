---
icon: lucide/library
---

# API Reference

Every symbol exported from `pedros`, grouped by area. For behavior details,
edge cases, and runnable examples, follow the link into the Guide.

## Decorators

### `timed`

```python
def timed(func=None, *, log_level: str | None = "DEBUG")
```

Logs how long the wrapped function took to run, at `log_level`. Usable bare
or configured, on sync and async functions. `log_level="NONE"` disables
logging. [Guide](guide/decorators/timed.md).

### `safe`

```python
def safe(
    func=None,
    *,
    catch: type[Exception] | tuple[type[Exception], ...] = Exception,
    log_level: str | None = "ERROR",
    re_raise: bool = True,
    on_error: Callable[[Exception], Any] | None = None,
    on_finally: Callable[[], Any] | None = None,
)
```

Wraps the function in a try/except: logs a caught `catch` exception at
`log_level`, invokes `on_error`/`on_finally`, and re-raises unless
`re_raise=False`. [Guide](guide/decorators/safe.md).

### `trace`

```python
def trace(func=None, *, log_level: str | None = "DEBUG")
```

Logs the call's arguments and its return value or raised exception, at
`log_level`. Never suppresses exceptions. [Guide](guide/decorators/trace.md).

### `monitor`

```python
def monitor(func)
```

Combines `@trace`, `@timed`, and `@safe` with their defaults; no
configuration of its own. [Guide](guide/decorators/monitor.md).

## Logging

### `setup_logging`

```python
def setup_logging(
    level: int | str = logging.INFO,
    logger_name: str = "pedros",
    *,
    add_handler: bool | None = None,
    propagate: bool | None = None,
) -> None
```

Configures one logger without touching root logging. Attaches a
[Rich](https://pypi.org/project/rich/) handler if installed, else a plain
`logging.StreamHandler`. [Guide](guide/logging.md).

### `get_logger`

```python
def get_logger(name: str | None = None) -> logging.Logger
```

Returns a logger. With no `name`, returns the `pedros` logger,
auto-configured on first use if nothing has configured it yet —
deterministically: its own handler, no propagation, regardless of call
order. [Guide](guide/logging.md).

### `normalize_log_level`

```python
def normalize_log_level(log_level: int | str | None) -> int | None
```

Normalizes a numeric level, a level name (case-insensitive), `"NONE"`, or
`None` to a numeric level or `None` (disabled). Raises `ValueError` on an
unrecognized name. Used internally by `setup_logging` and every decorator's
`log_level` parameter — the same mechanism behind `log_level="NONE"`.

## Progress bars

### `progbar`

```python
def progbar(
    iterable: Iterable[T],
    *args: Any,
    backend: Literal["auto", "rich", "tqdm", "none"] = "auto",
    **kwargs: Any,
) -> Iterable[T]
```

Wraps `iterable` with a progress bar, picking a backend automatically or per
`backend`. `desc`/`description` are normalized to whichever the chosen
backend expects. [Guide](guide/progress-bars.md).

## Dependency checks

### `has_dep`

```python
def has_dep(name: str, version: str | None = None) -> bool
```

Returns whether `name` is importable and, if `version` is given, whether the
installed version satisfies it (`==`, `!=`, `>=`, `>`, `<=`, `<`,
comma-separated clauses combined with AND). [Guide](guide/has-dep.md).
