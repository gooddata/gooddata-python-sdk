# (C) 2022 GoodData Corporation
from __future__ import annotations

from typing import Any

from gooddata_metadata_client.model.declarative_workspace import DeclarativeWorkspace
from gooddata_metadata_client.model.declarative_workspace_data_filter import DeclarativeWorkspaceDataFilter
from gooddata_metadata_client.model.declarative_workspace_data_filter_setting import (
    DeclarativeWorkspaceDataFilterSetting,
)
from gooddata_metadata_client.model.declarative_workspace_model import DeclarativeWorkspaceModel
from gooddata_metadata_client.model.declarative_workspaces import DeclarativeWorkspaces
from gooddata_sdk.catalog.entity import CatalogNameEntity, CatalogTitleEntity
from gooddata_sdk.catalog.identifier import CatalogWorkspaceIdentifier
from gooddata_sdk.catalog.workspace.declarative_model.workspace.analytics_model.analytics_model import (
    CatalogDeclarativeAnalyticsLayer,
)
from gooddata_sdk.catalog.workspace.declarative_model.workspace.logical_model.ldm import CatalogDeclarativeLdm


class CatalogDeclarativeWorkspaceModel:
    def __init__(self, ldm: CatalogDeclarativeLdm = None, analytics: CatalogDeclarativeAnalyticsLayer = None):
        self.ldm = ldm
        self.analytics = analytics

    @classmethod
    def from_api(cls, entity: dict[str, Any]) -> CatalogDeclarativeWorkspaceModel:
        ldm, analytics = None, None
        if entity.get("ldm"):
            ldm = CatalogDeclarativeLdm.from_api(entity["ldm"])
        if entity.get("analytics"):
            analytics = CatalogDeclarativeAnalyticsLayer.from_api(entity["analytics"])
        return cls(ldm, analytics)

    def to_api(self) -> DeclarativeWorkspaceModel:
        kwargs = dict()
        if self.ldm:
            kwargs["ldm"] = self.ldm.to_api()
        if self.analytics:
            kwargs["analytics"] = self.analytics.to_api()
        return DeclarativeWorkspaceModel(**kwargs)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, CatalogDeclarativeWorkspaceModel):
            return False
        return self.ldm == other.ldm and self.analytics == other.analytics


class CatalogDeclarativeWorkspace(CatalogNameEntity):
    def __init__(
        self,
        id: str,
        name: str,
        compute_client: str = None,
        model: CatalogDeclarativeWorkspaceModel = None,
        parent: CatalogWorkspaceIdentifier = None,
    ):
        super(CatalogDeclarativeWorkspace, self).__init__(id, name)
        self.compute_client = compute_client
        self.model = model
        self.parent = parent

    @classmethod
    def from_api(cls, entity: dict[str, Any]) -> CatalogDeclarativeWorkspace:
        return cls(
            entity["id"],
            entity["name"],
            entity.get("computeClient"),
            CatalogDeclarativeWorkspaceModel.from_api(entity["model"]) if "model" in entity else None,
            CatalogWorkspaceIdentifier.from_api(entity["parent"]) if "parent" in entity else None,
        )

    def to_api(self) -> DeclarativeWorkspace:
        kwargs = dict()
        if self.model:
            kwargs["model"] = self.model.to_api()
        if self.parent:
            kwargs["parent"] = self.parent.to_api()
        if self.compute_client:
            kwargs["computeClient"] = self.compute_client
        return DeclarativeWorkspace(id=self.id, name=self.name, **kwargs)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, CatalogDeclarativeWorkspace):
            return False
        return (
            self.id == other.id
            and self.name == other.name
            and self.compute_client == other.compute_client
            and self.model == other.model
            and self.parent == other.parent
        )


