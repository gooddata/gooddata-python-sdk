# (C) 2026 GoodData Corporation
import sys
from pathlib import Path

# The scripts are standalone files, not a package: make them importable by module name.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
