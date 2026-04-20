# (C) 2024 GoodData Corporation
from __future__ import annotations

import builtins
from typing import Any

from attrs import define, field
from gooddata_api_client.model.automation_alert import AutomationAlert
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


@define(kw_only=True)
class CatalogAutomationAlert(Base):
    """Wraps the alert configuration for an automation.

    The ``trigger`` field controls when the alert fires:
    - ``ALWAYS`` – fires every time the condition is met.
    - ``ONCE`` – fires only the first time the condition is met.
    - ``ONCE_PER_INTERVAL`` – fires when the condition is met, then is suppressed for the
      duration specified by ``interval``.

    The ``interval`` field is only used when ``trigger`` is ``ONCE_PER_INTERVAL`` and
    must be one of: ``DAY``, ``WEEK``, ``MONTH``, ``QUARTER``, ``YEAR``.
    """

    condition: dict[str, Any]
    execution: dict[str, Any]
    trigger: str | None = None
    interval: str | None = None

    @staticmethod
    def client_class() -> builtins.type[AutomationAlert]:
        return AutomationAlert


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
    alert: CatalogAutomationAlert | None = None

    @staticmethod
    def client_class() -> builtins.type[DeclarativeAutomation]:
        return DeclarativeAutomation
