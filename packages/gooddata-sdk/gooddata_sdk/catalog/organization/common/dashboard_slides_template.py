# (C) 2025 GoodData Corporation
from typing import Literal, Optional

from attrs import define

from gooddata_sdk.catalog.organization.common.slide_template import (
    CatalogContentSlideTemplate,
    CatalogCoverSlideTemplate,
    CatalogIntroSlideTemplate,
    CatalogSectionSlideTemplate,
)


@define
class CatalogDashboardSlidesTemplate:
    applied_on: list[Literal["PDF", "PPTX"]]
    cover_slide: Optional[CatalogCoverSlideTemplate] = None
    intro_slide: Optional[CatalogIntroSlideTemplate] = None
    section_slide: Optional[CatalogSectionSlideTemplate] = None
    content_slide: Optional[CatalogContentSlideTemplate] = None
