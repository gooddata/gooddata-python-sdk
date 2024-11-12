# (C) 2022 GoodData Corporation
from __future__ import annotations

import copy
from pathlib import Path
from typing import Any, Optional

import attr
from gooddata_api_client.model.declarative_filter_view import DeclarativeFilterView
from gooddata_api_client.model.declarative_user_data_filter import DeclarativeUserDataFilter
from gooddata_api_client.model.declarative_user_data_filters import DeclarativeUserDataFilters
from gooddata_api_client.model.declarative_workspace import DeclarativeWorkspace
from gooddata_api_client.model.declarative_workspace_data_filter import DeclarativeWorkspaceDataFilter
from gooddata_api_client.model.declarative_workspace_data_filter_setting import DeclarativeWorkspaceDataFilterSetting
from gooddata_api_client.model.declarative_workspace_data_filters import DeclarativeWorkspaceDataFilters
from gooddata_api_client.model.declarative_workspace_model import DeclarativeWorkspaceModel
from gooddata_api_client.model.declarative_workspaces import DeclarativeWorkspaces

from gooddata_sdk.catalog.base import Base
from gooddata_sdk.catalog.identifier import (
    CatalogDeclarativeAnalyticalDashboardIdentifier,
    CatalogDeclarativeUserGroupIdentifier,
    CatalogUserIdentifier,
    CatalogWorkspaceIdentifier,
)
from gooddata_sdk.catalog.permission.declarative_model.permission import (
    CatalogDeclarativeSingleWorkspacePermission,
    CatalogDeclarativeWorkspaceHierarchyPermission,
)
from gooddata_sdk.catalog.setting import CatalogDeclarativeCustomApplicationSetting, CatalogDeclarativeSetting
from gooddata_sdk.catalog.workspace.declarative_model.workspace.analytics_model.analytics_model import (
    CatalogDeclarativeAnalyticsLayer,
)
from gooddata_sdk.catalog.workspace.declarative_model.workspace.automation import CatalogDeclarativeAutomation
from gooddata_sdk.catalog.workspace.declarative_model.workspace.logical_model.ldm import CatalogDeclarativeLdm
from gooddata_sdk.utils import create_directory, get_sorted_yaml_files, read_layout_from_file, write_layout_to_file

LAYOUT_WORKSPACES_DIR = "workspaces"
LAYOUT_WORKSPACES_DATA_FILTERS_DIR = "workspaces_data_filters"
LAYOUT_USER_DATA_FILTERS_DIR = "user_data_filters"
LAYOUT_FILTER_VIEWS_DIR = "filter_views"


def get_workspace_folder(workspace_id: str, layout_organization_folder: Path) -> Path:
    return layout_organization_folder / LAYOUT_WORKSPACES_DIR / workspace_id


@attr.s(auto_attribs=True, kw_only=True)
class CatalogDeclarativeWorkspaceModel(Base):
    ldm: Optional[CatalogDeclarativeLdm] = None
    analytics: Optional[CatalogDeclarativeAnalyticsLayer] = None

    @staticmethod
    def client_class() -> type[DeclarativeWorkspaceModel]:
        return DeclarativeWorkspaceModel

    def store_to_disk(self, workspace_folder: Path) -> None:
        if self.ldm is not None:
            self.ldm.store_to_disk(workspace_folder)
        if self.analytics is not None:
            self.analytics.store_to_disk(workspace_folder)

    @classmethod
    def load_from_disk(cls, workspace_folder: Path) -> CatalogDeclarativeWorkspaceModel:
        ldm = CatalogDeclarativeLdm.load_from_disk(workspace_folder)
        analytics = CatalogDeclarativeAnalyticsLayer.load_from_disk(workspace_folder)
        return cls(ldm=ldm, analytics=analytics)

    def remove_wdf_refs(self) -> None:
        if self.ldm:
            self.ldm.remove_wdf_refs()

    def change_wdf_refs_id(self, mapping: dict[str, str]) -> None:
        if self.ldm:
            self.ldm.change_wdf_refs_id(mapping)


