from __future__ import annotations

from typing import (
    TYPE_CHECKING,
    Any,
    Iterable,
    Literal,
    TypeVar,
    Union,
    overload,
    cast,
)

from pedros.dependency_check import check_dependency
from pedros.logger import get_logger

T = TypeVar("T")
Backend = Literal["auto", "rich", "tqdm", "none"]

if TYPE_CHECKING and check_dependency("tqdm"):
    from tqdm.std import tqdm as Tqdm
else:
    Tqdm = Any


@overload
def progbar(iterable: Iterable[T], *args: Any, backend: Literal["none"], **kwargs: Any) -> Iterable[T]: ...
@overload
def progbar(iterable: Iterable[T], *args: Any, backend: Literal["rich"], **kwargs: Any) -> Iterable[T]: ...
@overload
def progbar(iterable: Iterable[T], *args: Any, backend: Literal["tqdm"], **kwargs: Any) -> Tqdm[T]: ...
@overload
def progbar(iterable: Iterable[T], *args: Any, backend: Literal["auto"] = "auto", **kwargs: Any) -> Union[Iterable[T], Tqdm[T]]: ...


def progbar(
    iterable: Iterable[T],
    *args: Any,
    backend: str = "auto",
    **kwargs: Any,
) -> Union[Iterable[T], Tqdm[T]]:
    """
    Provides a utility function for wrapping an iterable with a progress bar, supporting
    multiple backends. The choice of backend can be explicitly specified or automatically
    determined based on library availability. The supported backends include "rich",
    "tqdm", "none", and "auto".

    The function is designed to warn the user if an invalid backend is provided or if
    the required dependencies for a specific backend are missing. In such cases, a
    fallback mechanism ensures the function operates without disruption.

    Supported functionality includes customizable progress bar descriptions and other
    backend-specific configurations through keyword arguments.

    :param iterable: The input iterable to be wrapped with a progress bar.
    :param args: Additional positional arguments to customize the behavior of the
        selected backend.
    :param backend: Specifies the progress bar backend to use. Options are "auto",
        "rich", "tqdm", or "none". Defaults to "auto".
    :param kwargs: Additional keyword arguments that are passed directly to the
        specified backend for further customization.
    :return: If a progress bar backend is applied, an iterable or an instance based on
        the backend-specific implementation is returned. Otherwise, the original iterable
        is returned.
    """
    logger = get_logger()

    allowed = {"auto", "rich", "tqdm", "none"}
    if backend not in allowed:
        logger.warning(f"Invalid backend '{backend}'. Using 'auto' instead.")
        backend = "auto"

    backend_lit = cast(Backend, backend)

    description = kwargs.get("description")

    def _rich(it: Iterable[T]) -> Iterable[T]:
        from rich.progress import track
        return track(it, *args, **kwargs)

    def _tqdm(it: Iterable[T]) -> Tqdm[T]:
        from tqdm import tqdm
        if description and "desc" not in kwargs:
            local_kwargs = dict(kwargs)
            local_kwargs["desc"] = local_kwargs.pop("description")
        else:
            local_kwargs = kwargs
        return tqdm(it, *args, **local_kwargs)

    if backend_lit == "none":
        return iterable

    if backend_lit == "rich":
        if not check_dependency("rich"):
            logger.warning("backend='rich' requested but 'rich' is not installed. Falling back to 'none'.")
            return iterable
        return _rich(iterable)

    if backend_lit == "tqdm":
        if not check_dependency("tqdm"):
            logger.warning("backend='tqdm' requested but 'tqdm' is not installed. Falling back to 'none'.")
            return iterable
        return _tqdm(iterable)

    # auto
    if check_dependency("rich"):
        return _rich(iterable)
    if check_dependency("tqdm"):
        return _tqdm(iterable)

    logger.warning("No progress bar library found. Install either 'rich' or 'tqdm'.")
    return iterable
