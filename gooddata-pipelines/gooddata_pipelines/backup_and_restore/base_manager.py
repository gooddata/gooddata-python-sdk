# (C) 2025 GoodData Corporation

import abc
from pathlib import Path
from typing import Type, TypeVar

from gooddata_sdk.utils import PROFILES_FILE_PATH, profile_content

from gooddata_pipelines.api.gooddata_api_wrapper import GoodDataApi
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
from gooddata_pipelines.backup_and_restore.storage.s3_storage import S3Storage
from gooddata_pipelines.logger import LogObserver
from gooddata_pipelines.utils.file_utils import JsonUtils, YamlUtils

ManagerT = TypeVar("ManagerT", bound="BaseManager")


class BaseManager(abc.ABC):
    """Base class to provide constructors for backup and restore managers."""

    storage: BackupStorage

    def __init__(self, host: str, token: str, config: BackupRestoreConfig):
        self.config = config

        self._api: GoodDataApi = GoodDataApi(host, token)
        self.logger: LogObserver = LogObserver()

        self.storage = self._get_storage(self.config)

        self.yaml_utils = YamlUtils()
        self.json_utils = JsonUtils()

    def _get_storage(self, conf: BackupRestoreConfig) -> BackupStorage:
        """Returns the storage class based on the storage type."""
        if conf.storage_type == StorageType.S3:
            return S3Storage(conf)
        elif conf.storage_type == StorageType.LOCAL:
            return LocalStorage(conf)
        else:
            raise RuntimeError(
                f'Unsupported storage type "{conf.storage_type.value}".'
            )

    @classmethod
    def create(
        cls: Type[ManagerT],
        config: BackupRestoreConfig,
        host: str,
        token: str,
    ) -> ManagerT:
        """Creates a backup worker instance using the provided host and token."""
        return cls(host=host, token=token, config=config)

    @classmethod
    def create_from_profile(
        cls: Type[ManagerT],
        config: BackupRestoreConfig,
        profile: str = "default",
        profiles_path: Path = PROFILES_FILE_PATH,
    ) -> ManagerT:
        """Creates a backup worker instance using a GoodData profile file."""
        content = profile_content(profile, profiles_path)
        return cls(host=content["host"], token=content["token"], config=config)
