# (C) 2022 GoodData Corporation
from __future__ import annotations

import functools
from pathlib import Path
from typing import List

from gooddata_api_client.exceptions import NotFoundException
from gooddata_sdk.catalog.catalog_service_base import CatalogServiceBase
from gooddata_sdk.catalog.workspace.declarative_model.workspace.workspace import (
    CatalogDeclarativeWorkspaceDataFilters,
    CatalogDeclarativeWorkspaceModel,
    CatalogDeclarativeWorkspaces,
    get_workspace_folder,
)
from gooddata_sdk.catalog.workspace.entity_model.workspace import CatalogWorkspace
from gooddata_sdk.client import GoodDataApiClient
from gooddata_sdk.utils import load_all_entities


class CatalogWorkspaceService(CatalogServiceBase):
    def __init__(self, api_client: GoodDataApiClient) -> None:
        super(CatalogWorkspaceService, self).__init__(api_client)

    # Entities methods

    def create_or_update(self, workspace: CatalogWorkspace) -> None:
        try:
            found_workspace = self.get_workspace(workspace.id)
            # Update of parent is not allowed
            if found_workspace.parent_id == workspace.parent_id:
                self._entities_api.update_entity_workspaces(
                    workspace.id,
                    workspace.to_api(),
                )
            else:
                raise ValueError(
                    f"Workspace parent can not be update. "
                    f"Original parent {found_workspace.parent_id}, wanted parent {workspace.parent_id}."
                )
        except NotFoundException:
            self._entities_api.create_entity_workspaces(workspace.to_api())

    def get_workspace(self, workspace_id: str) -> CatalogWorkspace:
        """
        Gets workspace content and returns it as CatalogWorkspace object.

        :param workspace_id: An input string parameter of workspace id.
        :return: CatalogWorkspace object containing structure of workspace.
        """
        return CatalogWorkspace.from_api(
            self._entities_api.get_entity_workspaces(workspace_id, include=["workspaces"]).data
        )

    def delete_workspace(self, workspace_id: str) -> None:
        """
        This method is implemented according to our implementation of delete workspace,
        which returns HTTP 204 no matter if the workspace_id exists.
        """
        workspaces = self.list_workspaces()
        if workspace_id not in [w.id for w in workspaces]:
            raise ValueError(f"Can not delete {workspace_id} workspace. This workspace does not exist.")
        children = [w.id for w in workspaces if w.parent_id == workspace_id]
        if children:
            raise ValueError(
                f"Can not delete {workspace_id} workspace. "
                f"This workspace is parent of the following workspaces: {', '.join(children)}. "
            )
        self._entities_api.delete_entity_workspaces(workspace_id)

    def list_workspaces(self) -> List[CatalogWorkspace]:
        get_workspaces = functools.partial(
            self._entities_api.get_all_entities_workspaces,
            include=["workspaces"],
            _check_return_type=False,
        )
        workspaces = load_all_entities(get_workspaces)
        return [CatalogWorkspace.from_api(w) for w in workspaces.data]

    # Declarative methods - workspaces

    def get_declarative_workspaces(self) -> CatalogDeclarativeWorkspaces:
        return CatalogDeclarativeWorkspaces.from_api(self._layout_api.get_workspaces_layout())

    def put_declarative_workspaces(self, workspace: CatalogDeclarativeWorkspaces) -> None:
        self._layout_api.set_workspaces_layout(workspace.to_api())

    def store_declarative_workspaces(self, layout_root_path: Path = Path.cwd()) -> None:
        self.get_declarative_workspaces().store_to_disk(self.layout_organization_folder(layout_root_path))

    def load_declarative_workspaces(self, layout_root_path: Path = Path.cwd()) -> CatalogDeclarativeWorkspaces:
        return CatalogDeclarativeWorkspaces.load_from_disk(self.layout_organization_folder(layout_root_path))

    def load_and_put_declarative_workspaces(self, layout_root_path: Path = Path.cwd()) -> None:
        declarative_workspaces = self.load_declarative_workspaces(layout_root_path)
        self.put_declarative_workspaces(declarative_workspaces)

    # Declarative methods - workspace

    def get_declarative_workspace(self, workspace_id: str) -> CatalogDeclarativeWorkspaceModel:
        return CatalogDeclarativeWorkspaceModel.from_api(self._layout_api.get_workspace_layout(workspace_id))

    def put_declarative_workspace(self, workspace_id: str, workspace: CatalogDeclarativeWorkspaceModel) -> None:
        self._layout_api.put_workspace_layout(workspace_id, workspace.to_api())

    def store_declarative_workspace(self, workspace_id: str, layout_root_path: Path = Path.cwd()) -> None:
        workspace_folder = get_workspace_folder(
            workspace_id=workspace_id, layout_organization_folder=self.layout_organization_folder(layout_root_path)
        )
        self.get_declarative_workspace(workspace_id=workspace_id).store_to_disk(workspace_folder=workspace_folder)

    def load_declarative_workspace(
        self, workspace_id: str, layout_root_path: Path = Path.cwd()
    ) -> CatalogDeclarativeWorkspaceModel:
        workspace_folder = get_workspace_folder(
            workspace_id=workspace_id, layout_organization_folder=self.layout_organization_folder(layout_root_path)
        )
        return CatalogDeclarativeWorkspaceModel.load_from_disk(workspace_folder=workspace_folder)

    def load_and_put_declarative_workspace(self, workspace_id: str, layout_root_path: Path = Path.cwd()) -> None:
        declarative_workspace = self.load_declarative_workspace(
            workspace_id=workspace_id, layout_root_path=layout_root_path
        )
        self.put_declarative_workspace(workspace_id=workspace_id, workspace=declarative_workspace)

    # Declarative methods - workspace data filters

    def get_declarative_workspace_data_filters(self) -> CatalogDeclarativeWorkspaceDataFilters:
        return CatalogDeclarativeWorkspaceDataFilters.from_api(self._layout_api.get_workspace_data_filters_layout())

    def put_declarative_workspace_data_filters(
        self, workspace_data_filters: CatalogDeclarativeWorkspaceDataFilters
    ) -> None:
        self._layout_api.set_workspace_data_filters_layout(
            declarative_workspace_data_filters=workspace_data_filters.to_api()
        )

    def store_declarative_workspace_data_filters(self, layout_root_path: Path = Path.cwd()) -> None:
        self.get_declarative_workspace_data_filters().store_to_disk(self.layout_organization_folder(layout_root_path))

    def load_declarative_workspace_data_filters(
        self, layout_root_path: Path = Path.cwd()
    ) -> CatalogDeclarativeWorkspaceDataFilters:
        return CatalogDeclarativeWorkspaceDataFilters.load_from_disk(self.layout_organization_folder(layout_root_path))

    def load_and_put_declarative_workspace_data_filters(self, layout_root_path: Path = Path.cwd()) -> None:
        declarative_workspace_data_filters = CatalogDeclarativeWorkspaceDataFilters.load_from_disk(
            self.layout_organization_folder(layout_root_path)
        )
        self.put_declarative_workspace_data_filters(declarative_workspace_data_filters)
