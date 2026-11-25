# (C) 2026 GoodData Corporation
"""Recursive subset matcher for alert filter comparison."""

from decimal import Decimal, InvalidOperation
from typing import Any


def deep_subset(expected: Any, actual: Any) -> bool:
    """Return True if `expected` is a structural subset of `actual`.

    - dict: every key in expected must exist in actual with a matching value (deep).
    - list: same length; greedy order-insensitive match — each expected element
      claims the first unused actual element it deep-subset-matches. Sufficient
      for alert filters (small, distinct-type lists); may miss valid matchings
      when two expected items could match the same actual item.
    - other: equality. A number also matches a numeric string of the same value,
      because the agent's tools accept both (`500` and `"500"` set the same threshold);
      two strings, and booleans, still compare exactly.
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
    return expected == actual or _same_number(expected, actual) or _same_number(actual, expected)


def _same_number(input_a: Any, input_b: Any) -> bool:
    if not isinstance(input_a, (int, float)) or isinstance(input_a, bool) or not isinstance(input_b, str):
        return False
    # Decimal, not float: float("9007199254740993") rounds to 9007199254740992.
    try:
        return Decimal(input_b) == Decimal(str(input_a))
    except InvalidOperation:
        return False
