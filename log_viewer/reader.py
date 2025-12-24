"""Responsible for file I/O (kept tiny for testability)."""
from typing import List


def read_lines(path: str) -> List[str]:
    """Return list of raw lines as read from the file (including trailing newlines).

    This mirrors the behaviour of the original tool so matching semantics remain
    identical when the searcher applies substring matching.
    """
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        return f.readlines()
