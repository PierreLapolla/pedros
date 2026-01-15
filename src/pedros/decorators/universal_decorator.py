from __future__ import annotations

import contextlib
import inspect
from typing import Any, Awaitable, Callable, Generator, ParamSpec, TypeVar, overload, cast

import wrapt

P = ParamSpec("P")
T = TypeVar("T")


@overload
def universal_decorator(func: Callable[P, T]) -> Callable[P, T]: ...
@overload
def universal_decorator(func: Callable[P, Awaitable[T]]) -> Callable[P, Awaitable[T]]: ...


@overload
def universal_decorator() -> Callable[[Callable[P, T]], Callable[P, T]]: ...


@overload
def universal_decorator() -> Callable[[Callable[P, Awaitable[T]]], Callable[P, Awaitable[T]]]: ...


def universal_decorator(func: Callable[P, Any] | None = None) -> Any:
    def decorator(wrapped_func: Callable[P, Any]) -> Callable[P, Any]:
        @wrapt.decorator
        def wrapper(
                wrapped: Callable[P, Any],
            instance: Any,
                args: tuple[Any, ...],
                kwargs: dict[str, Any],
        ) -> Any:
            @contextlib.contextmanager
            def _execute() -> Generator[None, None, None]:
                try:
                    # 1) pre
                    yield
                    # 3) post (success)
                except Exception:
                    # 4) error
                    raise
                finally:
                    # 5) finally
                    pass

            if inspect.iscoroutinefunction(wrapped):
                async def _async_call() -> Any:
                    with _execute():
                        return await wrapped(*args, **kwargs)

                return _async_call()

            with _execute():
                return wrapped(*args, **kwargs)

        return cast(Callable[P, Any], wrapper(wrapped_func))

    return decorator(func) if func is not None else decorator
