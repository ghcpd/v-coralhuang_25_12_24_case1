# tests/test_architecture.py

import unittest
import os

class TestArchitecture(unittest.TestCase):
    def test_modular_structure(self):
        # Check if directories exist
        self.assertTrue(os.path.exists(os.path.join(os.path.dirname(__file__), '..', 'log_viewer')))
        self.assertTrue(os.path.exists(os.path.join(os.path.dirname(__file__), '..', 'log_viewer', 'formatters')))
        
        # Check if files exist
        files = ['reader.py', 'searcher.py', '__init__.py']
        for f in files:
            self.assertTrue(os.path.exists(os.path.join(os.path.dirname(__file__), '..', 'log_viewer', f)))
        
        formatters = ['text.py', 'json_fmt.py', 'pretty.py', '__init__.py']
        for f in formatters:
            self.assertTrue(os.path.exists(os.path.join(os.path.dirname(__file__), '..', 'log_viewer', 'formatters', f)))