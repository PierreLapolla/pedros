from __future__ import annotations

import contextlib
import inspect
from time import perf_counter
from typing import Any, Awaitable, Callable, ParamSpec, TypeVar, overload, Generator

import wrapt

from pedros.logger import get_logger

__all__ = ["timed"]

logger = get_logger()

P = ParamSpec("P")
R = TypeVar("R")


def _format_time(seconds: float) -> str:
    """
    Formats a given time duration in seconds into a human-readable string with
    appropriate units such as nanoseconds, microseconds, milliseconds,
    seconds, minutes, or hours.

    The format is selected based on the magnitude of the given seconds:
    - Less than a microsecond: formatted as nanoseconds.
    - Less than a millisecond: formatted as microseconds.
    - Less than a second: formatted as milliseconds.
    - Between a second and one minute: formatted as seconds.
    - Between one minute and one hour: formatted as minutes and seconds.
    - Greater than or equal to an hour: formatted as hours, minutes,
      and seconds.

    :param seconds: The time duration in seconds to be formatted.
    :type seconds: float
    :return: A human-readable string representing the time duration.
    :rtype: str
    """
    if seconds < 1e-6:
        return f"{seconds * 1e9:.2f} ns"
    if seconds < 1e-3:
        return f"{seconds * 1e6:.2f} µs"
    if seconds < 1:
        return f"{seconds * 1e3:.2f} ms"
    if seconds < 60:
        return f"{seconds:.2f} s"
    if seconds < 3600:
        minutes = int(seconds // 60)
        secs = seconds % 60
        return f"{minutes}:{secs:.2f} s"
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = seconds % 60
    return f"{hours}:{minutes}:{secs:.2f} s"


@overload
def timed(
        func: Callable[P, R]
) -> Callable[P, R]: ...


@overload
def timed(
        *,
        log_level: str | None = "INFO"
) -> Callable[[Callable[P, R]], Callable[P, R]]: ...


def timed(
        func: Callable[P, R] | None = None,
        *,
        log_level: str | None = "INFO",
) -> Any:
    """
    A decorator to measure and log the execution time of a function or method. It can
    be applied to both synchronous and asynchronous functions, and allows customization
    of the logging level.

    :param func: The function to be decorated. If not provided, the decorator can be used
        with additional configuration through keyword arguments.
    :param log_level: The logging level to use for reporting execution time. Defaults to
        "INFO". If set to "NONE" (case insensitive), no logging will occur.
    :return: A decorated function or an asynchronous coroutine that logs its execution
        time.
    """

    def decorator(wrapped: Callable[P, R]) -> Callable[P, R]:
        @wrapt.decorator
        def wrapper(
                wrapped: Callable[P, R],
                instance: Any,
                args: Any,
                kwargs: Any,
        ) -> R | Awaitable[R]:
            start_time = perf_counter()

            @contextlib.contextmanager
            def _time_it() -> Generator[None, None, None]:
                try:
                    yield
                finally:
                    elapsed = perf_counter() - start_time

                    if log_level and log_level.upper() != "NONE":
                        log_msg = f"{wrapped.__name__} took {_format_time(elapsed)} to execute."
                        getattr(logger, log_level.lower())(log_msg)

            if inspect.iscoroutinefunction(wrapped):
                async def _async_wrapper() -> R:
                    with _time_it():
                        return await wrapped(*args, **kwargs)

                return _async_wrapper()

            with _time_it():
                return wrapped(*args, **kwargs)

        return wrapper(wrapped)

    if func is None:
        return decorator
    return decorator(func)