@attr.s(auto_attribs=True, kw_only=True)
class CatalogDeclarativeWorkspace(Base):
    id: str
    name: str
    model: Optional[CatalogDeclarativeWorkspaceModel] = None
    parent: Optional[CatalogWorkspaceIdentifier] = None
    permissions: list[CatalogDeclarativeSingleWorkspacePermission] = attr.field(factory=list)
    hierarchy_permissions: list[CatalogDeclarativeWorkspaceHierarchyPermission] = attr.field(factory=list)
    early_access: Optional[str] = None
    settings: list[CatalogDeclarativeSetting] = attr.field(factory=list)
    user_data_filters: list[CatalogDeclarativeUserDataFilter] = attr.field(factory=list)
    custom_application_settings: list[CatalogDeclarativeCustomApplicationSetting] = attr.field(factory=list)
    automations: list[CatalogDeclarativeAutomation] = attr.field(factory=list)
    filter_views: list[CatalogDeclarativeFilterView] = attr.field(factory=list)

    @staticmethod
    def client_class() -> type[DeclarativeWorkspace]:
        return DeclarativeWorkspace

    def to_api(self, include_nested_structures: bool = True) -> DeclarativeWorkspace:
        client_class = self.client_class()
        dictionary = self._get_snake_dict()
        if self.model is not None and not include_nested_structures:
            del dictionary["model"]
        return client_class.from_dict(dictionary, camel_case=False)

    def store_to_disk(self, workspaces_folder: Path) -> None:
        workspace_folder = workspaces_folder / self.id
        file_path = workspace_folder / f"{self.id}.yaml"
        create_directory(workspace_folder)

        workspace_dict = self.to_api(include_nested_structures=False).to_dict(camel_case=True)
        write_layout_to_file(file_path, workspace_dict)

        if self.model is not None:
            self.model.store_to_disk(workspace_folder)

    @classmethod
    def load_from_disk(cls, workspaces_folder: Path, workspace_id: str) -> CatalogDeclarativeWorkspace:
        workspace_folder = workspaces_folder / workspace_id
        workspace_file_path = workspace_folder / f"{workspace_id}.yaml"
        model = CatalogDeclarativeWorkspaceModel.load_from_disk(workspace_folder)
        workspace_layout_data = read_layout_from_file(workspace_file_path)
        workspace_layout = CatalogDeclarativeWorkspace.from_dict(workspace_layout_data, camel_case=True)
        workspace_layout.model = model
        return workspace_layout


@attr.s(auto_attribs=True, kw_only=True)
class CatalogDeclarativeWorkspaceDataFilterSetting(Base):
    id: str
    title: str
    filter_values: list[str]
    workspace: CatalogWorkspaceIdentifier
    description: Optional[str] = None

    @staticmethod
    def client_class() -> type[DeclarativeWorkspaceDataFilterSetting]:
        return DeclarativeWorkspaceDataFilterSetting


@attr.s(auto_attribs=True, kw_only=True)
class CatalogDeclarativeWorkspaceDataFilters(Base):
    workspace_data_filters: list[CatalogDeclarativeWorkspaceDataFilter]

    @staticmethod
    def client_class() -> type[DeclarativeWorkspaceDataFilters]:
        return DeclarativeWorkspaceDataFilters

    def store_to_disk(self, layout_organization_folder: Path) -> None:
        workspaces_data_filters_folder = CatalogDeclarativeWorkspaces.workspace_data_filters_folder(
            layout_organization_folder
        )
        create_directory(workspaces_data_filters_folder)
        for workspace_data_filter in self.workspace_data_filters:
            workspace_data_filter.store_to_disk(workspaces_data_filters_folder)

    @classmethod
    def load_from_disk(cls, layout_organization_folder: Path) -> CatalogDeclarativeWorkspaceDataFilters:
        workspace_data_filters_files = get_sorted_yaml_files(
            CatalogDeclarativeWorkspaces.workspace_data_filters_folder(layout_organization_folder)
        )
        workspace_data_filters = [
            CatalogDeclarativeWorkspaceDataFilter.load_from_disk(workspace_data_filters_file)
            for workspace_data_filters_file in workspace_data_filters_files
        ]
        return cls(workspace_data_filters=workspace_data_filters)

    def create_copy(self, source_ws_id: str, target_ws_id: str) -> tuple[CatalogDeclarativeWorkspaceDataFilters, dict]:
        self_copy = copy.deepcopy(self)
        # update workspace data filter settings
        for wdf in self_copy.workspace_data_filters:
            new_settings = []
            for setting in wdf.workspace_data_filter_settings:
                if setting.workspace.id == source_ws_id:
                    new_setting = copy.deepcopy(setting)
                    new_setting.workspace.id = target_ws_id
                    new_settings.append(new_setting)
            wdf.workspace_data_filter_settings = wdf.workspace_data_filter_settings + new_settings
        # update workspace data filters
        new_filters = []
        wdf_ref_mapping = {}
        for wdf in self_copy.workspace_data_filters:
            if wdf.workspace is not None and wdf.workspace.id == source_ws_id:
                filter_copy = copy.deepcopy(wdf)
                wdf_copy_id = f"{filter_copy.id}_{target_ws_id}"
                wdf_ref_mapping[filter_copy.id] = wdf_copy_id
                filter_copy.id = wdf_copy_id
                filter_copy.workspace = CatalogWorkspaceIdentifier(id=target_ws_id)
                filter_copy.workspace_data_filter_settings = []
                new_filters.append(filter_copy)
        self_copy.workspace_data_filters = self_copy.workspace_data_filters + new_filters
        return self_copy, wdf_ref_mapping


