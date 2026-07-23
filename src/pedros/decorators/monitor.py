from __future__ import annotations

from typing import Any, Awaitable, Callable, ParamSpec, TypeVar, overload

from pedros.decorators.safe import safe
from pedros.decorators.timed import timed
from pedros.decorators.trace import trace

__all__ = ["monitor"]

P = ParamSpec("P")
R = TypeVar("R")


@overload
def monitor(func: Callable[P, R]) -> Callable[P, R]: ...


@overload
def monitor(func: Callable[P, Awaitable[R]]) -> Callable[P, Awaitable[R]]: ...


def monitor(func: Callable[P, Any]) -> Any:
    """
    A decorator that combines `@trace`, `@timed`, and `@safe` with their default
    settings, with no configuration of its own. Logs the call and return value,
    times execution, and catches/logs/re-raises exceptions.

    Equivalent to stacking all three with their defaults:

    ```python
    @trace
    @timed
    @safe
    def f(): ...
    ```

    :param func: The function to be decorated.
    :return: The decorated function, wrapped with tracing, timing, and error handling.
    """
    return trace(timed(safe(func)))
