# TableWarning

Warnings related to single table.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**columns** | [**List[ColumnWarning]**](ColumnWarning.md) |  | 
**message** | **str** | Warning message related to the table. | [optional] 
**name** | **str** | Table name. | 

## Example

```python
from gooddata_api_client.models.table_warning import TableWarning

# TODO update the JSON string below
json = "{}"
# create an instance of TableWarning from a JSON string
table_warning_instance = TableWarning.from_json(json)
# print the JSON string representation of the object
print(TableWarning.to_json())

# convert the object into a dict
table_warning_dict = table_warning_instance.to_dict()
# create an instance of TableWarning from a dict
table_warning_from_dict = TableWarning.from_dict(table_warning_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


