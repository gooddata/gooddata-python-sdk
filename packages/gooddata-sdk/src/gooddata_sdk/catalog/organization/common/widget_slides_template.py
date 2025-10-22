# (C) 2025 GoodData Corporation
from typing import Literal, Optional

from attrs import define

from gooddata_sdk.catalog.organization.common.slide_template import CatalogContentSlideTemplate


@define
class CatalogWidgetSlidesTemplate:
    applied_on: list[Literal["PDF", "PPTX"]]
    content_slide: Optional[CatalogContentSlideTemplate] = None
