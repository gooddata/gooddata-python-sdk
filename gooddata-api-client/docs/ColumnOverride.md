# ColumnOverride

Table column override.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**label_target_column** | **str** | Specifies the attribute&#39;s column to which this label is associated. | [optional] 
**label_type** | **str** | Label type for the target attribute. | [optional] 
**ldm_type_override** | **str** | Logical Data Model type for the column. | [optional] 
**name** | **str** | Column name. | 

## Example

```python
from gooddata_api_client.models.column_override import ColumnOverride

# TODO update the JSON string below
json = "{}"
# create an instance of ColumnOverride from a JSON string
column_override_instance = ColumnOverride.from_json(json)
# print the JSON string representation of the object
print(ColumnOverride.to_json())

# convert the object into a dict
column_override_dict = column_override_instance.to_dict()
# create an instance of ColumnOverride from a dict
column_override_from_dict = ColumnOverride.from_dict(column_override_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


