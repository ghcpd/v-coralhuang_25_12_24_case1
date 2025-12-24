"""
Search and analysis module.

Responsible for:
- Searching logs using the same semantics as original
- Extracting context lines (before/after)
- Parsing timestamps from log lines
- Building the result structure
"""

import re
from datetime import datetime
from .reader import read_lines


def _extract_timestamp(line):
    """
    Try to extract a timestamp from a log line.
    
    Looks for common timestamp patterns:
    - ISO 8601: 2025-12-24T10:30:45
    - Apache/Nginx: 24/Dec/2025:10:30:45
    - Syslog: Dec 24 10:30:45
    
    Args:
        line: str, log line
        
    Returns:
        str: timestamp string if found, else None
    """
    # ISO 8601
    iso_match = re.search(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}', line)
    if iso_match:
        return iso_match.group()
    
    # Apache/Nginx format
    apache_match = re.search(r'\d{2}/\w{3}/\d{4}:\d{2}:\d{2}:\d{2}', line)
    if apache_match:
        return apache_match.group()
    
    # Syslog format
    syslog_match = re.search(r'\w{3}\s+\d{1,2}\s+\d{2}:\d{2}:\d{2}', line)
    if syslog_match:
        return syslog_match.group()
    
    return None


def _highlight_keyword(line, keyword):
    """
    Create a highlighted version of the line.
    
    Args:
        line: str, the log line
        keyword: str, keyword to highlight
        
    Returns:
        str: line with keyword enclosed in [...] markers
    """
    # Simple approach: wrap each occurrence with [...]
    # To preserve exact character positions, we'll do a simple substitution
    return line.replace(keyword, f"[{keyword}]")


def search(path, keyword, context=0):
    """
    Enhanced search function with structured output.
    
    Maintains identical matching semantics to original:
    - Case-sensitive substring matching
    - Returns matched lines in order
    
    Args:
        path: str, file path to search
        keyword: str, substring to search for (case-sensitive)
        context: int, number of context lines before/after (default: 0)
        
    Returns:
        dict with structure:
        {
            "results": [
                {
                    "line_number": int (1-based),
                    "line": str,
                    "highlighted": str,
                    "context_before": list[str],
                    "context_after": list[str],
                    "timestamp": str | None
                },
                ...
            ],
            "summary": {
                "matches": int,
                "total_lines": int,
                "earliest_timestamp": str | None,
                "latest_timestamp": str | None
            }
        }
    """
    lines, total_count = read_lines(path)
    
    results = []
    all_timestamps = []
    
    for idx, line in enumerate(lines):
        # Keep original matching semantics: simple substring match
        if keyword in line:
            # Extract context
            start = max(0, idx - context)
            end = min(len(lines), idx + context + 1)
            
            context_before = lines[start:idx]
            context_after = lines[idx + 1:end]
            
            # Extract and store timestamp
            timestamp = _extract_timestamp(line)
            if timestamp:
                all_timestamps.append(timestamp)
            
            # Build result item
            result_item = {
                "line_number": idx + 1,  # 1-based
                "line": line,
                "highlighted": _highlight_keyword(line, keyword),
                "context_before": context_before,
                "context_after": context_after,
                "timestamp": timestamp
            }
            results.append(result_item)
    
    # Compute summary
    earliest_ts = None
    latest_ts = None
    if all_timestamps:
        earliest_ts = min(all_timestamps)
        latest_ts = max(all_timestamps)
    
    summary = {
        "matches": len(results),
        "total_lines": total_count,
        "earliest_timestamp": earliest_ts,
        "latest_timestamp": latest_ts
    }
    
    return {
        "results": results,
        "summary": summary
    }
