"""One-click test runner.

Uses pytest when available, otherwise falls back to unittest discovery.
Exits with the appropriate status code.
"""
import sys


def run_pytest():
    import pytest

    return pytest.main(["-q"])


def run_unittest():
    import unittest

    loader = unittest.TestLoader()
    suite = loader.discover(".", pattern="test_*.py")
    runner = unittest.TextTestRunner(verbosity=2)
    res = runner.run(suite)
    return 0 if res.wasSuccessful() else 1


if __name__ == "__main__":
    try:
        code = run_pytest()
    except Exception:
        code = run_unittest()
    sys.exit(code)
