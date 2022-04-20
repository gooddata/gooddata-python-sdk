# (C) 2022 GoodData Corporation
from __future__ import annotations

from pathlib import Path

import vcr

from gooddata_sdk import GoodDataSdk
from tests import VCR_MATCH_ON

_current_dir = Path(__file__).parent.absolute()
_fixtures_dir = _current_dir / "fixtures" / "organization"

gd_vcr = vcr.VCR(filter_headers=["authorization", "user-agent"], serializer="json", match_on=VCR_MATCH_ON)


@gd_vcr.use_cassette(str(_fixtures_dir / "organization.json"))
def test_get_organization(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    organization = sdk.catalog_organization.get_organization()
    assert organization.id == "default"
    assert organization.name == "Default Organization"
    assert organization.hostname == "localhost"
