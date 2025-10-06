---
title: "Workspaces"
linkTitle: "Workspaces"
weight: 1
---

Workspace provisioning allows you to create, update or delete child workspaces.

{{% alert color="info" title="Multitenancy in GoodData"%}}
See [Multitenancy: One Platform, Many Customers](https://www.gooddata.com/resources/multitenancy-product-tour/) to learn more about how to leverage child workspaces in GoodData.
{{% /alert %}}

You can provision child workspaces using full or incremental load methods. Each of these methods requires a specific input type.

{{% alert color="info" %}} This section covers the usage with manual data validation. You can also take advantage of the generic provisioning function. You can read more about it on the [Provisioning](../#generic-function) page. {{% /alert %}}

## Usage

Start by importing and initializing the WorkspaceProvisioner.

```python

from gooddata_pipelines import WorkspaceProvisioner

host = "http://localhost:3000"
token = "some_user_token"

# Initialize the provisioner with GoodData credentials
provisioner = WorkspaceProvisioner.create(host=host, token=token)

```

Then validate your data using an input model corresponding to the provisioned resource and selected workflow type, i.e., `WorkspaceFullLoad` if you intend to run the provisioning in full load mode, or `WorkspaceIncrementalLoad` if you want to provision incrementally.

The models expect the following fields:

- **parent_id**: ID of the parent workspace.
- **workspace_id**: ID of the child workspace.
- **workspace_name**: Name of the child workspace.
- **workspace_data_filter_id**: ID of the workspace data filter to apply (must exist on parent workspace).
- **workspace_data_filter_values**: List of filter values that determine which data this workspace can access.
- _**is_active**:_ Deletion flag. Present only in the IncrementalLoad models.

{{% alert color="info" title="Note on IDs"%}}
Each ID can only contain allowed characters. See [Workspace Object Identification](https://www.gooddata.com/docs/cloud/create-workspaces/objects-identification/) to learn more about object identifiers.
{{% /alert %}}

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

# Run the provisioning method
provisioner.full_load(validated_data)
```

## Workspace Data Filters

If you want to apply Workspace Data Filters to a child workspace, the filter must be set up on the parent workspace before you run the provisioning.

{{% alert color="info" title="Workspace Data Filters"%}}
See [Set Up Data Filters in Workspaces](https://www.gooddata.com/docs/cloud/workspaces/workspace-data-filters/) to learn how workspace data filters work in GoodData.
{{% /alert %}}

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

# Optional: set up logging and subscribe to logs emitted by the provisioner
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

# Optional: set up logging and subscribe to logs emitted by the provisioner
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
