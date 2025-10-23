# (C) 2024 GoodData Corporation
import builtins
from typing import Any, Optional

from attrs import define, field
from gooddata_api_client.model.automation_schedule import AutomationSchedule
from gooddata_api_client.model.automation_tabular_export import AutomationTabularExport
from gooddata_api_client.model.automation_visual_export import AutomationVisualExport
from gooddata_api_client.model.declarative_automation import DeclarativeAutomation

from gooddata_sdk.catalog.base import Base
from gooddata_sdk.catalog.export.request import (
    ExportRequest,
    VisualExportRequest,
)
from gooddata_sdk.catalog.identifier import (
    CatalogExportDefinitionIdentifier,
    CatalogNotificationChannelIdentifier,
    CatalogUserIdentifier,
)
from gooddata_sdk.catalog.workspace.declarative_model.workspace.analytics_model.base import CatalogAnalyticsBaseMeta


@define(auto_attribs=True, kw_only=True)
class CatalogAutomationSchedule(Base):
    cron: str
    cron_description: Optional[str] = field(default=None, eq=False)
    first_run: Optional[str] = None
    timezone: Optional[str] = "UTC"

    @staticmethod
    def client_class() -> builtins.type[AutomationSchedule]:
        return AutomationSchedule


@define(auto_attribs=True, kw_only=True)
class CatalogAutomationTabularExport(Base):
    request_payload: ExportRequest

    @staticmethod
    def client_class() -> builtins.type[AutomationTabularExport]:
        return AutomationTabularExport


@define(auto_attribs=True, kw_only=True)
class CatalogAutomationVisualExport(Base):
    request_payload: VisualExportRequest

    @staticmethod
    def client_class() -> builtins.type[AutomationVisualExport]:
        return AutomationVisualExport


@define(auto_attribs=True, kw_only=True)
class CatalogDeclarativeAutomation(CatalogAnalyticsBaseMeta):
    description: Optional[str] = None
    details: Optional[dict[str, Any]] = None
    state: Optional[str] = None
    tags: Optional[list[str]] = None
    title: Optional[str] = None
    recipients: Optional[list[CatalogUserIdentifier]] = None
    metadata: Optional[dict] = None
    export_definitions: Optional[list[CatalogExportDefinitionIdentifier]] = None
    notification_channel: Optional[CatalogNotificationChannelIdentifier] = None
    schedule: Optional[CatalogAutomationSchedule] = None
    tabular_exports: Optional[list[CatalogAutomationTabularExport]] = None
    visual_exports: Optional[list[CatalogAutomationVisualExport]] = None

    @staticmethod
    def client_class() -> builtins.type[DeclarativeAutomation]:
        return DeclarativeAutomation
