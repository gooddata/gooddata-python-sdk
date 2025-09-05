---
title: "Workspaces"
linkTitle: "Workspaces"
weight: 1
---

Workspace provisioning allows you to create, update or delete child workspaces.

You can provision child workspaces using full or incremental load methods. Each of these methods requires a specific input type.


## Usage

Start by importing and initializing the WorkspaceProvisioner.

```python

from gooddata_pipelines import WorkspaceProvisioner

host="http://localhost:3000"
token="some_user_token"

# Initialize the provisioner with GoodData credentials
provisioner = WorkspaceProvisioner.create(host=host, token=token)

```


Then validate your data using an input model corresponding with the provisioned resource and selected workflow type, i.e., `WorkspaceFullLoad` if you intend to run the provisioning in full load mode, or `WorkspaceIncrementalLoad` if you want to provision incrementally.

The models expect following fields:
```python
class WorkspaceFullLoad
    parent_id: str # ID of parent workspace
    workspace_id: str # ID of child workspace
    workspace_name: str # Name of child workspace
    workspace_data_filter_id: str | None = None # ID of applied workspace data filter
    workspace_data_filter_values: list[str] | None = None # Filter values to apply

class WorkspaceIncrementalLoad
    parent_id: str
    workspace_id: str
    workspace_name: str
    workspace_data_filter_id: str | None = None
    workspace_data_filter_values: list[str] | None = None
    is_active: bool # Set to True to keep the workspace, False to delete it

```

> **Note on IDs**: Each ID can only contain allowed characters. See [Workspace Object Identification](https://www.gooddata.com/docs/cloud/create-workspaces/objects-identification/) to learn more about object identifiers.

Use the appropriate model to validate your data:

```python
# Add the model to the imports
from gooddata_pipelines import WorkspaceFullLoad, WorkspaceProvisioner

host = "http://localhost:3000"
token = "some_user_token"

# Initialize the provisioner with GoodData credentials
provisioner = WorkspaceProvisioner.create(host=host, token=token)

# Load your data
raw_data = [
    {
        "parent_id": "parent_workspace_id",
        "workspace_id": "workspace_id_1",
        "workspace_name": "Workspace 1",
        "workspace_data_filter_id": "data_filter_id",
        "workspace_data_filter_values": ["workspace_data_filter_value_1"],
    },
]

# Validate the data
validated_data = [
    WorkspaceFullLoad(
        parent_id=item["parent_id"],
        workspace_id=item["workspace_id"],
        workspace_name=item["workspace_name"],
        workspace_data_filter_id=item["workspace_data_filter_id"],
        workspace_data_filter_values=item["workspace_data_filter_values"],
    )
    for item in raw_data
]


```

Now with the provisioner initialized and your data validated, you can run the provisioner:

```python
# Import, initialize, validate...
...

# Run the provisiong method
provisioner.full_load(validated_data)
```


## Workspace Data Filters

If you want to apply Workspace Data Filters on a child workspace, it needs to be set up on the parent workspace before you run the provisioning.

See [Set Up Data Filters in Workspaces](https://www.gooddata.com/docs/cloud/workspaces/workspace-data-filters/) to learn how workspace data filters work in GoodData.


## Examples

Here are full examples of a full load and incremental load workspace provisioning workflows:

### Full Load

```python
import logging

from gooddata_pipelines import WorkspaceFullLoad, WorkspaceProvisioner

host = "http://localhost:3000"
token = "some_user_token"

# Initialize the provisioner
provisioner = WorkspaceProvisioner.create(host=host, token=token)

# Optional: set up logging and subscribe to logs emited by the provisioner
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

provisioner.logger.subscribe(logger)

# Prepare your data
raw_data: list[dict] = [
    {
        "parent_id": "parent_workspace_id",
        "workspace_id": "workspace_id_1",
        "workspace_name": "Workspace 1",
        "workspace_data_filter_id": "data_filter_id",
        "workspace_data_filter_values": ["workspace_data_filter_value_1"],
    },
    {
        "parent_id": "parent_workspace_id",
        "workspace_id": "workspace_id_2",
        "workspace_name": "Workspace 2",
        "workspace_data_filter_id": "data_filter_id",
        "workspace_data_filter_values": ["workspace_data_filter_value_2"],
    },
    {
        "parent_id": "parent_workspace_id",
        "workspace_id": "child_workspace_id_1",
        "workspace_name": "Workspace 3",
        "workspace_data_filter_id": "data_filter_id",
        "workspace_data_filter_values": ["workspace_data_filter_value_3"],
    },
]

# Validate the data
validated_data = [
    WorkspaceFullLoad(
        parent_id=item["parent_id"],
        workspace_id=item["workspace_id"],
        workspace_name=item["workspace_name"],
        workspace_data_filter_id=item["workspace_data_filter_id"],
        workspace_data_filter_values=item["workspace_data_filter_values"],
    )
    for item in raw_data
]

# Run the provisioning with the validated data
provisioner.full_load(validated_data)

```

### Incremental Load

```python
import logging

from gooddata_pipelines import WorkspaceIncrementalLoad, WorkspaceProvisioner

host = "http://localhost:3000"
token = "some_user_token"

# Initialize the provisioner
provisioner = WorkspaceProvisioner.create(host=host, token=token)

# Optional: set up logging and subscribe to logs emited by the provisioner
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

provisioner.logger.subscribe(logger)

# Prepare your data
raw_data: list[dict] = [
    {
        "parent_id": "parent_workspace_id",
        "workspace_id": "workspace_id_1",
        "workspace_name": "Workspace 1",
        "workspace_data_filter_id": "data_filter_id",
        "workspace_data_filter_values": ["workspace_data_filter_value_1"],
        "is_active": True,
    },
    {
        "parent_id": "parent_workspace_id",
        "workspace_id": "workspace_id_2",
        "workspace_name": "Workspace 2",
        "workspace_data_filter_id": "data_filter_id",
        "workspace_data_filter_values": ["workspace_data_filter_value_2"],
        "is_active": True,
    },
    {
        "parent_id": "parent_workspace_id",
        "workspace_id": "child_workspace_id_1",
        "workspace_name": "Workspace 3",
        "workspace_data_filter_id": "data_filter_id",
        "workspace_data_filter_values": ["workspace_data_filter_value_3"],
        "is_active": False,  # This will mark the workspace for deletion
    },
]

# Validate the data
validated_data = [
    WorkspaceIncrementalLoad(
        parent_id=item["parent_id"],
        workspace_id=item["workspace_id"],
        workspace_name=item["workspace_name"],
        workspace_data_filter_id=item["workspace_data_filter_id"],
        workspace_data_filter_values=item["workspace_data_filter_values"],
        is_active=item["is_active"],
    )
    for item in raw_data
]

# Run the provisioning with the validated data
provisioner.incremental_load(validated_data)

```
