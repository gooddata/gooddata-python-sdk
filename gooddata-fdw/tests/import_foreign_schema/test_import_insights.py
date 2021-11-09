# (C) 2021 GoodData Corporation
import os

import vcr

from gooddata_fdw import GoodDataForeignDataWrapper as fdw
from tests import TEST_WORKSPACE
from tests.import_foreign_schema import _tables_to_dict

_current_dir = os.path.dirname(os.path.abspath(__file__))
_fixtures_dir = os.path.join(_current_dir, "fixtures")

gd_vcr = vcr.VCR(filter_headers=["authorization"], serializer="json")


@gd_vcr.use_cassette(
    os.path.join(_fixtures_dir, "import_insights_without_restrictions.json")
)
def test_import_insights_without_restrictions(import_srv_options):
    tables = fdw.import_schema(
        schema="gooddata_insights",
        srv_options=import_srv_options,
        options=dict(workspace=TEST_WORKSPACE),
        restriction_type=None,
        restricts=[],
    )

    # do a rough rub now.. there are 8 stable insights in the insurance-demo.. those should be mapped to
    # tables. then pick a couple of tables and make sure their columns are looking ok

    assert len(tables) == 9

    tables_idx = _tables_to_dict(tables)
    premium_revenue_structure = tables_idx["premium_revenue_structure"]
    kpi_claim = tables_idx["kpi_claim"]

    assert "car_car_make" in premium_revenue_structure.col_idx
    assert premium_revenue_structure.col_idx["car_car_make"].type_name == "VARCHAR(255)"
    assert "local_id" in premium_revenue_structure.col_idx["car_car_make"].options

    assert "customer_customer_age_group" in premium_revenue_structure.col_idx
    assert (
        premium_revenue_structure.col_idx["customer_customer_age_group"].type_name
        == "VARCHAR(255)"
    )
    assert (
        "local_id"
        in premium_revenue_structure.col_idx["customer_customer_age_group"].options
    )

    assert "premium_revenue" in premium_revenue_structure.col_idx
    assert (
        premium_revenue_structure.col_idx["premium_revenue"].type_name
        == "DECIMAL(15,5)"
    )
    assert "local_id" in premium_revenue_structure.col_idx["premium_revenue"].options

    assert "claim_amount" in kpi_claim.col_idx
    assert kpi_claim.col_idx["claim_amount"].type_name == "DECIMAL(15,5)"
    assert "local_id" in kpi_claim.col_idx["claim_amount"].options
