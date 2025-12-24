# Enhanced Log Viewer (exercise)

Summary
- Adds structured results, multiple formatters, observability and tests
- Preserves original matching semantics (case-sensitive substring, order)

Quickstart

- Run the demo:

  python examples/demo.py

- Run the test-suite:

  python run_tests.py

Project layout

- `log_viewer/` — enhanced implementation (modular)
  - `reader.py` — I/O
  - `searcher.py` — core search + report generation
  - `formatters/` — pure formatters (`text`, `json_fmt`, `pretty`)
- `examples/sample.log` — deterministic sample log used by tests
- `tests/` — automated acceptance tests (unittest)
- `run_tests.py` — one-click test runner

Design notes
- Matching semantics are intentionally the same as the original tool so the
  results are provably equivalent (see tests).
- Formatters are pure functions that accept the report dict and return str.
