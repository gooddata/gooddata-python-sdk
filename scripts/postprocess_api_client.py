#!/usr/bin/env python3
# (C) 2026 GoodData Corporation
"""Post-process the generated `gooddata-api-client` Python sources.

Two issues from openapi-generator-cli v6.6.0 with the `python-prior` generator
need patching after every regen — both relate to the regex pattern
`^[^\\u0000]*$` that the upstream OpenAPI spec uses on identifier fields:

1. The generator sometimes drops the `\\x00` literal from the character class,
   leaving the invalid Python regex `^[^]*$` (empty char class).
2. The generator sometimes embeds a literal NUL byte between the brackets,
   producing a Python source file with a NUL — which fails to import with
   `SyntaxError: source code string cannot contain null bytes`.

This script handles both shapes by rewriting any byte sequence resembling the
broken regex into the canonical `^[^\\\\x00]*$` form, and stripping any
remaining stray NULs from the generated tree.
"""

from __future__ import annotations

import sys
from pathlib import Path

BROKEN_NUL = b"[^\x00]"  # literal NUL inside char class
BROKEN_EMPTY = b"[^]"  # NUL was dropped entirely
FIXED = b"[^\\x00]"  # canonical Python escape


def patch(path: Path) -> bool:
    raw = path.read_bytes()
    new = raw.replace(BROKEN_NUL, FIXED).replace(BROKEN_EMPTY, FIXED)
    # Defensive: any stray NUL that wasn't inside the regex pattern. There
    # should be none after the replace above, but generated docstrings have
    # historically carried odd byte sequences.
    if b"\x00" in new:
        new = new.replace(b"\x00", b"")
    if new == raw:
        return False
    path.write_bytes(new)
    return True


def main(root: str) -> int:
    base = Path(root)
    if not base.is_dir():
        print(f"error: {root} is not a directory", file=sys.stderr)
        return 1
    fixed = 0
    for py in base.rglob("*.py"):
        if patch(py):
            fixed += 1
    print(f"postprocess_api_client: patched {fixed} file(s) under {root}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "gooddata-api-client/gooddata_api_client"))
