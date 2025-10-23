# (C) 2025 GoodData Corporation

import os
import shutil
import tempfile
import time
import traceback
from pathlib import Path
from typing import Any

import attrs
import requests

from gooddata_pipelines.backup_and_restore.backup_input_processor import (
    BackupInputProcessor,
)
from gooddata_pipelines.backup_and_restore.base_manager import BaseManager
from gooddata_pipelines.backup_and_restore.constants import (
    BackupSettings,
    DirNames,
)
from gooddata_pipelines.backup_and_restore.models.input_type import InputType
from gooddata_pipelines.backup_and_restore.models.storage import (
    BackupRestoreConfig,
)
from gooddata_pipelines.backup_and_restore.storage.base_storage import (
    BackupStorage,
)
from gooddata_pipelines.utils.rate_limiter import RateLimiter


@attrs.define
class BackupBatch:
    list_of_ids: list[str]


class BackupManager(BaseManager):
    storage: BackupStorage

    def __init__(self, host: str, token: str, config: BackupRestoreConfig):
        super().__init__(host, token, config)

        self.org_id = self._api.get_organization_id()

        self.loader = BackupInputProcessor(self._api, self.config.api_page_size)

        self._api_rate_limiter = RateLimiter(
            calls_per_second=self.config.api_calls_per_second,
        )

    def get_user_data_filters(self, ws_id: str) -> dict:
        """Returns the user data filters for the specified workspace."""
        with self._api_rate_limiter:
            response: requests.Response = self._api.get_user_data_filters(ws_id)
            if response.ok:
                return response.json()
            else:
                raise RuntimeError(f"{response.status_code}: {response.text}")

    def _store_user_data_filters(
        self,
        user_data_filters: dict,
        export_path: Path,
        ws_id: str,
    ) -> None:
        """Stores the user data filters in the specified export path."""
        os.mkdir(
            os.path.join(
                export_path,
                "gooddata_layouts",
                self.org_id,
                "workspaces",
                ws_id,
                "user_data_filters",
            )
        )

        for filter in user_data_filters["userDataFilters"]:
            udf_file_path = os.path.join(
                export_path,
                "gooddata_layouts",
                self.org_id,
                "workspaces",
                ws_id,
                "user_data_filters",
                filter["id"] + ".yaml",
            )
            self.yaml_utils.dump(udf_file_path, filter)

    @staticmethod
    def _move_folder(source: Path, destination: Path) -> None:
        """Moves the source folder to the destination."""
        shutil.move(source, destination)

    def _get_automations_from_api(self, workspace_id: str) -> Any:
        """Returns automations for the workspace as JSON."""
        with self._api_rate_limiter:
            response: requests.Response = self._api.get_automations(
                workspace_id
            )
            if response.ok:
                return response.json()
            else:
                raise RuntimeError(
                    f"Failed to get automations for {workspace_id}. "
                    + f"{response.status_code}: {response.text}"
                )

    def _store_automations(self, export_path: Path, workspace_id: str) -> None:
        """Stores the automations in the specified export path."""
        # Get the automations from the API
        automations: Any = self._get_automations_from_api(workspace_id)

        automations_folder_path: Path = Path(
            export_path,
            "gooddata_layouts",
            self.org_id,
            "workspaces",
            workspace_id,
            "automations",
        )

        automations_file_path: Path = Path(
            automations_folder_path, "automations.json"
        )

        os.mkdir(automations_folder_path)

        # Store the automations in a JSON file
        if len(automations["data"]) > 0:
            self.json_utils.dump(automations_file_path, automations)

    def store_declarative_filter_views(
        self, export_path: Path, workspace_id: str
    ) -> None:
        """Stores the filter views in the specified export path."""
        # Get the filter views YAML files from the API
        with self._api_rate_limiter:
            self._api.store_declarative_filter_views(workspace_id, export_path)

        # Move filter views to the subfolder containing the analytics model
        self._move_folder(
            Path(export_path, "gooddata_layouts", self.org_id, "filter_views"),
            Path(
                export_path,
                "gooddata_layouts",
                self.org_id,
                "workspaces",
                workspace_id,
                "filter_views",
            ),
        )

    def _get_workspace_export(
        self,
        local_target_path: str,
        workspaces_to_export: list[str],
    ) -> None:
        """
        Iterate over all workspaces in the workspaces_to_export list and store
        their declarative_workspace and their respective user data filters.
        """
        exported = False
        for workspace_id in workspaces_to_export:
            export_path = Path(
                local_target_path,
                self.org_id,
                workspace_id,
                BackupSettings.TIMESTAMP_SDK_FOLDER,
            )

            try:
                user_data_filters = self.get_user_data_filters(workspace_id)
            except Exception as e:
                self.logger.error(
                    f"Skipping backup of {workspace_id} - check if workspace exists."
                    + f"{e.__class__.__name__}: {e}"
                )
                continue

            try:
                # TODO: consider using the API to get JSON declarations in memory
                # or check if there is a way to get YAML structures directly from
                # the SDK. That way we could save and package all the declarations
                # directly instead of reorganizing the folder structures. That should
                # be more transparent/readable and possibly safer for threading
                with self._api_rate_limiter:
                    self._api.store_declarative_workspace(
                        workspace_id, export_path
                    )
                self.store_declarative_filter_views(export_path, workspace_id)
                self._store_automations(export_path, workspace_id)

                self._store_user_data_filters(
                    user_data_filters, export_path, workspace_id
                )
                self.logger.info(f"Stored export for {workspace_id}")
                exported = True
            except Exception as e:
                self.logger.error(
                    f"Skipping {workspace_id}. {e.__class__.__name__} encountered: {e}"
                )

        if not exported:
            raise RuntimeError(
                "None of the workspaces were exported. Check that the source file "
                + "is correct and that the workspaces exist."
            )

    def _archive_gooddata_layouts_to_zip(self, folder: str) -> None:
        """Archives the gooddata_layouts directory to a zip file."""
        try:
            target_subdir = ""
            for subdir, dirs, files in os.walk(folder):
                if DirNames.LAYOUTS in dirs:
                    target_subdir = os.path.join(subdir, dirs[0])
                if DirNames.LDM in dirs:
                    inner_layouts_dir = subdir + "/gooddata_layouts"
                    os.mkdir(inner_layouts_dir)
                    for dir in dirs:
                        shutil.move(
                            os.path.join(subdir, dir),
                            os.path.join(inner_layouts_dir),
                        )
                    shutil.make_archive(target_subdir, "zip", subdir)
                    shutil.rmtree(target_subdir)
        except Exception as e:
            self.logger.error(f"Error archiving {folder} to zip: {e}")
            raise

    @staticmethod
    def _split_to_batches(
        workspaces_to_export: list[str], batch_size: int
    ) -> list[BackupBatch]:
        """Splits the list of workspaces into batches of the specified size.
        The batch is represented as a list of workspace IDs.
        Returns a list of batches (i.e. list of lists of IDs)
        """
        list_of_batches = []
        while workspaces_to_export:
            batch = BackupBatch(workspaces_to_export[:batch_size])
            workspaces_to_export = workspaces_to_export[batch_size:]
            list_of_batches.append(batch)

        return list_of_batches

    def _process_batch(
        self,
        batch: BackupBatch,
        retry_count: int = 0,
    ) -> None:
        """Processes a single batch of workspaces for backup.
        If the batch processing fails, the function will wait
        and retry with exponential backoff up to BackupSettings.MAX_RETRIES.
        The base wait time is defined by BackupSettings.RETRY_DELAY.
        """
        try:
            with tempfile.TemporaryDirectory() as tmpdir:
                self._get_workspace_export(tmpdir, batch.list_of_ids)

                self._archive_gooddata_layouts_to_zip(
                    str(Path(tmpdir, self.org_id))
                )

                self.storage.export(tmpdir, self.org_id)

        except Exception as e:
            if retry_count < BackupSettings.MAX_RETRIES:
                # Retry with exponential backoff until MAX_RETRIES
                next_retry = retry_count + 1
                wait_time = BackupSettings.RETRY_DELAY**next_retry
                self.logger.info(
                    f"{e.__class__.__name__} encountered while processing a batch. "
                    + f"Retrying {next_retry}/{BackupSettings.MAX_RETRIES} "
                    + f"in {wait_time} seconds..."
                )

                time.sleep(wait_time)
                self._process_batch(batch, next_retry)
            else:
                # If the batch fails after MAX_RETRIES, raise the error
                self.logger.error(f"Batch failed: {e.__class__.__name__}: {e}")
                raise

    def _process_batches(
        self,
        batches: list[BackupBatch],
    ) -> None:
        """
        Processes batches sequentially to avoid overloading the API.
        If any batch fails, the processing will stop.
        """
        for i, batch in enumerate(batches, 1):
            self.logger.info(f"Processing batch {i}/{len(batches)}...")
            self._process_batch(batch)

    def backup_workspaces(
        self,
        path_to_csv: str | None = None,
        workspace_ids: list[str] | None = None,
    ) -> None:
        """Runs the backup process for a list of workspace IDs.

        Will take the list of workspace IDs or read the list of
        workspace IDs from a CSV file and create backup for each
        workspace in storage specified in the configuration.

        Args:
            path_to_csv (str): Path to a CSV file containing a list of workspace IDs
            workspace_ids (list[str]): List of workspace IDs
        """
        self._backup(InputType.LIST_OF_WORKSPACES, path_to_csv, workspace_ids)

    def backup_hierarchies(
        self,
        path_to_csv: str | None = None,
        workspace_ids: list[str] | None = None,
    ) -> None:
        """Runs the backup process for a list of hierarchies.

        Will take the list of workspace IDs or read the list of workspace IDs
        from a CSV file and create backup for each of those workspaces' hierarchies
        in storage specified in the configuration.
        Workspace hierarchy means the workspace itself and all its direct and
        indirect children.

        Args:
            path_to_csv (str): Path to a CSV file containing a list of workspace IDs
            workspace_ids (list[str]): List of workspace IDs
        """
        self._backup(InputType.HIERARCHY, path_to_csv, workspace_ids)

    def backup_entire_organization(self) -> None:
        """Runs the backup process for the entire organization.

        Will create backup for all workspaces in the organization in storage
        specified in the configuration.
        """
        self._backup(InputType.ORGANIZATION)

    def _backup(
        self,
        input_type: InputType,
        path_to_csv: str | None = None,
        workspace_ids: list[str] | None = None,
    ) -> None:
        """Runs the backup process with the selected input type."""
        try:
            workspaces_to_export: list[str] = self.loader.get_ids_to_backup(
                input_type,
                path_to_csv,
                workspace_ids,
            )
            batches = self._split_to_batches(
                workspaces_to_export, self.config.batch_size
            )

            self.logger.info(
                f"Exporting {len(workspaces_to_export)} workspaces in {len(batches)} batches."
            )

            self._process_batches(batches)

            self.logger.info("Backup completed")
        except Exception as e:
            self.logger.error(f"Backup failed: {e.__class__.__name__}: {e}")
            self.logger.error(traceback.format_exc())
            raise
