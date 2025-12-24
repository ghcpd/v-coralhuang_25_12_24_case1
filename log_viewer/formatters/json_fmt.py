# log_viewer/formatters/json_fmt.py

import json

def format(report):
    """Format report as JSON."""
    return json.dumps(report, indent=2)