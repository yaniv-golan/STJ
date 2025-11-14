import os
import sys
from pathlib import Path

current_dir = Path(__file__).resolve().parent
project_root = current_dir.parents[1]

tools_python = project_root / 'tools' / 'python'
vendor_python = project_root / 'vendor' / 'python'

sys.path.insert(0, str(tools_python))

try:
    import stjlib  # noqa: F401
except ImportError:
    if vendor_python.exists():
        vendor_path = str(vendor_python)
        if vendor_path not in sys.path:
            sys.path.append(vendor_path)
