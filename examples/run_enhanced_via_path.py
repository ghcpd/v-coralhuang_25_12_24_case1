"""Wrapper that ensures the repository root is on sys.path, then exercises
the enhanced API. Used by CI/demo where import paths can differ.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from log_viewer import search
from log_viewer.formatters import text, json_fmt, pretty


def run():
    p = "examples/sample.log"
    k = "ERROR"
    report = search(p, k, context=1)

    print("--- enhanced (text) ---")
    print(text.format(report))
    print("\n--- enhanced (json) ---")
    print(json_fmt.format(report))
    print("\n--- enhanced (pretty) ---")
    print(pretty.format(report))


if __name__ == '__main__':
    run()
