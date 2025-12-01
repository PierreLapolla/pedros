import logging
from typing import Optional


def setup_logging(level: int = logging.INFO) -> None:
    """Configure the application's logging behavior.

    This function attempts to use `rich`'s `RichHandler` for enhanced,
    colorful, and trace-friendly logging. If `rich` is not installed,
    it falls back to Python's standard logging configuration.

    Args:
        level (int, optional): Logging level to use. Defaults to
            ``logging.INFO``.

    Raises:
        None explicitly. If `rich` is unavailable, the function
        silently falls back to standard logging.
    """
    handler = None

    try:
        from rich.logging import RichHandler

        handler = RichHandler(rich_tracebacks=True)
        handlers = [handler]
        fmt = "%(message)s"
        datefmt = None

    except (ImportError, ModuleNotFoundError):
        handlers = None
        fmt = "%(asctime)s | %(levelname)-8s | %(message)s"
        datefmt = "%Y-%m-%d %H:%M:%S"

    logging.basicConfig(
        level=level,
        format=fmt,
        datefmt=datefmt,
        handlers=handlers,
    )

    logger = logging.getLogger(__name__)
    if handler is None:
        logger.debug("Rich library not found, using standard logging.")


def get_logger(name: Optional[str] = None) -> logging.Logger:
    """Return a logger instance.

    If no name is provided, the module's ``__name__`` is used.

    Args:
        name (str, optional): Name of the logger. If ``None``, defaults
            to the current module name.

    Returns:
        logging.Logger: A logger instance configured through
        ``setup_logging``.
    """
    return logging.getLogger(name or __name__)
