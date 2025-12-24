import os
from log_viewer import searcher
from log_viewer.reader import read_lines
from datetime import datetime


def test_summary_correctness_and_timestamps():
    path = os.path.join(os.path.dirname(__file__), "..", "examples", "sample.log")
    path = os.path.normpath(path)
    report = searcher.search(path, "keyword", context=0)
    summary = report["summary"]

    # total_lines equals actual file line count
    actual_total = len(read_lines(path))
    assert summary["total_lines"] == actual_total

    # matches equals len(results)
    assert summary["matches"] == len(report["results"])

    # timestamps validity
    et = summary["earliest_timestamp"]
    lt = summary["latest_timestamp"]
    if et and lt:
        e = datetime.fromisoformat(et)
        l = datetime.fromisoformat(lt)
        assert e <= l
    else:
        assert et is None and lt is None or isinstance(et, str) or isinstance(lt, str)
