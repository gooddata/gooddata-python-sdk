# (C) 2022 GoodData Corporation
from __future__ import annotations

from pathlib import Path
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
from gooddata_sdk.catalog.permissions.permission import (
    CatalogDeclarativeSingleWorkspacePermission,
    CatalogDeclarativeWorkspaceHierarchyPermission,
)
from gooddata_sdk.catalog.workspace.declarative_model.workspace.analytics_model.analytics_model import (
    CatalogDeclarativeAnalyticsLayer,
)
from gooddata_sdk.catalog.workspace.declarative_model.workspace.logical_model.ldm import CatalogDeclarativeLdm
from gooddata_sdk.utils import create_directory, get_sorted_yaml_files, read_layout_from_file, write_layout_to_file

LAYOUT_WORKSPACES_DIR = "workspaces"
LAYOUT_WORKSPACES_DATA_FILTERS_DIR = "workspaces_data_filters"


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
        permissions: list[CatalogDeclarativeSingleWorkspacePermission] = None,
        hierarchy_permissions: list[CatalogDeclarativeWorkspaceHierarchyPermission] = None,
    ):
        super(CatalogDeclarativeWorkspace, self).__init__(id, name)
        self.compute_client = compute_client
        self.model = model
        self.parent = parent
        self.permissions = permissions if permissions is not None else []
        self.hierarchy_permissions = hierarchy_permissions if hierarchy_permissions is not None else []

    @classmethod
    def from_api(cls, entity: dict[str, Any]) -> CatalogDeclarativeWorkspace:
        return cls(
            id=entity["id"],
            name=entity["name"],
            compute_client=entity.get("computeClient"),
            model=CatalogDeclarativeWorkspaceModel.from_api(entity["model"]) if "model" in entity else None,
            parent=CatalogWorkspaceIdentifier.from_api(entity["parent"]) if "parent" in entity else None,
            permissions=[
                CatalogDeclarativeSingleWorkspacePermission.from_api(permission)
                for permission in entity.get("permissions", [])
            ],
            hierarchy_permissions=[
                CatalogDeclarativeWorkspaceHierarchyPermission.from_api(hierarchy_permission)
                for hierarchy_permission in entity.get("hierarchy_permissions", [])
            ],
        )

    def to_api(self, include_nested_structures: bool = True) -> DeclarativeWorkspace:
        kwargs: dict[str, Any] = {
            "permissions": [permission.to_api() for permission in self.permissions],
            "hierarchy_permissions": [
                hierarchy_permission.to_api() for hierarchy_permission in self.hierarchy_permissions
            ],
        }
        if self.model is not None and include_nested_structures:
            kwargs["model"] = self.model.to_api()
        if self.parent is not None:
            kwargs["parent"] = self.parent.to_api()
        if self.compute_client is not None:
            kwargs["compute_client"] = self.compute_client
        return DeclarativeWorkspace(id=self.id, name=self.name, **kwargs)

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

    @classmethod
    def from_dict(cls, data: dict[str, Any], camel_case: bool = True) -> CatalogDeclarativeWorkspace:
        """
        :param data:    Data loaded for example from the file.
        :param camel_case:  True if the variable names in the input
                        data are serialized names as specified in the OpenAPI document.
                        False if the variables names in the input data are python
                        variable names in PEP-8 snake case.
        :return:    CatalogDeclarativeWorkspace object.
        """
        declarative_workspace = DeclarativeWorkspace.from_dict(data, camel_case)
        return cls.from_api(declarative_workspace)

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

    @staticmethod
    def workspaces_folder(layout_organization_folder: Path) -> Path:
        return layout_organization_folder / LAYOUT_WORKSPACES_DIR

    @staticmethod
    def workspace_data_filters_folder(layout_organization_folder: Path) -> Path:
        return layout_organization_folder / LAYOUT_WORKSPACES_DATA_FILTERS_DIR

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

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, CatalogDeclarativeWorkspaces):
            return False
        return self.workspaces == other.workspaces and self.workspace_data_filters == other.workspace_data_filters

    @classmethod
    def from_dict(cls, data: dict[str, Any], camel_case: bool = True) -> CatalogDeclarativeWorkspaces:
        """
        :param data:    Data loaded for example from the file.
        :param camel_case:  True if the variable names in the input
                        data are serialized names as specified in the OpenAPI document.
                        False if the variables names in the input data are python
                        variable names in PEP-8 snake case.
        :return:    CatalogDeclarativeWorkspaces object.
        """
        declarative_workspaces = DeclarativeWorkspaces.from_dict(data, camel_case)
        return cls.from_api(declarative_workspaces)
