# (C) 2025 GoodData Corporation

import os
import tempfile
import zipfile
from pathlib import Path
from typing import Any

import attrs
from gooddata_sdk.catalog.workspace.declarative_model.workspace.analytics_model.analytics_model import (
    CatalogDeclarativeAnalytics,
)
from gooddata_sdk.catalog.workspace.declarative_model.workspace.automation import (
    CatalogDeclarativeAutomation,
)
from gooddata_sdk.catalog.workspace.declarative_model.workspace.logical_model.ldm import (
    CatalogDeclarativeModel,
)
from gooddata_sdk.catalog.workspace.declarative_model.workspace.workspace import (
    CatalogDeclarativeFilterView,
)
from pydantic import BaseModel, ConfigDict

from gooddata_pipelines.backup_and_restore.base_manager import BaseManager
from gooddata_pipelines.backup_and_restore.constants import DirNames
from gooddata_pipelines.utils.decorators import log_and_reraise_exception


@attrs.define
class WorkspaceModel:
    logical_data_model: CatalogDeclarativeModel
    analytics_model: CatalogDeclarativeAnalytics


class WorkspaceToRestore(BaseModel):
    """Workspace to restore.

    Args:
        id: The ID of the workspace to restore.
        path: The path to the folder containing the `gooddata_layouts.zip` file
            to restore. Should be a continuation of the `backup_path` specified
            in the storage configuration. Typically, it would look something like
            `organization_id/workspace_id/backup_timestamp`
    """

    model_config = ConfigDict(extra="forbid")

    id: str
    path: str


