---
title: "Users"
linkTitle: "Users"
weight: 2
---


User provisioning allows you to create, update or delete user profiles.

You can provision users using full or incremental load methods. Each of these methods requires a specific input type.

## Usage

Start by importing and initializing the UserProvisioner.

```python

from gooddata_pipelines import UserProvisioner

host="http://localhost:3000"
token="some_user_token"

# Initialize the provisioner with GoodData credentials
provisioner = UserProvisioner.create(host=host, token=token)

```


Then validate your data using an input model corresponding with the provisioned resource and selected workflow type, i.e., `UserFullLoad` if you intend to run the provisioning in full load mode, or `UserIncrementalLoad` if you want to provision incrementally.

The models expect following fields:
```python
class UserFullLoad
    user_id: str
    firstname: str | None
    lastname: str | None
    email: str | None
    auth_id: str | None
    user_groups: list[str]

class UserIncrementalLoad
    user_id: str
    firstname: str | None
    lastname: str | None
    email: str | None
    auth_id: str | None
    user_groups: list[str]
    is_active: bool # Set to True to keep the user, False to delete it

```

> **Note on IDs**: Each ID can only contain allowed characters. See [Workspace Object Identification](https://www.gooddata.com/docs/cloud/create-workspaces/objects-identification/) to learn more about object identifiers.

Use the appropriate model to validate your data:

```python
# Add the model to the imports
from gooddata_pipelines import UserIncrementalLoad, UserProvisioner

host = "http://localhost:3000"
token = "some_user_token"

# Initialize the provisioner with GoodData credentials
provisioner = UserProvisioner.create(host=host, token=token)

# Load your data
raw_data = [
    {
        "user_id": "user_id_1",
        "firstname": "Example",
        "lastname": "User",
        "email": "example.user@gooddata.com",
        "auth_id": "",
        "user_groups": ["user_group_1", "user_group_2"],
        "is_active": True,
    },
]

# Validate the data
validated_data = [
    UserIncrementalLoad(
        user_id=item["user_id"],
        firstname=item["firstname"],
        lastname=item["lastname"],
        email=item["email"],
        auth_id=item["auth_id"],
        user_groups=item["user_groups"],
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

from gooddata_pipelines import UserFullLoad, UserProvisioner

host = "http://localhost:3000"
token = "some_user_token"

# Initialize the provisioner
provisioner = UserProvisioner.create(host=host, token=token)

# Optional: set up logging and subscribe to logs emited by the provisioner
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

provisioner.logger.subscribe(logger)

# Prepare your data
raw_data = [
    {
        "user_id": "user_id_1",
        "firstname": "Example",
        "lastname": "User",
        "email": "example.user@gooddata.com",
        "auth_id": "",
        "user_groups": ["user_group_1", "user_group_2"],
    },
]

# Validate the data
validated_data = [
    UserFullLoad(
        user_id=item["user_id"],
        firstname=item["firstname"],
        lastname=item["lastname"],
        email=item["email"],
        auth_id=item["auth_id"],
        user_groups=item["user_groups"],
    )
    for item in raw_data
]

# Run the provisioning with the validated data
provisioner.full_load(validated_data)

```


### Incremental Load

```python
import logging

from gooddata_pipelines import UserIncrementalLoad, UserProvisioner

host = "http://localhost:3000"
token = "some_user_token"

# Initialize the provisioner
provisioner = UserProvisioner.create(host=host, token=token)

# Optional: set up logging and subscribe to logs emited by the provisioner
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

provisioner.logger.subscribe(logger)

# Prepare your data
raw_data = [
    {
        "user_id": "user_id_1",
        "firstname": "Example",
        "lastname": "User",
        "email": "example.user@gooddata.com",
        "auth_id": "",
        "user_groups": ["user_group_1", "user_group_2"],
        "is_active": True,
    },
]

# Validate the data
validated_data = [
    UserIncrementalLoad(
        user_id=item["user_id"],
        firstname=item["firstname"],
        lastname=item["lastname"],
        email=item["email"],
        auth_id=item["auth_id"],
        user_groups=item["user_groups"],
        is_active=item["is_active"],
    )
    for item in raw_data
]

# Run the provisioning with the validated data
provisioner.incremental_load(validated_data)

```
