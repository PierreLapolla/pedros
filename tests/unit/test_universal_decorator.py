from typing import ParamSpec, TypeVar

import pytest
import wrapt

from pedros.decorators.universal_decorator import universal_decorator

P = ParamSpec("P")
R = TypeVar("R")


def test_universal_decorator_sync():
    """Test universal_decorator template with synchronous functions."""

    @universal_decorator
    def test_func(x: int, y: int) -> int:
        return x + y

    assert test_func(2, 3) == 5
    assert test_func.__name__ == "test_func"


@pytest.mark.asyncio
async def test_universal_decorator_async():
    """Test universal_decorator template with asynchronous functions."""

    @universal_decorator
    async def test_func(x: int, y: int) -> int:
        return x + y

    assert await test_func(2, 3) == 5
    assert test_func.__name__ == "test_func"


def test_universal_decorator_no_args():
    """Test universal_decorator template used as @decorator()."""

    @universal_decorator()
    def test_func(x: int) -> int:
        return x * 2

    assert test_func(10) == 20


def test_custom_decorator_from_template():
    """Test creating a custom decorator using the universal_decorator pattern."""

    def my_custom_decorator(func=None, *, prefix="[LOG]"):
        def decorator(wrapped):
            @wrapt.decorator
            def wrapper(wrapped, instance, args, kwargs):
                # We can add custom logic here
                res = wrapped(*args, **kwargs)
                return f"{prefix} {res}"

            return wrapper(wrapped)

        if func is None:
            return lambda f: decorator(f)
        return decorator(func)

    @my_custom_decorator(prefix="Result:")
    def add(a, b):
        return a + b

    assert add(1, 2) == "Result: 3"


def test_universal_decorator_method():
    """Test universal_decorator template with class methods."""

    class MyClass:
        def __init__(self, value: int):
            self.value = value

        @universal_decorator
        def get_value(self, multiplier: int) -> int:
            return self.value * multiplier

    obj = MyClass(10)
    assert obj.get_value(2) == 20
    assert obj.get_value.__name__ == "get_value"


@pytest.mark.asyncio
async def test_universal_decorator_async_method():
    """Test universal_decorator template with async class methods."""

    class MyClass:
        def __init__(self, value: int):
            self.value = value

        @universal_decorator
        async def get_value(self, multiplier: int) -> int:
            return self.value * multiplier

    obj = MyClass(10)
    assert await obj.get_value(3) == 30
    assert obj.get_value.__name__ == "get_value"