class CatalogDeclarativeWorkspaceDataFilterSetting(CatalogTitleEntity):
    def __init__(
        self,
        id: str,
        title: str,
        filter_values: list[str],
        workspace: CatalogWorkspaceIdentifier,
        description: str = None,
    ):
        super(CatalogDeclarativeWorkspaceDataFilterSetting, self).__init__(id, title)
        self.filter_values = filter_values
        self.workspace = workspace
        self.description = description

    @classmethod
    def from_api(cls, entity: dict[str, Any]) -> CatalogDeclarativeWorkspaceDataFilterSetting:
        return cls(
            entity["id"],
            entity["title"],
            entity["filter_values"],
            CatalogWorkspaceIdentifier.from_api(entity["workspace"]),
            entity.get("description"),
        )

    def to_api(self) -> DeclarativeWorkspaceDataFilterSetting:
        kwargs = {}
        if self.description:
            kwargs["description"] = self.description
        return DeclarativeWorkspaceDataFilterSetting(
            self.id, self.title, self.filter_values, self.workspace.to_api(), **kwargs
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, CatalogDeclarativeWorkspaceDataFilterSetting):
            return False
        return (
            self.id == other.id
            and self.title == other.title
            and self.filter_values == other.filter_values
            and self.workspace == other.workspace
            and self.description == other.description
        )


class CatalogDeclarativeWorkspaceDataFilter:
    def __init__(
        self,
        id: str,
        title: str,
        column_name: str,
        workspace_data_filter_settings: list[CatalogDeclarativeWorkspaceDataFilterSetting],
        description: str = None,
        workspace: CatalogWorkspaceIdentifier = None,
    ):
        self.id = id
        self.title = title
        self.column_name = column_name
        self.workspace_data_filter_settings = workspace_data_filter_settings
        self.description = description
        self.workspace = workspace

    @classmethod
    def from_api(cls, entity: dict[str, Any]) -> CatalogDeclarativeWorkspaceDataFilter:
        return cls(
            entity["id"],
            entity["title"],
            entity["column_name"],
            [
                CatalogDeclarativeWorkspaceDataFilterSetting.from_api(v)
                for v in entity["workspace_data_filter_settings"]
            ],
            entity.get("description"),
            CatalogWorkspaceIdentifier.from_api(entity["workspace"]) if entity.get("workspace") else None,
        )

    def to_api(self) -> DeclarativeWorkspaceDataFilter:
        kwargs = dict()
        if self.description:
            kwargs["description"] = self.description
        if self.workspace:
            kwargs["workspace"] = self.workspace.to_api()
        return DeclarativeWorkspaceDataFilter(
            self.id, self.title, self.column_name, [v.to_api() for v in self.workspace_data_filter_settings], **kwargs
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, CatalogDeclarativeWorkspaceDataFilter):
            return False
        return (
            self.id == other.id
            and self.title == other.title
            and self.column_name == other.column_name
            and self.workspace_data_filter_settings == other.workspace_data_filter_settings
            and self.description == other.description
            and self.workspace == other.workspace
        )


class CatalogDeclarativeWorkspaces:
    def __init__(
        self,
        workspaces: list[CatalogDeclarativeWorkspace],
        workspace_data_filters: list[CatalogDeclarativeWorkspaceDataFilter],
    ):
        self.workspaces = workspaces
        self.workspace_data_filters = workspace_data_filters

    @classmethod
    def from_api(cls, entity: dict[str, Any]) -> CatalogDeclarativeWorkspaces:
        return cls(
            [CatalogDeclarativeWorkspace.from_api(v) for v in entity["workspaces"]],
            [CatalogDeclarativeWorkspaceDataFilter.from_api(v) for v in entity["workspace_data_filters"]],
        )

    def to_api(self) -> DeclarativeWorkspaces:
        return DeclarativeWorkspaces(
            [v.to_api() for v in self.workspaces], [v.to_api() for v in self.workspace_data_filters]
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, CatalogDeclarativeWorkspaces):
            return False
        return self.workspaces == other.workspaces and self.workspace_data_filters == other.workspace_data_filters
