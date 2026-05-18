# (C) 2026 GoodData Corporation
from __future__ import annotations

from unittest.mock import patch

import pytest
from gooddata_sdk import ExecutionResultLimitBreak, GoodDataSdk
from gooddata_sdk.compute.model.attribute import Attribute
from gooddata_sdk.compute.model.execution import ExecutionDefinition, ExecutionResult, TableDimension


@pytest.mark.parametrize(
    "scenario,data,expected_limit,expected_limit_type,expected_value",
    [
        ("full", {"limit": 1000, "limitType": "rowCount", "value": 1500}, 1000, "rowCount", 1500),
        ("no_value", {"limit": 500, "limitType": "rowCount"}, 500, "rowCount", None),
        ("null_value", {"limit": 200, "limitType": "cellCount", "value": None}, 200, "cellCount", None),
    ],
)
def test_limit_break_from_api(scenario, data, expected_limit, expected_limit_type, expected_value):
    """ExecutionResultLimitBreak.from_api correctly maps camelCase keys and handles absent value."""
    result = ExecutionResultLimitBreak.from_api(data)
    assert result.limit == expected_limit
    assert result.limit_type == expected_limit_type
    assert result.value == expected_value


def _make_execution_result(limit_breaks=None):
    """Return a minimal ExecutionResult dict for unit testing."""
    metadata = {"dataSourceMessages": []}
    if limit_breaks is not None:
        metadata["limitBreaks"] = limit_breaks
    return {
        "data": [],
        "dimension_headers": [],
        "grand_totals": [],
        "metadata": metadata,
        "paging": {"count": [0], "offset": [0], "total": [0]},
    }


def test_execution_result_limit_breaks_absent():
    """When limitBreaks is absent from metadata, limit_breaks returns empty list."""
    raw = _make_execution_result()
    result = ExecutionResult(raw)  # type: ignore[arg-type]
    assert result.limit_breaks == []


def test_execution_result_limit_breaks_present():
    """When limitBreaks is present in metadata, limit_breaks returns correctly parsed list."""
    raw = _make_execution_result(limit_breaks=[{"limit": 1000, "limitType": "rowCount", "value": 1200}])
    result = ExecutionResult(raw)  # type: ignore[arg-type]
    breaks = result.limit_breaks
    assert len(breaks) == 1
    assert breaks[0].limit == 1000
    assert breaks[0].limit_type == "rowCount"
    assert breaks[0].value == 1200


def test_execution_result_limit_breaks_integration(test_config):
    """Integration test: limit_breaks property is accessible through the full SDK call chain.

    Uses mocking to avoid a real-server dependency — the AFM execution backend
    is unavailable in the CI environment (data-source unreachable).  The test
    still exercises the SDK path from for_exec_def → read_result → limit_breaks.
    """
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    workspace_id = test_config["workspace"]

    exec_def = ExecutionDefinition(
        attributes=[Attribute(local_id="a1", label="campaign_channel_id")],
        metrics=[],
        filters=[],
        dimensions=[TableDimension(item_ids=["a1"])],
    )

    # Synthetic execution response returned by the POST /execute endpoint.
    mock_exec_response = {
        "execution_response": {
            "links": {"executionResult": "test-result-id"},
            "dimensions": [],
        }
    }
    # Synthetic result returned by the GET /execute/result/... endpoint.
    mock_exec_result = _make_execution_result()

    with patch.object(
        sdk.compute._actions_api, "compute_report", return_value=(mock_exec_response, 200, {})
    ), patch.object(
        sdk.compute._actions_api, "retrieve_result", return_value=(mock_exec_result, 200, {})
    ):
        execution = sdk.compute.for_exec_def(workspace_id, exec_def)
        result = execution.read_result(limit=10)

    # limit_breaks returns a list (empty when result is complete, no limits broken)
    assert isinstance(result.limit_breaks, list)
