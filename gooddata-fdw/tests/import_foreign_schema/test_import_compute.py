# (C) 2021 GoodData Corporation
import os

import vcr

from gooddata_fdw import GoodDataForeignDataWrapper as fdw
from tests import TEST_WORKSPACE

_current_dir = os.path.dirname(os.path.abspath(__file__))
_fixtures_dir = os.path.join(_current_dir, "fixtures")

gd_vcr = vcr.VCR(filter_headers=["authorization"], serializer="json")


@gd_vcr.use_cassette(os.path.join(_fixtures_dir, "import_compute_without_restrictions.json"))
def test_import_compute_without_restrictions(import_srv_options):
    tables = fdw.import_schema(
        schema=TEST_WORKSPACE,
        srv_options=import_srv_options,
        options=dict(object_type="compute", numeric_max_size="24"),
        restriction_type=None,
        restricts=[],
    )

    # do a rough rub now.. check well known facts, labels and metrics

    assert len(tables) == 1
    compute_table = tables[0]

    # metric
    assert "claim_amount" in compute_table.col_idx
    # fact with name-clash
    assert "claim_amount_1" in compute_table.col_idx
    # date attribute label
    assert "coverage_created_date_day" in compute_table.col_idx
    # normal label
    assert "car_gears" in compute_table.col_idx

    assert compute_table.col_idx["claim_amount"].type_name == "DECIMAL(24, 1)"
    assert compute_table.col_idx["claim_amount"].options["id"] == "metric/claim-amount"

    assert compute_table.col_idx["claim_amount_1"].type_name == "DECIMAL(24, 2)"
    assert compute_table.col_idx["claim_amount_1"].options["id"] == "fact/claim.claim_amount"

    assert compute_table.col_idx["coverage_created_date_day"].type_name == "DATE"
    assert compute_table.col_idx["coverage_created_date_day"].options["id"] == "label/coverage_created_date.day"

    assert compute_table.col_idx["car_gears"].type_name == "VARCHAR(255)"
    assert compute_table.col_idx["car_gears"].options["id"] == "label/car.car_gears"
