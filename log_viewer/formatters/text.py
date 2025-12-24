# log_viewer/formatters/text.py

def format(report):
    """Format report as structured plain text."""
    output = []
    output.append("Summary:")
    output.append(f"  Matches: {report['summary']['matches']}")
    output.append(f"  Total Lines: {report['summary']['total_lines']}")
    output.append(f"  Earliest Timestamp: {report['summary']['earliest_timestamp'] or 'None'}")
    output.append(f"  Latest Timestamp: {report['summary']['latest_timestamp'] or 'None'}")
    output.append("")
    output.append("Results:")
    for res in report['results']:
        output.append(f"Line {res['line_number']}: {res['highlighted']}")
        if res['context_before']:
            output.append("  Context before:")
            for cb in res['context_before']:
                output.append(f"    {cb}")
        if res['context_after']:
            output.append("  Context after:")
            for ca in res['context_after']:
                output.append(f"    {ca}")
        output.append("")
    return '\n'.join(output)