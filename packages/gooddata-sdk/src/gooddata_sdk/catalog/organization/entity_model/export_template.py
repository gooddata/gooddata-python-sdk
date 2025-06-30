# (C) 2025 GoodData Corporation
from __future__ import annotations

import builtins
from typing import Optional

from attrs import define
from gooddata_api_client.model.json_api_export_template_in_attributes import JsonApiExportTemplateInAttributes
from gooddata_api_client.model.json_api_export_template_post_optional_id import JsonApiExportTemplatePostOptionalId

from gooddata_sdk.catalog.base import Base
from gooddata_sdk.catalog.organization.common.dashboard_slides_template import CatalogDashboardSlidesTemplate
from gooddata_sdk.catalog.organization.common.widget_slides_template import CatalogWidgetSlidesTemplate


@define(auto_attribs=True, kw_only=True)
class CatalogExportTemplate(Base):
    id: str
    attributes: Optional[CatalogExportTemplateAttributes] = None

    @staticmethod
    def client_class() -> builtins.type[JsonApiExportTemplatePostOptionalId]:
        return JsonApiExportTemplatePostOptionalId


@define(auto_attribs=True, kw_only=True)
class CatalogExportTemplateAttributes(Base):
    name: str
    dashboard_slides_template: Optional[CatalogDashboardSlidesTemplate] = None
    widget_slides_template: Optional[CatalogWidgetSlidesTemplate] = None

    @staticmethod
    def client_class() -> builtins.type[JsonApiExportTemplateInAttributes]:
        return JsonApiExportTemplateInAttributes
