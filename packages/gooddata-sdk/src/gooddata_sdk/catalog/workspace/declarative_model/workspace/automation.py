# (C) 2024 GoodData Corporation
import builtins
from typing import Any

from attrs import define, field
from gooddata_api_client.model.automation_dashboard_tabular_export import AutomationDashboardTabularExport
from gooddata_api_client.model.automation_schedule import AutomationSchedule
from gooddata_api_client.model.automation_tabular_export import AutomationTabularExport
from gooddata_api_client.model.automation_visual_export import AutomationVisualExport
from gooddata_api_client.model.dashboard_tabular_export_request_v2 import DashboardTabularExportRequestV2
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
class CatalogDashboardTabularExportRequestV2(Base):
    """SDK wrapper for DashboardTabularExportRequestV2.

    Represents the request payload for a dashboard tabular export, used within
    automation ``dashboard_tabular_exports``.

    The ``dashboard_filters_override`` field accepts raw filter dicts. Each dict
    must be a serialised ``DashboardFilter`` (one of: ``attributeFilter``,
    ``dateFilter``, ``arbitraryAttributeFilter``, ``matchAttributeFilter``).
    Use :class:`~gooddata_sdk.CatalogDashboardArbitraryAttributeFilter` or
    :class:`~gooddata_sdk.CatalogDashboardMatchAttributeFilter` to build these dicts.

    Attributes:
        dashboard_id: Dashboard identifier.
        file_name: Output filename without extension.
        format: Export format – ``"XLSX"`` or ``"PDF"``.
        dashboard_filters_override: Optional list of filter override dicts.
        dashboard_tabs_filters_overrides: Optional per-tab filter overrides.
        settings: Optional export settings dict.
        widget_ids: Optional list of widget IDs to export (max 1).
    """

    dashboard_id: str
    file_name: str
    format: str
    dashboard_filters_override: list[dict] | None = None
    dashboard_tabs_filters_overrides: dict | None = None
    settings: dict | None = None
    widget_ids: list[str] | None = None

    @staticmethod
    def client_class() -> builtins.type[DashboardTabularExportRequestV2]:
        return DashboardTabularExportRequestV2


@define(kw_only=True)
class CatalogAutomationDashboardTabularExport(Base):
    """SDK wrapper for AutomationDashboardTabularExport.

    Wraps a :class:`CatalogDashboardTabularExportRequestV2` for use in
    :class:`CatalogDeclarativeAutomation`.

    Attributes:
        request_payload: The dashboard tabular export request.
    """

    request_payload: CatalogDashboardTabularExportRequestV2

    @staticmethod
    def client_class() -> builtins.type[AutomationDashboardTabularExport]:
        return AutomationDashboardTabularExport


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
    dashboard_tabular_exports: list[CatalogAutomationDashboardTabularExport] | None = None

    @staticmethod
    def client_class() -> builtins.type[DeclarativeAutomation]:
        return DeclarativeAutomation
