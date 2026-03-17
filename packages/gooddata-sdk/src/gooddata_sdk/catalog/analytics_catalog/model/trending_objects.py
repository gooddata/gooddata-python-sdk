# (C) 2024 GoodData Corporation
from __future__ import annotations

from datetime import datetime

import attrs


@attrs.define(kw_only=True)
class CatalogTrendingObjectItem:
    """Represents a trending object in the Analytics Catalog."""

    id: str
    tags: list[str]
    title: str
    type: str
    usage_count: int
    workspace_id: str
    created_at: datetime | None = None
    created_by: str | None = None
    dataset_id: str | None = None
    dataset_title: str | None = None
    dataset_type: str | None = None
    description: str | None = None
    is_hidden: bool | None = None
    is_hidden_from_kda: bool | None = None
    metric_type: str | None = None
    modified_at: datetime | None = None
    modified_by: str | None = None
    visualization_url: str | None = None

    @classmethod
    def from_api_model(cls, api_model: object) -> CatalogTrendingObjectItem:
        return cls(
            id=api_model.id,
            tags=list(api_model.tags),
            title=api_model.title,
            type=api_model.type,
            usage_count=api_model.usage_count,
            workspace_id=api_model.workspace_id,
            created_at=getattr(api_model, "created_at", None),
            created_by=getattr(api_model, "created_by", None),
            dataset_id=getattr(api_model, "dataset_id", None),
            dataset_title=getattr(api_model, "dataset_title", None),
            dataset_type=getattr(api_model, "dataset_type", None),
            description=getattr(api_model, "description", None),
            is_hidden=getattr(api_model, "is_hidden", None),
            is_hidden_from_kda=getattr(api_model, "is_hidden_from_kda", None),
            metric_type=getattr(api_model, "metric_type", None),
            modified_at=getattr(api_model, "modified_at", None),
            modified_by=getattr(api_model, "modified_by", None),
            visualization_url=getattr(api_model, "visualization_url", None),
        )


@attrs.define(kw_only=True)
class CatalogTrendingObjectsResult:
    """Represents the result of a trending objects query."""

    objects: list[CatalogTrendingObjectItem] = attrs.field(factory=list)

    @classmethod
    def from_api_model(cls, api_model: object) -> CatalogTrendingObjectsResult:
        return cls(
            objects=[CatalogTrendingObjectItem.from_api_model(item) for item in api_model.objects],
        )
