"""Run only the enhanced API + formatters and print outputs (avoids importing
log_viewer_original to prevent module-import issues in some envs).
"""
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
