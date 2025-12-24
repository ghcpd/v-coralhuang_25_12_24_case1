"""Searcher implementation preserving original matching semantics.
Exposes search(path, keyword, context=0) -> dict
"""
from __future__ import annotations
import re
from datetime import datetime, timezone
from .reader import read_lines, total_lines
from typing import Optional, List, Dict, Any

# Timestamp regexes: ISO and space-separated
ISO_RE = re.compile(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z?")
SPACE_RE = re.compile(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}")


def _parse_timestamp_from_line(line: str) -> Optional[datetime]:
    m = ISO_RE.search(line)
    if m:
        txt = m.group(0)
        # normalize Z
        if txt.endswith("Z"):
            txt = txt[:-1] + "+00:00"
        try:
            dt = datetime.fromisoformat(txt)
            # normalize to UTC-naive for consistent comparisons
            if dt.tzinfo is not None:
                dt = dt.astimezone(timezone.utc).replace(tzinfo=None)
            return dt
        except Exception:
            pass
    m = SPACE_RE.search(line)
    if m:
        txt = m.group(0)
        try:
            # parsed as naive local time; treat as UTC-naive for summary consistency
            return datetime.strptime(txt, "%Y-%m-%d %H:%M:%S")
        except Exception:
            pass
    return None


def search(path: str, keyword: str, context: int = 0) -> Dict[str, Any]:
    """Search log file for substring `keyword` preserving original semantics.

    Returns structured report dictionary with `results` and `summary`.
    """
    lines = read_lines(path)

    results: List[Dict[str, Any]] = []

    # Collect timestamps across all lines for summary
    timestamps: List[datetime] = []
    for line in lines:
        t = _parse_timestamp_from_line(line)
        if t:
            timestamps.append(t)

    for idx, raw in enumerate(lines):
        # exact substring match (case-sensitive)
        if keyword in raw:
            before = lines[max(0, idx - context) : idx]
            after = lines[idx + 1 : idx + 1 + context]
            highlighted = raw.replace(keyword, f"<<{keyword}>>")
            ts = _parse_timestamp_from_line(raw)
            results.append(
                {
                    "line_number": idx + 1,
                    "line": raw,
                    "highlighted": highlighted,
                    "context_before": before,
                    "context_after": after,
                    "timestamp": ts.isoformat() if ts else None,
                }
            )

    summary = {
        "matches": len(results),
        "total_lines": total_lines(path),
        "earliest_timestamp": min(timestamps).isoformat() if timestamps else None,
        "latest_timestamp": max(timestamps).isoformat() if timestamps else None,
    }

    return {"results": results, "summary": summary}
