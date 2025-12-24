"""
Semantic equivalence tests.

Validates that the enhanced search produces identical results to the original tool.
"""

import sys
import os
import unittest

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from log_viewer_original import search_logs
from log_viewer.searcher import search


class TestSemanticEquivalence(unittest.TestCase):
    """Test that enhanced search has identical matching semantics as original."""
    
    @classmethod
    def setUpClass(cls):
        """Set up test fixtures."""
        cls.sample_log = os.path.join(
            os.path.dirname(__file__),
            "..",
            "examples",
            "sample.log"
        )
    
    def test_exact_match_count(self):
        """Enhanced search should find same number of matches as original."""
        keyword = "ERROR"
        
        original_results = search_logs(self.sample_log, keyword)
        enhanced_report = search(self.sample_log, keyword)
        
        self.assertEqual(
            len(original_results),
            enhanced_report["summary"]["matches"],
            f"Match count mismatch for keyword '{keyword}'"
        )
    
    def test_matched_lines_identical(self):
        """Enhanced and original should return identical raw lines."""
        keyword = "INFO"
        
        original_results = search_logs(self.sample_log, keyword)
        enhanced_report = search(self.sample_log, keyword)
        enhanced_lines = [r["line"] for r in enhanced_report["results"]]
        
        self.assertEqual(
            original_results,
            enhanced_lines,
            f"Matched lines differ for keyword '{keyword}'"
        )
    
    def test_order_preserved(self):
        """Results should be in file order."""
        keyword = "logged"
        
        enhanced_report = search(self.sample_log, keyword)
        results = enhanced_report["results"]
        
        # Check line numbers are in ascending order
        if results:
            line_nums = [r["line_number"] for r in results]
            self.assertEqual(
                line_nums,
                sorted(line_nums),
                "Results are not in file order"
            )
    
    def test_case_sensitivity(self):
        """Search should be case-sensitive."""
        log_path = self.sample_log
        
        # "ERROR" vs "error"
        errors_upper = search_logs(log_path, "ERROR")
        errors_lower = search_logs(log_path, "error")
        
        self.assertGreater(len(errors_upper), 0)
        self.assertEqual(len(errors_lower), 0)
        
        # Enhanced should have same behavior
        enhanced_upper = search(log_path, "ERROR")
        enhanced_lower = search(log_path, "error")
        
        self.assertEqual(
            len(errors_upper),
            enhanced_upper["summary"]["matches"]
        )
        self.assertEqual(
            len(errors_lower),
            enhanced_lower["summary"]["matches"]
        )
    
    def test_substring_matching(self):
        """Should match substrings, not whole words."""
        log_path = self.sample_log
        
        # "logged" should match "logged in" but also appear in other contexts
        original = search_logs(log_path, "logged")
        enhanced = search(log_path, "logged")
        
        self.assertEqual(
            len(original),
            enhanced["summary"]["matches"]
        )
    
    def test_empty_matches(self):
        """Should handle keyword with no matches."""
        log_path = self.sample_log
        
        original = search_logs(log_path, "NONEXISTENT_KEYWORD_XYZ")
        enhanced = search(log_path, "NONEXISTENT_KEYWORD_XYZ")
        
        self.assertEqual(len(original), 0)
        self.assertEqual(enhanced["summary"]["matches"], 0)
        self.assertEqual(len(enhanced["results"]), 0)
    
    def test_total_lines_count(self):
        """Total lines should equal actual file line count."""
        enhanced_report = search(self.sample_log, "anyKeyword")
        
        with open(self.sample_log, 'r') as f:
            actual_lines = len(f.readlines())
        
        self.assertEqual(
            enhanced_report["summary"]["total_lines"],
            actual_lines,
            "Total line count mismatch"
        )


if __name__ == "__main__":
    unittest.main()
