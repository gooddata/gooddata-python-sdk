# (C) 2021 GoodData Corporation
from __future__ import annotations

from pathlib import Path

import vcr

from gooddata_sdk import GoodDataSdk
from tests import VCR_MATCH_ON

_current_dir = Path(__file__).parent.absolute()
_fixtures_dir = _current_dir / "fixtures"

gd_vcr = vcr.VCR(filter_headers=["authorization", "user-agent"], serializer="json", match_on=VCR_MATCH_ON)


@gd_vcr.use_cassette(str(_fixtures_dir / "insurance_demo_catalog.json"))
def test_catalog_load(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    catalog = sdk.catalog.get_full_catalog(test_config["workspace"])

    # rough initial smoke-test; just do a quick 'rub'
    assert len(catalog.metrics) == 24
    assert len(catalog.datasets) == 6

    assert catalog.get_metric("order_amount") is not None
    assert catalog.get_metric("revenue") is not None
    assert catalog.get_dataset("customers") is not None
    assert catalog.get_dataset("order_lines") is not None
    assert catalog.get_dataset("products") is not None


@gd_vcr.use_cassette(str(_fixtures_dir / "insurance_demo_catalog_availability.json"))
def test_catalog_availability(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    catalog = sdk.catalog.get_full_catalog(test_config["workspace"])
    claim_count = catalog.get_metric("campaign_spend")

    filtered_catalog = catalog.catalog_with_valid_objects(claim_count)

    # rough initial smoke-test; just do a quick 'rub' that filtered catalog has less entries than full catalog
    assert len(filtered_catalog.metrics) == 24
    assert len(filtered_catalog.datasets) == 3
