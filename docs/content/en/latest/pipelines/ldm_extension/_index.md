---
title: "LDM Extension"
linkTitle: "LDM Extension"
weight: 3
no_list: true
---

Child workspaces inherit [Logical Data Model](https://www.gooddata.com/docs/cloud/model-data/concepts/logical-data-model/) (LDM) from their parent. You can use GoodData Pipelines to extend child workspace's LDM with extra datasets specific to the tenant requirements.

{{% alert color="info" %}} See [Set Up Multiple Tenants](https://www.gooddata.com/docs/cloud/workspaces/) to learn more about leveraging multitenancy in GoodData.{{% /alert %}}

This documentation operates with terms like *custom datasets* and *custom fields*. Within this context, *custom* refers to extension of the LDM beyond inherited datasets.

## Usage

Start by initializing the LdmExtensionManager:

```python
from gooddata_pipelines import LdmExtensionManager

host = "http://localhost:3000"
token = "some_user_token"

ldm_extension_manager = LdmExtensionManager.create(host=host, token=token)

```

To extend the LDM, you need to define the custom datasets and the fields they should contain. The script also checks the validity of analytical objects before and after the update. Updates introducing new invalid relations are automatically rolled back. You can opt out of this behavior by setting the `check_relations` parameter to False.

### Custom Dataset Definitions

The custom dataset represents a new dataset appended to the child LDM. It is defined by the following parameters:

| name | type | description |
|------|------|-------------|
| workspace_id | string | ID of the child workspace. |
| dataset_id | string | ID of the custom dataset. |
| dataset_name | string | Name of the custom dataset. |
| dataset_datasource_id | string | ID of the data source. |
| dataset_source_table | string | Name of the table in the Physical Data Model. |
| dataset_source_sql | string \| None | SQL query defining the dataset. |
| parent_dataset_reference | string \| None | ID of the parent dataset to which the custom one will be connected. |
| parent_dataset_reference_attribute_id | string | ID of the attribute used for creating the relationship in the parent dataset. |
| dataset_reference_source_column | string | Name of the column used for creating the relationship in the custom dataset. |
| dataset_reference_source_column_data_type | [ColumnDataType](#columndatatype) | Column data type. |
| workspace_data_filter_id | string | ID of the workspace data filter to use. |
| workspace_data_filter_column_name | string | Name of the column in custom dataset used for filtering. |

#### Validity constraints

Either `dataset_source_table` or `dataset_source_sql` must be specified with a truthy value, but not both. An exception will be raised if both parameters are falsy or if both have truthy values.

### Custom Field Definitions

The custom fields define the individual fields in the custom datasets defined above. Each custom field needs to be specified with the following parameters:

| name | type | description |
|---------------|----------|-----------------|
| workspace_id | string | ID of the child workspace. |
| dataset_id | string | ID of the custom dataset. |
| custom_field_id | string | ID of the custom field. |
| custom_field_name | string | Name of the custom field. |
| custom_field_type | [CustomFieldType](#customfieldtype) | Indicates whether the field represents an attribute, a date, or a fact. |
| custom_field_source_column | string | Name of the column in the physical data model. |
| custom_field_source_column_data_type | [ColumnDataType](#columndatatype) | Data type of the field. |

#### Validity constraints

The custom field definitions must comply with the following criteria:

- Each attribute and fact must have a unique combination of `workspace_id` and `custom_field_id` values.
- Each date must have a unique combination of `dataset_id` and `custom_field_id` values.

### Enumerations

Some parameters of custom fields' and datasets' definitions are specified via CustomFieldType and ColumnDataType enums.

#### CustomFieldType

The following field types are supported:

| name | value |
|------|-------|
| ATTRIBUTE | "attribute" |
| FACT | "fact" |
| DATE | "date" |

#### ColumnDataType

The following data types are supported:

| name | value |
|------|-------|
| INT | "INT" |
| STRING | "STRING" |
| DATE | "DATE" |
| NUMERIC | "NUMERIC" |
| TIMESTAMP | "TIMESTAMP" |
| TIMESTAMP_TZ | "TIMESTAMP_TZ" |
| BOOLEAN | "BOOLEAN" |

### Relations Check

As changes to the LDM may impact existing analytical objects, the script will perform checks to prevent potentially undesirable changes.

{{% alert color="warning" %}} Changes to the LDM can invalidate existing objects. For example, removing a previously added custom field will break any analytical objects using that field. {{% /alert %}}

To prevent this, the script will:

1. Store current workspace layout (analytical objects and LDM).
1. Check whether relations of metrics, visualizations and dashboards are valid. A set of current objects with invalid relations is created.
1. Push the updated LDM to GoodData Cloud.
1. Check object relations again. New set of objects with invalid relations is created.
1. The sets are compared:
   - If the new set is a subset of the old one, the update is considered successful.
   - Otherwise, the update is rolled back. The initially stored workspace layout will be pushed to GoodData Cloud again, reverting changes to the workspace.

You can opt out of this check and rollback behavior by setting `check_relations` parameter to `False` when using the LdmExtensionManager.

```python
# By setting the `check_relations` to False, you will bypass the default checks
# and rollback mechanism. Note that this may invalidate existing objects.
ldm_extension_manager.process(
    custom_datasets=custom_dataset_definitions,
    custom_fields=custom_field_definitions,
    check_relations=False,
)

```

## Example

Here is a complete example of extending a child workspace's LDM:

```python
from gooddata_pipelines import (
    ColumnDataType,
    CustomDatasetDefinition,
    CustomFieldDefinition,
    CustomFieldType,
    LdmExtensionManager,
)

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

host = "http://localhost:3000"
token = "some_user_token"

# Initialize the manager
ldm_extension_manager = LdmExtensionManager.create(host=host, token=token)

# Optionally, you can subscribe to the logger object to receive log messages
ldm_extension_manager.logger.subscribe(logger)

# Prepare the definitions
custom_dataset_definitions = [
    CustomDatasetDefinition(
        workspace_id="child_workspace_id",
        dataset_id="products_custom_dataset_id",
        dataset_name="Custom Products Dataset",
        dataset_datasource_id="gdc_datasource_id",
        dataset_source_table="products_custom",
        dataset_source_sql=None,
        parent_dataset_reference="products",
        parent_dataset_reference_attribute_id="products.product_id",
        dataset_reference_source_column="product_id",
        dataset_reference_source_column_data_type=ColumnDataType.INT,
        workspace_data_filter_id="wdf_id",
        workspace_data_filter_column_name="wdf_column",
    )
]

custom_field_definitions = [
    CustomFieldDefinition(
        workspace_id="child_workspace_id",
        dataset_id="products_custom_dataset_id",
        custom_field_id="is_sold_out",
        custom_field_name="Sold Out",
        custom_field_type=CustomFieldType.ATTRIBUTE,
        custom_field_source_column="is_sold_out",
        custom_field_source_column_data_type=ColumnDataType.BOOLEAN,
    ),
    CustomFieldDefinition(
        workspace_id="child_workspace_id",
        dataset_id="products_custom_dataset_id",
        custom_field_id="category_detail",
        custom_field_name="Category (Detail)",
        custom_field_type=CustomFieldType.ATTRIBUTE,
        custom_field_source_column="category_detail",
        custom_field_source_column_data_type=ColumnDataType.STRING,
    ),
]

# Call the process method to extend the LDM
ldm_extension_manager.process(
    custom_datasets=custom_dataset_definitions,
    custom_fields=custom_field_definitions,
)

```
