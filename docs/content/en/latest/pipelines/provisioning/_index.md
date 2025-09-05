---
title: "Provisioning"
linkTitle: "Provisioning"
weight: 1
no_list: true
---

Manage resources in GoodData.

## Supported Resources

Resources you can provision using GoodData Pipelines:

- [Workspaces](./workspaces.md)
- [Users](users.md)
- [User Groups](user_groups.md)
- [Workspace Permissions](workspace-permissions.md)


## Workflow Types

There are two types of provisioning supported by GoodData Pipelines:

- [Full load](#full-load)
- [Incremental load](#incremental-load)

The provisioning types employ different algorithms and expect different structure of input data. For details about the expected inputs, check out the documentation page of individual provisioned resource.

### Full Load

Full load provisioning aims to fully synchronize the state of your GoodData instance with the provided input. This workflow will create new resources and update existing ones based on the input. Any resources existing on GoodData Cloud not inluded in the input will be deleted.

### Incremental Load

During incremental provisioning, the algorithm will only interact with resources specified in the input. During the incremental load, the input data expects an extra parameter: `is_active`. Resources with `True` value will be updated. On the other hand, by setting it to `False`, you can mark resources for deletion. Any other resources already existing in GoodData will not be altered.


## Usage

Regardless of workflow type or provisioned resource, the typical usage can be broken down into following steps:

1. Initialize the provisioner

1. Validate your data using an input model

1. Run the selected provisioning method (`.full_load()` or `.incremental_load()`) with your validated data


Check the [resource pages](#supported-resources) for examples of workflow implementations.

## Logs

By default, the provisioners will not print out any information to the console. However, you can subscribe to the emitted logs using the `.subscribe()` method on the `logger` property of the provisioner instance. The logging service emits unformatted messages based on severity.

```python
# Import and set up your logger
import logging

# Import the provisioner
from gooddata_pipelines import WorkspaceProvisioner

host="http://localhost:3000", token="some_user_token"

# In this example, we will use Python standard logging library.
# However, you can subscribe any logger conforming to the LoggerLike protocol
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
