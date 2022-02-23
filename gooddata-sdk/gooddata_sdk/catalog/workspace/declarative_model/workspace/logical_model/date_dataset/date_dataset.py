# (C) 2022 GoodData Corporation
from __future__ import annotations

from typing import Any

from gooddata_metadata_client.model.declarative_date_dataset import DeclarativeDateDataset
from gooddata_metadata_client.model.granularities_formatting import GranularitiesFormatting
from gooddata_sdk.catalog.entity import CatalogTitleEntity


class CatalogDeclarativeDateDataset(CatalogTitleEntity):
    def __init__(
        self,
        id: str,
        title: str,
        granularities_formatting: CatalogGranularitiesFormatting,
        granularities: list[str],
        description: str = None,
        tags: list[str] = None,
    ):
        super(CatalogDeclarativeDateDataset, self).__init__(id, title)
        self.granularities_formatting = granularities_formatting
        self.granularities = granularities
        self.description = description
        self.tags = tags

    @classmethod
    def from_api(cls, entity: dict[str, Any]) -> CatalogDeclarativeDateDataset:
        return cls(
            entity["id"],
            entity["title"],
            CatalogGranularitiesFormatting.from_api(entity["granularities_formatting"]),
            entity["granularities"],
            entity.get("description"),
            entity.get("tags"),
        )

    def to_api(self) -> DeclarativeDateDataset:
        kwargs: dict[str, Any] = dict()
        if self.description:
            kwargs["description"] = self.description
        if self.tags:
            kwargs["tags"] = self.tags
        return DeclarativeDateDataset(
            self.id, self.title, self.granularities_formatting.to_api(), self.granularities, **kwargs
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, CatalogDeclarativeDateDataset):
            return False
        return (
            self.id == other.id
            and self.title == other.title
            and self.granularities_formatting == other.granularities_formatting
            and self.granularities == other.granularities
            and self.description == other.description
            and self.tags == other.tags
        )


class CatalogGranularitiesFormatting:
    def __init__(self, title_base: str, title_pattern: str):
        self.title_base = title_base
        self.title_pattern = title_pattern

    @classmethod
    def from_api(cls, entity: dict[str, Any]) -> CatalogGranularitiesFormatting:
        return cls(entity["title_base"], entity["title_pattern"])

    def to_api(self) -> GranularitiesFormatting:
        return GranularitiesFormatting(self.title_base, self.title_pattern)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, CatalogGranularitiesFormatting):
            return False
        return self.title_base == other.title_base and self.title_pattern == other.title_pattern
