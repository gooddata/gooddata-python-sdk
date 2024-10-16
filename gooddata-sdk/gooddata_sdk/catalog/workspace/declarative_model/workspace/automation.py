# (C) 2024 GoodData Corporation
import builtins
from datetime import datetime
from typing import Any, Optional

from attrs import define
from gooddata_api_client.model.automation_schedule import AutomationSchedule
from gooddata_api_client.model.declarative_automation import DeclarativeAutomation

from gooddata_sdk.catalog.base import Base
from gooddata_sdk.catalog.identifier import (
    CatalogExportDefinitionIdentifier,
    CatalogNotificationChannelIdentifier,
    CatalogUserIdentifier,
)
from gooddata_sdk.catalog.workspace.declarative_model.workspace.analytics_model.base import CatalogAnalyticsBaseMeta


@define(auto_attribs=True, kw_only=True)
class CatalogAutomationSchedule(Base):
    cron: str
    cron_description: Optional[str] = None
    first_run: Optional[datetime] = None
    timezone: Optional[str] = None

    @staticmethod
    def client_class() -> builtins.type[AutomationSchedule]:
        return AutomationSchedule


@define(auto_attribs=True, kw_only=True)
class CatalogDeclarativeAutomation(CatalogAnalyticsBaseMeta):
    description: Optional[str] = None
    details: Optional[dict[str, Any]] = None
    state: Optional[str] = None
    tags: Optional[list[str]] = None
    title: Optional[str] = None
    recipients: Optional[list[CatalogUserIdentifier]] = None
    metadata: Optional[dict[str, Any]] = None
    export_definitions: Optional[CatalogExportDefinitionIdentifier] = None
    notification_channel: Optional[CatalogNotificationChannelIdentifier] = None
    schedule: Optional[CatalogAutomationSchedule] = None

    @staticmethod
    def client_class() -> builtins.type[DeclarativeAutomation]:
        return DeclarativeAutomation
