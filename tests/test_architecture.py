"""
Architecture tests.

Validates that the code is properly modularized.
"""

import sys
import os
import unittest


class TestArchitecture(unittest.TestCase):
    """Test that code is properly modularized."""
    
    def test_modular_structure_exists(self):
        """Check that log_viewer is a package with multiple modules."""
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        log_viewer_dir = os.path.join(base_dir, "log_viewer")
        
        # Check main package exists
        self.assertTrue(os.path.isdir(log_viewer_dir))
        
        # Check required modules exist
        required_files = ["__init__.py", "reader.py", "searcher.py"]
        for fname in required_files:
            fpath = os.path.join(log_viewer_dir, fname)
            self.assertTrue(
                os.path.isfile(fpath),
                f"Missing required module: {fname}"
            )
    
    def test_formatters_subpackage_exists(self):
        """Check that formatters is a proper subpackage."""
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        formatters_dir = os.path.join(base_dir, "log_viewer", "formatters")
        
        self.assertTrue(os.path.isdir(formatters_dir))
        self.assertTrue(os.path.isfile(os.path.join(formatters_dir, "__init__.py")))
    
    def test_formatter_modules_exist(self):
        """Check that all required formatters exist."""
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        formatters_dir = os.path.join(base_dir, "log_viewer", "formatters")
        
        required_formatters = ["text.py", "json_fmt.py", "pretty.py"]
        for fname in required_formatters:
            fpath = os.path.join(formatters_dir, fname)
            self.assertTrue(
                os.path.isfile(fpath),
                f"Missing formatter: {fname}"
            )
    
    def test_can_import_modules(self):
        """Check that all modules can be imported."""
        try:
            from log_viewer import reader
            from log_viewer import searcher
            from log_viewer.formatters import text
            from log_viewer.formatters import json_fmt
            from log_viewer.formatters import pretty
        except ImportError as e:
            self.fail(f"Failed to import modules: {e}")
    
    def test_searcher_has_search_function(self):
        """Check that searcher exposes search() function."""
        from log_viewer import searcher
        
        self.assertTrue(
            hasattr(searcher, 'search'),
            "searcher module missing search() function"
        )
        self.assertTrue(callable(searcher.search))
    
    def test_formatters_have_format_function(self):
        """Check that all formatters expose format() function."""
        from log_viewer.formatters import text, json_fmt, pretty
        
        for formatter_module in [text, json_fmt, pretty]:
            self.assertTrue(
                hasattr(formatter_module, 'format'),
                f"{formatter_module.__name__} missing format() function"
            )
            self.assertTrue(callable(formatter_module.format))
    
    def test_no_core_logic_in_single_file(self):
        """Verify that logic is distributed across modules."""
        from log_viewer import reader, searcher
        
        # reader should have read_lines
        self.assertTrue(hasattr(reader, 'read_lines'))
        
        # searcher should have search
        self.assertTrue(hasattr(searcher, 'search'))
        
        # Both should exist (distributed responsibility)
        self.assertIsNotNone(reader.read_lines)
        self.assertIsNotNone(searcher.search)


if __name__ == "__main__":
    unittest.main()
