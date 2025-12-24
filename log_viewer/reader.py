"""
Log file reader module.

Responsible for:
- Reading log files line-by-line
- Handling encoding and errors gracefully
- Returning raw lines with metadata
"""

def read_lines(path):
    """
    Read all lines from a log file.
    
    Args:
        path: File path to read
        
    Returns:
        Tuple of (lines, total_count) where:
        - lines: list of strings (with newlines stripped)
        - total_count: int, total lines in file
    """
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        lines = f.readlines()
    
    raw_lines = [line.rstrip("\n") for line in lines]
    return raw_lines, len(raw_lines)
