"""JSON formatter for log viewer reports."""
import json
from typing import Dict


def format(report: Dict) -> str:
    return json.dumps(report, indent=2, ensure_ascii=False)
