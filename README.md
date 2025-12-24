# Log Viewer Enhancement

## Approach

The original `log_viewer_original.py` is a simple script that searches for a keyword in a log file using substring matching and returns the matching lines. To enhance it while preserving the exact matching semantics, I refactored the code into a modular architecture with separate responsibilities:

- `reader.py`: Handles file reading.
- `searcher.py`: Performs the search and structures the results.
- `formatters/`: Contains different output formatters (text, JSON, pretty).

The core search logic remains identical: case-sensitive substring match, returning raw lines without trailing newlines.

## Architecture

```
log_viewer/
├── __init__.py
├── reader.py          # File reading utility
├── searcher.py        # Core search logic and result structuring
└── formatters/
    ├── __init__.py
    ├── text.py        # Structured plain text output
    ├── json_fmt.py    # JSON output
    └── pretty.py      # ANSI-colored console output

tests/
├── __init__.py
├── test_architecture.py     # Checks modular structure
├── test_semantic_equivalence.py  # Ensures matching lines are identical
└── test_outputs.py          # Validates output formats and summary

examples/
└── sample.log         # Deterministic sample log for testing

run_tests.py           # Test runner
README.md              # This file
```

## API

The enhanced tool exposes:

```python
from log_viewer.searcher import search

report = search(path, keyword, context=0)
# Returns dict with 'results' and 'summary'
```

Formatters:

```python
from log_viewer.formatters.text import format
output = format(report)
```

## How to Run Tests

```bash
python run_tests.py
```

This will discover and run all tests in the `tests/` directory using Python's unittest framework.

## Before/After Comparison

### Original Tool Output

Running `python log_viewer_original.py examples/sample.log keyword`:

```
matches: 4
2023-01-01 10:00:00 INFO This is a log with keyword in it.
2023-01-02 12:00:00 ERROR Found keyword here again.
2023-01-02 13:00:00 WARN No keyword.
2023-01-03 14:00:00 INFO keyword at the end.
```

### Enhanced Tool Output (Text Format)

```python
from log_viewer.searcher import search
from log_viewer.formatters.text import format

report = search('examples/sample.log', 'keyword', context=1)
print(format(report))
```

Output:

```
Summary:
  Matches: 4
  Total Lines: 5
  Earliest Timestamp: 2023-01-01T10:00:00
  Latest Timestamp: 2023-01-03T14:00:00

Results:
Line 1: 2023-01-01 10:00:00 INFO This is a log with **keyword** in it.
  Context after:
    2023-01-01 11:00:00 DEBUG Another line without the word.

Line 3: 2023-01-02 12:00:00 ERROR Found **keyword** here again.
  Context before:
    2023-01-01 11:00:00 DEBUG Another line without the word.
  Context after:
    2023-01-02 13:00:00 WARN No keyword.

Line 4: 2023-01-02 13:00:00 WARN No **keyword**.
  Context before:
    2023-01-02 12:00:00 ERROR Found keyword here again.
  Context after:
    2023-01-03 14:00:00 INFO keyword at the end.

Line 5: 2023-01-03 14:00:00 INFO **keyword** at the end.
  Context before:
    2023-01-02 13:00:00 WARN No keyword.
```

### Enhanced Tool Output (JSON Format)

```python
from log_viewer.formatters.json_fmt import format
print(format(report))
```

Output (abbreviated):

```json
{
  "results": [
    {
      "line_number": 1,
      "line": "2023-01-01 10:00:00 INFO This is a log with keyword in it.",
      "highlighted": "2023-01-01 10:00:00 INFO This is a log with **keyword** in it.",
      "context_before": [],
      "context_after": ["2023-01-01 11:00:00 DEBUG Another line without the word."],
      "timestamp": "2023-01-01T10:00:00"
    },
    {
      "line_number": 3,
      "line": "2023-01-02 12:00:00 ERROR Found keyword here again.",
      "highlighted": "2023-01-02 12:00:00 ERROR Found **keyword** here again.",
      "context_before": ["2023-01-01 11:00:00 DEBUG Another line without the word."],
      "context_after": ["2023-01-02 13:00:00 WARN No keyword."],
      "timestamp": "2023-01-02T12:00:00"
    },
    {
      "line_number": 4,
      "line": "2023-01-02 13:00:00 WARN No keyword.",
      "highlighted": "2023-01-02 13:00:00 WARN No **keyword**.",
      "context_before": ["2023-01-02 12:00:00 ERROR Found keyword here again."],
      "context_after": ["2023-01-03 14:00:00 INFO keyword at the end."],
      "timestamp": "2023-01-02T13:00:00"
    },
    {
      "line_number": 5,
      "line": "2023-01-03 14:00:00 INFO keyword at the end.",
      "highlighted": "2023-01-03 14:00:00 INFO **keyword** at the end.",
      "context_before": ["2023-01-02 13:00:00 WARN No keyword."],
      "context_after": [],
      "timestamp": "2023-01-03T14:00:00"
    }
  ],
  "summary": {
    "matches": 4,
    "total_lines": 5,
    "earliest_timestamp": "2023-01-01T10:00:00",
    "latest_timestamp": "2023-01-03T14:00:00"
  }
}
```

## Improvements

1. **Structured Output**: Results include line numbers, context, and metadata.
2. **Modularity**: Code is split into logical components for better maintainability.
3. **Multiple Formats**: Support for text, JSON, and pretty console output.
4. **Observability**: Summary provides total lines and timestamp ranges.
5. **Testability**: Comprehensive automated tests ensure correctness and equivalence.