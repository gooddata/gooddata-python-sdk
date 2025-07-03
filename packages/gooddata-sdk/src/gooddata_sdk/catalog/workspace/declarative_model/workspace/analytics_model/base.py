# (C) 2024 GoodData Corporation
from pathlib import Path
from typing import Any, Optional, TypeVar

from attrs import define

from gooddata_sdk.catalog.base import Base
from gooddata_sdk.catalog.identifier import CatalogUserIdentifier
from gooddata_sdk.utils import read_layout_from_file, write_layout_to_file

T = TypeVar("T", bound="CatalogAnalyticsObjectBase")


@define(auto_attribs=True, kw_only=True)
class CatalogAnalyticsObjectBase(Base):
    id: str

    def store_to_disk(self, analytics_folder: Path) -> None:
        analytics_file = analytics_folder / f"{self.id}.yaml"
        write_layout_to_file(analytics_file, self.to_api().to_dict(camel_case=True))

    @classmethod
    def load_from_disk(cls: type[T], analytics_file: Path) -> T:
        analytics_layout = read_layout_from_file(analytics_file)
        return cls.from_dict(analytics_layout)


@define(auto_attribs=True, kw_only=True)
class CatalogAnalyticsBaseMeta(CatalogAnalyticsObjectBase):
    created_at: Optional[str] = None
    created_by: Optional[CatalogUserIdentifier] = None
    modified_at: Optional[str] = None
    modified_by: Optional[CatalogUserIdentifier] = None


@define(auto_attribs=True, kw_only=True)
class CatalogAnalyticsBase(CatalogAnalyticsBaseMeta):
    title: str
    content: dict[str, Any]
    description: Optional[str] = None
    tags: Optional[list[str]] = None
