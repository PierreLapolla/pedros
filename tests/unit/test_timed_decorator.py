from time import sleep

import pytest

from pedros.decorators.timed import timed, _format_time


def test_format_time():
    assert "100.00 ns" in _format_time(1e-7)
    assert "100.00 µs" in _format_time(1e-4)
    assert "100.00 ms" in _format_time(0.1)
    assert "1.23 s" in _format_time(1.234)
    assert "1:1.23 s" in _format_time(61.234)
    assert "1:1:1.23 s" in _format_time(3661.234)


def test_timed_sync():
    @timed
    def func():
        sleep(0.02)
        return True

    assert func()
    assert func.__name__ == "func"


@pytest.mark.asyncio
async def test_timed_async():
    @timed
    async def func():
        sleep(0.02)
        return True

    assert await func()
    assert func.__name__ == "func"


def test_timed_error():
    @timed
    def func():
        sleep(0.02)
        raise ValueError("Intended error raised in test")

    with pytest.raises(ValueError):
        func()


def test_timed_with_params(caplog):
    @timed(log_level="DEBUG")
    def func():
        return True

    with caplog.at_level("DEBUG"):
        assert func()
        assert "func took" in caplog.text


def test_timed_method():
    class MyClass:
        @timed
        def method(self):
            sleep(0.01)
            return True

    obj = MyClass()
    assert obj.method()


@pytest.mark.asyncio
async def test_timed_async_method():
    class MyClass:
        @timed
        async def method(self):
            sleep(0.01)
            return True

    obj = MyClass()
    assert await obj.method()


def test_timed_none_log(caplog):
    @timed(log_level="NONE")
    def func():
        return True

    with caplog.at_level("INFO"):
        assert func()
        assert "func took" not in caplog.text


def test_timed_no_args():
    @timed()
    def success():
        return "ok"

    assert success() == "ok"
    assert success.__name__ == "success"


@pytest.mark.asyncio
async def test_timed_async_no_args():
    @timed()
    async def success():
        return "async ok"

    assert await success() == "async ok"
    assert success.__name__ == "success"
