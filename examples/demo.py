"""Small demo that prints original vs enhanced outputs for the sample log."""
from __future__ import annotations

import json
import log_viewer_original as original
from log_viewer import search
from log_viewer.formatters import text, json_fmt, pretty


def run():
    p = "examples/sample.log"
    k = "ERROR"

    print("--- original tool output ---")
    orig = original.search_logs(p, k)
    print("matches:", len(orig))
    for l in orig:
        print(l)

    print("\n--- enhanced (text) ---")
    report = search(p, k, context=1)
    print(text.format(report))

    print("\n--- enhanced (json) ---")
    print(json_fmt.format(report))

    print("\n--- enhanced (pretty) ---")
    print(pretty.format(report))


if __name__ == "__main__":
    run()
