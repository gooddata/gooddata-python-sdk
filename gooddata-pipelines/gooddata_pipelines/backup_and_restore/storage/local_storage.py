# (C) 2025 GoodData Corporation

import shutil
from pathlib import Path

from gooddata_pipelines.backup_and_restore.models.storage import (
    BackupRestoreConfig,
)
from gooddata_pipelines.backup_and_restore.storage.base_storage import (
    BackupStorage,
)


class LocalStorage(BackupStorage):
    def __init__(self, conf: BackupRestoreConfig):
        super().__init__(conf)

    def _export(
        self, folder: str, org_id: str, export_folder: str = "local_backups"
    ) -> None:
        """Copies the content of the folder to local storage as backup."""
        self.logger.info(f"Saving {org_id} to local storage")
        shutil.copytree(
            Path(folder), Path(Path.cwd(), export_folder), dirs_exist_ok=True
        )

    def export(
        self, folder: str, org_id: str, export_folder: str = "local_backups"
    ) -> None:
        """Copies the content of the folder to local storage as backup."""
        try:
            self._export(folder, org_id, export_folder)
        except Exception as e:
            self.logger.error(
                f"Error exporting {folder} to {export_folder}: {e}"
            )
            raise
