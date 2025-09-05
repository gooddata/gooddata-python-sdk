---
title: "Pipelines Overview"
linkTitle: "Pipelines Overview"
weight: 14
---

GoodData Pipelines contains tools for automation of GoodData life cycle. Built over GoodData Python SDK, it allows you to conveniently manage user profiles, workspace permissions and more.

For further information, refer to the PIPELINES section in the left navigation menu.

## Installation


Run the following command to install the ``gooddata-pipelines`` package on your system:

```bash
pip install gooddata-pipelines
```

### Requirements

- Python 3.10 or newer
- GoodData.CN or GoodData Cloud



## Examples
Here are a couple of introductory examples how to manage GoodData resources using GoodData Pipelines:

### Provision Child Workspaces
```python
from gooddata_pipelines import WorkspaceFullLoad, WorkspaceProvisioner

# GoodData.CN host in the form of uri eg. "http://localhost:3000"
host = "http://localhost:3000"

# GoodData.CN user token
token = "some_user_token"

# Initialize the provisioner
provisioner = WorkspaceProvisioner.create(host=host, token=token)

# Gather the definitions of the workspaces you want to create
raw_data: list[dict] = [
    {
        "parent_id": "parent_workspace_id",
        "workspace_id": "child_workspace_0",
        "workspace_name": "Child Workspace 0",
        "workspace_data_filter_id": "data_filter_id",
        "workspace_data_filter_values": ["value_0"],
    },
]

# Validate the data
validated_data = [WorkspaceFullLoad(**item) for item in raw_data]

# Run the provisioning
provisioner.full_load(validated_data)

```

### Workspace Backup
```python
from gooddata_pipelines import BackupManager, BackupRestoreConfig

# GoodData.CN host in the form of uri eg. "http://localhost:3000"
host = "http://localhost:3000"

# GoodData.CN user token
token = "some_user_token"

# Define a list with IDs of workspaces you want to back up
workspaces_to_back_up = ["workspace_id_1", "workspace_id_2"]

# Configure backup options
config = BackupRestoreConfig(storage_type="local")

# Initialize the backup manager
backup_manager = BackupManager.create(config, host, token)

# Run the backup
backup_manager.backup_workspaces(workspace_ids=workspaces_to_back_up)

```
