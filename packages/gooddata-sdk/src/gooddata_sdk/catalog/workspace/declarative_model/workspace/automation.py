# (C) 2024 GoodData Corporation
import builtins
from typing import Any

from attrs import define, field
from gooddata_api_client.model.automation_external_recipient import AutomationExternalRecipient
from gooddata_api_client.model.automation_image_export import AutomationImageExport
from gooddata_api_client.model.automation_schedule import AutomationSchedule
from gooddata_api_client.model.automation_slides_export import AutomationSlidesExport
from gooddata_api_client.model.automation_tabular_export import AutomationTabularExport
from gooddata_api_client.model.automation_visual_export import AutomationVisualExport
from gooddata_api_client.model.declarative_automation import DeclarativeAutomation

from gooddata_sdk.catalog.base import Base
from gooddata_sdk.catalog.export.request import (
    ExportRequest,
    ImageExportRequest,
    SlidesExportRequest,
    VisualExportRequest,
)
from gooddata_sdk.catalog.identifier import (
    CatalogDeclarativeAnalyticalDashboardIdentifier,
    CatalogExportDefinitionIdentifier,
    CatalogNotificationChannelIdentifier,
    CatalogUserIdentifier,
)
from gooddata_sdk.catalog.workspace.declarative_model.workspace.analytics_model.base import CatalogAnalyticsBaseMeta


@define(kw_only=True)
class CatalogAutomationSchedule(Base):
    cron: str
    cron_description: str | None = field(default=None, eq=False)
    first_run: str | None = None
    timezone: str | None = "UTC"

    @staticmethod
    def client_class() -> builtins.type[AutomationSchedule]:
        return AutomationSchedule


@define(kw_only=True)
class CatalogAutomationTabularExport(Base):
    request_payload: ExportRequest

    @staticmethod
    def client_class() -> builtins.type[AutomationTabularExport]:
        return AutomationTabularExport


@define(kw_only=True)
class CatalogAutomationVisualExport(Base):
    request_payload: VisualExportRequest

    @staticmethod
    def client_class() -> builtins.type[AutomationVisualExport]:
        return AutomationVisualExport


@define(kw_only=True)
class CatalogAutomationImageExport(Base):
    request_payload: ImageExportRequest

    @staticmethod
    def client_class() -> builtins.type[AutomationImageExport]:
        return AutomationImageExport


@define(kw_only=True)
class CatalogAutomationSlidesExport(Base):
    request_payload: SlidesExportRequest

    @staticmethod
    def client_class() -> builtins.type[AutomationSlidesExport]:
        return AutomationSlidesExport


@define(kw_only=True)
class CatalogAutomationExternalRecipient(Base):
    email: str

    @staticmethod
    def client_class() -> builtins.type[AutomationExternalRecipient]:
        return AutomationExternalRecipient


@define(kw_only=True)
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
    image_exports: list[CatalogAutomationImageExport] | None = None
    slides_exports: list[CatalogAutomationSlidesExport] | None = None
    external_recipients: list[CatalogAutomationExternalRecipient] | None = None
    analytical_dashboard: CatalogDeclarativeAnalyticalDashboardIdentifier | None = None
    evaluation_mode: str | None = None

    @staticmethod
    def client_class() -> builtins.type[DeclarativeAutomation]:
        return DeclarativeAutomation
