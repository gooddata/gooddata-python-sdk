# (C) 2025 GoodData Corporation

import abc

from gooddata_pipelines.backup_and_restore.models.storage import (
    BackupRestoreConfig,
)
from gooddata_pipelines.logger import LogObserver


class BackupStorage(abc.ABC):
    def __init__(self, conf: BackupRestoreConfig):
        self.logger = LogObserver()

    @abc.abstractmethod
    def export(self, folder: str, org_id: str) -> None:
        """Exports the content of the folder to the storage."""
        raise NotImplementedError
