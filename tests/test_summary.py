from log_viewer import search
from log_viewer.reader import read_lines
import os


def test_summary_correctness_and_timestamps():
    sample = os.path.join(os.path.dirname(__file__), "..", "examples", "sample.log")
    sample = os.path.abspath(sample)
    lines = read_lines(sample)
    report = search(sample, "ERROR", context=0)

    summary = report["summary"]
    assert summary["total_lines"] == len(lines)
    assert summary["matches"] == len(report["results"])

    # timestamps: if present, earliest <= latest
    if summary["earliest_timestamp"] and summary["latest_timestamp"]:
        assert summary["earliest_timestamp"] <= summary["latest_timestamp"]
