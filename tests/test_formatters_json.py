"""Tests for JSON formatter output shape and validity."""
import os
import unittest
import json

from log_viewer import search
from log_viewer.formatters import json_fmt

SAMPLE = os.path.join(os.path.dirname(__file__), '..', 'examples', 'sample.log')


class JsonFormatterTests(unittest.TestCase):
    def test_json_parses_and_contains_expected_keys(self):
        report = search(SAMPLE, 'ERROR', context=0)
        out = json_fmt.format(report)
        parsed = json.loads(out)

        self.assertIn('results', parsed)
        self.assertIn('summary', parsed)
        self.assertIsInstance(parsed['results'], list)
        self.assertIsInstance(parsed['summary'], dict)


if __name__ == '__main__':
    unittest.main()
