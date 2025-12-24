"""Pretty console formatter with simple ANSI coloring."""
import re
from typing import Dict

_HL_RE = re.compile(r"<<(.+?)>>")

ANSI_BOLD = "\x1b[1m"
ANSI_RESET = "\x1b[0m"
ANSI_HL = "\x1b[31m"  # red


def _color_highlight(text: str) -> str:
    return _HL_RE.sub(lambda m: f"{ANSI_HL}{m.group(1)}{ANSI_RESET}", text)


def format(report: Dict) -> str:
    lines = []
    lines.append(f"{ANSI_BOLD}Summary{ANSI_RESET}")
    lines.append("-------")
    s = report["summary"]
    lines.append(f"matches: {s['matches']}")
    lines.append(f"total_lines: {s['total_lines']}")
    lines.append(f"earliest_timestamp: {s['earliest_timestamp']}")
    lines.append(f"latest_timestamp: {s['latest_timestamp']}")
    lines.append("")
    lines.append(f"{ANSI_BOLD}Results{ANSI_RESET}")
    lines.append("-------")

    for r in report["results"]:
        lines.append(f"Line {r['line_number']}:")
        for cb in r["context_before"]:
            lines.append(f"  {cb}")
        lines.append(f"  {_color_highlight(r['highlighted'])}")
        for ca in r["context_after"]:
            lines.append(f"  {ca}")
        lines.append("")
    return "\n".join(lines)