@attr.s(auto_attribs=True, kw_only=True)
class CatalogDeclarativeWorkspaceDataFilter(Base):
    id: str
    title: str
    column_name: str
    workspace_data_filter_settings: list[CatalogDeclarativeWorkspaceDataFilterSetting]
    description: Optional[str] = None
    workspace: Optional[CatalogWorkspaceIdentifier] = None

    @staticmethod
    def client_class() -> type[DeclarativeWorkspaceDataFilter]:
        return DeclarativeWorkspaceDataFilter

    def store_to_disk(self, workspaces_data_filters_folder: Path) -> None:
        workspaces_data_filter_file = workspaces_data_filters_folder / f"{self.id}.yaml"
        write_layout_to_file(workspaces_data_filter_file, self.to_api().to_dict(camel_case=True))

    @classmethod
    def load_from_disk(cls, workspaces_data_filter_file: Path) -> CatalogDeclarativeWorkspaceDataFilter:
        workspaces_data_filter = read_layout_from_file(workspaces_data_filter_file)
        return CatalogDeclarativeWorkspaceDataFilter.from_dict(workspaces_data_filter, camel_case=True)

    @classmethod
    def from_dict(cls, data: dict[str, Any], camel_case: bool = True) -> CatalogDeclarativeWorkspaceDataFilter:
        """
        Args:
            data (dict[str, Any]): Data loaded, for example, from a file.
            camel_case (bool): True if the variable names in the input data are serialized names as specified in the OpenAPI document.
                               False if the variable names in the input data are Python variable names in PEP-8 snake case.

        Returns:
            CatalogDeclarativeWorkspaceDataFilter: CatalogDeclarativeWorkspaceDataFilter object.
        """
        declarative_workspace_data_filter = DeclarativeWorkspaceDataFilter.from_dict(data, camel_case)
        return cls.from_api(declarative_workspace_data_filter)


@attr.s(auto_attribs=True, kw_only=True)
class CatalogDeclarativeUserDataFilters(Base):
    user_data_filters: list[CatalogDeclarativeUserDataFilter]

    @staticmethod
    def client_class() -> type[DeclarativeUserDataFilters]:
        return DeclarativeUserDataFilters

    def store_to_disk(self, layout_organization_folder: Path) -> None:
        user_data_filters_folder = CatalogDeclarativeWorkspaces.user_data_filters_folder(layout_organization_folder)
        create_directory(user_data_filters_folder)
        for user_data_filter in self.user_data_filters:
            user_data_filter.store_to_disk(user_data_filters_folder)

    @classmethod
    def load_from_disk(cls, layout_organization_folder: Path) -> CatalogDeclarativeUserDataFilters:
        user_data_filters_files = get_sorted_yaml_files(
            CatalogDeclarativeWorkspaces.user_data_filters_folder(layout_organization_folder)
        )
        user_data_filters = [
            CatalogDeclarativeUserDataFilter.load_from_disk(user_data_filters_file)
            for user_data_filters_file in user_data_filters_files
        ]
        return cls(user_data_filters=user_data_filters)


@attr.s(auto_attribs=True, kw_only=True)
class CatalogDeclarativeUserDataFilter(Base):
    id: str
    title: str
    maql: str
    user: Optional[CatalogUserIdentifier] = None
    user_group: Optional[CatalogDeclarativeUserGroupIdentifier] = None
    description: Optional[str] = None

    @staticmethod
    def client_class() -> type[DeclarativeUserDataFilter]:
        return DeclarativeUserDataFilter

    def store_to_disk(self, user_data_filters_folder: Path) -> None:
        user_data_filter_file = user_data_filters_folder / f"{self.id}.yaml"
        write_layout_to_file(user_data_filter_file, self.to_api().to_dict(camel_case=True))

    @classmethod
    def load_from_disk(cls, user_data_filter_file: Path) -> CatalogDeclarativeUserDataFilter:
        user_data_filter = read_layout_from_file(user_data_filter_file)
        return CatalogDeclarativeUserDataFilter.from_dict(user_data_filter, camel_case=True)

    @classmethod
    def from_dict(cls, data: dict[str, Any], camel_case: bool = True) -> CatalogDeclarativeUserDataFilter:
        """
        Args:
            data (dict[str, Any]): Data loaded, for example, from a file.
            camel_case (bool): True if the variable names in the input data are serialized names as specified in the OpenAPI document.
                               False if the variable names in the input data are Python variable names in PEP-8 snake case.

        Returns:
            CatalogDeclarativeUserDataFilter: CatalogDeclarativeUserDataFilter object.
        """
        declarative_user_data_filter = DeclarativeUserDataFilter.from_dict(data, camel_case)
        return cls.from_api(declarative_user_data_filter)