class RestoreManager(BaseManager):
    """Restores previsouly created backups of workspace metadata."""

    @log_and_reraise_exception("Failed to extract backup from zip archive.")
    def _extract_zip_archive(
        self, file_to_extract: Path, destination: Path
    ) -> None:
        """Extracts the backup from zip archive."""
        with zipfile.ZipFile(file_to_extract, "r") as zip_ref:
            zip_ref.extractall(destination)

    def _check_workspace_is_valid(self, workspace_root_dir_path: Path) -> None:
        """Checks if the workspace layout is valid."""
        if (
            not workspace_root_dir_path.exists()
            or not workspace_root_dir_path.is_dir()
        ):
            self.logger.error(
                "Invalid source path found upon backup fetch. "
                f"Got {workspace_root_dir_path}. "
                "Check if target zip contains gooddata_layouts directory."
            )
            raise RuntimeError("Invalid source path upon load.")

        children = list(workspace_root_dir_path.iterdir())
        am_path = workspace_root_dir_path / DirNames.AM
        ldm_path = workspace_root_dir_path / DirNames.LDM
        udf_path = workspace_root_dir_path / DirNames.UDF

        if (
            am_path not in children
            or ldm_path not in children
            or udf_path not in children
        ):
            self.logger.error(
                f"{DirNames.AM} or {DirNames.LDM} directory missing in the "
                + "workspace hierarchy. "
            )
            raise RuntimeError(
                f"{DirNames.AM} or {DirNames.LDM} directory missing."
            )

    @log_and_reraise_exception("Failed to load workspace declaration.")
    def _load_workspace_layout(
        self, workspace_root_dir_path: Path
    ) -> WorkspaceModel:
        """Loads the workspace layout from the backup."""
        sdk_catalog = self._api._sdk.catalog_workspace_content

        ldm = sdk_catalog.load_ldm_from_disk(workspace_root_dir_path)
        am = sdk_catalog.load_analytics_model_from_disk(workspace_root_dir_path)

        return WorkspaceModel(logical_data_model=ldm, analytics_model=am)

    @log_and_reraise_exception("Failed to load user data filters from folder.")
    def _load_user_data_filters(self, workspace_root_dir_path: Path) -> dict:
        user_data_filters: dict = {"userDataFilters": []}
        user_data_filters_folder = os.path.join(
            workspace_root_dir_path, DirNames.UDF
        )
        for filename in os.listdir(user_data_filters_folder):
            file_path = os.path.join(user_data_filters_folder, filename)
            user_data_filter = self.yaml_utils.safe_load(Path(file_path))
            user_data_filters["userDataFilters"].append(user_data_filter)

        return user_data_filters

    @log_and_reraise_exception("Failed to put workspace layout into GoodData.")
    def _put_workspace_layout(
        self, workspace_id: str, workspace_model: WorkspaceModel
    ) -> None:
        """Puts the workspace layout into GoodData."""
        self._api._sdk.catalog_workspace_content.put_declarative_ldm(
            workspace_id, workspace_model.logical_data_model
        )
        self._api._sdk.catalog_workspace_content.put_declarative_analytics_model(
            workspace_id, workspace_model.analytics_model
        )

    @log_and_reraise_exception("Failed to put user data filters.")
    def _put_user_data_filters(
        self, workspace_id: str, user_data_filters: dict
    ) -> None:
        """Puts the user data filters into GoodData workspace."""
        response = self._api.put_user_data_filters(
            workspace_id, user_data_filters
        )
        self._api.raise_if_response_not_ok(response)

    def _load_and_put_filter_views(
        self, workspace_id: str, workspace_root_dir_path: Path
    ) -> None:
        """Loads and puts filter views into GoodData workspace."""
        filter_views: list[CatalogDeclarativeFilterView] = []
        if not (workspace_root_dir_path / "filter_views").exists():
            # Skip if the filter_views directory does not exist
            return

        for file in Path(workspace_root_dir_path / "filter_views").iterdir():
            filter_view_content: dict[str, Any] = dict(
                self.yaml_utils.safe_load(file)
            )
            filter_view: CatalogDeclarativeFilterView = (
                CatalogDeclarativeFilterView.from_dict(filter_view_content)
            )
            filter_views.append(filter_view)

        if filter_views:
            self._api._sdk.catalog_workspace.put_declarative_filter_views(
                workspace_id, filter_views
            )

    def _load_and_post_automations(
        self, workspace_id: str, workspace_root_dir_path: Path
    ) -> None:
        """Loads automations from specified json file and creates them in the workspace."""
        # Load automations from JSON
        path_to_json: Path = Path(
            workspace_root_dir_path, "automations", "automations.json"
        )

        # Both the folder and the file must exist, otherwise skip
        if not (workspace_root_dir_path.exists() and path_to_json.exists()):
            return

        # Delete all automations from the workspace and restore the automations from the backup.
        self._delete_all_automations(workspace_id)

        data: dict = self.json_utils.load(path_to_json)
        automations: list[dict] = data["data"]

        for automation in automations:
            self._post_automation(workspace_id, automation)

    def _delete_all_automations(self, workspace_id: str) -> None:
        """Deletes all automations in the workspace."""
        automations: list[CatalogDeclarativeAutomation] = (
            self._api._sdk.catalog_workspace.get_declarative_automations(
                workspace_id
            )
        )
        for automation in automations:
            self._api.delete_automation(workspace_id, automation.id)

    def _post_automation(self, workspace_id: str, automation: dict) -> None:
        """Posts a scheduled export to the workspace."""
        attributes: dict = automation["attributes"]
        relationships: dict = automation["relationships"]
        id: str = automation["id"]

        if attributes.get("schedule"):
            if attributes["schedule"].get("cronDescription"):
                # The cron description attribute is causing a 500 ("No mapping found...")
                # error. Known and reported issue.
                del attributes["schedule"]["cronDescription"]

        data = {
            "data": {
                "attributes": attributes,
                "id": id,
                "type": "automation",
                "relationships": relationships,
            }
        }

        response = self._api.post_automation(workspace_id, data)

        if not response.ok:
            self.logger.error(
                f"Failed to post automation ({response.status_code}): {response.text}"
            )

    def _restore_backup(
        self, workspace_to_restore: WorkspaceToRestore, tempdir_path: Path
    ) -> None:
        """Restores the backup of a workspace."""

        zip_target = tempdir_path / f"{DirNames.LAYOUTS}.zip"
        src_path = tempdir_path / DirNames.LAYOUTS

        try:
            self.storage.get_ws_declaration(
                workspace_to_restore.path, str(zip_target)
            )
            self._extract_zip_archive(zip_target, tempdir_path)
            self._check_workspace_is_valid(src_path)
            workspace_model: WorkspaceModel = self._load_workspace_layout(
                src_path
            )
            user_data_filters = self._load_user_data_filters(src_path)
            self._put_workspace_layout(workspace_to_restore.id, workspace_model)
            self._put_user_data_filters(
                workspace_to_restore.id, user_data_filters
            )
            self._load_and_put_filter_views(workspace_to_restore.id, src_path)
            self._load_and_post_automations(workspace_to_restore.id, src_path)
            self.logger.info(
                f"Finished backup restore of {workspace_to_restore.id} from {workspace_to_restore.path}."
            )
        except Exception as e:
            self.logger.error(
                f"Failed to restore backup of {workspace_to_restore.id} from {workspace_to_restore.path}. "
                f"Error caused by {e.__class__.__name__}: {e}."
            )

    def restore(self, workspaces_to_restore: list[WorkspaceToRestore]) -> None:
        """Restores the backups of workspaces.

        Args:
            workspaces_to_restore: List of workspaces to restore.
        """
        for workspace_to_restore in workspaces_to_restore:
            with tempfile.TemporaryDirectory() as tempdir:
                tempdir_path = Path(tempdir)
                self._restore_backup(workspace_to_restore, tempdir_path)
