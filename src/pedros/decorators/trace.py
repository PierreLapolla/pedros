from __future__ import annotations

import inspect
from typing import (
    Any,
    Awaitable,
    Callable,
    ParamSpec,
    TypeVar,
    overload,
    cast,
)

import wrapt

from pedros.logger import get_logger, normalize_log_level

__all__ = ["trace"]

P = ParamSpec("P")
R = TypeVar("R")


@overload
def trace(func: Callable[P, R]) -> Callable[P, R]: ...


@overload
def trace(func: Callable[P, Awaitable[R]]) -> Callable[P, Awaitable[R]]: ...


@overload
def trace(
    *, log_level: str | None = "DEBUG"
) -> Callable[[Callable[P, R]], Callable[P, R]]: ...


@overload
def trace(
    *, log_level: str | None = "DEBUG"
) -> Callable[[Callable[P, Awaitable[R]]], Callable[P, Awaitable[R]]]: ...


def trace(
    func: Callable[P, Any] | None = None,
    *,
    log_level: str | None = "DEBUG",
) -> Any:
    """
    A decorator to log a function's arguments and return value, or the exception it
    raised. It never catches or suppresses exceptions, purely observational, and can
    be applied to both synchronous and asynchronous functions.

    :param func: The function to be decorated. If not provided, the decorator can be
        used with additional configuration through keyword arguments.
    :param log_level: The logging level to use for call/return/error traces. Defaults
        to "DEBUG". If set to "NONE" (case insensitive), no logging will occur.
    :return: A decorated function or an asynchronous coroutine that logs its calls.
    """

    def decorator(wrapped_func: Callable[P, Any]) -> Callable[P, Any]:
        normalized_level = normalize_log_level(log_level)

        @wrapt.decorator
        def wrapper(
            wrapped: Callable[P, Any],
            instance: Any,
            args: tuple[Any, ...],
            kwargs: dict[str, Any],
        ) -> Any:
            def _log_entry() -> None:
                if normalized_level is not None:
                    get_logger().log(
                        normalized_level,
                        f"Calling {wrapped.__name__}(args={args!r}, kwargs={kwargs!r})",
                    )

            def _log_result(result: Any) -> None:
                if normalized_level is not None:
                    get_logger().log(
                        normalized_level, f"{wrapped.__name__} returned {result!r}"
                    )

            def _log_error(exc: Exception) -> None:
                if normalized_level is not None:
                    get_logger().log(
                        normalized_level,
                        f"{wrapped.__name__} raised {type(exc).__name__}: {exc}",
                    )

            if inspect.iscoroutinefunction(wrapped):

                async def _async_call() -> Any:
                    _log_entry()
                    try:
                        result = await wrapped(*args, **kwargs)
                    except Exception as e:
                        _log_error(e)
                        raise
                    _log_result(result)
                    return result

                return _async_call()

            _log_entry()
            try:
                result = wrapped(*args, **kwargs)
            except Exception as e:
                _log_error(e)
                raise
            _log_result(result)
            return result

        return cast(Callable[P, Any], wrapper(wrapped_func))

    return decorator(func) if func is not None else decorator
