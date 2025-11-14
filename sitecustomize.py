"""
Ensure vendored Python dependencies (vendor/python) are importable.

Python automatically imports this module (if present on sys.path) after the
standard site setup completes, so we can safely inject the vendor directory
without requiring users to modify PYTHONPATH.
"""

from pathlib import Path
import sys

VENDOR_DIR = Path(__file__).resolve().parent / "vendor" / "python"

if VENDOR_DIR.exists():
    vendor_path = str(VENDOR_DIR)
    if vendor_path not in sys.path:
        sys.path.append(vendor_path)
