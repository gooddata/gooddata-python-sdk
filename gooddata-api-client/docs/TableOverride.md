# TableOverride

Table override settings.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**columns** | [**List[ColumnOverride]**](ColumnOverride.md) | An array of column overrides | 
**path** | **List[str]** | Path for the table. | 

## Example

```python
from gooddata_api_client.models.table_override import TableOverride

# TODO update the JSON string below
json = "{}"
# create an instance of TableOverride from a JSON string
table_override_instance = TableOverride.from_json(json)
# print the JSON string representation of the object
print(TableOverride.to_json())

# convert the object into a dict
table_override_dict = table_override_instance.to_dict()
# create an instance of TableOverride from a dict
table_override_from_dict = TableOverride.from_dict(table_override_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


