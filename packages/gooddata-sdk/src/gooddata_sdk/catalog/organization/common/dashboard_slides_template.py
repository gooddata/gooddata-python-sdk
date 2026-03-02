# (C) 2025 GoodData Corporation
from typing import Literal

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
    cover_slide: CatalogCoverSlideTemplate | None = None
    intro_slide: CatalogIntroSlideTemplate | None = None
    section_slide: CatalogSectionSlideTemplate | None = None
    content_slide: CatalogContentSlideTemplate | None = None
