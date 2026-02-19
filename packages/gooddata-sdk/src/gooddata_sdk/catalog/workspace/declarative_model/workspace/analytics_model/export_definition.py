# (C) 2024 GoodData Corporation

from attrs import define
from gooddata_api_client.model.declarative_export_definition import DeclarativeExportDefinition
from gooddata_api_client.model.declarative_export_definition_request_payload import (
    DeclarativeExportDefinitionRequestPayload,
)

from gooddata_sdk import ExportCustomOverride, ExportSettings
from gooddata_sdk.catalog.base import Base
from gooddata_sdk.catalog.workspace.declarative_model.workspace.analytics_model.base import CatalogAnalyticsBaseMeta


@define(auto_attribs=True, kw_only=True)
class CatalogDeclarativeExportDefinitionRequestPayload(Base):
    custom_override: ExportCustomOverride | None = None
    execution_result: str | None = None
    metadata: dict | None = None
    related_dashboard_id: str | None = None
    settings: ExportSettings | None = None
    visualization_object: str | None = None
    visualization_object_custom_filters: list[dict] | None = None
    file_name: str | None = None
    format: str | None = None
    dashboard_id: str | None = None

    @staticmethod
    def client_class() -> type[DeclarativeExportDefinitionRequestPayload]:
        return DeclarativeExportDefinitionRequestPayload


@define(auto_attribs=True, kw_only=True)
class CatalogDeclarativeExportDefinition(CatalogAnalyticsBaseMeta):
    id: str
    title: str
    request_payload: CatalogDeclarativeExportDefinitionRequestPayload
    description: str | None = None
    tags: list[str] | None = None

    @staticmethod
    def client_class() -> type[DeclarativeExportDefinition]:
        return DeclarativeExportDefinition
