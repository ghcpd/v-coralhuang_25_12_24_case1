"""Tests that validate summary correctness (counts, timestamps)."""
import os
import unittest
from datetime import datetime

from log_viewer import search

SAMPLE = os.path.join(os.path.dirname(__file__), '..', 'examples', 'sample.log')


class SummaryTests(unittest.TestCase):
    def test_total_lines_and_matches(self):
        report = search(SAMPLE, 'ERROR', context=0)
        # file has 10 lines in the sample
        self.assertEqual(report['summary']['total_lines'], 10)
        self.assertEqual(report['summary']['matches'], len(report['results']))

    def test_timestamps_ordering(self):
        report = search(SAMPLE, 'ERROR', context=0)
        earliest = report['summary']['earliest_timestamp']
        latest = report['summary']['latest_timestamp']
        # sample.log contains timestamped ERROR lines -> both should be present
        self.assertIsNotNone(earliest)
        self.assertIsNotNone(latest)
        e = datetime.fromisoformat(earliest)
        l = datetime.fromisoformat(latest)
        self.assertLessEqual(e, l)


if __name__ == '__main__':
    unittest.main()
