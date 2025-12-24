"""Plain structured text formatter for log viewer reports."""
from typing import Dict


def format(report: Dict) -> str:
    lines = []
    s = report.get("summary", {})
    lines.append("SUMMARY")
    lines.append(f"matches: {s.get('matches')}")
    lines.append(f"total_lines: {s.get('total_lines')}")
    lines.append(f"earliest_timestamp: {s.get('earliest_timestamp')}")
    lines.append(f"latest_timestamp: {s.get('latest_timestamp')}")
    lines.append("")
    lines.append("RESULTS")
    for r in report.get("results", []):
        lines.append(f"Line {r['line_number']}: {r['highlighted']}")
        if r.get("context_before"):
            for cb in r["context_before"]:
                lines.append(f"  - {cb}")
        if r.get("context_after"):
            for ca in r["context_after"]:
                lines.append(f"  - {ca}")
        lines.append("")
    return "\n".join(lines)
