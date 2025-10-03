---
title: "User Data Filters"
linkTitle: "User Data Filters"
weight: 4
---

User Data Filter (UDF) provisioning lets you manage UDFs in your GoodData environment.

UDFs are currently managed only in full load mode, meaning your input overwrites existing UDFs for each workspace present in the input.

This tool currently supports only the `{column} IN (udf_value)` MAQL pattern. UDFs using more complex MAQL expressions must be set up manually.

{{% alert color="info" %}} Visit [Set Up Data Filters for Users](https://www.gooddata.com/docs/cloud/workspaces/user-data-filters/) to learn more about User Data Filters setup and use cases in GoodData. {{% /alert %}}

## Usage

Start by importing and initializing the `UserDataFilterProvisioner`.

```python
from gooddata_pipelines import UserDataFilterProvisioner

host = "http://localhost:3000"
token = "some_user_token"

# Initialize the provisioner with GoodData credentials
provisioner = UserDataFilterProvisioner.create(host=host, token=token)

```

Then, set the LDM and MAQL column names used by the UDF:

```python
provisioner.set_ldm_column_name("ldm_column_name")
provisioner.set_maql_column_name("{attribute/dataset.field_name}")

```


Next, validate the input data using the `UserDataFilterFullLoad` model.

The model expects the following fields:

| name          | description                                                                                  |
|---------------|---------------------------------------------------------------------------------------------|
| workspace_id  | ID of the workspace where the UDF will be applied.                                          |
| udf_id        | ID of the UDF to be created. Should be equal to the ID of the user the UDF will be applied to. |
| udf_value     | Value for the UDF.                                                                          |

{{% alert color="info" title="Note on IDs"%}}
Each ID can only contain allowed characters. See [Workspace Object Identification](https://www.gooddata.com/docs/cloud/create-workspaces/objects-identification/) to learn more about object identifiers.
{{% /alert %}}

Add the model to your imports and create validated instances:

```python
# Add the model to the imports
from gooddata_pipelines import UserDataFilterFullLoad, UserDataFilterProvisioner

host = "http://localhost:3000"
token = "some_user_token"

# Initialize the provisioner with GoodData credentials
provisioner = UserDataFilterProvisioner.create(host=host, token=token)

# Validate your data
validated_data = [
        UserDataFilterFullLoad(
            workspace_id="workspace_id_1",
            udf_id="user_id_1",
            udf_value="udf_value_1",
        )
    ]

```

Now, with the provisioner initialized and your data validated, run the provisioner:

```python
# Import, initialize, validate...
...

# Run the provisioning method
provisioner.full_load(validated_data)

```

## Examples

Here is a complete example of a full load UDF provisioning workflow:

```python
import logging

from gooddata_pipelines import UserDataFilterFullLoad, UserDataFilterProvisioner

host = "http://localhost:3000"
token = "some_user_token"

# Initialize the provisioner
provisioner = UserDataFilterProvisioner.create(host=host, token=token)

# Set the column names to be used in the UDF
provisioner.set_ldm_column_name("ldm_column_name")
provisioner.set_maql_column_name("{attribute/dataset.field_name}")

# Optional: set up logging and subscribe to logs emitted by the provisioner
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

provisioner.logger.subscribe(logger)

# Prepare your data
raw_data = [
    {
        "workspace_id": "workspace_id_1",
        "udf_id": "user_id_1",
        "udf_value": "udf_value_1"
    },
    {
        "workspace_id": "workspace_id_1",
        "udf_id": "user_id_2",
        "udf_value": "udf_value_2"
    },
]

# Validate the data
validated_data = [
    UserDataFilterFullLoad(
        workspace_id=item["workspace_id"],
        udf_id=item["udf_id"],
        udf_value=item["udf_value"],
    )
    for item in raw_data
]

# Run the provisioning with the validated data
provisioner.full_load(validated_data)

```
