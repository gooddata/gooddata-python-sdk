# (C) 2025 GoodData Corporation
from typing import Optional

from attrs import define

from gooddata_sdk.catalog.base import Base
from gooddata_sdk.catalog.organization.common.running_section import CatalogRunningSection


@define
class CatalogCoverSlideTemplate(Base):
    background_image: bool
    description_field: Optional[str] = None
    header: Optional[CatalogRunningSection] = None
    footer: Optional[CatalogRunningSection] = None


@define
class CatalogIntroSlideTemplate(Base):
    background_image: bool
    title_field: Optional[str] = None
    description_field: Optional[str] = None
    header: Optional[CatalogRunningSection] = None
    footer: Optional[CatalogRunningSection] = None


@define
class CatalogSectionSlideTemplate(Base):
    background_image: bool
    header: Optional[CatalogRunningSection] = None
    footer: Optional[CatalogRunningSection] = None


@define
class CatalogContentSlideTemplate(Base):
    description_field: Optional[str] = None
    header: Optional[CatalogRunningSection] = None
    footer: Optional[CatalogRunningSection] = None
