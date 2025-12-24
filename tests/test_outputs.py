# tests/test_outputs.py

import unittest
import sys
import os
import json

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from log_viewer.searcher import search
from log_viewer.formatters import text, json_fmt, pretty

class TestOutputs(unittest.TestCase):
    def setUp(self):
        self.sample_path = os.path.join(os.path.dirname(__file__), '..', 'examples', 'sample.log')
        self.keyword = 'keyword'
        self.report = search(self.sample_path, self.keyword, context=1)
    
    def test_text_output(self):
        output = text.format(self.report)
        self.assertIn('Summary:', output)
        self.assertIn('Results:', output)
        self.assertIn('Line ', output)
        self.assertIn('**keyword**', output)
        self.assertIn('Context before:', output)
        self.assertIn('Context after:', output)
    
    def test_json_output(self):
        output = json_fmt.format(self.report)
        parsed = json.loads(output)
        self.assertIn('results', parsed)
        self.assertIn('summary', parsed)
        self.assertEqual(len(parsed['results']), parsed['summary']['matches'])
    
    def test_pretty_output(self):
        output = pretty.format(self.report)
        self.assertIn('\033[1;34m', output)  # ANSI codes
        self.assertIn('\033[1;31m', output)
    
    def test_summary_correctness(self):
        summary = self.report['summary']
        self.assertEqual(summary['matches'], len(self.report['results']))
        # total_lines check
        with open(self.sample_path, 'r') as f:
            total = len(f.readlines())
        self.assertEqual(summary['total_lines'], total)
        # timestamps
        if summary['earliest_timestamp'] and summary['latest_timestamp']:
            from datetime import datetime
            e = datetime.fromisoformat(summary['earliest_timestamp'])
            l = datetime.fromisoformat(summary['latest_timestamp'])
            self.assertLessEqual(e, l)