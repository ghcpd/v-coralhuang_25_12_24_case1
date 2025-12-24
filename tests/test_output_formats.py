"""
Output format tests.

Validates that formatters produce correct output.
"""

import sys
import os
import json
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from log_viewer.searcher import search
from log_viewer.formatters import text, json_fmt, pretty


class TestTextFormatter(unittest.TestCase):
    """Test plain text formatter output."""
    
    @classmethod
    def setUpClass(cls):
        """Set up test fixtures."""
        cls.sample_log = os.path.join(
            os.path.dirname(__file__),
            "..",
            "examples",
            "sample.log"
        )
        cls.report = search(cls.sample_log, "ERROR", context=1)
    
    def test_output_is_string(self):
        """Formatter should return a string."""
        output = text.format(self.report)
        self.assertIsInstance(output, str)
    
    def test_contains_header(self):
        """Output should contain section headers."""
        output = text.format(self.report)
        
        self.assertIn("LOG SEARCH RESULTS", output)
        self.assertIn("Matches:", output)
    
    def test_contains_line_numbers(self):
        """Output should show line numbers."""
        output = text.format(self.report)
        
        self.assertIn("Line Number:", output)
        # Check that actual line numbers appear
        for result in self.report["results"]:
            self.assertIn(str(result["line_number"]), output)
    
    def test_contains_highlighted_keyword(self):
        """Output should show highlighted keyword."""
        output = text.format(self.report)
        
        self.assertIn("Highlighted:", output)
        # Check that highlights are present
        for result in self.report["results"]:
            self.assertIn("[ERROR]", output)
    
    def test_shows_context_lines(self):
        """Output should show context lines when present."""
        output = text.format(self.report)
        
        if any(r["context_before"] or r["context_after"] for r in self.report["results"]):
            self.assertIn("Context", output)
    
    def test_no_matches_message(self):
        """Output should handle no matches gracefully."""
        empty_report = search(self.sample_log, "NONEXISTENT")
        output = text.format(empty_report)
        
        self.assertIn("No matches found", output)


class TestJSONFormatter(unittest.TestCase):
    """Test JSON formatter output."""
    
    @classmethod
    def setUpClass(cls):
        """Set up test fixtures."""
        cls.sample_log = os.path.join(
            os.path.dirname(__file__),
            "..",
            "examples",
            "sample.log"
        )
        cls.report = search(cls.sample_log, "logged")
    
    def test_output_is_valid_json(self):
        """JSON output should be parseable."""
        output = json_fmt.format(self.report)
        
        try:
            parsed = json.loads(output)
        except json.JSONDecodeError as e:
            self.fail(f"JSON is invalid: {e}")
    
    def test_contains_results_key(self):
        """JSON should have 'results' key."""
        output = json_fmt.format(self.report)
        parsed = json.loads(output)
        
        self.assertIn("results", parsed)
    
    def test_contains_summary_key(self):
        """JSON should have 'summary' key."""
        output = json_fmt.format(self.report)
        parsed = json.loads(output)
        
        self.assertIn("summary", parsed)
    
    def test_required_result_fields(self):
        """Each result should have all required fields."""
        output = json_fmt.format(self.report)
        parsed = json.loads(output)
        
        required_fields = [
            "line_number", "line", "highlighted",
            "context_before", "context_after", "timestamp"
        ]
        
        for result in parsed["results"]:
            for field in required_fields:
                self.assertIn(field, result)
    
    def test_required_summary_fields(self):
        """Summary should have all required fields."""
        output = json_fmt.format(self.report)
        parsed = json.loads(output)
        
        required_fields = [
            "matches", "total_lines",
            "earliest_timestamp", "latest_timestamp"
        ]
        
        for field in required_fields:
            self.assertIn(field, parsed["summary"])


class TestPrettyFormatter(unittest.TestCase):
    """Test pretty/colored formatter output."""
    
    @classmethod
    def setUpClass(cls):
        """Set up test fixtures."""
        cls.sample_log = os.path.join(
            os.path.dirname(__file__),
            "..",
            "examples",
            "sample.log"
        )
        cls.report = search(cls.sample_log, "INFO")
    
    def test_output_is_string(self):
        """Pretty formatter should return a string."""
        output = pretty.format(self.report)
        self.assertIsInstance(output, str)
    
    def test_contains_color_codes(self):
        """Output should contain ANSI color codes."""
        output = pretty.format(self.report)
        
        # Check for ANSI escape codes
        self.assertIn('\033[', output)
    
    def test_contains_summary_info(self):
        """Output should contain summary information."""
        output = pretty.format(self.report)
        
        self.assertIn("LOG SEARCH RESULTS", output)
        self.assertIn(str(self.report["summary"]["matches"]), output)


if __name__ == "__main__":
    unittest.main()
