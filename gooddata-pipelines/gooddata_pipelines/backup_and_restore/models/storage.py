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
    profile: Optional[str] = None
    aws_access_key_id: Optional[str] = None
    aws_secret_access_key: Optional[str] = None
    aws_default_region: Optional[str] = "us-east-1"

    @classmethod
    def from_iam_role(cls, backup_path: str, bucket: str) -> "S3StorageConfig":
        """Use default IAM role or environment credentials."""
        return cls(backup_path=backup_path, bucket=bucket)

    @classmethod
    def from_aws_credentials(
        cls,
        backup_path: str,
        bucket: str,
        aws_access_key_id: str,
        aws_secret_access_key: str,
        aws_default_region: str,
    ) -> "S3StorageConfig":
        """Use explicit AWS access keys and region."""
        return cls(
            backup_path=backup_path,
            bucket=bucket,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            aws_default_region=aws_default_region,
        )

    @classmethod
    def from_aws_profile(
        cls, backup_path: str, bucket: str, profile: str
    ) -> "S3StorageConfig":
        """Use a named AWS CLI profile."""
        return cls(backup_path=backup_path, bucket=bucket, profile=profile)


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
    api_calls_per_second: Annotated[
        float,
        Field(
            gt=0,
            description="Maximum API calls per second (rate limiting)",
        ),
    ] = Field(default=BackupSettings.DEFAULT_API_CALLS_PER_SECOND)

    @classmethod
    def from_yaml(cls, conf_path: str) -> "BackupRestoreConfig":
        with open(conf_path, "r") as stream:
            conf: dict = yaml.safe_load(stream)
        return cls(**conf)
