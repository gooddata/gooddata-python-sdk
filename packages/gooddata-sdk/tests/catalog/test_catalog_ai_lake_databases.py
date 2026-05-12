# (C) 2026 GoodData Corporation
"""Integration tests for AI Lake database data-source management.

These tests exercise the four new data-source CRUD methods on
``CatalogAILakeService``:

- ``list_database_data_sources``
- ``add_database_data_source``
- ``remove_database_data_source``
- ``update_database_data_source``

Each test function is backed by a VCR cassette that records / replays the
HTTP interaction. The cassettes do not exist yet — they are generated when
the test suite is run against a live server with VCR in record mode.

Assumptions about the test environment (staging / local Docker):
- ``test_config["ai_lake_instance_id"]`` names a pre-existing AI Lake
  database instance that the test account can manage.
- The instance already has at least one data source at test start so that
  ``list_database_data_sources`` returns a non-empty list.
- The test adds, updates, then removes a *second* data source so that the
  primary data source is never touched.
"""

from __future__ import annotations

from pathlib import Path

from gooddata_sdk import CatalogDataSourceInfo, GoodDataSdk
from tests_support.vcrpy_utils import get_vcr

gd_vcr = get_vcr()

_current_dir = Path(__file__).parent.absolute()
_fixtures_dir = _current_dir / "fixtures" / "ai_lake_databases"

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_TEST_DS_ID = "sdk-test-ds-secondary"
_TEST_DS_NAME = "SDK Test Secondary DS"
_TEST_DS_ID_RENAMED = "sdk-test-ds-secondary-v2"
_TEST_DS_NAME_RENAMED = "SDK Test Secondary DS v2"


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


@gd_vcr.use_cassette(str(_fixtures_dir / "test_list_database_data_sources.yaml"))
def test_list_database_data_sources(test_config):
    """list_database_data_sources returns a non-empty list of CatalogDataSourceInfo."""
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    instance_id = test_config["ai_lake_instance_id"]

    result = sdk.catalog_ai_lake.list_database_data_sources(instance_id)

    assert isinstance(result, list)
    assert len(result) >= 1
    for ds_info in result:
        assert isinstance(ds_info, CatalogDataSourceInfo)
        assert ds_info.data_source_id
        assert ds_info.data_source_name
        assert ds_info.id is not None


@gd_vcr.use_cassette(str(_fixtures_dir / "test_add_database_data_source.yaml"))
def test_add_database_data_source(test_config):
    """add_database_data_source creates a new association and returns CatalogDataSourceInfo."""
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    instance_id = test_config["ai_lake_instance_id"]

    try:
        result = sdk.catalog_ai_lake.add_database_data_source(
            instance_id,
            _TEST_DS_ID,
            data_source_name=_TEST_DS_NAME,
        )

        assert isinstance(result, CatalogDataSourceInfo)
        assert result.data_source_id == _TEST_DS_ID
        assert result.data_source_name == _TEST_DS_NAME
        assert result.id is not None

        # Confirm it shows up in the list
        sources = sdk.catalog_ai_lake.list_database_data_sources(instance_id)
        ids = [s.data_source_id for s in sources]
        assert _TEST_DS_ID in ids
    finally:
        # Clean up: remove the test data source if it was created
        try:
            sdk.catalog_ai_lake.remove_database_data_source(instance_id, _TEST_DS_ID)
        except Exception:
            pass


@gd_vcr.use_cassette(str(_fixtures_dir / "test_remove_database_data_source.yaml"))
def test_remove_database_data_source(test_config):
    """remove_database_data_source removes the association and returns the data_source_id."""
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    instance_id = test_config["ai_lake_instance_id"]

    # First add a data source to remove
    sdk.catalog_ai_lake.add_database_data_source(
        instance_id,
        _TEST_DS_ID,
        data_source_name=_TEST_DS_NAME,
    )

    removed_id = sdk.catalog_ai_lake.remove_database_data_source(instance_id, _TEST_DS_ID)

    assert removed_id == _TEST_DS_ID

    # Confirm it no longer shows up in the list
    sources = sdk.catalog_ai_lake.list_database_data_sources(instance_id)
    ids = [s.data_source_id for s in sources]
    assert _TEST_DS_ID not in ids


@gd_vcr.use_cassette(str(_fixtures_dir / "test_update_database_data_source.yaml"))
def test_update_database_data_source(test_config):
    """update_database_data_source renames the data source and returns updated info."""
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    instance_id = test_config["ai_lake_instance_id"]

    # Add a data source first
    sdk.catalog_ai_lake.add_database_data_source(
        instance_id,
        _TEST_DS_ID,
        data_source_name=_TEST_DS_NAME,
    )

    try:
        result = sdk.catalog_ai_lake.update_database_data_source(
            instance_id,
            old_data_source_id=_TEST_DS_ID,
            new_data_source_id=_TEST_DS_ID_RENAMED,
            data_source_name=_TEST_DS_NAME_RENAMED,
        )

        assert isinstance(result, CatalogDataSourceInfo)
        assert result.data_source_id == _TEST_DS_ID_RENAMED
        assert result.data_source_name == _TEST_DS_NAME_RENAMED
        # id is None for update responses (not returned by the endpoint)
        assert result.id is None

        # Confirm new ID is visible in the list
        sources = sdk.catalog_ai_lake.list_database_data_sources(instance_id)
        ids = [s.data_source_id for s in sources]
        assert _TEST_DS_ID_RENAMED in ids
        assert _TEST_DS_ID not in ids
    finally:
        # Remove the renamed data source
        try:
            sdk.catalog_ai_lake.remove_database_data_source(instance_id, _TEST_DS_ID_RENAMED)
        except Exception:
            pass
