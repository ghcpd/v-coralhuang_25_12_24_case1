# Enhanced Log Viewer

A structured, modular, and extensible enhancement of the original `log_viewer_original.py` primitive tool.

## Overview

The original tool was simple but limited:
- Unstructured text output
- No metadata or context
- Hard to extend with new features
- Difficult to test programmatically

The enhanced version maintains **identical matching semantics** while providing:
- **Structured results** with line numbers, timestamps, and context
- **Multiple output formats** (plain text, JSON, pretty ANSI colors)
- **Modular architecture** with clear separation of concerns
- **Programmatic API** for integration and testing
- **Comprehensive test suite** validating semantic equivalence

## Architecture

```
log_viewer/
├── __init__.py          # Package metadata
├── reader.py            # File reading (read_lines)
├── searcher.py          # Core search logic (search)
└── formatters/
    ├── __init__.py
    ├── text.py          # Structured text output
    ├── json_fmt.py      # JSON formatter
    └── pretty.py        # ANSI-colored output

examples/
└── sample.log           # Test data

tests/
├── __init__.py
├── test_semantic_equivalence.py   # Matching semantics
├── test_architecture.py           # Modular structure
├── test_output_formats.py         # Formatter correctness
└── test_summary.py               # Metadata accuracy

run_tests.py            # One-click test runner
demo.py                 # Before/after demonstration
```

## Core API

### Search Function

```python
from log_viewer.searcher import search

report = search(
    path="/path/to/logfile",
    keyword="ERROR",
    context=2  # lines before/after match
)
```

**Returns:** Dictionary with structure:
```python
{
    "results": [
        {
            "line_number": 42,           # 1-based
            "line": "2025-12-24T... ERROR ...",
            "highlighted": "2025-12-24T... [ERROR] ...",
            "context_before": [...],
            "context_after": [...],
            "timestamp": "2025-12-24T10:30:45" | None
        },
        ...
    ],
    "summary": {
        "matches": 5,
        "total_lines": 100,
        "earliest_timestamp": "2025-12-24T08:15:23" | None,
        "latest_timestamp": "2025-12-24T08:22:15" | None
    }
}
```

### Formatters

Each formatter is a pure function:

```python
from log_viewer.formatters import text, json_fmt, pretty

# Plain text
output = text.format(report)

# Machine-readable JSON
output = json_fmt.format(report)

# ANSI-colored console output
output = pretty.format(report)
```

## Matching Semantics

**Preserved from original:**
- ✓ Case-sensitive substring matching
- ✓ Returns lines in file order
- ✓ Same set of matched lines
- ✓ Reads file line-by-line
- ✓ Trailing newlines removed from results

**Tested by:** `test_semantic_equivalence.py`

## Running Tests

### One-Click Test Runner
```bash
python run_tests.py
```

This discovers and runs all tests:
- `test_semantic_equivalence.py` - 7 tests
- `test_architecture.py` - 7 tests
- `test_output_formats.py` - 10 tests
- `test_summary.py` - 7 tests

**Total: 31 automated tests**

### Run Specific Test Suite
```bash
python -m unittest tests.test_semantic_equivalence -v
python -m unittest tests.test_architecture -v
python -m unittest tests.test_output_formats -v
python -m unittest tests.test_summary -v
```

### Demo Comparison
```bash
python demo.py
```

Shows before/after output with original tool vs. enhanced tool in all formats.

## Key Improvements

### 1. Structured Output
**Before:**
```
matches: 2
ERROR line 1
ERROR line 2
```

**After (Text Format):**
```
======================================================================
LOG SEARCH RESULTS
======================================================================

Matches: 2
Total Lines Scanned: 100
Earliest Timestamp: 2025-12-24T08:15:23
Latest Timestamp: 2025-12-24T08:20:45

----------------------------------------------------------------------

Match #1
  Line Number: 6
  Timestamp: 2025-12-24T08:15:30
  Content: 2025-12-24T08:15:30 ERROR Failed to connect to cache server
  Highlighted: 2025-12-24T08:15:30 [ERROR] Failed to connect to cache server
  Context Before:
    | 2025-12-24T08:15:29 INFO Database connection established

Match #2
  Line Number: 13
  ...

======================================================================
```

### 2. Machine-Readable JSON
```json
{
  "results": [
    {
      "line_number": 6,
      "line": "2025-12-24T08:15:30 ERROR Failed to connect to cache server",
      "highlighted": "2025-12-24T08:15:30 [ERROR] Failed to connect to cache server",
      "context_before": [...],
      "context_after": [...],
      "timestamp": "2025-12-24T08:15:30"
    }
  ],
  "summary": {
    "matches": 2,
    "total_lines": 100,
    "earliest_timestamp": "2025-12-24T08:15:23",
    "latest_timestamp": "2025-12-24T08:20:45"
  }
}
```

