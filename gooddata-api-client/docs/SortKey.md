# SortKey


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**attribute** | [**SortKeyAttributeAttribute**](SortKeyAttributeAttribute.md) |  | 
**value** | [**SortKeyValueValue**](SortKeyValueValue.md) |  | 
**total** | [**SortKeyTotalTotal**](SortKeyTotalTotal.md) |  | 

## Example

```python
from gooddata_api_client.models.sort_key import SortKey

# TODO update the JSON string below
json = "{}"
# create an instance of SortKey from a JSON string
sort_key_instance = SortKey.from_json(json)
# print the JSON string representation of the object
print(SortKey.to_json())

# convert the object into a dict
sort_key_dict = sort_key_instance.to_dict()
# create an instance of SortKey from a dict
sort_key_from_dict = SortKey.from_dict(sort_key_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


