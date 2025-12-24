"""JSON formatter (pure function)."""
import json
from typing import Dict


def format(report: Dict) -> str:
    # Do not mutate the report; ensure all datetimes are serialisable (they're strings)
    return json.dumps(report, indent=2, ensure_ascii=False)
