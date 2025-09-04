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


## Workflow Types

There are two types of provisioning supported by GoodData Pipelines:

- [Full load](#full-load)
- [Incremental load](#incremental-load)

The provisioning types employ different algorithms and expect different structures of input data. For details about the expected inputs, check out the documentation page for each individual resource.

### Full Load

Full load provisioning aims to fully synchronize the state of your GoodData instance with the provided input. This workflow will create new resources and update existing ones based on the input. Any resources existing on GoodData Cloud not included in the input will be deleted.

{{% alert color="warning" title="Full loads are destrucitve"%}}
Full load provisioning will delete any existing resources not included in your input data. Test in non-production environment.
{{% /alert %}}

### Incremental Load

During incremental provisioning, the algorithm will only interact with resources specified in the input. During the incremental load, the input data expects an extra parameter: `is_active`. Resources with `True` value will be updated. On the other hand, by setting it to `False`, you can mark resources for deletion. Any other resources already existing in GoodData will not be altered.

### Workflow Comparison

| **Aspect** | **Full Load** | **Incremental Load** |
|------------|---------------|----------------------|
| **Scope** | Synchronizes entire state | Only specified resources |
| **Deletion** | Deletes unspecified resources | Only deletes resources marked `is_active: False` |
| **Use Case** | Complete environment setup | Targeted updates |

## Usage

Regardless of workflow type or resource being provisioned, the typical usage follows these steps:

1. Initialize the provisioner

1. Validate your data using an input model

1. Run the selected provisioning method (`.full_load()` or `.incremental_load()`) with your validated data


Check the [resource pages](#supported-resources) for detailed instructions and examples of workflow implementations.

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
