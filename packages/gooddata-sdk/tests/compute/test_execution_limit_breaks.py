# (C) 2026 GoodData Corporation
from __future__ import annotations

from pathlib import Path

import pytest
from gooddata_sdk import ExecutionResultLimitBreak, GoodDataSdk, ObjId, SimpleMetric, TableDimension
from gooddata_sdk.compute.model.execution import ExecutionDefinition, ExecutionResult
from tests_support.vcrpy_utils import get_vcr

gd_vcr = get_vcr()

_current_dir = Path(__file__).parent.absolute()
_fixtures_dir = _current_dir / "fixtures"


# ---------------------------------------------------------------------------
# Unit tests — ExecutionResultLimitBreak.from_api
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "scenario, data, expected_limit, expected_limit_type, expected_value",
    [
        (
            "all_fields",
            {"limit": 1000, "limitType": "rowCount", "value": 1500},
            1000,
            "rowCount",
            1500,
        ),
        (
            "absent_value",
            {"limit": 500, "limitType": "cellCount"},
            500,
            "cellCount",
            None,
        ),
        (
            "null_value",
            {"limit": 200, "limitType": "rowCount", "value": None},
            200,
            "rowCount",
            None,
        ),
    ],
)
def test_execution_result_limit_break_from_api(
    scenario: str,
    data: dict,
    expected_limit: int,
    expected_limit_type: str,
    expected_value: int | None,
) -> None:
    lb = ExecutionResultLimitBreak.from_api(data)
    assert lb.limit == expected_limit
    assert lb.limit_type == expected_limit_type
    assert lb.value == expected_value


# ---------------------------------------------------------------------------
# Unit tests — ExecutionResult.limit_breaks property
# ---------------------------------------------------------------------------


def _make_execution_result(metadata: dict) -> ExecutionResult:
    """Build an ExecutionResult from a plain-dict mock result."""
    result = {
        "data": [],
        "dimension_headers": [],
        "grand_totals": [],
        "paging": {"total": [0], "count": [0], "offset": [0]},
        "metadata": metadata,
    }
    return ExecutionResult(result)


def test_limit_breaks_absent_returns_empty_list() -> None:
    """When limitBreaks is not in the metadata, limit_breaks returns []."""
    er = _make_execution_result({"dataSourceMessages": []})
    assert er.limit_breaks == []


def test_limit_breaks_present_returns_parsed_objects() -> None:
    """When limitBreaks is present, limit_breaks returns a list of ExecutionResultLimitBreak."""
    metadata = {
        "dataSourceMessages": [],
        "limitBreaks": [
            {"limit": 1000, "limitType": "rowCount", "value": 1234},
            {"limit": 500, "limitType": "cellCount"},
        ],
    }
    er = _make_execution_result(metadata)
    breaks = er.limit_breaks
    assert len(breaks) == 2

    assert breaks[0].limit == 1000
    assert breaks[0].limit_type == "rowCount"
    assert breaks[0].value == 1234

    assert breaks[1].limit == 500
    assert breaks[1].limit_type == "cellCount"
    assert breaks[1].value is None


# ---------------------------------------------------------------------------
# Integration test — limit_breaks accessible after real execution
# ---------------------------------------------------------------------------


@gd_vcr.use_cassette(str(_fixtures_dir / "test_execution_limit_breaks.yaml"))
def test_execution_limit_breaks_integration(test_config):
    """Integration test: execute a computation and verify limit_breaks is accessible.

    In normal operation (no limits exceeded) limit_breaks returns an empty list.
    This test verifies the SDK correctly handles the absent limitBreaks field.
    """
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])

    exec_def = ExecutionDefinition(
        attributes=None,
        metrics=[SimpleMetric(local_id="m1", item=ObjId(type="metric", id="order_amount"))],
        filters=None,
        dimensions=[TableDimension(item_ids=["measureGroup"])],
    )

    execution = sdk.compute.for_exec_def(test_config["workspace"], exec_def)
    result = execution.read_result(limit=1)

    assert isinstance(result.limit_breaks, list)
