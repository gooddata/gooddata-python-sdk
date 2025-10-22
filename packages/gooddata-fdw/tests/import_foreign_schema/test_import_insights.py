# (C) 2021 GoodData Corporation
from pathlib import Path

from gooddata_fdw import GoodDataForeignDataWrapper as fdw
from tests_support.vcrpy_utils import get_vcr

from tests.import_foreign_schema import _tables_to_dict

gd_vcr = get_vcr()


_current_dir = Path(__file__).parent.absolute()
_fixtures_dir = _current_dir / "fixtures"


@gd_vcr.use_cassette(str(_fixtures_dir / "import_insights_without_restrictions.yaml"))
def test_import_insights_without_restrictions(test_config):
    tables = fdw.import_schema(
        schema=test_config["workspace"],
        srv_options=dict(host=test_config["host"], token=test_config["token"]),
        options=dict(object_type="insights"),
        restriction_type=None,
        restricts=[],
    )

    # do a rough rub now.. fetch stable insights in the demo workspace.. those should be mapped to
    # tables. Then pick a couple of tables and make sure their columns are looking ok

    assert len(tables) == 15

    tables_idx = _tables_to_dict(tables)
    campaign_spend = tables_idx["campaign_spend"]
    # TODO: enrich demo workspace with single value insight (kpi)

    assert "campaign_channels_category" in campaign_spend.col_idx
    assert campaign_spend.col_idx["campaign_channels_category"].type_name == "VARCHAR(255)"
    assert "local_id" in campaign_spend.col_idx["campaign_channels_category"].options

    assert "campaign_name" in campaign_spend.col_idx
    assert campaign_spend.col_idx["campaign_name"].type_name == "VARCHAR(255)"
    assert "local_id" in campaign_spend.col_idx["campaign_name"].options

    assert "campaign_spend" in campaign_spend.col_idx
    assert campaign_spend.col_idx["campaign_spend"].type_name == "DECIMAL(18, 2)"
    assert "local_id" in campaign_spend.col_idx["campaign_spend"].options
