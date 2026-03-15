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


def setup_logging(level: int | str = logging.INFO) -> None:
    """
    Configure the application's logging behavior.

    This function attempts to use Rich's ``RichHandler`` for enhanced,
    colorful, and trace-friendly logging. If Rich is not installed,
    it silently falls back to Python's standard logging configuration.
    See more about Rich (https://pypi.org/project/rich/).

    :param level: Logging level to use as integer or string name. Defaults to ``logging.INFO``.
    :return: None
    """
    fmt = None
    datefmt = None
    handlers = []

    if has_dep("rich"):
        from rich.logging import RichHandler

        handler = RichHandler(rich_tracebacks=True)
        handlers.append(handler)
    else:
        fmt = "%(asctime)s | %(levelname)-8s | %(message)s"
        datefmt = "%Y-%m-%d %H:%M:%S"
        handler = logging.StreamHandler()
        handlers.append(handler)

    if isinstance(level, int):
        normalized_level = level
    elif isinstance(level, str):
        normalized_level = _LOG_LEVEL_NAME_TO_VALUE.get(level.strip().upper())
        if normalized_level is None:
            raise ValueError(f"Invalid logging level '{level}'.")
    else:
        raise ValueError(f"Invalid logging level '{level}'.")

    logging.basicConfig(
        level=normalized_level,
        format=fmt,
        datefmt=datefmt,
        handlers=handlers,
        force=True,
    )


def get_logger(name: Optional[str] = None) -> logging.Logger:
    """
    Return a logger instance.

    If no name is provided, the module's ``__name__`` is used.

    :param name: Name of the logger. If ``None``, defaults to the current module.
    :return: A configured logger instance.
    """
    return logging.getLogger(name or __name__)
