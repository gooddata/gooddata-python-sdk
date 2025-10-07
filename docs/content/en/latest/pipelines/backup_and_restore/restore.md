---
title: "Workspace Restore"
linkTitle: "Workspace Restore"
weight: 3
---

Workspace Restore lets you restore previously created backups of your workspaces.

## Usage

Start by importing the `RestoreManager` and the `BackupRestoreConfig` configuration object from GoodData Pipelines.

```python
from gooddata_pipelines import BackupRestoreConfig, RestoreManager

```

Initialize the restore manager with your configuration and GoodData credentials. If you store your backups locally, you can use the default configuration values.

```python
config = BackupRestoreConfig()

restore_manager = RestoreManager.create(
        config, "host", "token"
    )

```

You will need to define which backups should be restored. You can do this by creating a list of `WorkspaceToRestore` objects. The object carries two pieces of information - the ID of the workspace that will be restored, and the location of the backup file in the [backup tree](/latest/pipelines/backup_and_restore/configuration/#storage).

```python
from gooddata_pipelines import WorkspaceToRestore

workspaces_to_restore = [
    WorkspaceToRestore(
        id="workspace_id_1",
        path="local_backups/org_id/workspace_id_1/20251008-102252-1_52_0",
    ),
]

```

Now you can run the restore method of the manager.

```python
restore_manager.restore(workspaces_to_restore=workspaces_to_restore)

```

## Configuration

See [Configuration](/latest/pipelines/backup_and_restore/configuration/) for details on how to set up the configuration object.

## Example

Here is a full example of a workspace restore process:

```python
import logging
import os

from gooddata_pipelines import (
    BackupRestoreConfig,
    RestoreManager,
    S3StorageConfig,
    StorageType,
    WorkspaceToRestore,
)

# Create storage configuration
storage_config = S3StorageConfig.from_aws_profile(
    backup_path="backup_folder", bucket="backup_bucket", profile="dev"
)

# Create restore configuration
config = BackupRestoreConfig(storage_type=StorageType.S3, storage=storage_config)

# Initialize the restore manager with the configuration object and GoodData credentials
restore_manager = RestoreManager.create(
    config, os.environ["GD_HOST"], os.environ["GD_TOKEN"]
)

# Optionally, set up a logger and subscribe it to RestoreManager's logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
restore_manager.logger.subscribe(logger)

# Run the restore method with a list of WorkspaceToRestore objects
restore_manager.restore(
    workspaces_to_restore=[
        WorkspaceToRestore(
            id="workspace_id_1",
            path="org-id/workspace_id_1/20251007-144543-1_52_0",
        ),
        WorkspaceToRestore(
            id="workspace_id_2",
            path="org-id/workspace_id_2/20251007-144543-1_52_0",
        ),
    ]
)

```
