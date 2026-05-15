# (C) 2026 GoodData Corporation
"""Tests for AI Lake database data-source management.

These tests exercise the four new data-source CRUD methods on
``CatalogAILakeService``:

- ``list_database_data_sources``
- ``add_database_data_source``
- ``remove_database_data_source``
- ``update_database_data_source``

The tests use mocks against ``AILakeDatabasesApi`` rather than VCR cassettes
because the staging environment may not have an AI Lake entitlement.  The
service is a thin wrapper; its correctness is fully verifiable without a live
stack.
"""

from __future__ import annotations

from types import SimpleNamespace
from unittest.mock import MagicMock, patch

from gooddata_sdk import CatalogDataSourceInfo
from gooddata_sdk.catalog.ai_lake.service import CatalogAILakeService

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_INSTANCE_ID = "demo-ai-lake"
_TEST_DS_ID = "sdk-test-ds-secondary"
_TEST_DS_NAME = "SDK Test Secondary DS"
_TEST_DS_ID_RENAMED = "sdk-test-ds-secondary-v2"
_TEST_DS_NAME_RENAMED = "SDK Test Secondary DS v2"


def _make_service() -> tuple[CatalogAILakeService, MagicMock]:
    """Build a service whose api-client side is fully mocked."""
    fake_ai_lake_api = MagicMock(name="AILakeApi")
    fake_databases_api = MagicMock(name="AILakeDatabasesApi")
    fake_client = SimpleNamespace(_api_client=MagicMock(name="ApiClient"))

    with (
        patch("gooddata_sdk.catalog.ai_lake.service.AILakeApi", return_value=fake_ai_lake_api),
        patch("gooddata_sdk.catalog.ai_lake.service.AILakeDatabasesApi", return_value=fake_databases_api),
    ):
        service = CatalogAILakeService(fake_client)  # type: ignore[arg-type]

    return service, fake_databases_api


def _api_response(**fields: object) -> MagicMock:
    """Mimic the api-client's deserialized response (``.to_dict()`` returns the raw dict)."""
    response = MagicMock()
    response.to_dict.return_value = dict(fields)
    return response


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


def test_list_database_data_sources() -> None:
    """list_database_data_sources returns a non-empty list of CatalogDataSourceInfo."""
    service, api = _make_service()
    api.list_ai_lake_database_data_sources.return_value = _api_response(
        data_sources=[
            {"id": "assoc-1", "data_source_id": "primary-ds", "data_source_name": "Primary DS"},
        ]
    )

    result = service.list_database_data_sources(_INSTANCE_ID)

    assert isinstance(result, list)
    assert len(result) >= 1
    for ds_info in result:
        assert isinstance(ds_info, CatalogDataSourceInfo)
        assert ds_info.data_source_id
        assert ds_info.data_source_name
        assert ds_info.id is not None


def test_add_database_data_source() -> None:
    """add_database_data_source creates a new association and returns CatalogDataSourceInfo."""
    service, api = _make_service()
    api.add_ai_lake_database_data_source.return_value = _api_response(
        data_source={"id": "assoc-2", "data_source_id": _TEST_DS_ID, "data_source_name": _TEST_DS_NAME}
    )
    api.list_ai_lake_database_data_sources.return_value = _api_response(
        data_sources=[
            {"id": "assoc-1", "data_source_id": "primary-ds", "data_source_name": "Primary DS"},
            {"id": "assoc-2", "data_source_id": _TEST_DS_ID, "data_source_name": _TEST_DS_NAME},
        ]
    )
    api.remove_ai_lake_database_data_source.return_value = _api_response(data_source_id=_TEST_DS_ID)

    try:
        result = service.add_database_data_source(
            _INSTANCE_ID,
            _TEST_DS_ID,
            data_source_name=_TEST_DS_NAME,
        )

        assert isinstance(result, CatalogDataSourceInfo)
        assert result.data_source_id == _TEST_DS_ID
        assert result.data_source_name == _TEST_DS_NAME
        assert result.id is not None

        # Confirm it shows up in the list
        sources = service.list_database_data_sources(_INSTANCE_ID)
        ids = [s.data_source_id for s in sources]
        assert _TEST_DS_ID in ids
    finally:
        # Clean up: remove the test data source if it was created
        try:
            service.remove_database_data_source(_INSTANCE_ID, _TEST_DS_ID)
        except Exception:
            pass


def test_remove_database_data_source() -> None:
    """remove_database_data_source removes the association and returns the data_source_id."""
    service, api = _make_service()
    api.add_ai_lake_database_data_source.return_value = _api_response(
        data_source={"id": "assoc-2", "data_source_id": _TEST_DS_ID, "data_source_name": _TEST_DS_NAME}
    )
    api.remove_ai_lake_database_data_source.return_value = _api_response(data_source_id=_TEST_DS_ID)
    api.list_ai_lake_database_data_sources.return_value = _api_response(
        data_sources=[
            {"id": "assoc-1", "data_source_id": "primary-ds", "data_source_name": "Primary DS"},
        ]
    )

    # First add a data source to remove
    service.add_database_data_source(
        _INSTANCE_ID,
        _TEST_DS_ID,
        data_source_name=_TEST_DS_NAME,
    )

    removed_id = service.remove_database_data_source(_INSTANCE_ID, _TEST_DS_ID)

    assert removed_id == _TEST_DS_ID

    # Confirm it no longer shows up in the list
    sources = service.list_database_data_sources(_INSTANCE_ID)
    ids = [s.data_source_id for s in sources]
    assert _TEST_DS_ID not in ids


def test_update_database_data_source() -> None:
    """update_database_data_source renames the data source and returns updated info."""
    service, api = _make_service()
    api.add_ai_lake_database_data_source.return_value = _api_response(
        data_source={"id": "assoc-2", "data_source_id": _TEST_DS_ID, "data_source_name": _TEST_DS_NAME}
    )
    api.update_ai_lake_database_data_source.return_value = _api_response(
        data_source_id=_TEST_DS_ID_RENAMED,
        data_source_name=_TEST_DS_NAME_RENAMED,
    )
    api.list_ai_lake_database_data_sources.return_value = _api_response(
        data_sources=[
            {"id": "assoc-1", "data_source_id": "primary-ds", "data_source_name": "Primary DS"},
            {"id": "assoc-3", "data_source_id": _TEST_DS_ID_RENAMED, "data_source_name": _TEST_DS_NAME_RENAMED},
        ]
    )
    api.remove_ai_lake_database_data_source.return_value = _api_response(
        data_source_id=_TEST_DS_ID_RENAMED
    )

    # Add a data source first
    service.add_database_data_source(
        _INSTANCE_ID,
        _TEST_DS_ID,
        data_source_name=_TEST_DS_NAME,
    )

    try:
        result = service.update_database_data_source(
            _INSTANCE_ID,
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
        sources = service.list_database_data_sources(_INSTANCE_ID)
        ids = [s.data_source_id for s in sources]
        assert _TEST_DS_ID_RENAMED in ids
        assert _TEST_DS_ID not in ids
    finally:
        # Remove the renamed data source
        try:
            service.remove_database_data_source(_INSTANCE_ID, _TEST_DS_ID_RENAMED)
        except Exception:
            pass
