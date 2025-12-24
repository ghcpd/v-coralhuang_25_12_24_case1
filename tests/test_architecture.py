import os
import pkgutil
import importlib
from pathlib import Path


def test_package_has_multiple_files():
    root = Path(__file__).parent.parent / "log_viewer"
    py_files = list(root.glob("*.py"))
    assert len(py_files) >= 2


def test_formatters_dir_exists():
    fmt_dir = Path(__file__).parent.parent / "log_viewer" / "formatters"
    assert fmt_dir.exists() and fmt_dir.is_dir()
    files = list(fmt_dir.glob("*.py"))
    assert len(files) >= 1


def test_core_logic_not_single_file():
    # ensure searcher and reader are separate
    import log_viewer.searcher as s
    import log_viewer.reader as r
    assert hasattr(s, "search")
    assert hasattr(r, "read_lines")
