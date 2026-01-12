import logging
from unittest.mock import MagicMock

import pytest

from pedros.decorators.safe import safe


def test_safe_sync_success():
    @safe
    def success():
        return "ok"

    assert success() == "ok"


def test_safe_sync_error_re_raise(caplog):
    @safe(re_raise=True)
    def fail():
        raise ValueError("test error")

    with caplog.at_level(logging.ERROR):
        with pytest.raises(ValueError, match="test error"):
            fail()
        assert "Error in fail: test error" in caplog.text


def test_safe_sync_error_no_re_raise(caplog):
    @safe(re_raise=False)
    def fail():
        raise ValueError("test error")

    with caplog.at_level(logging.ERROR):
        result = fail()
        assert result is None
        assert "Error in fail: test error" in caplog.text


def test_safe_callbacks():
    on_error = MagicMock()
    on_finally = MagicMock()

    @safe(on_error=on_error, on_finally=on_finally, re_raise=False)
    def fail():
        raise ValueError("boom")

    fail()
    on_error.assert_called_once()
    assert isinstance(on_error.call_args[0][0], ValueError)
    on_finally.assert_called_once()


def test_safe_finally_only():
    on_finally = MagicMock()

    @safe(on_finally=on_finally)
    def success():
        return 1

    assert success() == 1
    on_finally.assert_called_once()


@pytest.mark.asyncio
async def test_safe_async_success():
    @safe
    async def success():
        return "async ok"

    assert await success() == "async ok"


@pytest.mark.asyncio
async def test_safe_async_error(caplog):
    @safe(re_raise=False)
    async def fail():
        raise RuntimeError("async fail")

    with caplog.at_level(logging.ERROR):
        result = await fail()
        assert result is None
        assert "Error in fail: async fail" in caplog.text


def test_safe_method():
    class Test:
        @safe(re_raise=False)
        def method(self):
            raise ValueError("method fail")

    t = Test()
    assert t.method() is None


@pytest.mark.asyncio
async def test_safe_async_method():
    class Test:
        @safe(re_raise=False)
        async def method(self):
            raise ValueError("async method fail")

    t = Test()
    assert await t.method() is None


def test_safe_different_log_level(caplog):
    @safe(log_level="WARNING", re_raise=False)
    def fail():
        raise ValueError("warn me")

    with caplog.at_level(logging.WARNING):
        fail()
        assert "Error in fail: warn me" in caplog.text
        # Check it's not ERROR level but WARNING
        for record in caplog.records:
            if "warn me" in record.message:
                assert record.levelno == logging.WARNING


def test_safe_no_log(caplog):
    @safe(log_level=None, re_raise=False)
    def fail():
        raise ValueError("silent fail")

    with caplog.at_level(logging.DEBUG):
        fail()
        assert "silent fail" not in caplog.text


def test_safe_catch_specific():
    @safe(catch=ValueError, re_raise=False)
    def fail():
        raise ValueError("catch me")

    assert fail() is None


def test_safe_catch_specific_re_raise_others():
    @safe(catch=ValueError, re_raise=False)
    def fail():
        raise TypeError("don't catch me")

    with pytest.raises(TypeError):
        fail()


def test_safe_catch_tuple():
    @safe(catch=(ValueError, TypeError), re_raise=False)
    def fail_val():
        raise ValueError("val")

    @safe(catch=(ValueError, TypeError), re_raise=False)
    def fail_type():
        raise TypeError("type")

    assert fail_val() is None
    assert fail_type() is None


def test_safe_none_log_string(caplog):
    @safe(log_level="NONE", re_raise=False)
    def fail():
        raise ValueError("silent fail")

    with caplog.at_level(logging.DEBUG):
        fail()
        assert "silent fail" not in caplog.text
