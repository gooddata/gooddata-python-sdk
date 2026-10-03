# (C) 2026 GoodData Corporation
"""Integration tests for CatalogAILakeService.

These tests exercise the full SDK → HTTP → server round-trip via VCR cassettes.
Each test function maps to exactly one cassette YAML.
"""

from __future__ import annotations

from pathlib import Path

from gooddata_sdk import GoodDataSdk
from tests_support.vcrpy_utils import get_vcr

gd_vcr = get_vcr()

_current_dir = Path(__file__).parent.absolute()
_fixtures_dir = _current_dir / "fixtures" / "ai_lake"


@gd_vcr.use_cassette(str(_fixtures_dir / "test_refresh_partition.yaml"))
def test_refresh_partition(test_config):
    """(BETA) Trigger a refresh-partition operation and verify a valid operation ID is returned.

    The test seeds a caller-supplied operation_id so the cassette is deterministic,
    then confirms the returned ID is exactly what was supplied.
    """
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    op_id = sdk.catalog_ai_lake.refresh_partition(
        instance_id="demo-db",
        table_name="fact_orders",
        partition_spec={"year": "2024", "month": "01"},
        operation_id="aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee",
    )
    assert op_id == "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee"
