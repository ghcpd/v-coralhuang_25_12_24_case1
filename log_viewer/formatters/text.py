"""
Plain text formatter with structure and readability.
"""


def format(report):
    """
    Format search results as structured plain text.
    
    Args:
        report: dict, search report from searcher.search()
        
    Returns:
        str: formatted text output
    """
    lines = []
    summary = report["summary"]
    results = report["results"]
    
    # Summary section
    lines.append("=" * 70)
    lines.append("LOG SEARCH RESULTS")
    lines.append("=" * 70)
    lines.append("")
    lines.append(f"Matches: {summary['matches']}")
    lines.append(f"Total Lines Scanned: {summary['total_lines']}")
    
    if summary['earliest_timestamp']:
        lines.append(f"Earliest Timestamp: {summary['earliest_timestamp']}")
    if summary['latest_timestamp']:
        lines.append(f"Latest Timestamp: {summary['latest_timestamp']}")
    
    lines.append("")
    lines.append("-" * 70)
    lines.append("")
    
    # Results section
    if not results:
        lines.append("No matches found.")
    else:
        for i, result in enumerate(results, 1):
            lines.append(f"Match #{i}")
            lines.append(f"  Line Number: {result['line_number']}")
            lines.append(f"  Timestamp: {result['timestamp'] or 'N/A'}")
            lines.append(f"  Content: {result['line']}")
            lines.append(f"  Highlighted: {result['highlighted']}")
            
            if result['context_before']:
                lines.append("  Context Before:")
                for ctx_line in result['context_before']:
                    lines.append(f"    | {ctx_line}")
            
            if result['context_after']:
                lines.append("  Context After:")
                for ctx_line in result['context_after']:
                    lines.append(f"    | {ctx_line}")
            
            lines.append("")
    
    lines.append("=" * 70)
    
    return "\n".join(lines)
