---
title: "Workspace Permissions"
linkTitle: "Workspace Permissions"
weight: 4
---

Workspace permission provisioning allows you to create, update or delete user permissions. See [Manage Workspace Permissions](https://www.gooddata.com/docs/cloud/manage-organization/manage-permissions/set-permissions-for-workspace/) to learn more about workspace permissions in GoodData Cloud.

You can provision workspace permissions using full or incremental load methods. Each of these methods requires a specific input type.

## Usage

Start by importing and initializing the PermissionProvisioner.

```python

from gooddata_pipelines import PermissionProvisioner

host="http://localhost:3000"
token="some_user_token"

# Initialize the provisioner with GoodData credentials
provisioner = PermissionProvisioner.create(host=host, token=token)

```


Then validate your data using an input model corresponding with the provisioned resource and selected workflow type, i.e., `PermissionFullLoad` if you intend to run the provisioning in full load mode, or `PermissionIncrementalLoad` if you want to provision incrementally.

The models expect following fields:
```python
class PermissionFullLoad
    permission: str # Permission you want to grant, e.g., "VIEW", "ANALYZE", "MANAGE"
    workspace_id: str # Workspace the permission will be applied to
    entity_id: str # ID of the entity (user or user group) which will receive the permission
    entity_type: EntityType # Enumeration, accepts "user" or "userGroup" values

class PermissionIncrementalLoad
    permission: str
    workspace_id: str
    entity_id: str
    entity_type: EntityType
    is_active: bool # Set to True to keep the user, False to delete it

```

> **Note on IDs**: Each ID can only contain allowed characters. See [Workspace Object Identification](https://www.gooddata.com/docs/cloud/create-workspaces/objects-identification/) to learn more about object identifiers.

Use the appropriate model to validate your data:

```python
# Add the model and the EntityType enumeration to the imports
from gooddata_pipelines import (
    EntityType,
    PermissionIncrementalLoad,
    PermissionProvisioner,
)

host = "http://localhost:3000"
token = "some_user_token"

# Initialize the provisioner with GoodData credentials
provisioner = PermissionProvisioner.create(host=host, token=token)

raw_data = [
    {
        "permission": "VIEW",
        "workspace_id": "workspace_id_1",
        "entity_id": "user_1",
        "entity_type": "user",
        "is_active": True,
    }
]

# Validate the data
validated_data = [
    PermissionIncrementalLoad(
        permission=item["permission"],
        workspace_id=item["workspace_id"],
        entity_id=item["entity_id"],
        entity_type=EntityType(item["entity_type"]),
        is_active=item["is_active"],
    )
    for item in raw_data
]

```

Now with the provisioner initialized and your data validated, you can run the provisioner:

```python
# Import, initialize, validate...
...

# Run the provisiong method
provisioner.incremental_load(validated_data)

```

## Examples

Here are full examples of a full load and incremental load user provisioning workflows:

### Full Load

```python
import logging

from gooddata_pipelines import EntityType, PermissionFullLoad, PermissionProvisioner

host = "http://localhost:3000"
token = "some_user_token"

# Initialize the provisioner
provisioner = PermissionProvisioner.create(host=host, token=token)

# Optional: set up logging and subscribe to logs emited by the provisioner
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

provisioner.logger.subscribe(logger)

# Prepare your data
raw_data = [
    {
        "permission": "VIEW",
        "workspace_id": "workspace_id_1",
        "entity_id": "user_1",
        "entity_type": "user",
    }
]

# Validate the data
validated_data = [
    PermissionFullLoad(
        permission=item["permission"],
        workspace_id=item["workspace_id"],
        entity_id=item["entity_id"],
        entity_type=EntityType(item["entity_type"]),
    )
    for item in raw_data
]

# Run the provisioning with the validated data
provisioner.full_load(validated_data)

```


### Incremental Load

```python
import logging

from gooddata_pipelines import (
    EntityType,
    PermissionIncrementalLoad,
    PermissionProvisioner,
)

host = "http://localhost:3000"
token = "some_user_token"

# Initialize the provisioner
provisioner = PermissionProvisioner.create(host=host, token=token)

# Optional: set up logging and subscribe to logs emited by the provisioner
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

provisioner.logger.subscribe(logger)

# Prepare your data
raw_data = [
    {
        "permission": "VIEW",
        "workspace_id": "workspace_id_1",
        "entity_id": "user_1",
        "entity_type": "user",
        "is_active": True,
    }
]

# Validate the data
validated_data = [
    PermissionIncrementalLoad(
        permission=item["permission"],
        workspace_id=item["workspace_id"],
        entity_id=item["entity_id"],
        entity_type=EntityType(item["entity_type"]),
        is_active=item["is_active"],
    )
    for item in raw_data
]

# Run the provisioning with the validated data
provisioner.incremental_load(validated_data)

```
