"""Ensure enhanced tool returns exactly the same matched raw lines as the
original (order preserved).
"""
import os
import unittest

import log_viewer_original as original
from log_viewer import search as enhanced_search

SAMPLE = os.path.join(os.path.dirname(__file__), '..', 'examples', 'sample.log')


class SemanticEquivalenceTests(unittest.TestCase):
    def test_matches_equal_to_original(self):
        orig = original.search_logs(SAMPLE, 'ERROR')
        report = enhanced_search(SAMPLE, 'ERROR', context=0)

        self.assertEqual(report['summary']['matches'], len(orig))
        self.assertEqual([r['line'] for r in report['results']], orig)

    def test_order_preserved(self):
        orig = original.search_logs(SAMPLE, 'ERROR')
        report = enhanced_search(SAMPLE, 'ERROR', context=0)
        # ensure same order
        for idx, line in enumerate(orig):
            self.assertEqual(report['results'][idx]['line'], line)


if __name__ == '__main__':
    unittest.main()
