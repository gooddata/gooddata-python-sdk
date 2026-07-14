# (C) 2024 GoodData Corporation
from __future__ import annotations

import pytest
from gooddata_sdk import ExecutionResultLimitBreak


@pytest.mark.parametrize(
    "scenario, data, expected_limit, expected_limit_type, expected_value",
    [
        (
            "required_fields_only",
            {"limit": 100000, "limitType": "rowCount"},
            100000,
            "rowCount",
            None,
        ),
        (
            "with_known_value",
            {"limit": 100000, "limitType": "rowCount", "value": 123456},
            100000,
            "rowCount",
            123456,
        ),
        (
            "with_null_value",
            {"limit": 500, "limitType": "columnCount", "value": None},
            500,
            "columnCount",
            None,
        ),
        (
            "different_limit_type",
            {"limit": 50, "limitType": "dimensionItemCount"},
            50,
            "dimensionItemCount",
            None,
        ),
    ],
)
def test_from_dict(
    scenario: str,
    data: dict,
    expected_limit: int,
    expected_limit_type: str,
    expected_value: int | None,
) -> None:
    lb = ExecutionResultLimitBreak.from_dict(data)

    assert lb.limit == expected_limit
    assert lb.limit_type == expected_limit_type
    assert lb.value == expected_value


def test_importable_from_gooddata_sdk() -> None:
    """ExecutionResultLimitBreak must be importable from the top-level package."""
    # The top-level import at the module level already validates this.
    assert ExecutionResultLimitBreak.__name__ == "ExecutionResultLimitBreak"
