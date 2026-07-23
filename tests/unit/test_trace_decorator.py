import pytest

from pedros.decorators.trace import trace


def test_trace_sync():
    @trace
    def func(x, y):
        return x + y

    assert func(1, 2) == 3
    assert func.__name__ == "func"


@pytest.mark.asyncio
async def test_trace_async():
    @trace
    async def func(x, y):
        return x + y

    assert await func(1, 2) == 3
    assert func.__name__ == "func"


def test_trace_logs_call_and_result(caplog):
    @trace(log_level="DEBUG")
    def func(x, y):
        return x + y

    with caplog.at_level("DEBUG", logger="pedros"):
        assert func(1, 2) == 3

    assert "Calling func" in caplog.text
    assert "returned 3" in caplog.text
    assert any(record.name == "pedros" for record in caplog.records)


def test_trace_logs_error_and_reraises(caplog):
    @trace(log_level="DEBUG")
    def func():
        raise ValueError("boom")

    with caplog.at_level("DEBUG", logger="pedros"):
        with pytest.raises(ValueError, match="boom"):
            func()

    assert "func raised ValueError: boom" in caplog.text


@pytest.mark.asyncio
async def test_trace_async_error_and_reraises(caplog):
    @trace(log_level="DEBUG")
    async def func():
        raise RuntimeError("async boom")

    with caplog.at_level("DEBUG", logger="pedros"):
        with pytest.raises(RuntimeError, match="async boom"):
            await func()

    assert "func raised RuntimeError: async boom" in caplog.text


def test_trace_none_log(caplog):
    @trace(log_level="NONE")
    def func():
        return True

    with caplog.at_level("DEBUG"):
        assert func()
        assert "Calling func" not in caplog.text


def test_trace_no_args():
    @trace()
    def success():
        return "ok"

    assert success() == "ok"
    assert success.__name__ == "success"


@pytest.mark.asyncio
async def test_trace_async_no_args():
    @trace()
    async def success():
        return "async ok"

    assert await success() == "async ok"


def test_trace_invalid_log_level():
    with pytest.raises(ValueError, match="Invalid log level"):

        @trace(log_level="INVALID")
        def func():
            return True

        func()


def test_trace_method():
    class MyClass:
        @trace
        def method(self, value):
            return value * 2

    obj = MyClass()
    assert obj.method(5) == 10
    assert obj.method.__name__ == "method"


@pytest.mark.asyncio
async def test_trace_async_method():
    class MyClass:
        @trace
        async def method(self, value):
            return value * 2

    obj = MyClass()
    assert await obj.method(5) == 10


def test_trace_does_not_suppress_exception():
    @trace
    def func():
        raise KeyError("not caught")

    with pytest.raises(KeyError):
        func()
