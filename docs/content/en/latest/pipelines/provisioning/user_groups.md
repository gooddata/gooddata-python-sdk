---
title: "User Groups"
linkTitle: "User Group"
weight: 3
---

User group provisioning allows you to create, update or delete user groups.

You can provision user groups using full or incremental load methods. Each of these methods requires a specific input type.

## Usage

Start by importing and initializing the UserGroupProvisioner.

```python

from gooddata_pipelines import UserGroupProvisioner

host="http://localhost:3000"
token="some_user_token"

# Initialize the provisioner with GoodData credentials
provisioner = UserGroupProvisioner.create(host=host, token=token)

```


Then validate your data using an input model corresponding with the provisioned resource and selected workflow type, i.e., `UserGroupFullLoad` if you intend to run the provisioning in full load mode, or `UserGroupIncrementalLoad` if you want to provision incrementally.

The models expect following fields:
```python
class UserGroupFullLoad
    user_group_id: str
    user_group_name: str
    parent_user_groups: list[str] # A list of parent user group IDs. Can be empty or None

class UserGroupIncrementalLoad
    user_group_id: str
    user_group_name: str
    parent_user_groups: list[str]
    is_active: bool # Set to True to keep the user, False to delete it

```

> **Note on IDs**: Each ID can only contain allowed characters. See [Workspace Object Identification](https://www.gooddata.com/docs/cloud/create-workspaces/objects-identification/) to learn more about object identifiers.

Use the appropriate model to validate your data:

```python
# Add the model to the imports
from gooddata_pipelines import UserGroupFullLoad, UserGroupProvisioner

host = "http://localhost:3000"
token = "some_user_token"

# Initialize the provisioner with GoodData credentials
provisioner = UserGroupProvisioner.create(host=host, token=token)

# Load your data
raw_data = [
    {
        "user_group_id": "user_group_1",
        "user_group_name": "User Group 1",
        "parent_user_groups": [],
    },
]

# Validate the data
validated_data = [
    UserGroupFullLoad(
        user_group_id=item["user_group_id"],
        user_group_name=item["user_group_name"],
        parent_user_groups=item["parent_user_groups"],
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

## Examples

Here are full examples of a full load and incremental load user group provisioning workflows:

### Full Load

```python
import logging

from gooddata_pipelines import UserGroupFullLoad, UserGroupProvisioner

host = "http://localhost:3000"
token = "some_user_token"

# Initialize the provisioner
provisioner = UserGroupProvisioner.create(host=host, token=token)

# Optional: set up logging and subscribe to logs emited by the provisioner
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

provisioner.logger.subscribe(logger)

# Prepare your data
raw_data = [
    {
        "user_group_id": "user_group_1",
        "user_group_name": "User Group 1",
        "parent_user_groups": [],
    },
]

# Validate the data
validated_data = [
    UserGroupFullLoad(
        user_group_id=item["user_group_id"],
        user_group_name=item["user_group_name"],
        parent_user_groups=item["parent_user_groups"],
    )
    for item in raw_data
]

# Run the provisioning with the validated data
provisioner.full_load(validated_data)

```


### Incremental Load

```python
import logging

from gooddata_pipelines import UserGroupIncrementalLoad, UserGroupProvisioner

host = "http://localhost:3000"
token = "some_user_token"

# Initialize the provisioner
provisioner = UserGroupProvisioner.create(host=host, token=token)

# Optional: set up logging and subscribe to logs emited by the provisioner
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

provisioner.logger.subscribe(logger)

# Prepare your data
raw_data = [
    {
        "user_group_id": "user_group_1",
        "user_group_name": "User Group 1",
        "parent_user_groups": [],
        "is_active": True,
    },
]

# Validate the data
validated_data = [
    UserGroupIncrementalLoad(
        user_group_id=item["user_group_id"],
        user_group_name=item["user_group_name"],
        parent_user_groups=item["parent_user_groups"],
        is_active=item["is_active"],
    )
    for item in raw_data
]

# Run the provisioning with the validated data
provisioner.incremental_load(validated_data)

```
