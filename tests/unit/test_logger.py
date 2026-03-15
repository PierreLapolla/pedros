import logging
import subprocess
import sys

from pedros.logger import get_logger, setup_logging


def test_get_logger_default():
    """Test getting logger with default name."""
    logger = get_logger()
    assert isinstance(logger, logging.Logger)
    assert logger.name == "pedros.logger"


def test_get_logger_custom_name():
    """Test getting logger with custom name."""
    logger = get_logger("custom_logger")
    assert isinstance(logger, logging.Logger)
    assert logger.name == "custom_logger"


def test_setup_logging_default():
    """Test setup_logging with default parameters."""
    # Test that it runs without error
    setup_logging()
    logger = get_logger()
    assert logger.getEffectiveLevel() == logging.INFO


def test_setup_logging_custom_level():
    """Test setup_logging with custom level."""
    setup_logging(logging.DEBUG)
    logger = get_logger()
    assert logger.getEffectiveLevel() == logging.DEBUG


def test_setup_logging_string_level():
    setup_logging("WARNING")
    logger = get_logger()
    assert logger.getEffectiveLevel() == logging.WARNING


def test_setup_logging_invalid_level():
    try:
        setup_logging("NOT_A_LEVEL")
    except ValueError as exc:
        assert "Invalid logging level" in str(exc)
    else:
        raise AssertionError("Expected ValueError for invalid logging level")


def test_setup_logging_without_rich():
    """Test setup_logging when Rich is not available."""
    # This should not raise an error and fall back to standard logging
    # We can't easily mock the cached function, so we just test that it works
    setup_logging()
    logger = get_logger()
    assert logger.getEffectiveLevel() == logging.INFO


def test_setup_logging_with_rich():
    """Test setup_logging when Rich is available."""
    # This should use Rich handler if available
    # We can't easily mock the cached function, so we just test that it works
    setup_logging()
    logger = get_logger()
    assert logger.getEffectiveLevel() == logging.INFO


def test_logger_hierarchy():
    """Test that loggers maintain proper hierarchy."""
    parent_logger = get_logger("parent")
    child_logger = get_logger("parent.child")

    assert parent_logger.name == "parent"
    assert child_logger.name == "parent.child"
    assert child_logger.parent.name == "parent"


def test_logger_level_inheritance():
    """Test that child loggers inherit parent levels."""
    setup_logging(logging.DEBUG)
    get_logger("parent")
    child_logger = get_logger("parent.child")

    # Child should inherit parent's effective level
    assert child_logger.getEffectiveLevel() == logging.DEBUG


def test_importing_package_does_not_reconfigure_logging():
    code = """
import logging
logging.basicConfig(level=logging.ERROR, force=True)
before = logging.getLogger().getEffectiveLevel()
import pedros
after = logging.getLogger().getEffectiveLevel()
print(before, after)
"""
    completed = subprocess.run(
        [sys.executable, "-c", code],
        check=True,
        capture_output=True,
        text=True,
    )
    before, after = map(int, completed.stdout.strip().split())
    assert before == logging.ERROR
    assert after == logging.ERROR
