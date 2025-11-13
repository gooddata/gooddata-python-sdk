# (C) 2025 GoodData Corporation

from enum import Enum
from typing import Annotated

import yaml
from pydantic import BaseModel, Field, model_validator

from gooddata_pipelines.backup_and_restore.constants import BackupSettings


class StorageType(Enum):
    """Type of storage."""

    S3 = "s3"
    LOCAL = "local"
    AZURE = "azure"


class S3StorageConfig(BaseModel):
    """Configuration for S3 storage.

    Can be created using the following constructor methods:
    - `from_iam_role`
    - `from_aws_credentials`
    - `from_aws_profile`
    """

    backup_path: str
    bucket: str
    profile: str | None = None
    aws_access_key_id: str | None = None
    aws_secret_access_key: str | None = None
    aws_default_region: str = "us-east-1"

    @classmethod
    def from_iam_role(cls, backup_path: str, bucket: str) -> "S3StorageConfig":
        """Use default IAM role or environment credentials.

        Args:
            backup_path: The path to the backup directory.
            bucket: The name of the S3 bucket.

        Returns:
            S3StorageConfig: The S3 storage configuration.
        """
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
        """Use explicit AWS access keys and region.

        Args:
            backup_path: The path to the backup directory.
            bucket: The name of the S3 bucket.
            aws_access_key_id: The AWS access key ID.
            aws_secret_access_key: The AWS secret access key.
            aws_default_region: The AWS default region.

        Returns:
            S3StorageConfig: The S3 storage configuration.
        """
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
        """Use a named AWS CLI profile.

        Args:
            backup_path: The path to the backup directory.
            bucket: The name of the S3 bucket.
            profile: The name of the AWS profile.

        Returns:
            S3StorageConfig: The S3 storage configuration.
        """
        return cls(backup_path=backup_path, bucket=bucket, profile=profile)


class AzureStorageConfig(BaseModel):
    """Configuration for Azure Blob Storage.

    Can be created using the following constructor methods:
    - `from_workload_identity`
    - `from_connection_string`
    - `from_service_principal`
    """

    backup_path: str
    account_name: str
    container: str
    connection_string: str | None = None
    client_id: str | None = None
    client_secret: str | None = None
    tenant_id: str | None = None

    @classmethod
    def from_workload_identity(
        cls, backup_path: str, account_name: str, container: str
    ) -> "AzureStorageConfig":
        """Use Azure Workload Identity (for Kubernetes).

        Args:
            backup_path: The path to the backup directory.
            account_name: The Azure storage account name.
            container: The name of the blob container.

        Returns:
            AzureStorageConfig: The Azure storage configuration.
        """
        return cls(
            backup_path=backup_path,
            account_name=account_name,
            container=container,
        )

    @classmethod
    def from_connection_string(
        cls,
        backup_path: str,
        account_name: str,
        container: str,
        connection_string: str,
    ) -> "AzureStorageConfig":
        """Use Azure Storage connection string.

        Args:
            backup_path: The path to the backup directory.
            account_name: The Azure storage account name.
            container: The name of the blob container.
            connection_string: The Azure Storage connection string.

        Returns:
            AzureStorageConfig: The Azure storage configuration.
        """
        return cls(
            backup_path=backup_path,
            account_name=account_name,
            container=container,
            connection_string=connection_string,
        )

    @classmethod
    def from_service_principal(
        cls,
        backup_path: str,
        account_name: str,
        container: str,
        client_id: str,
        client_secret: str,
        tenant_id: str,
    ) -> "AzureStorageConfig":
        """Use Azure Service Principal credentials.

        Args:
            backup_path: The path to the backup directory.
            account_name: The Azure storage account name.
            container: The name of the blob container.
            client_id: The Azure client ID.
            client_secret: The Azure client secret.
            tenant_id: The Azure tenant ID.

        Returns:
            AzureStorageConfig: The Azure storage configuration.
        """
        return cls(
            backup_path=backup_path,
            account_name=account_name,
            container=container,
            client_id=client_id,
            client_secret=client_secret,
            tenant_id=tenant_id,
        )


class LocalStorageConfig(BaseModel):
    """Placeholder for local storage config."""

    backup_path: str = Field(default="local_backups")


class BackupRestoreConfig(BaseModel):
    """Configuration for backup and restore.

    Args:
        storage_type: The type of storage to use. Defaults to `StorageType.LOCAL`.
        storage: Storage configuration. Either `S3StorageConfig`, `AzureStorageConfig`, or `LocalStorageConfig`. Defaults to `LocalStorageConfig()`.
        api_page_size: The page size for fetching workspace relationships. Defaults to `BackupSettings.API.PAGE_SIZE`.
        batch_size: The batch size for fetching workspace relationships. Defaults to `BackupSettings.API.BATCH_SIZE`.
        api_calls_per_second: The maximum API calls per second (rate limiting). Defaults to `BackupSettings.API.CALLS_PER_SECOND`.
    """

    storage_type: StorageType = Field(default=StorageType.LOCAL)
    storage: S3StorageConfig | AzureStorageConfig | LocalStorageConfig = Field(
        default_factory=LocalStorageConfig
    )
    api_page_size: Annotated[
        int,
        Field(
            gt=0,
            description="Page size must be greater than 0",
        ),
    ] = Field(default=BackupSettings.API.PAGE_SIZE)
    batch_size: Annotated[
        int,
        Field(
            gt=0,
            description="Batch size must be greater than 0",
        ),
    ] = Field(default=BackupSettings.API.BATCH_SIZE)
    api_calls_per_second: Annotated[
        float,
        Field(
            gt=0,
            description="Maximum API calls per second (rate limiting)",
        ),
    ] = Field(default=BackupSettings.API.CALLS_PER_SECOND)

    @classmethod
    def from_yaml(cls, conf_path: str) -> "BackupRestoreConfig":
        with open(conf_path, "r") as stream:
            conf: dict = yaml.safe_load(stream)
        return cls(**conf)

    @model_validator(mode="after")
    def validate_storage(self) -> "BackupRestoreConfig":
        """Check that the storage gets correct configuration"""
        if self.storage_type == StorageType.S3:
            if not isinstance(self.storage, S3StorageConfig):
                raise ValueError(
                    "S3 storage must be configured with S3StorageConfig object"
                )
        elif self.storage_type == StorageType.AZURE:
            if not isinstance(self.storage, AzureStorageConfig):
                raise ValueError(
                    "Azure storage must be configured with AzureStorageConfig object"
                )
        elif self.storage_type == StorageType.LOCAL:
            if not isinstance(self.storage, LocalStorageConfig):
                raise ValueError(
                    "Local storage must be configured with LocalStorageConfig object"
                )
        return self
