---
icon: lucide/blocks
---

# Universal decorator (template)

`pedros.decorators.universal_decorator` is not part of the public API: it
isn't exported from `pedros` or from `pedros.decorators`. It exists as a
**template** for writing new decorators that need the same shape as
`@timed` and `@safe`: usable bare or configured, transparent on both sync
and async functions, built on [`wrapt`](https://pypi.org/project/wrapt/) so
the wrapped function's signature is preserved.

```python title="src/pedros/decorators/universal_decorator.py"
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
```

The full file also carries `@overload` signatures for bare vs. configured,
sync vs. async usage, see `src/pedros/decorators/universal_decorator.py`
for those; they don't affect runtime behavior.

## The hook points

Inside `_execute`, the numbered comments mark where your own decorator's
behavior goes:

1. **pre**: runs before the wrapped call
2. **post (success)**: runs immediately after a successful call
3. **error**: runs if the wrapped call raises; re-raises by default
4. **finally**: always runs, success or failure

`@timed` fills in *pre* (start a timer) and *finally* (log the elapsed
time). `@safe` fills in *error* (log, invoke `on_error`, decide whether to
re-raise) and *finally* (invoke `on_finally`).

## Building your own decorator from it

1. Copy `universal_decorator.py` into your own module and rename it.
2. Add whatever configuration parameters your decorator needs as keyword
   arguments on the outer function (see `safe`'s `catch`, `log_level`,
   `on_error`, ... for the pattern).
3. Fill in the hook(s) you need inside `_execute`.
4. Leave the `inspect.iscoroutinefunction` branch and the
   `decorator(func) if func is not None else decorator` return alone,
   that's what makes bare (`@my_decorator`) and configured
   (`@my_decorator(...)`) usage both work on sync and async functions.
