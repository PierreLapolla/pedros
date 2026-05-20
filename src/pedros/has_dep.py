from __future__ import annotations

import re
from importlib import metadata
from importlib.util import find_spec
from typing import Final

__all__ = ["has_dep"]

_VERSION_RE: Final[re.Pattern[str]] = re.compile(
    r"^(?P<release>\d+(?:\.\d+)*)"
    r"(?:(?:[-_.]?)(?P<pre_tag>a|alpha|b|beta|rc|c)(?P<pre_num>\d+)?)?"
    r"(?:(?:[-_.]?)(?P<post_tag>post|rev|r)(?P<post_num>\d+)?)?"
    r"(?:(?:[-_.]?)(?P<dev_tag>dev)(?P<dev_num>\d+)?)?$",
    re.IGNORECASE,
)

_SPEC_RE: Final[re.Pattern[str]] = re.compile(
    r"^(?P<op>==|!=|>=|<=|>|<)?\s*(?P<version>.+?)\s*$"
)


def _get_installed_version(name: str) -> str | None:
    try:
        return metadata.version(name)
    except metadata.PackageNotFoundError:
        return None


def _version_key(version: str) -> tuple[tuple[int, ...], tuple[int, int, int]]:
    """
    Build a comparable key for a version string.

    The parser is intentionally small and stdlib-only. It handles common numeric
    releases plus the usual pre/dev/post markers used by Python packages.
    """
    normalized = version.strip()
    match = _VERSION_RE.fullmatch(normalized)
    if match is None:
        return ((), (0, 0, 0))

    release_parts = [int(part) for part in match.group("release").split(".")]
    while len(release_parts) > 1 and release_parts[-1] == 0:
        release_parts.pop()
    release = tuple(release_parts)

    pre_tag = match.group("pre_tag")
    pre_num = int(match.group("pre_num") or 0)
    post_tag = match.group("post_tag")
    post_num = int(match.group("post_num") or 0)
    dev_tag = match.group("dev_tag")
    dev_num = int(match.group("dev_num") or 0)

    if dev_tag:
        stage = (-1, 0, dev_num)
    elif pre_tag:
        stage_order = {"a": 0, "alpha": 0, "b": 1, "beta": 1, "rc": 2, "c": 2}
        stage = (0, stage_order[pre_tag.lower()], pre_num)
    elif post_tag:
        stage = (2, 0, post_num)
    else:
        stage = (1, 0, 0)

    return release, stage


def _compare_versions(installed: str, expected: str) -> int:
    installed_key = _version_key(installed)
    expected_key = _version_key(expected)

    if installed_key == expected_key:
        return 0
    if installed_key < expected_key:
        return -1
    return 1


def _matches_version(installed: str, requirement: str) -> bool:
    requirement = requirement.strip()
    if not requirement:
        return True

    clauses = [part.strip() for part in requirement.split(",") if part.strip()]
    if not clauses:
        return True

    for clause in clauses:
        match = _SPEC_RE.fullmatch(clause)
        if match is None:
            return False

        op = match.group("op") or "=="
        expected = match.group("version")
        cmp_result = _compare_versions(installed, expected)

        if op == "==" and cmp_result != 0:
            return False
        if op == "!=" and cmp_result == 0:
            return False
        if op == ">=" and cmp_result < 0:
            return False
        if op == ">" and cmp_result <= 0:
            return False
        if op == "<=" and cmp_result > 0:
            return False
        if op == "<" and cmp_result >= 0:
            return False

    return True


def has_dep(name: str, version: str | None = None) -> bool:
    """
    Check if a specified dependency is available on the system.

    This function verifies the availability of a Python module or package by
    checking if it can be located using the Python runtime's import system.
    When a version constraint is provided, the dependency must also satisfy the
    constraint using installed distribution metadata.

    :param name: The name of the dependency to check.
    :type name: str
    :param version: Optional exact version or comma-separated range constraint.
    :type version: str | None
    :return: True if the dependency is available, False otherwise.
    :rtype: bool
    """
    if find_spec(name) is None:
        return False

    if version is None:
        return True

    installed_version = _get_installed_version(name)
    if installed_version is None:
        return False

    return _matches_version(installed_version, version)
