# (C) 2025 GoodData Corporation

import abc

from gooddata_pipelines.backup_and_restore.models.storage import (
    BackupRestoreConfig,
)
from gooddata_pipelines.logger import LogObserver


class BackupStorage(abc.ABC):
    def __init__(self, conf: BackupRestoreConfig):
        self.logger = LogObserver()

        suffix = "/" if not conf.storage.backup_path.endswith("/") else ""
        self._backup_path = conf.storage.backup_path + suffix

    @abc.abstractmethod
    def export(self, folder: str, org_id: str) -> None:
        """Exports the content of the folder to the storage."""
        raise NotImplementedError

    @abc.abstractmethod
    def get_ws_declaration(
        self, target_path: str, local_target_path: str
    ) -> None:
        raise NotImplementedError(
            "This method should be implemented by the subclass."
        )
