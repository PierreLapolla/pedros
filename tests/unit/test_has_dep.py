import importlib

from pedros.has_dep import has_dep


has_dep_module = importlib.import_module("pedros.has_dep")


def test_has_dep_available():
    """Test has_dep with an available module."""
    # Test with a module that should always be available
    result = has_dep("sys")
    assert result is True


def test_has_dep_unavailable():
    """Test has_dep with an unavailable module."""
    # Test with a module that should never be available
    result = has_dep("nonexistent_module_12345")
    assert result is False


def test_has_dep_case_sensitivity():
    """Test that has_dep is case-sensitive."""
    # This tests that the function respects Python's case-sensitive module names
    # Most standard library modules are lowercase
    result_lower = has_dep("sys")
    result_upper = has_dep("SYS")

    assert result_lower is True
    assert result_upper is False


def test_has_dep_with_dots():
    """Test has_dep with dotted module names."""
    # Test with a submodule
    result = has_dep("os.path")
    assert result is True


def test_has_dep_version_exact(monkeypatch):
    """Test has_dep with an exact version requirement."""
    monkeypatch.setattr(has_dep_module, "find_spec", lambda name: object())
    monkeypatch.setattr(has_dep_module.metadata, "version", lambda name: "1.2.3")

    assert has_dep("demo", "1.2.3") is True
    assert has_dep("demo", "1.2.4") is False


def test_has_dep_version_range(monkeypatch):
    """Test has_dep with a version range requirement."""
    monkeypatch.setattr(has_dep_module, "find_spec", lambda name: object())
    monkeypatch.setattr(has_dep_module.metadata, "version", lambda name: "1.5.0")

    assert has_dep("demo", ">=1.2,<2.0") is True
    assert has_dep("demo", ">=1.6,<2.0") is False


def test_has_dep_version_missing_metadata(monkeypatch):
    """Test has_dep when the distribution has no version metadata."""
    monkeypatch.setattr(has_dep_module, "find_spec", lambda name: object())

    def raise_not_found(name):
        raise has_dep_module.metadata.PackageNotFoundError

    monkeypatch.setattr(has_dep_module.metadata, "version", raise_not_found)

    assert has_dep("demo", ">=1.0") is False
