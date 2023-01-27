# (C) 2022 GoodData Corporation
from __future__ import annotations

import functools
from pathlib import Path
from typing import List, Optional

import attrs

from gooddata_api_client.exceptions import NotFoundException
from gooddata_sdk.catalog.catalog_service_base import CatalogServiceBase
from gooddata_sdk.catalog.permission.service import CatalogPermissionService
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
        self._permissions_service = CatalogPermissionService(api_client)

    # Entities methods

    def create_or_update(self, workspace: CatalogWorkspace) -> None:
        """Create a new workspace or overwrite an existing workspace with the same id.

        Args:
            workspace (CatalogWorkspace):
                Catalog Workspace object to be created or updated.

        Returns:
            None

        Raises:
            ValueError: Workspace parent can not be updated.
        """
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
                    f"Workspace parent can not be updated. "
                    f"Original parent {found_workspace.parent_id}, wanted parent {workspace.parent_id}."
                )
        except NotFoundException:
            self._entities_api.create_entity_workspaces(workspace.to_api())

    def get_workspace(self, workspace_id: str) -> CatalogWorkspace:
        """Get an individual workspace.

        Args:
            workspace_id (str):
                Workspace identification string e.g. "demo"

        Returns:
            CatalogWorkspace:
                Catalog workspace object containing structure of the workspace.
        """
        return CatalogWorkspace.from_api(
            self._entities_api.get_entity_workspaces(workspace_id, include=["workspaces"]).data
        )

    def delete_workspace(self, workspace_id: str) -> None:
        """Delete a workspace with all its content - logical model and analytics model.

        Args:
            workspace_id (str):
                Workspace identification string e.g. "demo"

        Returns:
            None

        Raises:
            ValueError:
                Workspace does not exist.
            ValueError:
                Workspace is a parent of a workspace.
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
        """Returns a list of all workspaces in current organization

        Args:
            List[CatalogWorkspace]

        Returns:
            List[CatalogWorkspace]:
                List of workspaces in the current organization.
        """
        get_workspaces = functools.partial(
            self._entities_api.get_all_entities_workspaces,
            include=["workspaces"],
            _check_return_type=False,
        )
        workspaces = load_all_entities(get_workspaces)
        return [CatalogWorkspace.from_api(w) for w in workspaces.data]

    # Declarative methods - workspaces

    def get_declarative_workspaces(self) -> CatalogDeclarativeWorkspaces:
        """Get all workspaces in the current organization in a declarative form.

        Args:
            None

        Returns:
            CatalogDeclarativeWorkspaces:
                Declarative Workspaces object including all the workspaces for given organization.
        """
        return CatalogDeclarativeWorkspaces.from_api(self._layout_api.get_workspaces_layout())

    def put_declarative_workspaces(self, workspace: CatalogDeclarativeWorkspaces) -> None:
        """Set layout of all workspaces and their hierarchy. Parameter is in declarative form.

        Args:
            workspace (CatalogDeclarativeWorkspaces):
                Declarative Workspaces object including all the workspaces for given organization.


        Returns:
            None
        """
        self._layout_api.set_workspaces_layout(workspace.to_api())

    def store_declarative_workspaces(self, layout_root_path: Path = Path.cwd()) -> None:
        """Stores declarative workspaces in a given path, as folder hierarchy.

        Args:
            layout_root_path (Path, optional):
                Path to the root of the layout directory. Defaults to Path.cwd().

        Returns:
            None
        """
        self.get_declarative_workspaces().store_to_disk(self.layout_organization_folder(layout_root_path))

    def load_declarative_workspaces(self, layout_root_path: Path = Path.cwd()) -> CatalogDeclarativeWorkspaces:
        """Load declarative workspaces layout, which was stored using store_declarative_workspaces

        Args:
            layout_root_path (Path, optional):
                Path to the root of the layout directory. Defaults to Path.cwd().
        Returns:
            CatalogDeclarativeWorkspaces:
                Declarative Workspaces Object
        """
        return CatalogDeclarativeWorkspaces.load_from_disk(self.layout_organization_folder(layout_root_path))

    def load_and_put_declarative_workspaces(self, layout_root_path: Path = Path.cwd()) -> None:
        """This method combines load_declarative_workspaces and put_declarative_workspaces
        methods to load and set layouts stored using store_declarative_workspaces.

        Args:
            layout_root_path (Path, optional):
                Path to the root of the layout directory. Defaults to Path.cwd().

        Returns:
            None
        """
        declarative_workspaces = self.load_declarative_workspaces(layout_root_path)
        self.put_declarative_workspaces(declarative_workspaces)

    # Declarative methods - workspace

    def get_declarative_workspace(self, workspace_id: str) -> CatalogDeclarativeWorkspaceModel:
        """Retrieve a workspace layout.

        Args:
            workspace_id (str):
                Workspace identification string e.g. "demo"

        Returns:
            CatalogDeclarativeWorkspaceModel:
                Object Containing declarative Logical Data Model and declarative Analytical Model.
        """
        return CatalogDeclarativeWorkspaceModel.from_api(self._layout_api.get_workspace_layout(workspace_id))

    def put_declarative_workspace(self, workspace_id: str, workspace: CatalogDeclarativeWorkspaceModel) -> None:
        """Set a workspace layout.

        Args:
            workspace_id (str):
                Workspace identification string e.g. "demo"
            workspace (CatalogDeclarativeWorkspaceModel):
                Object Containing declarative Logical Data Model and declarative Analytical Model.

        Returns:
            None
        """
        self._layout_api.put_workspace_layout(workspace_id, workspace.to_api())

    def store_declarative_workspace(self, workspace_id: str, layout_root_path: Path = Path.cwd()) -> None:
        """Store workspace layout in a directory hierarchy.

        Args:
            workspace_id (str):
                Workspace identification string e.g. "demo"
            layout_root_path (Path, optional):
                Path to the root of the layout directory. Defaults to Path.cwd().
        """
        workspace_folder = get_workspace_folder(
            workspace_id=workspace_id, layout_organization_folder=self.layout_organization_folder(layout_root_path)
        )
        self.get_declarative_workspace(workspace_id=workspace_id).store_to_disk(workspace_folder=workspace_folder)

    def load_declarative_workspace(
        self, workspace_id: str, layout_root_path: Path = Path.cwd()
    ) -> CatalogDeclarativeWorkspaceModel:
        """Load declarative workspaces layout, which was stored using store_declarative_workspace.

        Args:
            workspace_id (str):
                Workspace identification string e.g. "demo"
            layout_root_path (Path, optional):
                Path to the root of the layout directory. Defaults to Path.cwd().

        Returns:
            CatalogDeclarativeWorkspaceModel:
                Object Containing declarative Logical Data Model and declarative Analytical Model.
        """
        workspace_folder = get_workspace_folder(
            workspace_id=workspace_id, layout_organization_folder=self.layout_organization_folder(layout_root_path)
        )
        return CatalogDeclarativeWorkspaceModel.load_from_disk(workspace_folder=workspace_folder)

    def load_and_put_declarative_workspace(self, workspace_id: str, layout_root_path: Path = Path.cwd()) -> None:
        """This method combines load_declarative_workspace and put_declarative_workspace methods
        to load and set layouts stored using store_declarative_workspace.

        Args:
            workspace_id (str):
                Workspace identification string e.g. "demo"
            layout_root_path (Path, optional):
                Path to the root of the layout directory. Defaults to Path.cwd().

        Returns:
            None
        """
        declarative_workspace = self.load_declarative_workspace(
            workspace_id=workspace_id, layout_root_path=layout_root_path
        )
        self.put_declarative_workspace(workspace_id=workspace_id, workspace=declarative_workspace)

    def clone_workspace(
        self,
        source_workspace_id: str,
        target_workspace_id: Optional[str] = None,
        target_workspace_name: Optional[str] = None,
        overwrite_existing: Optional[bool] = None,
        data_source_mapping: Optional[dict] = None,
        upper_case: Optional[bool] = True,
    ) -> None:
        """Clone workspace from existing workspace.
        Clones complete workspace content - LDM, ADM, permissions.

        If the target workspace already exists, it's content is overwritten.
        This can be useful when testing changes in the clone
          - once you are satisfied, you can clone it back to the origin workspace.
        For the safety, you have to enforce this behavior by the dedicated input argument `overwrite_existing`.

        Beware of workspace data filters - after the clone you have to set WDF value for the new workspace.

        Args:
            source_workspace_id (str):
                Source workspace ID, from which we wanna create a clone
            target_workspace_id (str):
                Target workspace ID, where we wanna clone the source workspace
                Optional, if empty, we generate <source_workspace_id>_clone
            target_workspace_name (str):
                Target workspace name
                Optional, if empty, we generate <source_workspace_name> (Clone)
            overwrite_existing (bool):
                Overwrite existing workspace.
            data_source_mapping (dict):
                Optional, allows users to map LDM to different data source ID
            upper_case (bool):
                Optional, allows users to change the case of all physical object IDs (table names, columns names)
                True changes it to upper-case, False to lower-case, None(default) is noop
                Useful when migrating to Snowflake, which is the only DB with upper-case default.

        Returns:
            None
        """
        # TODO - what if it has already been cloned? List existing WS and find first free WS ID?
        source_declarative_ws = self.get_declarative_workspace(workspace_id=source_workspace_id)
        source_ws = self.get_workspace(source_workspace_id)

        final_target_workspace_id = target_workspace_id or f"{source_workspace_id}_clone"
        final_target_workspace_name = target_workspace_name or f"{source_ws.name} (Clone)"
        # TODO - enable cloning into another hierarchy
        final_target_parent_id = source_ws.parent_id

        try:
            self.get_workspace(final_target_workspace_id)
            if not overwrite_existing:
                raise Exception(
                    f"Target workspace {final_target_workspace_id} already exists, "
                    "and `overwrite_existing` argument is False"
                )
        except NotFoundException:
            self.create_or_update(
                CatalogWorkspace(
                    workspace_id=final_target_workspace_id,
                    name=final_target_workspace_name,
                    parent_id=final_target_parent_id,
                )
            )

        target_declarative_ws = source_declarative_ws
        if source_declarative_ws.ldm:
            target_declarative_ws = attrs.evolve(
                source_declarative_ws,
                ldm=source_declarative_ws.ldm.modify_mapped_data_source(data_source_mapping).change_tables_columns_case(
                    upper_case
                ),
            )

        self.put_declarative_workspace(workspace_id=final_target_workspace_id, workspace=target_declarative_ws)
        self._permissions_service.put_declarative_permissions(
            final_target_workspace_id, self._permissions_service.get_declarative_permissions(source_workspace_id)
        )

    # Declarative methods - workspace data filters

    def get_declarative_workspace_data_filters(self) -> CatalogDeclarativeWorkspaceDataFilters:
        """Retrieve a workspace data filers layout.

        Args:
            None

        Returns:
            CatalogDeclarativeWorkspaceDataFilters:
                Object containing List of declarative workspace data filters.
        """
        return CatalogDeclarativeWorkspaceDataFilters.from_api(self._layout_api.get_workspace_data_filters_layout())

    def put_declarative_workspace_data_filters(
        self, workspace_data_filters: CatalogDeclarativeWorkspaceDataFilters
    ) -> None:
        """Set workspace data filers layout.

        Args:
            workspace_data_filters (CatalogDeclarativeWorkspaceDataFilters):
                Object containing List of declarative workspace data filters.

        Returns:
            None
        """
        self._layout_api.set_workspace_data_filters_layout(
            declarative_workspace_data_filters=workspace_data_filters.to_api()
        )

    def store_declarative_workspace_data_filters(self, layout_root_path: Path = Path.cwd()) -> None:
        """Store workspace data filters layout in a directory hierarchy.

        Args:
            layout_root_path (Path, optional):
                Path to the root of the layout directory. Defaults to Path.cwd().

        Returns:
            None
        """
        self.get_declarative_workspace_data_filters().store_to_disk(self.layout_organization_folder(layout_root_path))

    def load_declarative_workspace_data_filters(
        self, layout_root_path: Path = Path.cwd()
    ) -> CatalogDeclarativeWorkspaceDataFilters:
        """Loads workspace data filters layout, which was stored using store_declarative_workspace_data_filters.

        Args:
            layout_root_path (Path, optional):
                Path to the root of the layout directory. Defaults to Path.cwd().

        Returns:
            CatalogDeclarativeWorkspaceDataFilters:
                Object containing List of declarative workspace data filters.
        """
        return CatalogDeclarativeWorkspaceDataFilters.load_from_disk(self.layout_organization_folder(layout_root_path))

    def load_and_put_declarative_workspace_data_filters(self, layout_root_path: Path = Path.cwd()) -> None:
        """This method combines load_declarative_workspace_data_filters and put_declarative_workspace_data_filters
        methods to load and set layouts stored using store_declarative_workspace_data_filters.

        Args:
            layout_root_path (Path, optional):
                Path to the root of the layout directory. Defaults to Path.cwd().

        Returns:
            None
        """
        declarative_workspace_data_filters = CatalogDeclarativeWorkspaceDataFilters.load_from_disk(
            self.layout_organization_folder(layout_root_path)
        )
        self.put_declarative_workspace_data_filters(declarative_workspace_data_filters)
