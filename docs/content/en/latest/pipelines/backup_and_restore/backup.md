---
title: "Workspace Backup"
linkTitle: "Workspace Backup"
weight: 2
---

Workspace Backup allows you to create backups of one or more workspaces. Backups can be stored locally, uploaded to an S3 bucket, or uploaded to Azure Blob Storage.

The backup stores following definitions:

- Logical Data Model
- Analytics Model
- User Data Filters
- Filter Views
- Automations

## Usage

Import and initialize the BackupManager and BackupRestoreConfig from GoodData Pipelines:

```python
from gooddata_pipelines import BackupManager, BackupRestoreConfig

host = "http://localhost:3000"
token = "some_user_token"

# Create your customized backup configuration or use default values
config = BackupRestoreConfig(
        storage_type="local"
    )

# Initialize the BackupManager with your configuration and GoodData Cloud credentials
backup_manager = BackupManager.create(config=config, host=host, token=token)

# Run a backup method. For example, the `backup_entire_organization` method backs up all workspaces in GoodData Cloud.
backup_manager.backup_entire_organization()

```

## Configuration

See [Configuration](/latest/pipelines/backup_and_restore/configuration/) for details on how to set up the configuration object.

## Backup Methods

You can use one of these methods to back up your workspaces:

### Back up specific workspaces

This methods allows you to back up specific workspaces. You can supply the list of their IDs either directly or by specifying a path to a CSV file.

#### Usage with direct input:

```python
workspace_ids = ["workspace_1", "workspace_2", "workspace_3"]

backup_manager.backup_workspaces(workspace_ids=workspace_ids)

```

#### Usage with a csv:

```python
path_to_csv = "path/to/local/file.csv"

backup_manager.backup_workspaces(path_to_csv=path_to_csv)

```

### Back up workspace hierarchies

This method accepts a list of parent workspace IDs and created a backup of each workspace within their hierarchy. That includes the parent workspace and both its direct and indirect children (i.e., the children of child workspaces etc.). The IDs can be provided either directly as a list or as a path to a CSV file containing the IDs.

#### Usage with direct input:

```python
parent_workspace_ids = ["parent_1", "parent_2", "parent_3"]

backup_manager.backup_hierarchies(workspace_ids=parent_workspace_ids)

```

#### Usage with a csv:

```python
path_to_csv = "path/to/local/file.csv"

backup_manager.backup_hierarchies(path_to_csv=path_to_csv)

```

### Back up entire organization

Create a backup of all workspaces within the GoodData organization. The method requires no arguments.

```python
backup_manager.backup_entire_organization()

```

### Input CSV Format

When using a CSV as input for backup, following format is expected:

| **workspace_id** |
| ---------------- |
| parent_1         |
| parent_2         |
| parent_3         |

## Example

Here is a full example of a workspace backup process:

```python
import logging
import os

from gooddata_pipelines import (
    BackupManager,
    BackupRestoreConfig,
    S3StorageConfig,
    StorageType,
)

# Create storage configuration
s3_storage_config = S3StorageConfig.from_aws_profile(
    backup_path="backup_folder", bucket="backup_bucket", profile="dev"
)

# Create backup configuration
config = BackupRestoreConfig(storage_type=StorageType.S3, storage=s3_storage_config)

# Initialize the BackupManager with your configuration and GoodData credentials
backup_manager = BackupManager.create(
    config, os.environ["GD_HOST"], os.environ["GD_TOKEN"]
)

# Optionally set up a logger and subscribe it to the logs from the BackupManager
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
backup_manager.logger.subscribe(logger)

# Run the backup
backup_manager.backup_workspaces(workspace_ids=["workspace_id_1", "workspace_id_2"])
```

### Example with Azure Blob Storage

Here is an example using Azure Blob Storage with Workload Identity:

```python
import logging
import os

from gooddata_pipelines import (
    BackupManager,
    BackupRestoreConfig,
    AzureStorageConfig,
    StorageType,
)

# Create storage configuration
azure_storage_config = AzureStorageConfig.from_workload_identity(
    backup_path="backup_folder", account_name="mystorageaccount", container="my-container"
)

# Create backup configuration
config = BackupRestoreConfig(storage_type=StorageType.AZURE, storage=azure_storage_config)

# Initialize the BackupManager with your configuration and GoodData credentials
backup_manager = BackupManager.create(
    config, os.environ["GD_HOST"], os.environ["GD_TOKEN"]
)

# Optionally set up a logger and subscribe it to the logs from the BackupManager
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
backup_manager.logger.subscribe(logger)

# Run the backup
backup_manager.backup_workspaces(workspace_ids=["workspace_id_1", "workspace_id_2"])

```
