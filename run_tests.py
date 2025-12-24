#!/usr/bin/env python
"""
One-click test runner for enhanced log viewer.

Discovers and runs all tests using unittest.
Exits with appropriate status code.
"""

import sys
import os
import unittest


def main():
    """Discover and run all tests."""
    # Get the tests directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    tests_dir = os.path.join(script_dir, "tests")
    
    # Discover all tests
    loader = unittest.TestLoader()
    suite = loader.discover(tests_dir, pattern="test_*.py")
    
    # Run with verbose output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Exit with appropriate code
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(main())
