# (C) 2022 GoodData Corporation
from __future__ import annotations

from pathlib import Path
from typing import Any, List, Optional, Type

import attr

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
    CatalogUserGroupIdentifier,
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
from gooddata_sdk.catalog.workspace.declarative_model.workspace.logical_model.ldm import CatalogDeclarativeLdm
from gooddata_sdk.utils import create_directory, get_sorted_yaml_files, read_layout_from_file, write_layout_to_file

LAYOUT_WORKSPACES_DIR = "workspaces"
LAYOUT_WORKSPACES_DATA_FILTERS_DIR = "workspaces_data_filters"
LAYOUT_USER_DATA_FILTERS_DIR = "user_data_filters"


def get_workspace_folder(workspace_id: str, layout_organization_folder: Path) -> Path:
    return layout_organization_folder / LAYOUT_WORKSPACES_DIR / workspace_id


@attr.s(auto_attribs=True, kw_only=True)
class CatalogDeclarativeWorkspaceModel(Base):
    ldm: Optional[CatalogDeclarativeLdm] = None
    analytics: Optional[CatalogDeclarativeAnalyticsLayer] = None

    @staticmethod
    def client_class() -> Type[DeclarativeWorkspaceModel]:
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


@attr.s(auto_attribs=True, kw_only=True)
class CatalogDeclarativeWorkspace(Base):
    id: str
    name: str
    model: Optional[CatalogDeclarativeWorkspaceModel] = None
    parent: Optional[CatalogWorkspaceIdentifier] = None
    permissions: List[CatalogDeclarativeSingleWorkspacePermission] = attr.field(factory=list)
    hierarchy_permissions: List[CatalogDeclarativeWorkspaceHierarchyPermission] = attr.field(factory=list)
    early_access: Optional[str] = None
    settings: List[CatalogDeclarativeSetting] = attr.field(factory=list)
    user_data_filters: List[CatalogDeclarativeUserDataFilter] = attr.field(factory=list)
    custom_application_settings: List[CatalogDeclarativeCustomApplicationSetting] = attr.field(factory=list)

    @staticmethod
    def client_class() -> Type[DeclarativeWorkspace]:
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
    filter_values: List[str]
    workspace: CatalogWorkspaceIdentifier
    description: Optional[str] = None

    @staticmethod
    def client_class() -> Type[DeclarativeWorkspaceDataFilterSetting]:
        return DeclarativeWorkspaceDataFilterSetting


@attr.s(auto_attribs=True, kw_only=True)
class CatalogDeclarativeWorkspaceDataFilters(Base):
    workspace_data_filters: List[CatalogDeclarativeWorkspaceDataFilter]

    @staticmethod
    def client_class() -> Type[DeclarativeWorkspaceDataFilters]:
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
        workspace_data_filters = []
        for workspace_data_filters_file in workspace_data_filters_files:
            workspace_data_filters.append(
                CatalogDeclarativeWorkspaceDataFilter.load_from_disk(workspace_data_filters_file)
            )
        return cls(workspace_data_filters=workspace_data_filters)


@attr.s(auto_attribs=True, kw_only=True)
class CatalogDeclarativeWorkspaceDataFilter(Base):
    id: str
    title: str
    column_name: str
    workspace_data_filter_settings: List[CatalogDeclarativeWorkspaceDataFilterSetting]
    description: Optional[str] = None
    workspace: Optional[CatalogWorkspaceIdentifier] = None

    @staticmethod
    def client_class() -> Type[DeclarativeWorkspaceDataFilter]:
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
        :param data:    Data loaded for example from the file.
        :param camel_case:  True if the variable names in the input
                        data are serialized names as specified in the OpenAPI document.
                        False if the variables names in the input data are python
                        variable names in PEP-8 snake case.
        :return:    CatalogDeclarativeWorkspaceDataFilter object.
        """
        declarative_workspace_data_filter = DeclarativeWorkspaceDataFilter.from_dict(data, camel_case)
        return cls.from_api(declarative_workspace_data_filter)


@attr.s(auto_attribs=True, kw_only=True)
class CatalogDeclarativeUserDataFilters(Base):
    user_data_filters: List[CatalogDeclarativeUserDataFilter]

    @staticmethod
    def client_class() -> Type[DeclarativeUserDataFilters]:
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
        user_data_filters = []
        for user_data_filters_file in user_data_filters_files:
            user_data_filters.append(CatalogDeclarativeUserDataFilter.load_from_disk(user_data_filters_file))
        return cls(user_data_filters=user_data_filters)


@attr.s(auto_attribs=True, kw_only=True)
class CatalogDeclarativeUserDataFilter(Base):
    id: str
    title: str
    maql: str
    user: Optional[CatalogUserIdentifier] = None
    user_group: Optional[CatalogUserGroupIdentifier] = None
    description: Optional[str] = None

    @staticmethod
    def client_class() -> Type[DeclarativeUserDataFilter]:
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
        :param data:    Data loaded for example from the file.
        :param camel_case:  True if the variable names in the input
                        data are serialized names as specified in the OpenAPI document.
                        False if the variables names in the input data are python
                        variable names in PEP-8 snake case.
        :return:    CatalogDeclarativeUserDataFilter object.
        """
        declarative_user_data_filter = DeclarativeUserDataFilter.from_dict(data, camel_case)
        return cls.from_api(declarative_user_data_filter)


@attr.s(auto_attribs=True, kw_only=True)
class CatalogDeclarativeWorkspaces(Base):
    workspaces: List[CatalogDeclarativeWorkspace]
    workspace_data_filters: List[CatalogDeclarativeWorkspaceDataFilter]

    @staticmethod
    def client_class() -> Type[DeclarativeWorkspaces]:
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