### 3. Modular Architecture
- **reader.py** - Pure file reading logic
- **searcher.py** - Pure search and analysis
- **formatters/text.py** - Plain text formatting
- **formatters/json_fmt.py** - JSON formatting
- **formatters/pretty.py** - Colored console output

Each module has a single responsibility, making it easy to:
- Test individual components
- Add new formatters
- Modify search behavior
- Reuse in other projects

### 4. Timestamp Extraction
Automatically extracts timestamps from common log formats:
- ISO 8601: `2025-12-24T10:30:45`
- Apache/Nginx: `24/Dec/2025:10:30:45`
- Syslog: `Dec 24 10:30:45`

Provides `earliest_timestamp` and `latest_timestamp` in summary.

### 5. Context Lines
Shows configurable lines before/after each match:

```python
search(path, "ERROR", context=3)  # 3 lines before and after
```

Useful for understanding error context in logs.

### 6. Extensibility

Adding a new formatter is trivial:

```python
# formatters/xml.py
import xml.etree.ElementTree as ET

def format(report):
    root = ET.Element("report")
    # ... build XML structure ...
    return ET.tostring(root, encoding='unicode')
```

Adding a new matcher type:
```python
# searcher.py
def search_regex(path, pattern, context=0):
    # Alternative matching logic
    ...
```

## Test Coverage

### Semantic Equivalence (7 tests)
- ✓ Exact match count matches original
- ✓ Matched lines are identical
- ✓ Order is preserved
- ✓ Case sensitivity
- ✓ Substring matching
- ✓ Empty matches handled
- ✓ Total line count accurate

### Architecture (7 tests)
- ✓ Modular structure exists
- ✓ Formatters subpackage exists
- ✓ All required modules present
- ✓ Can import all modules
- ✓ searcher.search() exists
- ✓ All formatters have format()
- ✓ Logic distributed across files

### Output Formats (10 tests)
- ✓ Text output is string
- ✓ Text contains headers
- ✓ Text shows line numbers
- ✓ Text highlights keywords
- ✓ Text shows context when present
- ✓ JSON is valid JSON
- ✓ JSON has required keys
- ✓ JSON results have all fields
- ✓ Pretty has ANSI codes
- ✓ Pretty has summary info

### Summary Correctness (7 tests)
- ✓ Total lines equals file lines
- ✓ Matches equals results length
- ✓ Timestamps are valid or None
- ✓ Earliest ≤ Latest
- ✓ All required keys present
- ✓ Match counts are accurate
- ✓ Timestamps from log content

## Example Usage

### Basic Search
```python
from log_viewer.searcher import search
from log_viewer.formatters import text

report = search("access.log", "ERROR")
print(text.format(report))
```

### With Context
```python
report = search("app.log", "Database", context=2)
print(text.format(report))
```

### JSON Output for Processing
```python
import json
from log_viewer.formatters import json_fmt

report = search("system.log", "WARN")
json_str = json_fmt.format(report)
data = json.loads(json_str)

for result in data["results"]:
    print(f"Line {result['line_number']}: {result['timestamp']}")
```

### Pretty Console Output
```python
from log_viewer.formatters import pretty

report = search("app.log", "CRITICAL")
print(pretty.format(report))  # Colors in terminal
```

## Files Overview

| File | Purpose | Lines |
|------|---------|-------|
| `log_viewer/__init__.py` | Package metadata | 8 |
| `log_viewer/reader.py` | File I/O | 26 |
| `log_viewer/searcher.py` | Search logic + API | 139 |
| `log_viewer/formatters/text.py` | Text formatter | 49 |
| `log_viewer/formatters/json_fmt.py` | JSON formatter | 12 |
| `log_viewer/formatters/pretty.py` | Pretty formatter | 70 |
| `tests/test_semantic_equivalence.py` | Semantic tests | 85 |
| `tests/test_architecture.py` | Architecture tests | 75 |
| `tests/test_output_formats.py` | Format tests | 115 |
| `tests/test_summary.py` | Summary tests | 97 |
| `run_tests.py` | Test runner | 27 |
| `demo.py` | Demonstration | 108 |

**Total: ~811 lines of code + tests**

## Performance Characteristics

- **Time:** O(n) where n = number of lines (same as original)
- **Space:** O(m) where m = number of matches (same as original)
- **Timestamp extraction:** O(1) per line (regex on short strings)
- **Context gathering:** O(1) per match (just array slicing)

No performance regression from original tool.

## Compatibility

- Python 3.6+
- No external dependencies
- Windows/Linux/macOS compatible
- UTF-8 file handling with error replacement

## License

Same as original `log_viewer_original.py`
