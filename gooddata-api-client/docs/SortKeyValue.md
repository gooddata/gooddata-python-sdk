# SortKeyValue

Sorting rule for sorting by measure value. DataColumnLocators for each dimension opposite to the sorted one must be specified.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**value** | [**SortKeyValueValue**](SortKeyValueValue.md) |  | 

## Example

```python
from gooddata_api_client.models.sort_key_value import SortKeyValue

# TODO update the JSON string below
json = "{}"
# create an instance of SortKeyValue from a JSON string
sort_key_value_instance = SortKeyValue.from_json(json)
# print the JSON string representation of the object
print(SortKeyValue.to_json())

# convert the object into a dict
sort_key_value_dict = sort_key_value_instance.to_dict()
# create an instance of SortKeyValue from a dict
sort_key_value_from_dict = SortKeyValue.from_dict(sort_key_value_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


