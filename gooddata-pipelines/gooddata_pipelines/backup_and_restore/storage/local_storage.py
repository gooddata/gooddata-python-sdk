# (C) 2025 GoodData Corporation

import shutil
from pathlib import Path

from gooddata_pipelines.backup_and_restore.models.storage import (
    BackupRestoreConfig,
    LocalStorageConfig,
)
from gooddata_pipelines.backup_and_restore.storage.base_storage import (
    BackupStorage,
)


class LocalStorage(BackupStorage):
    def __init__(self, conf: BackupRestoreConfig):
        super().__init__(conf)
        if not isinstance(conf.storage, LocalStorageConfig):
            raise ValueError("Local storage config is required")
        self._config: LocalStorageConfig = conf.storage

    def _export(self, folder: str, org_id: str, export_folder: str) -> None:
        """Copies the content of the folder to local storage as backup."""

        self.logger.info(f"Saving {org_id} to local storage")
        shutil.copytree(
            Path(folder), Path(Path.cwd(), export_folder), dirs_exist_ok=True
        )

    def export(self, folder: str, org_id: str) -> None:
        """Copies the content of the folder to local storage as backup."""
        try:
            self._export(folder, org_id, self._config.backup_path)
        except Exception as e:
            self.logger.error(
                f"Error exporting {folder} to {self._config.backup_path}: {e}"
            )
            raise

    def get_ws_declaration(
        self, target_path: str, local_target_path: str
    ) -> None:
        """Retrieves workspace declaration from local storage and copies to the local target path.

        The local target should be a temporary directory.
        """
        file_to_copy = self._backup_path + target_path + "/gooddata_layouts.zip"
        shutil.copy(file_to_copy, local_target_path)
