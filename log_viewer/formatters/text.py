"""Plain structured text formatter."""
from typing import Dict


def format(report: Dict) -> str:
    lines = []
    lines.append("Summary")
    lines.append("-------")
    s = report["summary"]
    lines.append(f"matches: {s['matches']}")
    lines.append(f"total_lines: {s['total_lines']}")
    lines.append(f"earliest_timestamp: {s['earliest_timestamp']}")
    lines.append(f"latest_timestamp: {s['latest_timestamp']}")
    lines.append("")
    lines.append("Results")
    lines.append("-------")

    for r in report["results"]:
        lines.append(f"Line {r['line_number']}:")
        # context before
        for cb in r["context_before"]:
            lines.append(f"  {cb}")
        # Show highlighted with **bold** markers
        display = r["highlighted"].replace("<<", "**").replace(">>", "**")
        lines.append(f"  {display}")
        for ca in r["context_after"]:
            lines.append(f"  {ca}")
        lines.append("")

    return "\n".join(lines)
