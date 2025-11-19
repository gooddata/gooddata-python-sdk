---
title: "Configuration"
linkTitle: "Configuration"
weight: 1
---

The backup algorithm is configured via the `BackupRestoreConfig` class.

## Usage

Import `BackupRestoreConfig` from GoodData Pipelines.

```python
from gooddata_pipelines import BackupRestoreConfig

```

If you plan on storing your backups on S3 or Azure Blob Storage, you will also need to import the `StorageType` enum and the appropriate storage config class (`S3StorageConfig` or `AzureStorageConfig`). You can find more details about configuration for each storage type below in the [S3 Storage](#s3-storage) and [Azure Blob Storage](#azure-blob-storage) sections.

```python
from gooddata_pipelines import BackupRestoreConfig, S3StorageConfig, AzureStorageConfig, StorageType

```

The `BackupRestoreConfig` accepts following parameters:

| name                 | description                                                                                                  |
| -------------------- | ------------------------------------------------------------------------------------------------------------ |
| storage_type         | The type of storage to use - either `local`, `s3`, or `azure`. Defaults to `local`.                         |
| storage              | Configuration for the storage type. Defaults to local storage configuration.                                 |
| api_page_size        | Page size for fetching workspace relationships. Defaults to 100 when unspecified.                            |
| batch_size           | Configures how many workspaces are backed up in a single batch. Defaults to 100 when unspecified.            |
| api_calls_per_second | Limits the maximum number of API calls to your GoodData instance. Defaults to 1. Only applied during Backup. |

## Storage

The configuration supports three types of storage - local, S3, and Azure Blob Storage.

The backups are organized in a tree with following nodes:

- Organization ID
- Workspace ID
- Timestamped folder

The timestamped folder will contain a `gooddata_layouts.zip` file containing the stored definitions.

### Local Storage

Local storage requires a single parameter - `backup_path`. It defines where the backup tree will be saved in your file system. If not defined, the script will default to creating a `local_backups` folder in current working directory and store the backups there.

### S3 Storage

To configure upload of the backups to S3, use the S3StorageConfig object:

```python
from gooddata_pipelines.backup_and_restore.models.storage import S3StorageConfig

```

The configuration is responsible for establishing a valid connection to S3, connecting to a bucket and specyfing the folder where the backups will be stored or read. You can create the object in three ways, depending on the type of AWS credentials you want to use. The common arguments for all three ways are:

| name        | description                                                   |
| ----------- | ------------------------------------------------------------- |
| bucket      | The name of the bucket to use                                 |
| backup_path | Path to the folder serving as the root for the backup storage |

#### Config from IAM Role

Will use default IAM role or environment. You only need to specify the `bucket` and `backup_path` arguments.

```python
s3_storage_config = S3StorageConfig.from_iam_role(
        backup_path="backups_folder", bucket="backup_bucket"
    )

```

#### Config from AWS Profile

Will use an existing profile to authenticate with AWS.

```python
s3_storage_config = S3StorageConfig.from_aws_profile(
        backup_path="backups_folder", bucket="backup_bucket", profile="dev"
    )

```

#### Config from AWS Credentials

Will use long lived AWS Access Keys to authenticate with AWS.

```python
s3_storage_config = S3StorageConfig.from_aws_credentials(
        backup_path="backups_folder",
        bucket="backup_bucket",
        aws_access_key_id="AWS_ACCESS_KEY_ID",
        aws_secret_access_key="AWS_SECRET_ACCESS_KEY",
        aws_default_region="us-east-1",
    )
```

### Azure Blob Storage

To configure upload of the backups to Azure Blob Storage, use the AzureStorageConfig object:

```python
from gooddata_pipelines.backup_and_restore.models.storage import AzureStorageConfig

```

The configuration is responsible for establishing a valid connection to Azure Blob Storage, connecting to a storage account and container, and specifying the folder where the backups will be stored or read. You can create the object in three ways, depending on the type of Azure authentication you want to use. The common arguments for all three ways are:

| name         | description                                                   |
| ------------ | ------------------------------------------------------------- |
| account_name | The name of the Azure storage account                         |
| container    | The name of the blob container                                |
| backup_path  | Path to the folder serving as the root for the backup storage |

#### Config from Workload Identity

Will use Azure Workload Identity (for Kubernetes environments). You only need to specify the `account_name`, `container`, and `backup_path` arguments.

```python
azure_storage_config = AzureStorageConfig.from_workload_identity(
        backup_path="backups_folder", account_name="mystorageaccount", container="my-container"
    )

```

#### Config from Connection String

Will use an Azure Storage connection string to authenticate.

```python
azure_storage_config = AzureStorageConfig.from_connection_string(
        backup_path="backups_folder",
        account_name="mystorageaccount",
        container="my-container",
        connection_string="DefaultEndpointsProtocol=https;AccountName=...",
    )

```

#### Config from Service Principal

Will use Azure Service Principal credentials to authenticate.

```python
azure_storage_config = AzureStorageConfig.from_service_principal(
        backup_path="backups_folder",
        account_name="mystorageaccount",
        container="my-container",
        client_id="your-client-id",
        client_secret="your-client-secret",
        tenant_id="your-tenant-id",
    )
```

## Examples

Here is a couple of examples of different configuration cases.

### Simple Local Backups

If you want to store your backups locally and are okay with the default values, you can create the configuration object without having to specify any values:

```python
from gooddata_pipelines import BackupRestoreConfig

config = BackupRestoreConfig()

```

### Config with S3 and AWS Profile

If you plan to use S3, your config might look like this:

```python
from gooddata_pipelines import (
    BackupRestoreConfig,
    S3StorageConfig,
    StorageType,
)

s3_storage_config = S3StorageConfig.from_aws_profile(
        backup_path="backups_folder", bucket="backup_bucket", profile="dev"
    )

config = BackupRestoreConfig(storage_type=StorageType.S3, storage=s3_storage_config)

```

### Config with Azure Blob Storage and Workload Identity

If you plan to use Azure Blob Storage, your config might look like this:

```python
from gooddata_pipelines import (
    BackupRestoreConfig,
    AzureStorageConfig,
    StorageType,
)

azure_storage_config = AzureStorageConfig.from_workload_identity(
        backup_path="backups_folder", account_name="mystorageaccount", container="my-container"
    )

config = BackupRestoreConfig(storage_type=StorageType.AZURE, storage=azure_storage_config)

```
