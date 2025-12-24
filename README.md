# Log Viewer Enhancement

## Overview ✅
This change enhances `log_viewer_original.py` by adding a modular, testable, and observable `log_viewer` package without changing the original matching semantics (substring, case-sensitive, line-order preserved).

## Architecture 🔧
- `log_viewer/reader.py` — file reading helpers
- `log_viewer/searcher.py` — `search(path, keyword, context=0)` returning structured report
- `log_viewer/formatters/text.py` — structured plain text formatter
- `log_viewer/formatters/json_fmt.py` — JSON formatter
- `log_viewer/formatters/pretty.py` — ANSI colored console formatter

## How to run tests 🧪
Run the provided test runner:

```bash
python run_tests.py
```

This uses `pytest` if available, otherwise falls back to `unittest`.

## Demonstration ✨
See `examples/sample.log` for a deterministic sample. The tests include assertions that validate:
- Semantic equivalence with `log_viewer_original.search_logs`
- Output structure for text and JSON formatters
- Summary metadata correctness (matches, total lines, timestamps)

