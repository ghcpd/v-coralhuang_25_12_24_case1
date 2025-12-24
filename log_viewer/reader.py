from typing import List


def read_lines(path: str) -> List[str]:
    """Read a file and return its lines (preserve order).

    This is intentionally simple to keep parity with the original tool.
    """
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        return [ln.rstrip("\n") for ln in f.readlines()]
