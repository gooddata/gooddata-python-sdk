# (C) 2025 GoodData Corporation

import json
import os
import shutil
import tempfile
import threading
import time
import traceback
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Type

import requests
import yaml
from gooddata_sdk.utils import PROFILES_FILE_PATH, profile_content

from gooddata_pipelines.api.gooddata_api_wrapper import GoodDataApi
from gooddata_pipelines.backup_and_restore.backup_input_processor import (
    BackupInputProcessor,
)
from gooddata_pipelines.backup_and_restore.constants import (
    BackupSettings,
    DirNames,
)
from gooddata_pipelines.backup_and_restore.models.input_type import InputType
from gooddata_pipelines.backup_and_restore.models.storage import (
    BackupRestoreConfig,
    StorageType,
)
from gooddata_pipelines.backup_and_restore.storage.base_storage import (
    BackupStorage,
)
from gooddata_pipelines.backup_and_restore.storage.local_storage import (
    LocalStorage,
)
from gooddata_pipelines.backup_and_restore.storage.s3_storage import (
    S3Storage,
)
from gooddata_pipelines.logger import LogObserver


@dataclass
class BackupBatch:
    list_of_ids: list[str]


class BackupManager:
    storage: BackupStorage

    def __init__(self, host: str, token: str, config: BackupRestoreConfig):
        self._api = GoodDataApi(host, token)
        self.logger = LogObserver()

        self.config = config

        self.storage = self.get_storage(self.config)
        self.org_id = self._api.get_organization_id()

        self.loader = BackupInputProcessor(self._api, self.config.api_page_size)

    @classmethod
    def create(
        cls: Type["BackupManager"],
        config: BackupRestoreConfig,
        host: str,
        token: str,
    ) -> "BackupManager":
        """Creates a backup worker instance using provided host and token."""
        return cls(host=host, token=token, config=config)

    @classmethod
    def create_from_profile(
        cls: Type["BackupManager"],
        config: BackupRestoreConfig,
        profile: str = "default",
        profiles_path: Path = PROFILES_FILE_PATH,
    ) -> "BackupManager":
        """Creates a backup worker instance using a GoodData profile file."""
        content = profile_content(profile, profiles_path)
        return cls(**content, config=config)

    def get_storage(self, conf: BackupRestoreConfig) -> BackupStorage:
        """Returns the storage class based on the storage type."""
        if conf.storage_type == StorageType.S3:
            return S3Storage(conf)
        elif conf.storage_type == StorageType.LOCAL:
            return LocalStorage(conf)
        else:
            raise RuntimeError(
                f'Unsupported storage type "{conf.storage_type.value}".'
            )

    def get_user_data_filters(self, ws_id: str) -> dict:
        """Returns the user data filters for the specified workspace."""
        response: requests.Response = self._api.get_user_data_filters(ws_id)
        if response.ok:
            return response.json()
        else:
            raise RuntimeError(f"{response.status_code}: {response.text}")

    def store_user_data_filters(
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
            self.write_to_yaml(udf_file_path, filter)

    @staticmethod
    def move_folder(source: Path, destination: Path) -> None:
        """Moves the source folder to the destination."""
        shutil.move(source, destination)

    @staticmethod
    def write_to_yaml(path: str, source: Any) -> None:
        """Writes the source to a YAML file."""
        with open(path, "w") as outfile:
            yaml.dump(source, outfile)

    def get_automations_from_api(self, workspace_id: str) -> Any:
        """Returns automations for the workspace as JSON."""
        response: requests.Response = self._api.get_automations(workspace_id)
        if response.ok:
            return response.json()
        else:
            raise RuntimeError(
                f"Failed to get automations for {workspace_id}. "
                + f"{response.status_code}: {response.text}"
            )

    def store_automations(self, export_path: Path, workspace_id: str) -> None:
        """Stores the automations in the specified export path."""
        # Get the automations from the API
        automations: Any = self.get_automations_from_api(workspace_id)

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
            with open(automations_file_path, "w") as f:
                json.dump(automations, f)

    def store_declarative_filter_views(
        self, export_path: Path, workspace_id: str
    ) -> None:
        """Stores the filter views in the specified export path."""
        # Get the filter views YAML files from the API
        self._api.store_declarative_filter_views(workspace_id, export_path)

        # Move filter views to the subfolder containing analytics model
        self.move_folder(
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

    def get_workspace_export(
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
                self._api.store_declarative_workspace(workspace_id, export_path)
                self.store_declarative_filter_views(export_path, workspace_id)
                self.store_automations(export_path, workspace_id)

                self.store_user_data_filters(
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

    def archive_gooddata_layouts_to_zip(self, folder: str) -> None:
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

    def split_to_batches(
        self, workspaces_to_export: list[str], batch_size: int
    ) -> list[BackupBatch]:
        """Splits the list of workspaces to into batches of the specified size.
        The batch is respresented as a list of workspace IDs.
        Returns a list of batches (i.e. list of lists of IDs)
        """
        list_of_batches = []
        while workspaces_to_export:
            batch = BackupBatch(workspaces_to_export[:batch_size])
            workspaces_to_export = workspaces_to_export[batch_size:]
            list_of_batches.append(batch)

        return list_of_batches

    def process_batch(
        self,
        batch: BackupBatch,
        stop_event: threading.Event,
        retry_count: int = 0,
    ) -> None:
        """Processes a single batch of workspaces for backup.
        If the batch processing fails, the function will wait
        and retry with exponential backoff up to BackupSettings.MAX_RETRIES.
        The base wait time is defined by BackupSettings.RETRY_DELAY.
        """
        if stop_event.is_set():
            # If the stop_event flag is set, return. This will terminate the thread.
            return

        try:
            with tempfile.TemporaryDirectory() as tmpdir:
                self.get_workspace_export(tmpdir, batch.list_of_ids)

                self.archive_gooddata_layouts_to_zip(
                    str(Path(tmpdir, self.org_id))
                )

                self.storage.export(tmpdir, self.org_id)

        except Exception as e:
            if stop_event.is_set():
                return

            elif retry_count < BackupSettings.MAX_RETRIES:
                # Retry with exponential backoff until MAX_RETRIES.
                next_retry = retry_count + 1
                wait_time = BackupSettings.RETRY_DELAY**next_retry
                self.logger.info(
                    f"{e.__class__.__name__} encountered while processing a batch. "
                    + f"Retrying {next_retry}/{BackupSettings.MAX_RETRIES} "
                    + f"in {wait_time} seconds..."
                )

                time.sleep(wait_time)
                self.process_batch(batch, stop_event, next_retry)
            else:
                # If the batch fails after MAX_RETRIES, raise the error.
                self.logger.error(f"Batch failed: {e.__class__.__name__}: {e}")
                raise

    def process_batches_in_parallel(
        self,
        batches: list[BackupBatch],
    ) -> None:
        """
        Processes batches in parallel using concurrent.futures. Will stop the processing
        if any one of the batches fails.
        """

        # Create a threading flag to control the threads that have already been started
        stop_event = threading.Event()

        with ThreadPoolExecutor(
            max_workers=BackupSettings.MAX_WORKERS
        ) as executor:
            # Set the futures tasks.
            futures = []
            for batch in batches:
                futures.append(
                    executor.submit(
                        self.process_batch,
                        batch,
                        stop_event,
                    )
                )

            # Process futures as they complete
            for future in as_completed(futures):
                try:
                    future.result()
                except Exception:
                    # On failure, set the flag to True - signal running processes to stop.
                    stop_event.set()

                    # Cancel unstarted threads.
                    for f in futures:
                        if not f.done():
                            f.cancel()

                    raise

    def backup_workspaces(
        self, path_to_csv: str | None, workspace_ids: list[str] | None
    ) -> None:
        """Runs the backup process for a list of workspace IDs.

        Will take the list of workspace IDs or read the list of
        workspace IDs from a CSV file and create backup for each
        workspace in storage specified in the configuration.

        Args:
            path_to_csv (str): Path to a CSV file containing a list of workspace IDs.
            workspace_ids (list[str]): List of workspace IDs
        """
        self.backup(InputType.LIST_OF_WORKSPACES, path_to_csv, workspace_ids)

    def backup_hierarchies(
        self, path_to_csv: str | None, workspace_ids: list[str] | None
    ) -> None:
        """Runs the backup process for a list of hierarchies.

        Will take the list of workspace IDs or read the list of workspace IDs
        from a CSV file and create backup for each those workspaces' hierarchies
        in storage specified in the configuration.
        Workspace hierarchy means the workspace itself and all its direct and
        indirect children.

        Args:
            path_to_csv (str): Path to a CSV file containing a list of workspace IDs.
            workspace_ids (list[str]): List of workspace IDs
        """
        self.backup(InputType.HIERARCHY, path_to_csv, workspace_ids)

    def backup_entire_organization(self) -> None:
        """Runs the backup process for the entire organization.

        Will create backup for all workspaces in the organization in storage
        specified in the configuration.
        """
        self.backup(InputType.ORGANIZATION)

    def backup(
        self,
        input_type: InputType,
        path_to_csv: str | None = None,
        workspace_ids: list[str] | None = None,
    ) -> None:
        """Runs the backup process with selected input type."""
        try:
            workspaces_to_export: list[str] = self.loader.get_ids_to_backup(
                input_type,
                path_to_csv,
                workspace_ids,
            )
            batches = self.split_to_batches(
                workspaces_to_export, self.config.batch_size
            )

            self.logger.info(
                f"Exporting {len(workspaces_to_export)} workspaces in {len(batches)} batches."
            )

            self.process_batches_in_parallel(batches)

            self.logger.info("Backup completed")
        except Exception as e:
            self.logger.error(f"Backup failed: {e.__class__.__name__}: {e}")
            self.logger.error(traceback.format_exc())
            raise
