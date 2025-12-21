import pytest
from unittest.mock import patch
from pedros.dependency_check import check_dependency
from pedros.progress_bar import progbar


def test_progbar_with_rich():
    check_dependency.cache_clear()

    with patch("pedros.dependency_check.find_spec") as mock_find:
        mock_find.side_effect = lambda name: True if name == "rich" else None
        track_func = progbar()
        assert track_func.__module__.startswith("rich")


def test_progbar_with_tqdm():
    check_dependency.cache_clear()

    with patch("pedros.dependency_check.find_spec") as mock_find:
        mock_find.side_effect = lambda name: True if name == "tqdm" else None
        track_func = progbar()
        assert track_func.__module__.startswith("tqdm")


def test_progbar_without_dependencies():
    check_dependency.cache_clear()

    with patch("pedros.dependency_check.find_spec") as mock_find:
        mock_find.return_value = None
        track_func = progbar()
        items = [1, 2, 3]
        assert list(track_func(items)) == items
