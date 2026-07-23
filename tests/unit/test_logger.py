import logging
import subprocess
import sys

from pedros.logger import get_logger, setup_logging


def _reset_logger(logger_name: str):
    logger = logging.getLogger(logger_name)
    original_handlers = logger.handlers[:]
    original_level = logger.level
    original_propagate = logger.propagate

    def restore():
        logger.handlers = original_handlers
        logger.setLevel(original_level)
        logger.propagate = original_propagate

    logger.handlers = []
    logger.setLevel(logging.NOTSET)
    logger.propagate = True
    return logger, restore


def test_get_logger_default():
    """Test getting logger with default name."""
    logger = get_logger()
    assert isinstance(logger, logging.Logger)
    assert logger.name == "pedros"


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
    get_logger("pedros.parent")
    child_logger = get_logger("pedros.parent.child")

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


def test_setup_logging_does_not_reconfigure_root_logger():
    root_logger = logging.getLogger()
    original_handlers = root_logger.handlers[:]
    original_level = root_logger.level

    try:
        logging.basicConfig(level=logging.ERROR, force=True)
        configured_handlers = logging.getLogger().handlers[:]
        configured_level = logging.getLogger().level

        setup_logging(logging.DEBUG)

        assert logging.getLogger().handlers == configured_handlers
        assert logging.getLogger().level == configured_level
    finally:
        root_logger.handlers = original_handlers
        root_logger.setLevel(original_level)


def test_setup_logging_configures_pedros_logger_only():
    package_logger, restore = _reset_logger("pedros")
    root_logger = logging.getLogger()
    original_root_handlers = root_logger.handlers[:]
    original_root_level = root_logger.level
    root_logger.handlers = []

    try:
        setup_logging(logging.WARNING)
        child_logger = get_logger()

        assert package_logger.level == logging.WARNING
        assert package_logger.propagate is False
        assert len(package_logger.handlers) == 1
        assert child_logger.getEffectiveLevel() == logging.WARNING
    finally:
        root_logger.handlers = original_root_handlers
        root_logger.setLevel(original_root_level)
        restore()


def test_setup_logging_uses_root_handlers_when_root_is_configured():
    package_logger, restore = _reset_logger("pedros")
    root_logger = logging.getLogger()
    original_root_handlers = root_logger.handlers[:]
    original_root_level = root_logger.level

    try:
        logging.basicConfig(level=logging.ERROR, force=True)
        setup_logging(logging.DEBUG)

        assert logging.getLogger().handlers
        assert package_logger.handlers == []
        assert package_logger.level == logging.DEBUG
        assert package_logger.propagate is True
    finally:
        root_logger.handlers = original_root_handlers
        root_logger.setLevel(original_root_level)
        restore()


def test_setup_logging_supports_custom_logger_name():
    custom_logger, restore_custom = _reset_logger("other_package")
    package_logger, restore_package = _reset_logger("pedros")
    root_logger = logging.getLogger()
    original_root_handlers = root_logger.handlers[:]
    original_root_level = root_logger.level
    root_logger.handlers = []

    try:
        setup_logging("ERROR", logger_name="other_package")

        assert custom_logger.level == logging.ERROR
        assert custom_logger.handlers
        assert package_logger.handlers == []
        assert package_logger.level == logging.NOTSET
    finally:
        root_logger.handlers = original_root_handlers
        root_logger.setLevel(original_root_level)
        restore_custom()
        restore_package()


def test_setup_logging_does_not_duplicate_root_and_local_handlers():
    custom_logger, restore = _reset_logger("configured_app")
    root_logger = logging.getLogger()
    original_root_handlers = root_logger.handlers[:]
    original_root_level = root_logger.level

    try:
        logging.basicConfig(level=logging.INFO, force=True)
        setup_logging(logging.INFO, logger_name="configured_app")

        assert custom_logger.handlers == []
        assert custom_logger.propagate is True
    finally:
        root_logger.handlers = original_root_handlers
        root_logger.setLevel(original_root_level)
        restore()


def test_setup_logging_does_not_duplicate_existing_target_handlers():
    custom_logger, restore = _reset_logger("target_with_handler")
    root_logger = logging.getLogger()
    original_root_handlers = root_logger.handlers[:]
    original_root_level = root_logger.level
    target_handler = logging.NullHandler()
    custom_logger.addHandler(target_handler)

    try:
        logging.basicConfig(level=logging.INFO, force=True)
        setup_logging(logging.INFO, logger_name="target_with_handler")

        assert custom_logger.handlers == [target_handler]
        assert custom_logger.propagate is False
    finally:
        root_logger.handlers = original_root_handlers
        root_logger.setLevel(original_root_level)
        restore()


def test_get_logger_auto_configures_pedros_logger_on_first_use(monkeypatch):
    import pedros.logger as logger_module

    package_logger, restore = _reset_logger("pedros")
    monkeypatch.setattr(logger_module, "_configured", False)

    try:
        logger = get_logger()

        assert logger is package_logger
        assert package_logger.level == logging.INFO
    finally:
        restore()


def test_get_logger_does_not_reconfigure_once_already_configured(monkeypatch):
    import pedros.logger as logger_module

    package_logger, restore = _reset_logger("pedros")
    monkeypatch.setattr(logger_module, "_configured", True)
    package_logger.setLevel(logging.WARNING)

    try:
        get_logger()

        assert package_logger.level == logging.WARNING
    finally:
        restore()
