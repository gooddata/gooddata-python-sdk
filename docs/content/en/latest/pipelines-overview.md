---
title: "Pipelines Overview"
linkTitle: "Pipelines Overview"
weight: 14
---

GoodData Pipelines contains tools for automating GoodData lifecycle management. Built on top of [GoodData Python SDK](https://www.gooddata.com/docs/python-sdk/latest/), it enables you to programmatically provision and manage workspaces, users, user groups, and their permissions.

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

Here is an introductory example of how to manage GoodData resources using GoodData Pipelines:

### Provision Child Workspaces
```python
from gooddata_pipelines import WorkspaceFullLoad, WorkspaceProvisioner

# GoodData.CN host URI (e.g., "http://localhost:3000")
host = "http://localhost:3000"

# GoodData.CN user token
token = "some_user_token"

# Initialize the provisioner
provisioner = WorkspaceProvisioner.create(host=host, token=token)

# Gather the definitions of the workspaces you want to create
raw_data: list[dict] = [
    {
        "parent_id": "demo_parent_workspace",
        "workspace_id": "sales_team_workspace",
        "workspace_name": "Sales Team Workspace",
        "workspace_data_filter_id": "region_filter",
        "workspace_data_filter_values": ["north_america"],
    },
]

# Validate the data
validated_data = [WorkspaceFullLoad(**item) for item in raw_data]

# Run the provisioning
provisioner.full_load(validated_data)

```
