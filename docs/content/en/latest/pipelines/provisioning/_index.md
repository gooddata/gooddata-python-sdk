---
title: "Provisioning"
linkTitle: "Provisioning"
weight: 1
no_list: true
---

Programmatically manage and provision resources in your GoodData environment.

## Supported Resources

Resources you can provision using GoodData Pipelines:

- [Workspaces](workspaces/)
- [Users](users/)
- [User Groups](user_groups/)
- [Workspace Permissions](workspace-permissions/)
- [User Data Filters](user_data_filters/)

## Workflow Types

There are two types of provisioning supported by GoodData Pipelines:

- [Full load](#full-load)
- [Incremental load](#incremental-load)

The provisioning types employ different algorithms and expect different structures of input data. For details about the expected inputs, check out the documentation page for each individual resource.

### Full Load

Full load provisioning aims to fully synchronize the state of your GoodData instance with the provided input. This workflow will create new resources and update existing ones based on the input. Any resources existing on GoodData Cloud not included in the input will be deleted.

{{% alert color="warning" title="Full loads are destructive"%}}
Full load provisioning will delete any existing resources not included in your input data. Test in a non-production environment.
{{% /alert %}}

### Incremental Load

During incremental provisioning, the algorithm will only interact with resources specified in the input. During the incremental load, the input data expects an extra parameter: `is_active`. Resources with `True` value will be updated. On the other hand, by setting it to `False`, you can mark resources for deletion. Any other resources already existing in GoodData will not be altered.

### Workflow Comparison

| **Aspect**   | **Full Load**                 | **Incremental Load**                             |
| ------------ | ----------------------------- | ------------------------------------------------ |
| **Scope**    | Synchronizes entire state     | Only specified resources                         |
| **Deletion** | Deletes unspecified resources | Only deletes resources marked `is_active: False` |
| **Use Case** | Complete environment setup    | Targeted updates                                 |

## Usage

You can use either resource-specific Provisioner objects, or a generic function to handle the provisioning logic.

The generic function validates the data, creates a provisioner instance, and runs the provisioning under the hood, reducing the boilerplate code. On the other hand, the resource-specific approach is more transparent with expected data structures.

### Provisioner Objects

Regardless of workflow type or resource being provisioned, the typical usage follows these steps:

1. Initialize the provisioner

1. Validate your data using an input model

1. Run the selected provisioning method (`.full_load()` or `.incremental_load()`) with your validated data

Check the [resource pages](#supported-resources) for detailed instructions and examples of workflow implementations.

### Generic Function

You can also use a generic provisioning function:

```python
from gooddata_pipelines import WorkflowType, provision

```

The function requires the following arguments:

| name          | description                                            |
| ------------- | ------------------------------------------------------ |
| data          | Raw data as a list of dictionaries                     |
| workflow_type | Enum indicating provisioned resource and workflow type |
| host          | URL of your GoodData instance                          |
| token         | GoodData Personal Access Token                         |
| logger        | Logger object to subscribe to the logs _[optional]_    |

The function will validate the raw data against the model corresponding to the selected `workflow_type` value. Note that the function only supports resources listed in the `WorkflowType` enum.

To see the expected data structure, check out the pages dedicated to individual resources. The raw dictionaries should have the same structure as the validation models outlined there.

To run the provisioning, simply call the function with its required arguments.

```python
provision(raw_data, WorkflowType.WORKSPACE_INCREMENTAL_LOAD, host, token)

```

## Logs

By default, the provisioners operate silently. To monitor progress and troubleshoot issues, you can subscribe to the emitted logs using the `.subscribe()` method on the `logger` property of the provisioner instance.

```python
# Import and set up your logger
import logging

# Import the provisioner
from gooddata_pipelines import WorkspaceProvisioner

host = "http://localhost:3000"
token = "some_user_token"

# In this example, we will use Python standard logging library.
# However, you can use any logger conforming to the LoggerLike protocol
# defined in gooddata_pipelines.logger.logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Initialize the provisioner
provisioner = WorkspaceProvisioner.create(host=host, token=token)

# Subscribe to the logging service
provisioner.logger.subscribe(logger)

# Continue with the provisioning
...
```

## Example

Here is an example of workspace provisioning using the generic function.

```python
import logging

# Import the WorkflowType enum and the generic function from GoodData Pipelines
from gooddata_pipelines import WorkflowType, provision

# Optional: set up a logger to pass to the function. The logger will be subscribed
# to the logs emitted by the provisioning scripts.
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


host = "http://localhost:3000"
token = "some_user_token"

# Prepare your raw data
raw_data: list[dict] = [
    {
        "parent_id": "parent_workspace_id",
        "workspace_id": "workspace_id_1",
        "workspace_name": "Workspace 1",
        "workspace_data_filter_id": "wdf__id",
        "workspace_data_filter_values": ["wdf_value_1"],
        "is_active": True,
    },
    {
        "parent_id": "parent_workspace_id",
        "workspace_id": "workspace_id_2",
        "workspace_name": "Workspace 2",
        "workspace_data_filter_id": "wdf__id",
        "workspace_data_filter_values": ["wdf_value_2"],
        "is_active": True,
    },
    {
        "parent_id": "parent_workspace_id",
        "workspace_id": "child_workspace_id_1",
        "workspace_name": "Workspace 3",
        "workspace_data_filter_id": "wdf__id",
        "workspace_data_filter_values": ["wdf_value_3"],
        "is_active": True,
    },
]

# Run the provisioning function
provision(
    data=raw_data,
    workflow_type=WorkflowType.WORKSPACE_INCREMENTAL_LOAD,
    host=host,
    token=token,
    logger=logger,
)
```
