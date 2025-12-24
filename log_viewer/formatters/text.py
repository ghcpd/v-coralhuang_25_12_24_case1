"""Plain structured text formatter (pure function)."""
from typing import Dict


def format(report: Dict) -> str:
    parts = []
    s = report["summary"]
    parts.append("SUMMARY")
    parts.append(f"matches: {s['matches']}")
    parts.append(f"total_lines: {s['total_lines']}")
    parts.append(f"earliest_timestamp: {s['earliest_timestamp']}")
    parts.append(f"latest_timestamp: {s['latest_timestamp']}")
    parts.append("")
    parts.append("RESULTS")

    for r in report["results"]:
        parts.append(f"Line {r['line_number']}: {r['highlighted']}")
        if r["context_before"]:
            parts.append("  context_before:")
            for cb in r["context_before"]:
                parts.append(f"    {cb}")
        if r["context_after"]:
            parts.append("  context_after:")
            for ca in r["context_after"]:
                parts.append(f"    {ca}")
        parts.append("")

    return "\n".join(parts)
