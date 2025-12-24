import os
from log_viewer import searcher
from log_viewer_original import search_logs


def test_semantic_equivalence():
    path = os.path.join(os.path.dirname(__file__), "..", "examples", "sample.log")
    path = os.path.normpath(path)
    keyword = "keyword"

    original = search_logs(path, keyword)
    enhanced = searcher.search(path, keyword, context=0)

    # matches count
    assert enhanced["summary"]["matches"] == len(original)

    # matched lines correspond exactly and in order
    enhanced_lines = [r["line"] for r in enhanced["results"]]
    assert enhanced_lines == original
