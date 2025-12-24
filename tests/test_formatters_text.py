"""Tests for the plain text formatter."""
import os
import unittest

from log_viewer import search
from log_viewer.formatters import text

SAMPLE = os.path.join(os.path.dirname(__file__), '..', 'examples', 'sample.log')


class TextFormatterTests(unittest.TestCase):
    def test_text_contains_headers_and_line_numbers_and_highlight(self):
        report = search(SAMPLE, 'ERROR', context=1)
        out = text.format(report)

        self.assertIn('SUMMARY', out)
        self.assertIn('RESULTS', out)
        # line numbers
        self.assertIn('Line 4:', out)
        # highlighted marker (searcher uses <<keyword>>)
        self.assertIn('<<ERROR>>', out)
        # context line appears
        self.assertIn('context_before:', out)
        self.assertIn('context_after:', out)


if __name__ == '__main__':
    unittest.main()
