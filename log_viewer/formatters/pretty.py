"""Pretty console formatter that adds ANSI coloring to the keyword."""
from typing import Dict

# ANSI escapes for highlighting
_HIGHLIGHT_START = "\x1b[1;31m"  # bold red
_HIGHLIGHT_END = "\x1b[0m"


def _color_highlight(text: str, keyword: str) -> str:
    return text.replace(keyword, f"{_HIGHLIGHT_START}{keyword}{_HIGHLIGHT_END}")


def format(report: Dict, keyword: str | None = None) -> str:
    # keyword param is optional; if given, highlight accordingly in displayed lines
    lines = []
    s = report.get("summary", {})
    lines.append("\x1b[1mSUMMARY\x1b[0m")
    lines.append(f"matches: {s.get('matches')}")
    lines.append(f"total_lines: {s.get('total_lines')}")
    lines.append(f"earliest_timestamp: {s.get('earliest_timestamp')}")
    lines.append(f"latest_timestamp: {s.get('latest_timestamp')}")
    lines.append("")
    lines.append("\x1b[1mRESULTS\x1b[0m")
    for r in report.get("results", []):
        display = r['line']
        if keyword:
            display = _color_highlight(display, keyword)
        else:
            # fallback: use already-highlighted field but color markers
            display = r.get('highlighted', r['line']).replace('<<', _HIGHLIGHT_START).replace('>>', _HIGHLIGHT_END)
        lines.append(f"Line {r['line_number']}: {display}")
        lines.append("")
    return "\n".join(lines)
