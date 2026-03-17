# (C) 2024 GoodData Corporation
from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock

import pytest
from gooddata_sdk import CatalogTrendingObjectItem, CatalogTrendingObjectsResult, GoodDataSdk
from tests_support.vcrpy_utils import get_vcr

gd_vcr = get_vcr()

_fixtures_dir = Path(__file__).parent / "fixtures"


def _make_mock_item(
    id: str = "obj-1",
    title: str = "Revenue Dashboard",
    type: str = "dashboard",
    usage_count: int = 42,
    workspace_id: str = "ws-1",
    tags: list | None = None,
) -> MagicMock:
    item = MagicMock()
    item.id = id
    item.title = title
    item.type = type
    item.usage_count = usage_count
    item.workspace_id = workspace_id
    item.tags = tags or []
    # optional fields not set
    item.configure_mock(**{attr: None for attr in [
        "created_at", "created_by", "dataset_id", "dataset_title",
        "dataset_type", "description", "is_hidden", "is_hidden_from_kda",
        "metric_type", "modified_at", "modified_by", "visualization_url",
    ]})
    return item


def test_catalog_trending_object_item_from_api_model():
    """Unit test: CatalogTrendingObjectItem.from_api_model converts required fields correctly."""
    mock_item = _make_mock_item(
        id="dash-1",
        title="My Dashboard",
        type="dashboard",
        usage_count=10,
        workspace_id="workspace-123",
        tags=["finance", "monthly"],
    )

    result = CatalogTrendingObjectItem.from_api_model(mock_item)

    assert result.id == "dash-1"
    assert result.title == "My Dashboard"
    assert result.type == "dashboard"
    assert result.usage_count == 10
    assert result.workspace_id == "workspace-123"
    assert result.tags == ["finance", "monthly"]
    assert result.created_at is None
    assert result.description is None


def test_catalog_trending_objects_result_from_api_model():
    """Unit test: CatalogTrendingObjectsResult.from_api_model converts a list of items correctly."""
    item1 = _make_mock_item(id="obj-1", title="Dashboard A", type="dashboard", usage_count=5, workspace_id="ws-1")
    item2 = _make_mock_item(id="obj-2", title="Metric B", type="metric", usage_count=3, workspace_id="ws-1")

    mock_result = MagicMock()
    mock_result.objects = [item1, item2]

    result = CatalogTrendingObjectsResult.from_api_model(mock_result)

    assert len(result.objects) == 2
    assert result.objects[0].id == "obj-1"
    assert result.objects[1].id == "obj-2"
    assert result.objects[0].type == "dashboard"
    assert result.objects[1].type == "metric"


def test_catalog_trending_objects_result_empty():
    """Unit test: CatalogTrendingObjectsResult.from_api_model handles empty objects list."""
    mock_result = MagicMock()
    mock_result.objects = []

    result = CatalogTrendingObjectsResult.from_api_model(mock_result)

    assert result.objects == []


@gd_vcr.use_cassette(str(_fixtures_dir / "test_get_trending_objects.yaml"))
def test_get_trending_objects(test_config):
    """Integration test: get_trending_objects returns CatalogTrendingObjectsResult."""
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    workspace_id = test_config["workspace"]

    result = sdk.catalog_smart_functions.get_trending_objects(workspace_id=workspace_id)

    assert isinstance(result, CatalogTrendingObjectsResult)
    assert isinstance(result.objects, list)
    for item in result.objects:
        assert isinstance(item, CatalogTrendingObjectItem)
        assert item.id
        assert item.workspace_id
        assert item.usage_count >= 0
