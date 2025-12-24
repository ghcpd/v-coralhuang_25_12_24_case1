"""
JSON formatter for machine-readable output.
"""

import json


def format(report):
    """
    Format search results as JSON.
    
    Args:
        report: dict, search report from searcher.search()
        
    Returns:
        str: formatted JSON output
    """
    return json.dumps(report, indent=2)
