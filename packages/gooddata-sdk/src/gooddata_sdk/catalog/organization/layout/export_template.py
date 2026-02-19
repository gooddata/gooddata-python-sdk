# (C) 2025 GoodData Corporation
import builtins

from attrs import define
from gooddata_api_client.model.declarative_export_template import DeclarativeExportTemplate

from gooddata_sdk.catalog.base import Base
from gooddata_sdk.catalog.organization.common.dashboard_slides_template import CatalogDashboardSlidesTemplate
from gooddata_sdk.catalog.organization.common.widget_slides_template import CatalogWidgetSlidesTemplate


@define
class CatalogDeclarativeExportTemplate(Base):
    id: str
    name: str
    dashboard_slides_template: CatalogDashboardSlidesTemplate | None = None
    widget_slides_template: CatalogWidgetSlidesTemplate | None = None

    @staticmethod
    def client_class() -> builtins.type[DeclarativeExportTemplate]:
        return DeclarativeExportTemplate
