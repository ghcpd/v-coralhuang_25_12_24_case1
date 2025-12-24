"""Reader utilities for log viewer."""

def read_lines(path):
    """Read file and return list of lines without trailing newline characters."""
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        lines = f.readlines()
    return [l.rstrip("\n") for l in lines]


def total_lines(path):
    return len(read_lines(path))
