# Enhanced Log Viewer

Summary
- Small, modular enhancement of the primitive `log_viewer_original.py`.
- Preserves original matching semantics (substring, case-sensitive, line order).
- Adds structured results, multiple formatters, observability, and tests.

Architecture
- `log_viewer/reader.py`  — file IO (reads lines)
- `log_viewer/searcher.py` — core search logic, timestamp extraction, report shape
- `log_viewer/formatters/` — pure formatters: `text.py`, `json_fmt.py`, `pretty.py`
- `examples/sample.log` — deterministic sample log used by tests
- `tests/` — automated acceptance tests
- `run_tests.py` — one-click test runner (pytest preferred)

Key features
- Results include line number, raw line, `highlighted` (<<keyword>>), context_before/after, and optional parsed timestamp
- Summary contains `matches`, `total_lines`, `earliest_timestamp`, `latest_timestamp`
- Formatters are pure functions: `format(report: dict) -> str`
- Modular layout for extensibility and easier testing

How to run tests
1. python run_tests.py

Notes
- Matching semantics unchanged: every line matches iff `keyword` is a substring (case-sensitive).
- Timestamp parsing is best-effort (ISO-8601 and common log formats). If not parseable, `timestamp` is `None`.
