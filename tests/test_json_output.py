import os
import json
from log_viewer import searcher
from log_viewer.formatters import json_fmt


def test_json_output_parses_and_has_required_fields():
    path = os.path.join(os.path.dirname(__file__), "..", "examples", "sample.log")
    path = os.path.normpath(path)
    report = searcher.search(path, "keyword", context=0)
    out = json_fmt.format(report)
    parsed = json.loads(out)
    assert "results" in parsed and "summary" in parsed
    # check required fields in a result
    if parsed["results"]:
        r = parsed["results"][0]
        assert all(k in r for k in ["line_number", "line", "highlighted", "context_before", "context_after", "timestamp"])
