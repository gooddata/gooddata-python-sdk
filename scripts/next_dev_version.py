# (C) 2026 GoodData Corporation
"""Print the next dev release version for a branch.

Usage: next_dev_version.py [--pyproject PATH] COMPONENT [COMPONENT ...]

PATH is the branch's pyproject.toml (default: the one next to this script), so the script
can run from a newer revision than the branch being released.

The base is the branch's own version with the patch bumped: 1.79.0 in pyproject.toml gives
1.79.1.devN. N is one past the highest 1.79.1.devN already on PyPI for any of the given
components, so every component of one dev release gets the same version even if an earlier
run published only some of them.

Only versions with exactly that base are compared, so there is no general version ordering
to get wrong (`sort -V` ranks 1.79.1.dev10 above 1.79.1, PEP 440 does the opposite).
"""

from __future__ import annotations

import argparse
import json
import re
import tomllib
import urllib.error
import urllib.request
from collections.abc import Iterable
from pathlib import Path

_ROOT_DIR = Path(__file__).resolve().parent.parent
_STABLE = re.compile(r"^(?P<major>\d+)\.(?P<minor>\d+)\.(?P<patch>\d+)$")
_VERSION = re.compile(r"^(?P<base>\d+\.\d+\.\d+)(?:\.dev(?P<dev>\d+))?$")


def dev_base(current: str) -> str:
    """Return the version the dev releases of a branch at ``current`` lead up to."""
    match = _STABLE.match(current)
    if match is None:
        raise ValueError(f"Branch version {current!r} is not N.N.N")
    return f"{match['major']}.{match['minor']}.{int(match['patch']) + 1}"


def next_dev_version(base: str, released: Iterable[str]) -> str:
    """Return ``base.devN`` with N one past the highest dev number already released for ``base``."""
    dev_numbers = []
    for version in released:
        match = _VERSION.match(version)
        if match is None or match["base"] != base:
            continue
        if match["dev"] is None:
            # A dev release of an already released version would sort below it.
            raise ValueError(f"{base} is already released; the branch is behind, merge the release into it first")
        dev_numbers.append(int(match["dev"]))
    return f"{base}.dev{max(dev_numbers, default=0) + 1}"


def released_versions(component: str) -> list[str]:
    """Return every version of ``component`` on PyPI, yanked ones included (their numbers stay taken)."""
    request = urllib.request.Request(
        f"https://pypi.org/pypi/{component}/json",
        headers={"Accept": "application/json", "User-Agent": "gooddata-python-sdk-release"},
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            data = json.load(response)
    except urllib.error.HTTPError as e:
        if e.code == 404:  # a component that has never been published
            return []
        raise
    # Fail rather than read an unexpected shape as "nothing released" and reuse a devN.
    releases = data.get("releases") if isinstance(data, dict) else None
    if not isinstance(releases, dict):
        raise ValueError(f"Unexpected PyPI response for {component}: no 'releases' mapping")
    return list(releases)


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Print the next dev release version for a branch.")
    parser.add_argument(
        "--pyproject",
        type=Path,
        default=_ROOT_DIR / "pyproject.toml",
        help="pyproject.toml of the branch being released",
    )
    parser.add_argument("components", nargs="+", metavar="COMPONENT", help="PyPI project to check")
    args = parser.parse_args(argv)
    with open(args.pyproject, "rb") as f:
        current = tomllib.load(f)["tool"]["tbump"]["version"]["current"]
    released = [version for component in args.components for version in released_versions(component)]
    print(next_dev_version(dev_base(current), released))


if __name__ == "__main__":
    main()
