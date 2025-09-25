# ColumnWarning

Warning related to single column.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**message** | **str** | Warning message related to the column. | 
**name** | **str** | Column name. | 

## Example

```python
from gooddata_api_client.models.column_warning import ColumnWarning

# TODO update the JSON string below
json = "{}"
# create an instance of ColumnWarning from a JSON string
column_warning_instance = ColumnWarning.from_json(json)
# print the JSON string representation of the object
print(ColumnWarning.to_json())

# convert the object into a dict
column_warning_dict = column_warning_instance.to_dict()
# create an instance of ColumnWarning from a dict
column_warning_from_dict = ColumnWarning.from_dict(column_warning_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


