"""Architecture tests: ensure modular layout and formatter placement."""
import os
import unittest

ROOT = os.path.dirname(os.path.dirname(__file__))
LV_DIR = os.path.join(ROOT, "log_viewer")
FMT_DIR = os.path.join(LV_DIR, "formatters")


class ArchitectureTests(unittest.TestCase):
    def test_package_exists(self):
        self.assertTrue(os.path.isdir(LV_DIR))

    def test_multiple_core_modules(self):
        py_files = [f for f in os.listdir(LV_DIR) if f.endswith('.py')]
        # __init__ + at least 2 core modules (reader, searcher)
        self.assertIn('reader.py', py_files)
        self.assertIn('searcher.py', py_files)
        self.assertGreaterEqual(len([p for p in py_files if p != '__init__.py']), 2)

    def test_formatters_location(self):
        self.assertTrue(os.path.isdir(FMT_DIR))
        fmt_files = os.listdir(FMT_DIR)
        self.assertIn('text.py', fmt_files)
        self.assertIn('json_fmt.py', fmt_files)
        self.assertIn('pretty.py', fmt_files)


if __name__ == '__main__':
    unittest.main()
