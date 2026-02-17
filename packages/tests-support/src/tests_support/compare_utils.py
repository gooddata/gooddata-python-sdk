# (C) 2023 GoodData Corporation
from __future__ import annotations

from deepdiff import DeepDiff


def deep_eq(expected: any, actual: any, exclude_regex_paths: list[str] | None = None) -> bool:
    if expected != actual:
        print(DeepDiff(expected, actual, exclude_regex_paths=exclude_regex_paths))
        return False

    return True
