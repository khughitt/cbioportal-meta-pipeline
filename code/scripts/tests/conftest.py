"""Test infrastructure for the cbioportal pipeline scripts.

Adds ``code/scripts/`` to ``sys.path`` so tests can import the script modules under test
without requiring them to be a package.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
