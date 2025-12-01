import logging
from typing import Optional


def setup_logging(level: int = logging.INFO) -> None:
    """
    Configure root logging once for the application.
    Call this from your main entry point, not inside libraries.
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
    """
    Get a logger. Use get_logger(__name__) in your modules.
    """
    return logging.getLogger(name or __name__)
