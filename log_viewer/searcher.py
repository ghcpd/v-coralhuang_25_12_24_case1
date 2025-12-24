# log_viewer/searcher.py

import re
from datetime import datetime
from .reader import read_lines

def parse_timestamp(line):
    """Parse timestamp from the beginning of the line if possible."""
    match = re.match(r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})', line)
    if match:
        try:
            return datetime.fromisoformat(match.group(1))
        except ValueError:
            return None
    return None

def search(path, keyword, context=0):
    """Search for keyword in log file, return structured results."""
    all_lines = read_lines(path)
    total_lines = len(all_lines)
    results = []
    earliest_ts = None
    latest_ts = None

    for i, line in enumerate(all_lines, 1):
        if keyword in line:
            ts = parse_timestamp(line)
            if ts:
                if earliest_ts is None or ts < earliest_ts:
                    earliest_ts = ts
                if latest_ts is None or ts > latest_ts:
                    latest_ts = ts

            start = max(0, i - 1 - context)
            end = min(len(all_lines), i - 1 + context + 1)
            context_before = all_lines[start:i-1]
            context_after = all_lines[i:end]

            highlighted = line.replace(keyword, f'**{keyword}**')

            results.append({
                'line_number': i,
                'line': line,
                'highlighted': highlighted,
                'context_before': context_before,
                'context_after': context_after,
                'timestamp': ts.isoformat() if ts else None
            })

    summary = {
        'matches': len(results),
        'total_lines': total_lines,
        'earliest_timestamp': earliest_ts.isoformat() if earliest_ts else None,
        'latest_timestamp': latest_ts.isoformat() if latest_ts else None
    }

    return {'results': results, 'summary': summary}