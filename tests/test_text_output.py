import os
from log_viewer import searcher
from log_viewer.formatters import text as text_fmt


def test_text_output_contains_headers_and_highlight_and_context():
    path = os.path.join(os.path.dirname(__file__), "..", "examples", "sample.log")
    path = os.path.normpath(path)
    report = searcher.search(path, "keyword", context=1)
    out = text_fmt.format(report)
    assert "Summary" in out
    assert "Results" in out
    # check line numbers
    assert "Line 2:" in out or "Line 4:" in out
    # highlighted should show bold markers
    assert "**keyword**" in out
    # context should be present when context > 0
    assert "Starting process" in out or "Some other line" in out
