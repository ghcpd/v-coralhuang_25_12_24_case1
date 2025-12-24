# log_viewer/formatters/pretty.py

def format(report):
    """Format report as pretty console output with ANSI coloring."""
    output = []
    output.append("\033[1;34mSummary:\033[0m")  # Blue bold
    output.append(f"  Matches: {report['summary']['matches']}")
    output.append(f"  Total Lines: {report['summary']['total_lines']}")
    output.append(f"  Earliest Timestamp: {report['summary']['earliest_timestamp'] or 'None'}")
    output.append(f"  Latest Timestamp: {report['summary']['latest_timestamp'] or 'None'}")
    output.append("")
    output.append("\033[1;34mResults:\033[0m")
    for res in report['results']:
        # Highlight keyword in red
        pretty_highlighted = res['highlighted'].replace('**', '\033[1;31m', 1).replace('**', '\033[0m', 1)
        output.append(f"Line {res['line_number']}: {pretty_highlighted}")
        if res['context_before']:
            output.append("  \033[1;32mContext before:\033[0m")  # Green
            for cb in res['context_before']:
                output.append(f"    {cb}")
        if res['context_after']:
            output.append("  \033[1;32mContext after:\033[0m")
            for ca in res['context_after']:
                output.append(f"    {ca}")
        output.append("")
    return '\n'.join(output)