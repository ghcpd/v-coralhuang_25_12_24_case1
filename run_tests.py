"""Discover and run tests. Uses pytest if available, otherwise unittest."""
import sys


def main():
    try:
        import pytest
    except Exception:
        # fallback to unittest
        import unittest
        loader = unittest.TestLoader()
        tests = loader.discover("tests")
        runner = unittest.TextTestRunner(verbosity=2)
        result = runner.run(tests)
        sys.exit(not result.wasSuccessful())
    else:
        # run pytest
        rc = pytest.main(["-q"])
        sys.exit(rc)


if __name__ == "__main__":
    main()
