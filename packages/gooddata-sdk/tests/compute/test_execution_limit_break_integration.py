# (C) 2024 GoodData Corporation
"""Integration test: verify ExecutionResultLimitBreak is surfaced correctly.

The cassette for this test must be recorded against a server whose row-count
limit is configured lower than the result size produced by the execution below.
When the limit is broken the backend returns a non-empty ``limitBreaks`` list
inside ``metadata``; this test asserts that each item can be parsed into an
``ExecutionResultLimitBreak`` instance with the expected field types.
"""

from __future__ import annotations

from pathlib import Path

from gooddata_sdk import (
    Attribute,
    ExecutionDefinition,
    ExecutionResultLimitBreak,
    GoodDataSdk,
    ObjId,
    SimpleMetric,
    TableDimension,
)
from tests_support.vcrpy_utils import get_vcr

gd_vcr = get_vcr()

_current_dir = Path(__file__).parent.absolute()
_fixtures_dir = _current_dir / "fixtures"


@gd_vcr.use_cassette(str(_fixtures_dir / "test_execution_result_limit_break.yaml"))
def test_execution_result_limit_break(test_config):
    """Execution result metadata exposes limit-break info via raw dict access.

    The cassette captures a response where the row-count limit is triggered so
    that ``metadata["limitBreaks"]`` is non-empty.  This test verifies that:
    * the raw field is accessible from the result metadata dict
    * every item parses into an ``ExecutionResultLimitBreak`` with correct types
    * required fields (``limit``, ``limit_type``) are populated
    * optional ``value`` is ``int | None``
    """
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    workspace_id = test_config["workspace"]

    exec_def = ExecutionDefinition(
        attributes=[Attribute(local_id="a_region", label="region")],
        metrics=[SimpleMetric(local_id="m_order_amount", item=ObjId(type="metric", id="order_amount"))],
        filters=[],
        dimensions=[
            TableDimension(item_ids=["a_region"]),
            TableDimension(item_ids=["m_order_amount"]),
        ],
    )

    execution = sdk.compute.for_exec_def(workspace_id=workspace_id, exec_def=exec_def)
    result = execution.read_result(limit=1000)

    # Access limitBreaks from the raw metadata dict (the generated client does not
    # expose this field yet — it will once gooddata-api-client is regenerated).
    raw_breaks = result.metadata.get("limitBreaks") or []  # type: ignore[union-attr]

    # The cassette is recorded with at least one limit break present.
    assert len(raw_breaks) > 0, (
        "Expected at least one limitBreak in the result metadata. "
        "Re-record the cassette against a server with a low row-count limit."
    )

    for raw in raw_breaks:
        lb = ExecutionResultLimitBreak.from_dict(raw)
        assert isinstance(lb.limit, int), f"limit must be int, got {type(lb.limit)}"
        assert isinstance(lb.limit_type, str), f"limit_type must be str, got {type(lb.limit_type)}"
        assert lb.value is None or isinstance(lb.value, int), f"value must be int or None, got {type(lb.value)}"
        assert lb.limit > 0, "limit threshold must be positive"
        assert lb.limit_type, "limit_type must not be empty"
