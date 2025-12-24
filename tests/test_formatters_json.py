from log_viewer import search
from log_viewer.formatters import json_fmt
import json
import os


def test_json_output_structure():
    sample = os.path.join(os.path.dirname(__file__), "..", "examples", "sample.log")
    sample = os.path.abspath(sample)
    report = search(sample, "ERROR", context=0)
    out = json_fmt.format(report)
    loaded = json.loads(out)
    assert "results" in loaded and "summary" in loaded
    # required fields in a result
    r = loaded["results"][0]
    for f in ("line_number", "line", "highlighted", "context_before", "context_after", "timestamp"):
        assert f in r
