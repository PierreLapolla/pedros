from __future__ import annotations

import contextlib
import inspect
from typing import Any, Awaitable, Callable, ParamSpec, TypeVar, overload, Generator

import wrapt

from pedros.logger import get_logger

__all__ = ["safe"]

logger = get_logger()

P = ParamSpec("P")
R = TypeVar("R")


@overload
def safe(
        func: Callable[P, R]
) -> Callable[P, R]: ...


@overload
def safe(
        *,
        catch: type[Exception] | tuple[type[Exception], ...] = Exception,
        log_level: str | None = "ERROR",
        re_raise: bool = True,
        on_error: Callable[[Exception], Any] | None = None,
        on_finally: Callable[[], Any] | None = None,
) -> Callable[[Callable[P, R]], Callable[P, R]]: ...


def safe(
        func: Callable[P, R] | None = None,
        *,
        catch: type[Exception] | tuple[type[Exception], ...] = Exception,
        log_level: str | None = "ERROR",
        re_raise: bool = True,
        on_error: Callable[[Exception], Any] | None = None,
        on_finally: Callable[[], Any] | None = None,
) -> Any:
    """
    A decorator function for safely executing another function within a context
    where exceptions can be logged, handled, and optionally propagated or suppressed.
    This utility can also execute additional actions when an error occurs or after the
    final execution, whether an exception was raised or not.

    :param func: The target function to be decorated. If not provided, the decorator
        is returned to be used with a target function. Defaults to None.
    :param catch: The type of exception or a tuple of exception types to catch.
        Defaults to Exception.
    :param log_level: The logging level to use when an exception is caught. If set to
        "NONE", no logging is performed. Defaults to "ERROR".
    :param re_raise: Determines whether the caught exceptions should be re-raised
        after handling. If True, the exception is re-raised. If False, the exception
        is suppressed. Defaults to True.
    :param on_error: An optional callable to be executed when an exception is caught.
        The callable should accept the exception instance as its parameter. Defaults
        to None.
    :param on_finally: An optional callable to be executed in a `finally` block after
        the function execution, regardless of whether an exception was raised or not.
        It does not accept any parameters. Defaults to None.
    :return: If `func` is provided, it returns the decorated version of `func`. If
        `func` is None, it returns the decorator to be used with a target function.
    """

    @wrapt.decorator
    def wrapper(
            wrapped: Callable[P, R],
            instance: Any,
            args: Any,
            kwargs: Any,
    ) -> R | Awaitable[R]:

        @contextlib.contextmanager
        def _handle_exception() -> Generator[None, None, None]:
            try:
                yield
            except catch as e:
                if log_level and log_level.upper() != "NONE":
                    log_msg = f"Error in {wrapped.__name__}: {str(e)}"
                    getattr(logger, log_level.lower())(log_msg, exc_info=True)

                if on_error:
                    on_error(e)

                if re_raise:
                    raise
            finally:
                if on_finally:
                    on_finally()

        if inspect.iscoroutinefunction(wrapped):
            async def _async_wrapper() -> R:
                with _handle_exception():
                    return await wrapped(*args, **kwargs)

            return _async_wrapper()

        with _handle_exception():
            return wrapped(*args, **kwargs)

    if func is None:
        return wrapper
    return wrapper(func)
