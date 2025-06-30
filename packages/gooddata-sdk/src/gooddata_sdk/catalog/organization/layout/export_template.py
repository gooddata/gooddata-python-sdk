# (C) 2025 GoodData Corporation
import builtins
from typing import Optional

from attrs import define
from gooddata_api_client.model.declarative_export_template import DeclarativeExportTemplate

from gooddata_sdk.catalog.base import Base
from gooddata_sdk.catalog.organization.common.dashboard_slides_template import CatalogDashboardSlidesTemplate
from gooddata_sdk.catalog.organization.common.widget_slides_template import CatalogWidgetSlidesTemplate


@define
class CatalogDeclarativeExportTemplate(Base):
    id: str
    name: str
    dashboard_slides_template: Optional[CatalogDashboardSlidesTemplate] = None
    widget_slides_template: Optional[CatalogWidgetSlidesTemplate] = None

    @staticmethod
    def client_class() -> builtins.type[DeclarativeExportTemplate]:
        return DeclarativeExportTemplate