@attr.s(auto_attribs=True, kw_only=True)
class CatalogDeclarativeFilterView(Base):
    id: str
    title: str
    analytical_dashboard: Optional[CatalogDeclarativeAnalyticalDashboardIdentifier] = None
    content: Optional[dict[str, Any]] = None
    description: Optional[str] = None
    is_default: Optional[bool] = None
    tags: Optional[list[str]] = None
    user: Optional[CatalogUserIdentifier] = None

    @staticmethod
    def client_class() -> type[DeclarativeFilterView]:
        return DeclarativeFilterView

    def store_to_disk(self, filter_views_folder: Path) -> None:
        filter_view_file = filter_views_folder / f"{self.id}.yaml"
        write_layout_to_file(filter_view_file, self.to_api().to_dict(camel_case=True))

    @classmethod
    def load_from_disk(cls, filter_view_file: Path) -> CatalogDeclarativeFilterView:
        filter_view = read_layout_from_file(filter_view_file)
        return CatalogDeclarativeFilterView.from_dict(filter_view, camel_case=True)

    @classmethod
    def store_filter_views_to_disk(
        cls, filter_views: list[CatalogDeclarativeFilterView], layout_organization_folder: Path
    ) -> None:
        filter_views_folder = CatalogDeclarativeWorkspaces.filter_views_folder(layout_organization_folder)
        create_directory(filter_views_folder)
        for filter_view in filter_views:
            filter_view.store_to_disk(filter_views_folder)

    @classmethod
    def load_filter_views_from_disk(cls, layout_organization_folder: Path) -> list[CatalogDeclarativeFilterView]:
        filter_views_files = get_sorted_yaml_files(
            CatalogDeclarativeWorkspaces.filter_views_folder(layout_organization_folder)
        )
        return [
            CatalogDeclarativeFilterView.load_from_disk(filter_views_file) for filter_views_file in filter_views_files
        ]


@attr.s(auto_attribs=True, kw_only=True)
class CatalogDeclarativeWorkspaces(Base):
    workspaces: list[CatalogDeclarativeWorkspace]
    workspace_data_filters: list[CatalogDeclarativeWorkspaceDataFilter]

    @staticmethod
    def client_class() -> type[DeclarativeWorkspaces]:
        return DeclarativeWorkspaces

    @staticmethod
    def workspaces_folder(layout_organization_folder: Path) -> Path:
        return layout_organization_folder / LAYOUT_WORKSPACES_DIR

    @staticmethod
    def workspace_data_filters_folder(layout_organization_folder: Path) -> Path:
        return layout_organization_folder / LAYOUT_WORKSPACES_DATA_FILTERS_DIR

    @staticmethod
    def user_data_filters_folder(layout_organization_folder: Path) -> Path:
        return layout_organization_folder / LAYOUT_USER_DATA_FILTERS_DIR

    @staticmethod
    def filter_views_folder(layout_organization_folder: Path) -> Path:
        return layout_organization_folder / LAYOUT_FILTER_VIEWS_DIR

    def store_to_disk(self, layout_organization_folder: Path) -> None:
        workspaces_folder = self.workspaces_folder(layout_organization_folder)
        workspaces_data_filters_folder = self.workspace_data_filters_folder(layout_organization_folder)
        create_directory(workspaces_folder)
        create_directory(workspaces_data_filters_folder)
        for workspace in self.workspaces:
            workspace.store_to_disk(workspaces_folder)
        for workspace_data_filter in self.workspace_data_filters:
            workspace_data_filter.store_to_disk(workspaces_data_filters_folder)

    @classmethod
    def load_from_disk(cls, layout_organization_folder: Path) -> CatalogDeclarativeWorkspaces:
        workspaces_folder = cls.workspaces_folder(layout_organization_folder)
        workspace_data_filters_folder = cls.workspace_data_filters_folder(layout_organization_folder)
        workspace_ids = sorted([p.stem for p in workspaces_folder.iterdir() if p.is_dir()])
        workspace_data_filters_files = get_sorted_yaml_files(workspace_data_filters_folder)

        workspaces = [
            CatalogDeclarativeWorkspace.load_from_disk(workspaces_folder, workspace_id)
            for workspace_id in workspace_ids
        ]
        workspace_data_filters = [
            CatalogDeclarativeWorkspaceDataFilter.load_from_disk(workspace_data_filters_file)
            for workspace_data_filters_file in workspace_data_filters_files
        ]
        return cls(workspaces=workspaces, workspace_data_filters=workspace_data_filters)
