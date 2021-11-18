# (C) 2021 GoodData Corporation
from __future__ import annotations
import os

import vcr

from gooddata_sdk import GoodDataSdk
from tests import TEST_HOST, test_token, TEST_WORKSPACE

_current_dir = os.path.dirname(os.path.abspath(__file__))
_fixtures_dir = os.path.join(_current_dir, "fixtures")

gd_vcr = vcr.VCR(filter_headers=["authorization"], serializer="json")


@gd_vcr.use_cassette(os.path.join(_fixtures_dir, "insurance_demo_catalog.json"))
def test_catalog_load():
    sdk = GoodDataSdk.new(host=TEST_HOST, token=test_token())
    catalog = sdk.catalog.get_full_catalog(TEST_WORKSPACE)

    # rough initial smoke-test; just do a quick 'rub'
    assert len(catalog.metrics) == 25
    assert len(catalog.datasets) == 9

    assert catalog.get_metric("claim-count") is not None
    assert catalog.get_metric("total-car-count") is not None
    assert catalog.get_dataset("region") is not None
    assert catalog.get_dataset("claim") is not None
    assert catalog.get_dataset("coverage_cancelled_date") is not None


@gd_vcr.use_cassette(os.path.join(_fixtures_dir, "insurance_demo_catalog_availability.json"))
def test_catalog_availability():
    sdk = GoodDataSdk.new(host=TEST_HOST, token=test_token())
    catalog = sdk.catalog.get_full_catalog(TEST_WORKSPACE)
    claim_count = catalog.get_metric("claim-count")

    filtered_catalog = catalog.catalog_with_valid_objects(claim_count)

    # rough initial smoke-test; just do a quick 'rub' that filtered catalog has less entries than full catalog
    assert len(filtered_catalog.metrics) == 25
    assert len(filtered_catalog.datasets) == 7
