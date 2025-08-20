# (C) 2024 GoodData Corporation
from typing import Optional

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
    custom_override: Optional[ExportCustomOverride] = None
    execution_result: Optional[str] = None
    metadata: Optional[dict] = None
    related_dashboard_id: Optional[str] = None
    settings: Optional[ExportSettings] = None
    visualization_object: Optional[str] = None
    visualization_object_custom_filters: Optional[list[dict]] = None
    file_name: Optional[str] = None
    format: Optional[str] = None
    dashboard_id: Optional[str] = None

    @staticmethod
    def client_class() -> type[DeclarativeExportDefinitionRequestPayload]:
        return DeclarativeExportDefinitionRequestPayload


@define(auto_attribs=True, kw_only=True)
class CatalogDeclarativeExportDefinition(CatalogAnalyticsBaseMeta):
    id: str
    title: str
    request_payload: CatalogDeclarativeExportDefinitionRequestPayload
    description: Optional[str] = None
    tags: Optional[list[str]] = None

    @staticmethod
    def client_class() -> type[DeclarativeExportDefinition]:
        return DeclarativeExportDefinition
