import os


def test_package_layout_exists():
    base = os.path.join(os.path.dirname(__file__), "..")
    base = os.path.abspath(base)
    assert os.path.exists(os.path.join(base, "log_viewer", "reader.py"))
    assert os.path.exists(os.path.join(base, "log_viewer", "searcher.py"))
    assert os.path.exists(os.path.join(base, "log_viewer", "formatters", "text.py"))
    assert os.path.exists(os.path.join(base, "log_viewer", "formatters", "json_fmt.py"))
    assert os.path.exists(os.path.join(base, "log_viewer", "formatters", "pretty.py"))
