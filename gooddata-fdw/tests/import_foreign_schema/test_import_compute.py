# (C) 2021 GoodData Corporation
from pathlib import Path

import vcr

from gooddata_fdw import GoodDataForeignDataWrapper as fdw
from tests import VCR_MATCH_ON

_current_dir = Path(__file__).parent.absolute()
_fixtures_dir = _current_dir / "fixtures"

gd_vcr = vcr.VCR(filter_headers=["authorization", "user-agent"], serializer="json", match_on=VCR_MATCH_ON)


@gd_vcr.use_cassette(str(_fixtures_dir / "import_compute_without_restrictions.json"))
def test_import_compute_without_restrictions(test_config):
    tables = fdw.import_schema(
        schema=test_config["workspace"],
        srv_options=dict(host=test_config["host"], token=test_config["token"]),
        options=dict(object_type="compute", numeric_max_size="24"),
        restriction_type=None,
        restricts=[],
    )

    # do a rough rub now.. check well known facts, labels and metrics

    assert len(tables) == 1
    compute_table = tables[0]

    # metrics
    assert "order_amount" in compute_table.col_idx
    assert "percent_revenue" in compute_table.col_idx
    # fact
    assert "campaign_channels_budget" in compute_table.col_idx
    # date attribute label
    assert "date_day" in compute_table.col_idx
    # normal label
    assert "campaign_channels_category" in compute_table.col_idx

    assert compute_table.col_idx["order_amount"].type_name == "DECIMAL(24, 2)"
    assert compute_table.col_idx["order_amount"].options["id"] == "metric/order_amount"

    assert compute_table.col_idx["percent_revenue"].type_name == "DECIMAL(24, 1)"
    assert compute_table.col_idx["percent_revenue"].options["id"] == "metric/percent_revenue"

    assert compute_table.col_idx["campaign_channels_budget"].type_name == "DECIMAL(24, 2)"
    assert compute_table.col_idx["campaign_channels_budget"].options["id"] == "fact/campaign_channels.budget"

    assert compute_table.col_idx["date_day"].type_name == "DATE"
    assert compute_table.col_idx["date_day"].options["id"] == "label/date.day"

    assert compute_table.col_idx["campaign_channels_category"].type_name == "VARCHAR(255)"
    assert compute_table.col_idx["campaign_channels_category"].options["id"] == "label/campaign_channels.category"
