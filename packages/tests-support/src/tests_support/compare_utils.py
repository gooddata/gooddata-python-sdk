# (C) 2023 GoodData Corporation
from __future__ import annotations

from deepdiff import DeepDiff


def deep_eq(expected: any, actual: any) -> bool:
    if expected != actual:
        print(DeepDiff(expected, actual))
        return False

    return True
