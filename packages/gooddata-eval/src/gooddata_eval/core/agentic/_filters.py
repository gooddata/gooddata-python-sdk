# (C) 2026 GoodData Corporation
"""Attribute filter selections and filter values, shared by the dashboard and document graders.

Both read a selection with ``selection_of``. Only the document grader compares two selections with
``same_selection``, ignoring the order of their values; the dashboard grader compares them as read.
"""

from __future__ import annotations


def selection_of(attribute_filter: dict) -> tuple[str, list] | None:
    """The elements an attribute filter restricts to, or ``None`` when it restricts nothing.

    An unrestricted filter is spelled as the absence of a selection, and an empty list means
    the same thing, so both read as "all".
    """
    state = attribute_filter.get("state") or {}
    for kind in ("include", "exclude"):
        values = state.get(kind)
        if values:
            return kind, list(values)
    return None


def describe_selection(selection: tuple[str, list] | None) -> str:
    return "all" if selection is None else f"{selection[0]} {selection[1]!r}"


def same_selection(actual: tuple[str, list] | None, expected: tuple[str, list] | None) -> bool:
    """Whether two selections restrict to the same elements: an include or exclude list is a set, not a sequence."""
    if actual is None or expected is None:
        return actual is None and expected is None
    return actual[0] == expected[0] and same_unordered_values(expected[1], actual[1])


def same_unordered_values(want: list, got: list) -> bool:
    """One-to-one match in any order, with each pair of the same type.

    Not sorted: AAC allows `null` among the values, and Python cannot order it with strings.
    Not stringified: `1` and `"1"` are different values.
    """
    remaining = list(got)
    for expected in want:
        index = next(
            (i for i, actual in enumerate(remaining) if type(actual) is type(expected) and actual == expected), None
        )
        if index is None:
            return False
        del remaining[index]
    return not remaining
