# (C) 2024 GoodData Corporation
import builtins
from typing import Any

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
    cron_description: str | None = field(default=None, eq=False)
    first_run: str | None = None
    timezone: str | None = "UTC"

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
    description: str | None = None
    details: dict[str, Any] | None = None
    state: str | None = None
    tags: list[str] | None = None
    title: str | None = None
    recipients: list[CatalogUserIdentifier] | None = None
    metadata: dict | None = None
    export_definitions: list[CatalogExportDefinitionIdentifier] | None = None
    notification_channel: CatalogNotificationChannelIdentifier | None = None
    schedule: CatalogAutomationSchedule | None = None
    tabular_exports: list[CatalogAutomationTabularExport] | None = None
    visual_exports: list[CatalogAutomationVisualExport] | None = None

    @staticmethod
    def client_class() -> builtins.type[DeclarativeAutomation]:
        return DeclarativeAutomation
