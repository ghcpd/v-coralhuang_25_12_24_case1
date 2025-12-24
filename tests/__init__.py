"""
Initialization for tests package.
"""

import sys
import os

# Add parent directory to path so tests can import log_viewer
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
