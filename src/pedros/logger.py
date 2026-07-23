from __future__ import annotations

import logging
from typing import Optional

from pedros.has_dep import has_dep

__all__ = ["setup_logging", "get_logger", "normalize_log_level"]

_LOG_LEVEL_NAME_TO_VALUE: dict[str, int] = {
    "CRITICAL": logging.CRITICAL,
    "ERROR": logging.ERROR,
    "WARNING": logging.WARNING,
    "INFO": logging.INFO,
    "DEBUG": logging.DEBUG,
    "NOTSET": logging.NOTSET,
}

_LIBRARY_LOGGER_NAME = "pedros"
_SETUP_HANDLER_ATTR = "_pedros_setup_logging_handler"
_configured = False


def normalize_log_level(log_level: str | None) -> int | None:
    """
    Normalize a textual log level to a numeric logging value.

    :param log_level: A textual level (e.g., ``"INFO"``), ``"NONE"``, or ``None``.
    :return: Numeric level, ``None`` for no logging, or ``None`` when disabled.
    :raises ValueError: If the provided level is unknown.
    """
    if log_level is None:
        return None

    upper = log_level.strip().upper()
    if upper == "NONE":
        return None

    level = _LOG_LEVEL_NAME_TO_VALUE.get(upper)
    if level is None:
        allowed = ", ".join((*_LOG_LEVEL_NAME_TO_VALUE.keys(), "NONE"))
        raise ValueError(f"Invalid log level '{log_level}'. Allowed values: {allowed}.")
    return level


def _create_logging_handler() -> logging.Handler:
    if has_dep("rich"):
        from rich.logging import RichHandler

        handler: logging.Handler = RichHandler(rich_tracebacks=True)
    else:
        handler = logging.StreamHandler()
        handler.setFormatter(
            logging.Formatter(
                fmt="%(asctime)s | %(levelname)-8s | %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
            )
        )

    setattr(handler, _SETUP_HANDLER_ATTR, True)
    return handler


def _normalize_setup_level(level: int | str) -> int:
    if isinstance(level, int):
        return level
    try:
        normalized_level = normalize_log_level(level)
    except ValueError as exc:
        raise ValueError(f"Invalid logging level '{level}'.") from exc
    if normalized_level is not None:
        return normalized_level
    raise ValueError(f"Invalid logging level '{level}'.")


def setup_logging(
    level: int | str = logging.INFO,
    logger_name: str = _LIBRARY_LOGGER_NAME,
    *,
    add_handler: bool | None = None,
    propagate: bool | None = None,
) -> None:
    """
    Configure logging for one logger without reconfiguring root logging.

    This function attempts to use Rich's ``RichHandler`` for enhanced,
    colorful, and trace-friendly logging. If Rich is not installed,
    it silently falls back to Python's standard logging handler.
    See more about Rich (https://pypi.org/project/rich/).

    :param level: Logging level to use as integer or string name. Defaults to ``logging.INFO``.
    :param logger_name: Logger to configure. Defaults to the ``pedros`` package logger.
    :param add_handler: Whether to attach a handler to ``logger_name``. By default,
        a handler is added only when neither root nor the target logger has handlers.
    :param propagate: Whether records should propagate to ancestor loggers. By default,
        propagation is enabled only when root logging is the selected handler path.
    :return: None
    """
    global _configured

    target_logger = logging.getLogger(logger_name)
    normalized_level = _normalize_setup_level(level)
    root_has_handlers = bool(logging.getLogger().handlers)

    target_logger.handlers = [
        handler
        for handler in target_logger.handlers
        if not getattr(handler, _SETUP_HANDLER_ATTR, False)
    ]

    if add_handler is None:
        add_handler = not root_has_handlers and not target_logger.handlers
    if propagate is None:
        propagate = root_has_handlers and not add_handler and not target_logger.handlers

    if add_handler:
        target_logger.addHandler(_create_logging_handler())

    target_logger.setLevel(normalized_level)
    target_logger.propagate = propagate
    _configured = True


def get_logger(name: Optional[str] = None) -> logging.Logger:
    """
    Return a logger instance.

    If no name is provided, the ``pedros`` package logger is returned, and it is
    auto-configured with :func:`setup_logging` defaults on first use if nothing
    has configured it yet. This is what powers ``pedros``'s own decorators and
    utilities without requiring any setup.

    :param name: Name of the logger. If ``None``, defaults to the ``pedros`` logger.
    :return: A configured logger instance.
    """
    if name is None and not _configured:
        setup_logging()
    return logging.getLogger(name or _LIBRARY_LOGGER_NAME)
