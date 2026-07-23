import pytest

from pedros.decorators.monitor import monitor


def test_monitor_sync_success():
    @monitor
    def func(x, y):
        return x + y

    assert func(1, 2) == 3
    assert func.__name__ == "func"


@pytest.mark.asyncio
async def test_monitor_async_success():
    @monitor
    async def func(x, y):
        return x + y

    result = func(1, 2)
    assert await result == 3
    assert func.__name__ == "func"


def test_monitor_logs_call_timing_and_result(caplog):
    @monitor
    def func(x, y):
        return x + y

    with caplog.at_level("DEBUG", logger="pedros"):
        assert func(1, 2) == 3

    assert "calling func" in caplog.text
    assert "func returned 3" in caplog.text
    assert "func took" in caplog.text


def test_monitor_sync_error_is_logged_and_reraised(caplog):
    @monitor
    def func():
        raise ValueError("boom")

    with caplog.at_level("DEBUG", logger="pedros"):
        with pytest.raises(ValueError, match="boom"):
            func()

    assert "Error in func: boom" in caplog.text
    assert "func took" in caplog.text


@pytest.mark.asyncio
async def test_monitor_async_error_is_logged_and_reraised(caplog):
    @monitor
    async def func():
        raise RuntimeError("async boom")

    with caplog.at_level("DEBUG", logger="pedros"):
        with pytest.raises(RuntimeError, match="async boom"):
            await func()

    assert "Error in func: async boom" in caplog.text


def test_monitor_method():
    class MyClass:
        @monitor
        def method(self, value):
            return value * 2

    obj = MyClass()
    assert obj.method(5) == 10
    assert obj.method.__name__ == "method"


@pytest.mark.asyncio
async def test_monitor_async_method():
    class MyClass:
        @monitor
        async def method(self, value):
            return value * 2

    obj = MyClass()
    assert await obj.method(5) == 10
