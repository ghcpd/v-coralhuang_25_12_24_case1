#!/usr/bin/env python
"""
Demonstration script showing before/after comparison.

Shows:
1. Original tool output
2. Enhanced tool text format
3. Enhanced tool JSON format
4. Enhanced tool pretty format
"""

import sys
import os
import json

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from log_viewer_original import search_logs
from log_viewer.searcher import search
from log_viewer.formatters import text, json_fmt, pretty


def print_section(title):
    """Print a section header."""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80 + "\n")


def main():
    """Run demonstration."""
    sample_log = os.path.join(
        os.path.dirname(__file__),
        "examples",
        "sample.log"
    )
    
    if not os.path.exists(sample_log):
        print("Error: sample.log not found")
        return 1
    
    keyword = "ERROR"
    context = 1
    
    print_section("ORIGINAL TOOL OUTPUT")
    print(f"Command: python log_viewer_original.py {sample_log} {keyword}\n")
    
    original_results = search_logs(sample_log, keyword)
    print(f"matches: {len(original_results)}")
    for line in original_results:
        print(line)
    
    print_section("ENHANCED TOOL - TEXT FORMAT")
    print(f"Function: search('{sample_log}', '{keyword}', context={context})")
    print("Formatter: text.format()\n")
    
    report = search(sample_log, keyword, context=context)
    text_output = text.format(report)
    print(text_output)
    
    print_section("ENHANCED TOOL - JSON FORMAT")
    print(f"Function: search('{sample_log}', '{keyword}')")
    print("Formatter: json_fmt.format()\n")
    
    json_output = json_fmt.format(report)
    print(json_output)
    
    print_section("ENHANCED TOOL - PRETTY FORMAT")
    print(f"Function: search('{sample_log}', '{keyword}', context={context})")
    print("Formatter: pretty.format()\n")
    
    pretty_output = pretty.format(report)
    print(pretty_output)
    
    print_section("VERIFICATION - SEMANTIC EQUIVALENCE")
    
    # Show that we get the same results
    enhanced_lines = [r["line"] for r in report["results"]]
    
    print(f"Original tool found: {len(original_results)} matches")
    print(f"Enhanced tool found: {len(enhanced_lines)} matches")
    print(f"Lines are identical: {original_results == enhanced_lines}")
    
    print_section("KEY IMPROVEMENTS")
    
    improvements = [
        "✓ Structured results with line numbers and timestamps",
        "✓ Context lines (before/after) for each match",
        "✓ Keyword highlighting with [...] markers",
        "✓ Summary metadata (total lines, timestamp range)",
        "✓ Multiple output formats (text, JSON, pretty with colors)",
        "✓ Modular architecture across 5 files",
        "✓ Programmatic API for testing and integration",
        "✓ Full test coverage with 4 test suites",
    ]
    
    for improvement in improvements:
        print(improvement)
    
    print("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
