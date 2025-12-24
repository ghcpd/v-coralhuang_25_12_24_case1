from log_viewer import search
from log_viewer.formatters import text as text_fmt
import os


def test_text_output_contains_headers_and_highlight_and_context():
    sample = os.path.join(os.path.dirname(__file__), "..", "examples", "sample.log")
    sample = os.path.abspath(sample)
    report = search(sample, "ERROR", context=1)
    out = text_fmt.format(report)
    assert "SUMMARY" in out
    assert "RESULTS" in out
    # line numbers
    assert "Line " in out
    # highlighted uses <<keyword>> markers
    assert "<<ERROR>>" in out
    # context lines should be present because we used context=1
    assert "Retrying" in out or "DEBUG" in out
