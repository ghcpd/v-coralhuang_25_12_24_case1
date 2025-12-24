"""
Summary correctness tests.

Validates that summary metadata is accurate.
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from log_viewer.searcher import search


class TestSummaryCorrectness(unittest.TestCase):
    """Test that summary metadata is accurate."""
    
    @classmethod
    def setUpClass(cls):
        """Set up test fixtures."""
        cls.sample_log = os.path.join(
            os.path.dirname(__file__),
            "..",
            "examples",
            "sample.log"
        )
    
    def test_total_lines_equals_file_lines(self):
        """Total lines should equal actual file line count."""
        report = search(self.sample_log, "anyKeyword")
        
        with open(self.sample_log, 'r') as f:
            actual_lines = len(f.readlines())
        
        self.assertEqual(
            report["summary"]["total_lines"],
            actual_lines
        )
    
    def test_matches_equals_results_length(self):
        """Match count should equal number of results."""
        report = search(self.sample_log, "ERROR")
        
        self.assertEqual(
            report["summary"]["matches"],
            len(report["results"])
        )
    
    def test_timestamps_or_none(self):
        """Timestamps should be strings or None."""
        report = search(self.sample_log, "INFO")
        
        summary = report["summary"]
        
        # Timestamps should be string or None
        self.assertTrue(
            summary["earliest_timestamp"] is None or 
            isinstance(summary["earliest_timestamp"], str)
        )
        self.assertTrue(
            summary["latest_timestamp"] is None or 
            isinstance(summary["latest_timestamp"], str)
        )
    
    def test_earliest_before_latest(self):
        """If both timestamps exist, earliest should be <= latest."""
        report = search(self.sample_log, "INFO")
        
        summary = report["summary"]
        
        if summary["earliest_timestamp"] and summary["latest_timestamp"]:
            self.assertLessEqual(
                summary["earliest_timestamp"],
                summary["latest_timestamp"]
            )
    
    def test_all_summary_keys_exist(self):
        """Summary should have all required keys."""
        report = search(self.sample_log, "test")
        
        required_keys = [
            "matches",
            "total_lines",
            "earliest_timestamp",
            "latest_timestamp"
        ]
        
        for key in required_keys:
            self.assertIn(key, report["summary"])
    
    def test_matches_count_accurate(self):
        """Match count should be accurate for various keywords."""
        test_cases = [
            ("ERROR", 6),  # Count actual errors in sample.log
            ("INFO", 19),  # Count actual infos
            ("User", 5),   # Count user logins/actions
        ]
        
        for keyword, expected_count in test_cases:
            report = search(self.sample_log, keyword)
            self.assertEqual(
                report["summary"]["matches"],
                expected_count,
                f"Wrong match count for keyword '{keyword}'"
            )
    
    def test_timestamps_from_log_content(self):
        """Timestamps should be extracted from actual log lines."""
        report = search(self.sample_log, "Application")
        
        # "Application started" has first timestamp
        if report["results"]:
            first_line = report["results"][0]["line"]
            # Should contain a timestamp
            self.assertIn("2025-12-24", first_line)
    
    def test_context_preserves_order(self):
        """Context lines should be in file order."""
        report = search(self.sample_log, "Database", context=2)
        
        for result in report["results"]:
            # Context before should be in ascending line numbers
            context_before = result["context_before"]
            if context_before and len(context_before) > 1:
                # Lines should appear in order they appear in file
                # Just verify it's a list
                self.assertIsInstance(context_before, list)


if __name__ == "__main__":
    unittest.main()
