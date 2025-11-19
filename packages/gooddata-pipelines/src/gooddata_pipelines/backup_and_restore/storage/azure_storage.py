# (C) 2025 GoodData Corporation

import os

from azure.core.credentials import TokenCredential
from azure.identity import DefaultAzureCredential, ClientSecretCredential
from azure.storage.blob import BlobServiceClient

from gooddata_pipelines.backup_and_restore.models.storage import (
    BackupRestoreConfig,
    AzureStorageConfig,
)
from gooddata_pipelines.backup_and_restore.storage.base_storage import (
    BackupStorage,
)


class AzureStorage(BackupStorage):
    def __init__(self, conf: BackupRestoreConfig):
        super().__init__(conf)

        if not isinstance(conf.storage, AzureStorageConfig):
            raise ValueError("Azure storage config is required")

        self._config = conf.storage
        self._blob_service_client = self._create_blob_service_client(
            self._config
        )
        self._container_client = self._blob_service_client.get_container_client(
            self._config.container
        )

        self._verify_connection()

    def _create_blob_service_client(
        self, config: AzureStorageConfig
    ) -> BlobServiceClient:
        account_url = f"https://{config.account_name}.blob.core.windows.net"

        if config.connection_string:
            try:
                return BlobServiceClient.from_connection_string(
                    config.connection_string
                )
            except Exception as e:
                self.logger.warning(
                    f"Failed to create Azure client with connection string: {e}"
                )

        if config.client_id and config.client_secret and config.tenant_id:
            try:
                credential = ClientSecretCredential(
                    tenant_id=config.tenant_id,
                    client_id=config.client_id,
                    client_secret=config.client_secret,
                )
                return BlobServiceClient(
                    account_url=account_url, credential=credential
                )
            except Exception as e:
                self.logger.warning(
                    f"Failed to create Azure client with service principal: {e}"
                )

        try:
            default_credential: TokenCredential = DefaultAzureCredential()
            return BlobServiceClient(
                account_url=account_url, credential=default_credential
            )
        except Exception as e:
            self.logger.error(
                f"Failed to create Azure client with default credentials: {e}"
            )
            raise RuntimeError(
                "Unable to create Azure Blob Storage client. Please check your authentication configuration. "
                "Supported methods: connection string, service principal, or Azure Workload/Managed Identity."
            )

    def _verify_connection(self) -> None:
        """
        Pings the Azure container to verify that the connection is working.
        """
        try:
            self._container_client.get_container_properties()
        except Exception as e:
            raise RuntimeError(
                f"Failed to connect to Azure container '{self._config.container}' "
                f"in storage account '{self._config.account_name}': {e}"
            )

    def export(self, folder: str, org_id: str) -> None:
        """Uploads the content of the folder to Azure Blob Storage as a backup."""
        storage_path = f"{self._config.account_name}/{self._config.container}/{self._backup_path}"
        self.logger.info(f"Uploading {org_id} to {storage_path}")
        folder = f"{folder}/{org_id}"

        for subdir, dirs, files in os.walk(folder):
            for file in files:
                full_path = os.path.join(subdir, file)
                with open(full_path, "rb") as data:
                    export_path = f"{self._backup_path}{org_id}/{full_path[len(folder) + 1 :]}"
                    blob_client = self._container_client.get_blob_client(
                        export_path
                    )
                    blob_client.upload_blob(data, overwrite=True)

    def get_ws_declaration(
        self, target_path: str, local_target_path: str
    ) -> None:
        """Retrieves workspace declaration from Azure Blob Storage."""
        target_blob_prefix = f"{self._backup_path}{target_path}"

        blobs_found = list(
            self._container_client.list_blobs(
                name_starts_with=target_blob_prefix
            )
        )

        if not blobs_found:
            message = f"No target backup found for {target_blob_prefix}."
            self.logger.error(message)
            raise Exception(message)

        if len(blobs_found) > 1:
            self.logger.warning(
                f"Multiple backups found at {target_blob_prefix}."
                " Continuing with the first one, ignoring the rest..."
            )

        blob = blobs_found[0]
        blob_client = self._container_client.get_blob_client(blob.name)

        with open(local_target_path, "wb") as download_file:
            download_file.write(blob_client.download_blob().readall())
