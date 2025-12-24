from __future__ import annotations

import re
from datetime import datetime
from typing import List, Dict, Any, Optional

from .reader import read_lines

TIMESTAMP_PATTERNS = [
    # ISO 8601 at start: 2024-12-24T12:34:56 or 2024-12-24 12:34:56
    r"(?P<ts>\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2}(?:\.\d+)?)",
    # Common log format: 24/Dec/2024:12:34:56
    r"(?P<ts>\d{2}/[A-Za-z]{3}/\d{4}:\d{2}:\d{2}:\d{2})",
]


def _parse_timestamp_from_line(line: str) -> Optional[str]:
    """Attempt to extract a timestamp string from a line and return ISO format.

    Returns None if not found/parseable.
    """
    for pat in TIMESTAMP_PATTERNS:
        m = re.search(pat, line)
        if not m:
            continue
        s = m.group("ts")
        try:
            # try ISO-like parse
            if "T" in s or "-" in s:
                # normalize space -> T for fromisoformat
                s2 = s.replace(" ", "T")
                dt = datetime.fromisoformat(s2)
                return dt.isoformat()
            else:
                # fallback for 24/Dec/2024:12:34:56
                dt = datetime.strptime(s, "%d/%b/%Y:%H:%M:%S")
                return dt.isoformat()
        except Exception:
            return None
    return None


def _highlight(line: str, keyword: str) -> str:
    # deterministic, marks every occurrence with << >> (preserves case)
    return line.replace(keyword, f"<<{keyword}>>")


def search(path: str, keyword: str, context: int = 0) -> Dict[str, Any]:
    """Search `path` for lines containing `keyword` (substring, case-sensitive).

    Returns a report dict with `results` and `summary` keys (see project spec).
    The matching semantics are intentionally identical to the original tool.
    """
    lines = read_lines(path)
    total_lines = len(lines)

    results: List[Dict[str, Any]] = []
    timestamps: List[str] = []

    for idx, line in enumerate(lines, start=1):
        if keyword in line:
            before_start = max(0, idx - 1 - context)
            after_end = min(total_lines, idx + context)
            context_before = lines[before_start: idx - 1]
            context_after = lines[idx: after_end]
            ts = _parse_timestamp_from_line(line)
            if ts:
                timestamps.append(ts)
            results.append(
                {
                    "line_number": idx,
                    "line": line,
                    "highlighted": _highlight(line, keyword),
                    "context_before": context_before,
                    "context_after": context_after,
                    "timestamp": ts,
                }
            )

    earliest = min(timestamps) if timestamps else None
    latest = max(timestamps) if timestamps else None

    summary = {
        "matches": len(results),
        "total_lines": total_lines,
        "earliest_timestamp": earliest,
        "latest_timestamp": latest,
    }

    return {"results": results, "summary": summary}
