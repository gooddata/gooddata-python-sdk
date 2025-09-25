# SortKeyAttribute

Sorting rule for sorting by attribute value in current dimension.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**attribute** | [**SortKeyAttributeAttribute**](SortKeyAttributeAttribute.md) |  | 

## Example

```python
from gooddata_api_client.models.sort_key_attribute import SortKeyAttribute

# TODO update the JSON string below
json = "{}"
# create an instance of SortKeyAttribute from a JSON string
sort_key_attribute_instance = SortKeyAttribute.from_json(json)
# print the JSON string representation of the object
print(SortKeyAttribute.to_json())

# convert the object into a dict
sort_key_attribute_dict = sort_key_attribute_instance.to_dict()
# create an instance of SortKeyAttribute from a dict
sort_key_attribute_from_dict = SortKeyAttribute.from_dict(sort_key_attribute_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


