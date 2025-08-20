# (C) 2025 GoodData Corporation

import os

import boto3

from gooddata_pipelines.backup_and_restore.models.storage import (
    BackupRestoreConfig,
    S3StorageConfig,
)
from gooddata_pipelines.backup_and_restore.storage.base_storage import (
    BackupStorage,
)


class S3Storage(BackupStorage):
    def __init__(self, conf: BackupRestoreConfig):
        super().__init__(conf)

        if not isinstance(conf.storage, S3StorageConfig):
            raise ValueError("S3 storage config is required")

        self._config = conf.storage
        self._session = self._create_boto_session(self._config)
        self._resource = self._session.resource("s3")
        self._bucket = self._resource.Bucket(self._config.bucket)  # type: ignore [missing library stubs]
        suffix = "/" if not self._config.backup_path.endswith("/") else ""
        self._backup_path = self._config.backup_path + suffix

        self._verify_connection()

    def _create_boto_session(self, config: S3StorageConfig) -> boto3.Session:
        if config.aws_access_key_id and config.aws_secret_access_key:
            if not config.aws_default_region:
                self.logger.warning(
                    "No AWS region specified. Defaulting to us-east-1."
                )
            try:
                return boto3.Session(
                    aws_access_key_id=config.aws_access_key_id,
                    aws_secret_access_key=config.aws_secret_access_key,
                    region_name=config.aws_default_region,
                )
            except Exception:
                self.logger.warning(
                    "Failed to create boto3 session with supplied credentials. Falling back to profile..."
                )

        try:
            return boto3.Session(profile_name=config.profile)
        except Exception:
            self.logger.warning(
                'AWS profile "[default]" not found. Trying other fallback methods...'
            )

        return boto3.Session()

    def _verify_connection(self) -> None:
        """
        Pings the S3 bucket to verify that the connection is working.
        """
        try:
            # TODO: install boto3 s3 stubs
            self._resource.meta.client.head_bucket(Bucket=self._config.bucket)
        except Exception as e:
            raise RuntimeError(
                f"Failed to connect to S3 bucket {self._config.bucket}: {e}"
            )

    def export(self, folder: str, org_id: str) -> None:
        """Uploads the content of the folder to S3 as backup."""
        storage_path = f"{self._config.bucket}/{self._backup_path}"
        self.logger.info(f"Uploading {org_id} to {storage_path}")
        folder = f"{folder}/{org_id}"
        for subdir, dirs, files in os.walk(folder):
            full_path = os.path.join(subdir)
            export_path = (
                f"{self._backup_path}{org_id}/{full_path[len(folder) + 1 :]}/"
            )
            self._bucket.put_object(Key=export_path)

            for file in files:
                full_path = os.path.join(subdir, file)
                with open(full_path, "rb") as data:
                    export_path = f"{self._backup_path}{org_id}/{full_path[len(folder) + 1 :]}"
                    self._bucket.put_object(Key=export_path, Body=data)
