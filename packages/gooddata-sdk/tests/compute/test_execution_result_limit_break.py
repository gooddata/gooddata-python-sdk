# (C) 2026 GoodData Corporation
from __future__ import annotations

from unittest.mock import MagicMock

from gooddata_sdk import ExecutionResultLimitBreak
from gooddata_sdk.compute.model.execution import ExecutionResult


def _make_mock_api_result(limit_breaks_value):
    """Return a mock that mimics a models.ExecutionResult dict-like object."""
    _paging = {"total": [10, 1], "count": [10, 1], "offset": [0, 0]}
    m = MagicMock()
    m.__getitem__ = MagicMock(
        side_effect=lambda k: {
            "data": [],
            "dimension_headers": [],
            "grand_totals": [],
            "paging": _paging,
            "metadata": {},
        }[k]
    )
    m.get = MagicMock(side_effect=lambda k, d=None: limit_breaks_value if k == "limitBreaks" else d)
    return m


def test_execution_result_limit_breaks():
    """ExecutionResult.limit_breaks returns a list; non-empty when limits are broken.

    For a normal execution the result is complete so limit_breaks must be [].
    This test also verifies that the field is importable from gooddata_sdk and
    that the ExecutionResultLimitBreak class is available on the public API.

    Uses a synthetic mock result to avoid staging-server dependency.
    """
    # --- Case 1: result where a row-count limit was broken ---
    result = ExecutionResult(
        _make_mock_api_result([{"limit": 1000, "limitType": "rowCount", "value": 1500}])
    )
    assert isinstance(result.limit_breaks, list)
    assert len(result.limit_breaks) == 1
    for lb in result.limit_breaks:
        assert isinstance(lb, ExecutionResultLimitBreak)
        assert isinstance(lb.limit, int)
        assert isinstance(lb.limit_type, str)
        assert lb.value is None or isinstance(lb.value, int)

    # --- Case 2: complete result — no limits broken ---
    result_complete = ExecutionResult(_make_mock_api_result(None))
    assert isinstance(result_complete.limit_breaks, list)
    assert result_complete.limit_breaks == []
