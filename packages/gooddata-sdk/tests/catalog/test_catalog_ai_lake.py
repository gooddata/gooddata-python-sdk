# (C) 2026 GoodData Corporation
"""Integration tests for AI Lake SDK methods backed by VCR cassettes.

These tests exercise the HTTP surface of `CatalogAILakeService`.  Each test
needs a cassette recorded against a live stack; the cassette files are created
by the recorder and are not hand-edited.
"""

from __future__ import annotations

from pathlib import Path

import pytest
from gooddata_sdk import CatalogObjectStorageInfo, GoodDataSdk
from tests_support.vcrpy_utils import get_vcr

gd_vcr = get_vcr()

_current_dir = Path(__file__).parent.absolute()
_fixtures_dir = _current_dir / "fixtures" / "ai_lake"

_cassette_list_object_storages = _fixtures_dir / "test_list_ai_lake_object_storages.yaml"


@pytest.mark.skipif(
    not _cassette_list_object_storages.exists(),
    reason="Cassette not yet recorded — requires an AI Lake-enabled environment",
)
@gd_vcr.use_cassette(str(_cassette_list_object_storages))
def test_list_ai_lake_object_storages(test_config):
    """List registered AI Lake ObjectStorages and verify the response shape."""
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    storages = sdk.catalog_ai_lake.list_object_storages()

    assert isinstance(storages, list)
    for storage in storages:
        assert isinstance(storage, CatalogObjectStorageInfo)
        assert storage.name, "name must be non-empty"
        assert storage.storage_id, "storage_id must be non-empty"
        assert storage.storage_type, "storage_type must be non-empty"
        assert isinstance(storage.storage_config, dict)
