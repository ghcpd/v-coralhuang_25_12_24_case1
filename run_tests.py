"""One-click test runner: prefer pytest if available, otherwise use unittest.
Exits with the underlying test runner exit code.
"""
import sys
import subprocess


def main():
    # prefer pytest when available for nicer output
    try:
        import pytest  # type: ignore
        rc = pytest.main(["-q"])  # returns exit code
        raise SystemExit(rc)
    except Exception:
        # fallback to unittest discovery
        proc = subprocess.run([sys.executable, "-m", "unittest", "discover", "-v"]) 
        raise SystemExit(proc.returncode)


if __name__ == "__main__":
    main()
