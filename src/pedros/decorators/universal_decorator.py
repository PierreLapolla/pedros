from __future__ import annotations

import contextlib
import inspect
from typing import Any, Awaitable, Callable, ParamSpec, TypeVar, overload, Generator

import wrapt

__all__ = ["universal_decorator"]

P = ParamSpec("P")
R = TypeVar("R")


@overload
def universal_decorator(func: Callable[P, R]) -> Callable[P, R]: ...


@overload
def universal_decorator() -> Callable[[Callable[P, R]], Callable[P, R]]: ...


def universal_decorator(
        func: Callable[P, R] | None = None,
) -> Any:
    @wrapt.decorator
    def wrapper(
            wrapped: Callable[P, R],
            instance: Any,
            args: Any,
            kwargs: Any,
    ) -> R | Awaitable[R]:

        @contextlib.contextmanager
        def _execute() -> Generator[None, None, None]:
            # --- 1. PRE-EXECUTION (Shared) ---
            # Place logic here that should run before the call.
            try:
                yield
                # --- 3. POST-EXECUTION (Shared) ---
                # Runs after a successful call.
            except Exception:
                # --- 4. ERROR HANDLING (Shared) ---
                # Runs if an exception is raised.
                raise
            finally:
                # --- 5. FINALLY (Shared) ---
                # Always runs at the end.
                pass

        if inspect.iscoroutinefunction(wrapped):
            async def _async_wrapper() -> R:
                with _execute():
                    return await wrapped(*args, **kwargs)

            return _async_wrapper()

        with _execute():
            return wrapped(*args, **kwargs)

    if func is None:
        return wrapper
    return wrapper(func)
