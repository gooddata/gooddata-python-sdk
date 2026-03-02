# (C) 2025 GoodData Corporation

from attrs import define

from gooddata_sdk.catalog.base import Base
from gooddata_sdk.catalog.organization.common.running_section import CatalogRunningSection


@define
class CatalogCoverSlideTemplate(Base):
    background_image: bool
    description_field: str | None = None
    header: CatalogRunningSection | None = None
    footer: CatalogRunningSection | None = None


@define
class CatalogIntroSlideTemplate(Base):
    background_image: bool
    title_field: str | None = None
    description_field: str | None = None
    header: CatalogRunningSection | None = None
    footer: CatalogRunningSection | None = None


@define
class CatalogSectionSlideTemplate(Base):
    background_image: bool
    header: CatalogRunningSection | None = None
    footer: CatalogRunningSection | None = None


@define
class CatalogContentSlideTemplate(Base):
    description_field: str | None = None
    header: CatalogRunningSection | None = None
    footer: CatalogRunningSection | None = None
