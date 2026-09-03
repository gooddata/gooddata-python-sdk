# (C) 2026 GoodData Corporation
"""One-write console output.

``print`` emits the text and the newline as two separate writes. Trace linking and the
item pool both run on worker threads, so a second write arriving between those two halves
splits a line down the middle. Everything that writes progress or warnings goes through
``emit_line`` instead, which cannot interleave.
"""

from __future__ import annotations

import sys


def emit_line(message: str) -> None:
    """Write one line to stdout in a single write."""
    sys.stdout.write(message + "\n")
    sys.stdout.flush()
