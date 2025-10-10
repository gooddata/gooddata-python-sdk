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
        self._client = self._session.client("s3")
        self._resource = self._session.resource("s3")
        self._bucket = self._resource.Bucket(self._config.bucket)  # type: ignore [missing library stubs]

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
                    "Failed to create boto3 session with supplied credentials."
                )

        if config.profile:
            try:
                return boto3.Session(profile_name=config.profile)
            except Exception:
                self.logger.warning(
                    f"AWS profile [{config.profile}] not found."
                )

        try:
            return boto3.Session()
        except Exception:
            self.logger.error(
                "Failed to create boto3 session with default IAM role or environment credentials."
            )
            raise RuntimeError(
                "Unable to create AWS session. Please check your AWS credentials, profile, or IAM role configuration."
            )

    def _verify_connection(self) -> None:
        """
        Pings the S3 bucket to verify that the connection is working.
        """
        try:
            self._client.head_bucket(Bucket=self._config.bucket)
        except Exception as e:
            raise RuntimeError(
                f"Failed to connect to S3 bucket {self._config.bucket}: {e}"
            )

    def export(self, folder: str, org_id: str) -> None:
        """Uploads the content of the folder to S3 as a backup."""
        storage_path = f"{self._config.bucket}/{self._backup_path}"
        self.logger.info(f"Uploading {org_id} to {storage_path}")
        folder = f"{folder}/{org_id}"
        for subdir, dirs, files in os.walk(folder):
            full_path = os.path.join(subdir)
            export_path = (
                f"{self._backup_path}{org_id}/{full_path[len(folder) + 1 :]}/"
            )
            self._client.put_object(Bucket=self._config.bucket, Key=export_path)

            for file in files:
                full_path = os.path.join(subdir, file)
                with open(full_path, "rb") as data:
                    export_path = f"{self._backup_path}{org_id}/{full_path[len(folder) + 1 :]}"
                    self._client.put_object(
                        Bucket=self._config.bucket, Key=export_path, Body=data
                    )

    def get_ws_declaration(
        self, target_path: str, local_target_path: str
    ) -> None:
        """Retrieves workspace declaration from S3 bucket."""
        target_s3_prefix = f"{self._backup_path}{target_path}"

        objs_found = list(self._bucket.objects.filter(Prefix=target_s3_prefix))

        # Remove the included directory (which equals prefix) on hit
        objs_found = objs_found[1:] if len(objs_found) > 0 else objs_found

        if not objs_found:
            message = f"No target backup found for {target_s3_prefix}."
            self.logger.error(message)
            raise Exception(message)

        if len(objs_found) > 1:
            self.logger.warning(
                f"Multiple backups found at {target_s3_prefix}."
                " Continuing with the first one, ignoring the rest..."
            )

        s3_obj = objs_found[0]
        self._bucket.download_file(s3_obj.key, local_target_path)
