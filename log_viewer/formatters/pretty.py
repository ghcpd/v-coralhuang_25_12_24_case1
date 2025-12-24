"""Pretty (ANSI-coloured) formatter. Kept pure and deterministic.

This formatter adds ANSI escapes around the highlighted markers produced by the
searcher ("<<keyword>>") so tests can still inspect the underlying data.
"""
from typing import Dict

# simple ANSI helpers
_RED = "\x1b[31;1m"
_BLUE = "\x1b[34m"
_RESET = "\x1b[0m"


def _colour_highlighted(text: str) -> str:
    # the searcher places <<keyword>> markers; replace them with ANSI
    return text.replace("<<", _RED).replace(">>", _RESET)


def format(report: Dict) -> str:
    s = report["summary"]
    parts = []
    parts.append(f"{_BLUE}SUMMARY{_RESET}")
    parts.append(f"matches: {s['matches']}")
    parts.append(f"total_lines: {s['total_lines']}")
    parts.append("")
    parts.append(f"{_BLUE}RESULTS{_RESET}")

    for r in report["results"]:
        parts.append(f"{_BLUE}Line {r['line_number']}{_RESET}: {_colour_highlighted(r['highlighted'])}")
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
