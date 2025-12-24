# tests/test_semantic_equivalence.py

import unittest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from log_viewer.searcher import search
from log_viewer_original import search_logs

class TestSemanticEquivalence(unittest.TestCase):
    def test_equivalence(self):
        sample_path = os.path.join(os.path.dirname(__file__), '..', 'examples', 'sample.log')
        keyword = 'keyword'
        original_results = search_logs(sample_path, keyword)
        enhanced_report = search(sample_path, keyword)
        
        self.assertEqual(len(original_results), enhanced_report['summary']['matches'])
        for orig, res in zip(original_results, enhanced_report['results']):
            self.assertEqual(orig, res['line'])