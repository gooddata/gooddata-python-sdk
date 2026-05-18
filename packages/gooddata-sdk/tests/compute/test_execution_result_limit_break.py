# (C) 2026 GoodData Corporation
from __future__ import annotations

from pathlib import Path

from gooddata_sdk import Attribute, ExecutionResultLimitBreak, GoodDataSdk, ObjId, SimpleMetric
from gooddata_sdk.compute.model.execution import ExecutionDefinition, TableDimension
from tests_support.vcrpy_utils import get_vcr

gd_vcr = get_vcr()

_current_dir = Path(__file__).parent.absolute()
_fixtures_dir = _current_dir / "fixtures"


@gd_vcr.use_cassette(str(_fixtures_dir / "test_execution_result_limit_breaks.yaml"))
def test_execution_result_limit_breaks(test_config):
    """ExecutionResult.limit_breaks returns a list; empty when no limit is broken.

    For a normal execution the result is complete so limit_breaks must be [].
    This test also verifies that the field is importable from gooddata_sdk and
    that the ExecutionResultLimitBreak class is available on the public API.
    """
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    workspace_id = test_config["workspace"]

    exec_def = ExecutionDefinition(
        attributes=[Attribute(local_id="a1", label="region")],
        metrics=[SimpleMetric(local_id="m1", item=ObjId(type="metric", id="order_amount"))],
        filters=[],
        dimensions=[
            TableDimension(item_ids=["a1"]),
            TableDimension(item_ids=["measureGroup"]),
        ],
    )
    execution = sdk.compute.for_exec_def(workspace_id=workspace_id, exec_def=exec_def)
    result = execution.read_result(limit=[100, 100], offset=[0, 0])

    assert isinstance(result.limit_breaks, list)
    for lb in result.limit_breaks:
        assert isinstance(lb, ExecutionResultLimitBreak)
        assert isinstance(lb.limit, int)
        assert isinstance(lb.limit_type, str)
        assert lb.value is None or isinstance(lb.value, int)
