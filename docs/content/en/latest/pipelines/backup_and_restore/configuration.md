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

If you plan on storing your backups on S3, you will also need to import the `StorageType` enum and `S3StorageConfig` class. You can find more details about configuration for the S3 storage below in the [S3 Storage](#s3-storage) section.

```python
from gooddata_pipelines import BackupRestoreConfig, S3StorageConfig, StorageType

```

The `BackupRestoreConfig` accepts following parameters:

| name                 | description                                                                                                  |
| -------------------- | ------------------------------------------------------------------------------------------------------------ |
| storage_type         | The type of storage to use - either `local` or `s3`. Defaults to `local`.                                    |
| storage              | Configuration for the storage type. Defaults to local storage configuration.                                 |
| api_page_size        | Page size for fetching workspace relationships. Defaults to 100 when unspecified.                            |
| batch_size           | Configures how many workspaces are backed up in a single batch. Defaults to 100 when unspecified.            |
| api_calls_per_second | Limits the maximum number of API calls to your GoodData instance. Defaults to 1. Only applied during Backup. |

## Storage

The configuration supports two types of storage - local and S3.

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
