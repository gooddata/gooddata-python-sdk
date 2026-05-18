# (C) 2026 GoodData Corporation
"""Integration tests for `CatalogAILakeService`."""

from __future__ import annotations

from pathlib import Path

from gooddata_sdk import CatalogObjectStorageInfo, GoodDataSdk
from tests_support.vcrpy_utils import get_vcr

gd_vcr = get_vcr()

_current_dir = Path(__file__).parent.absolute()
_fixtures_dir = _current_dir / "fixtures" / "ai_lake"


@gd_vcr.use_cassette(str(_fixtures_dir / "test_list_object_storages.yaml"))
def test_list_object_storages(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    storages = sdk.catalog_ai_lake.list_object_storages()
    assert isinstance(storages, list)
    for s in storages:
        assert isinstance(s, CatalogObjectStorageInfo)
        assert s.name
        assert s.storage_id
        assert s.storage_type
