import os
from log_viewer_original import search_logs as original_search
from log_viewer import search as enhanced_search


def test_semantic_equivalence():
    sample = os.path.join(os.path.dirname(__file__), "..", "examples", "sample.log")
    sample = os.path.abspath(sample)
    keyword = "ERROR"

    orig = original_search(sample, keyword)
    enhanced = enhanced_search(sample, keyword, context=0)

    # original returns list of raw lines
    assert isinstance(orig, list)

    # summary matches count
    assert enhanced["summary"]["matches"] == len(orig)

    # lines correspond exactly and order preserved
    enhanced_lines = [r["line"] for r in enhanced["results"]]
    assert enhanced_lines == orig
