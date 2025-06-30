# (C) 2025 GoodData Corporation

from enum import Enum
from typing import Annotated, TypeAlias, Optional

import yaml
from pydantic import BaseModel, Field

from gooddata_pipelines.backup_and_restore.constants import BackupSettings


class StorageType(Enum):
    """Type of storage."""

    S3 = "s3"
    LOCAL = "local"


class S3StorageConfig(BaseModel):
    """Configuration for S3 storage."""

    backup_path: str
    bucket: str
    profile: str = "default"
    aws_access_key_id: Optional[str] = None
    aws_secret_access_key: Optional[str] = None
    aws_default_region: Optional[str] = None


class LocalStorageConfig(BaseModel):
    """Placeholder for local storage config."""


StorageConfig: TypeAlias = S3StorageConfig | LocalStorageConfig


class BackupRestoreConfig(BaseModel):
    """Configuration for backup and restore."""

    storage_type: StorageType
    storage: StorageConfig | None = Field(default=None)
    api_page_size: Annotated[
        int,
        Field(
            gt=0,
            description="Page size must be greater than 0",
        ),
    ] = Field(default=BackupSettings.DEFAULT_PAGE_SIZE)
    batch_size: Annotated[
        int,
        Field(
            gt=0,
            description="Batch size must be greater than 0",
        ),
    ] = Field(default=BackupSettings.DEFAULT_BATCH_SIZE)

    @classmethod
    def from_yaml(cls, conf_path: str) -> "BackupRestoreConfig":
        with open(conf_path, "r") as stream:
            conf: dict = yaml.safe_load(stream)
        return cls(**conf)
