# (C) 2022 GoodData Corporation
from __future__ import annotations

import builtins

import attr
from attrs import define
from gooddata_api_client.model.assignee_identifier import AssigneeIdentifier
from gooddata_api_client.model.dataset_workspace_data_filter_identifier import DatasetWorkspaceDataFilterIdentifier
from gooddata_api_client.model.declarative_analytical_dashboard_identifier import (
    DeclarativeAnalyticalDashboardIdentifier,
)
from gooddata_api_client.model.declarative_export_definition_identifier import DeclarativeExportDefinitionIdentifier
from gooddata_api_client.model.declarative_notification_channel_identifier import (
    DeclarativeNotificationChannelIdentifier,
)
from gooddata_api_client.model.declarative_user_group_identifier import DeclarativeUserGroupIdentifier
from gooddata_api_client.model.declarative_user_identifier import DeclarativeUserIdentifier
from gooddata_api_client.model.grain_identifier import GrainIdentifier
from gooddata_api_client.model.label_identifier import LabelIdentifier
from gooddata_api_client.model.reference_identifier import ReferenceIdentifier
from gooddata_api_client.model.workspace_identifier import WorkspaceIdentifier

from gooddata_sdk.catalog.base import Base, value_in_allowed


@attr.s(auto_attribs=True, kw_only=True)
class CatalogWorkspaceIdentifier(Base):
    id: str

    @staticmethod
    def client_class() -> builtins.type[WorkspaceIdentifier]:
        return WorkspaceIdentifier


@attr.s(auto_attribs=True, kw_only=True)
class CatalogReferenceIdentifier(Base):
    id: str

    @staticmethod
    def client_class() -> builtins.type[ReferenceIdentifier]:
        return ReferenceIdentifier


@attr.s(auto_attribs=True, kw_only=True)
class CatalogGrainIdentifier(Base):
    id: str
    type: str = attr.field(validator=value_in_allowed)

    @staticmethod
    def client_class() -> builtins.type[GrainIdentifier]:
        return GrainIdentifier


@attr.s(auto_attribs=True, kw_only=True)
class CatalogAssigneeIdentifier(Base):
    id: str
    type: str = attr.field(validator=value_in_allowed)

    @staticmethod
    def client_class() -> builtins.type[AssigneeIdentifier]:
        return AssigneeIdentifier


@attr.s(auto_attribs=True, kw_only=True)
class CatalogDeclarativeUserGroupIdentifier(Base):
    id: str
    type: str = attr.field(validator=value_in_allowed)

    @staticmethod
    def client_class() -> builtins.type[DeclarativeUserGroupIdentifier]:
        return DeclarativeUserGroupIdentifier


@attr.s(auto_attribs=True, kw_only=True)
class CatalogUserIdentifier(Base):
    id: str
    type: str = attr.field(validator=value_in_allowed)

    @staticmethod
    def client_class() -> builtins.type[DeclarativeUserIdentifier]:
        return DeclarativeUserIdentifier


@attr.s(auto_attribs=True, kw_only=True)
class CatalogLabelIdentifier(Base):
    id: str
    type: str = attr.field(validator=value_in_allowed)

    @staticmethod
    def client_class() -> builtins.type[LabelIdentifier]:
        return LabelIdentifier


@attr.s(auto_attribs=True, kw_only=True)
class CatalogDatasetWorkspaceDataFilterIdentifier(Base):
    id: str

    @staticmethod
    def client_class() -> builtins.type[DatasetWorkspaceDataFilterIdentifier]:
        return DatasetWorkspaceDataFilterIdentifier


@define(auto_attribs=True, kw_only=True)
class CatalogExportDefinitionIdentifier(Base):
    id: str

    @staticmethod
    def client_class() -> builtins.type[DeclarativeExportDefinitionIdentifier]:
        return DeclarativeExportDefinitionIdentifier


@define(auto_attribs=True, kw_only=True)
class CatalogNotificationChannelIdentifier(Base):
    id: str

    @staticmethod
    def client_class() -> builtins.type[DeclarativeNotificationChannelIdentifier]:
        return DeclarativeNotificationChannelIdentifier


@attr.s(auto_attribs=True, kw_only=True)
class CatalogDeclarativeAnalyticalDashboardIdentifier(Base):
    id: str
    type: str = attr.field(validator=value_in_allowed)

    @staticmethod
    def client_class() -> builtins.type[DeclarativeAnalyticalDashboardIdentifier]:
        return DeclarativeAnalyticalDashboardIdentifier
