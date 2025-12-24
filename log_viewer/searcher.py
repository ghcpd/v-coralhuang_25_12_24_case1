"""Search logic: preserves original matching semantics and returns a
rich, structured report suitable for formatters and tests.
"""
from __future__ import annotations

from typing import List, Dict, Optional, Any
from datetime import datetime
import re

from .reader import read_lines

_TIMESTAMP_REGEXES = [
    # ISO 8601 (basic subset)
    re.compile(r"(?P<ts>\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z?)"),
    # common: YYYY-MM-DD HH:MM:SS
    re.compile(r"(?P<ts>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})"),
]


def _parse_timestamp_from_line(line: str) -> Optional[datetime]:
    for rx in _TIMESTAMP_REGEXES:
        m = rx.search(line)
        if m:
            s = m.group("ts")
            # try parsing with a couple formats
            for fmt in ("%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M:%S"):
                try:
                    # strip trailing Z if present for the simple ISO case
                    s_clean = s.rstrip("Z")
                    return datetime.strptime(s_clean.split(".")[0], fmt)
                except Exception:
                    continue
    return None


def search(path: str, keyword: str, context: int = 0) -> Dict[str, Any]:
    """Search `path` for `keyword` (case-sensitive substring match).

    Returns a structured report (see project README). The exact set and order
    of matched *raw lines* is preserved from the original implementation.
    """
    lines = read_lines(path)
    total_lines = len(lines)

    results: List[Dict[str, Any]] = []
    timestamps: List[datetime] = []

    for i, raw in enumerate(lines, start=1):
        # preserve original matching semantics: substring (case-sensitive)
        if keyword in raw:
            raw_stripped = raw.rstrip("\n")

            ts = _parse_timestamp_from_line(raw)
            if ts:
                timestamps.append(ts)

            # context slices (keep same stripping behaviour)
            before_start = max(0, i - 1 - context)
            after_end = min(total_lines, i - 1 + context + 1)

            context_before = [l.rstrip("\n") for l in lines[before_start : i - 1]]
            context_after = [l.rstrip("\n") for l in lines[i:after_end]]

            # highlighted: literal marker around exact substring occurrences
            highlighted = raw_stripped.replace(keyword, f"<<{keyword}>>")

            results.append(
                {
                    "line_number": i,
                    "line": raw_stripped,
                    "highlighted": highlighted,
                    "context_before": context_before,
                    "context_after": context_after,
                    "timestamp": ts.isoformat() if ts else None,
                }
            )

    summary = {
        "matches": len(results),
        "total_lines": total_lines,
        "earliest_timestamp": min(timestamps).isoformat() if timestamps else None,
        "latest_timestamp": max(timestamps).isoformat() if timestamps else None,
    }

    return {"results": results, "summary": summary}
