# (C) 2026 GoodData Corporation
"""Recursive subset matcher for alert filter comparison."""

from typing import Any


def deep_subset(expected: Any, actual: Any) -> bool:
    """Return True if `expected` is a structural subset of `actual`.

    - dict: every key in expected must exist in actual with a matching value (deep).
    - list: same length; greedy order-insensitive match — each expected element
      claims the first unused actual element it deep-subset-matches. Sufficient
      for alert filters (small, distinct-type lists); may miss valid matchings
      when two expected items could match the same actual item.
    - other: equality.
    """
    if isinstance(expected, dict):
        if not isinstance(actual, dict):
            return False
        return all(k in actual and deep_subset(v, actual[k]) for k, v in expected.items())
    if isinstance(expected, list):
        if not isinstance(actual, list) or len(expected) != len(actual):
            return False
        used = [False] * len(actual)
        for exp_item in expected:
            matched = False
            for i, act_item in enumerate(actual):
                if not used[i] and deep_subset(exp_item, act_item):
                    used[i] = True
                    matched = True
                    break
            if not matched:
                return False
        return True
    return expected == actual
