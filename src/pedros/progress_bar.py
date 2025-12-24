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
            raise ImportError("backend='rich' requested but 'rich' is not installed.")
        return _rich(iterable)

    if backend_lit == "tqdm":
        if not check_dependency("tqdm"):
            raise ImportError("backend='tqdm' requested but 'tqdm' is not installed.")
        return _tqdm(iterable)

    # auto
    if check_dependency("rich"):
        return _rich(iterable)
    if check_dependency("tqdm"):
        return _tqdm(iterable)

    logger.warning("No progress bar library found. Install either 'rich' or 'tqdm'.")
    return iterable
