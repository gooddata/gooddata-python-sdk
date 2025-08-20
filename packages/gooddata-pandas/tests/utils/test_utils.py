# (C) 2025 GoodData Corporation
from pathlib import Path

from gooddata_pandas.utils import get_catalog_attributes_for_extract
from gooddata_sdk import (
    Attribute,
    GoodDataSdk,
)
from tests_support.vcrpy_utils import get_vcr

gd_vcr = get_vcr()

_current_dir = Path(__file__).parent.absolute()
_fixtures_dir = _current_dir / "fixtures"


@gd_vcr.use_cassette(str(_fixtures_dir / "test_get_catalog_attributes_for_extract.yaml"))
def test_get_catalog_attributes_for_extract(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    workspace_id = "demo"
    attributes = [Attribute(local_id="0", label="campaign_name"), Attribute(local_id="1", label="region")]
    catalog_attributes = get_catalog_attributes_for_extract(sdk, workspace_id, attributes, character_limit=28)
    assert len(catalog_attributes) == 2
    assert [ca.id for ca in catalog_attributes] == ["campaign_name", "region"]
