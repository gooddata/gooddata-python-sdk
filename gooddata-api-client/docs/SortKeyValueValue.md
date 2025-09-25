# SortKeyValueValue


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**data_column_locators** | [**DataColumnLocators**](DataColumnLocators.md) |  | 
**direction** | **str** | Sorting elements - ascending/descending order. | [optional] 

## Example

```python
from gooddata_api_client.models.sort_key_value_value import SortKeyValueValue

# TODO update the JSON string below
json = "{}"
# create an instance of SortKeyValueValue from a JSON string
sort_key_value_value_instance = SortKeyValueValue.from_json(json)
# print the JSON string representation of the object
print(SortKeyValueValue.to_json())

# convert the object into a dict
sort_key_value_value_dict = sort_key_value_value_instance.to_dict()
# create an instance of SortKeyValueValue from a dict
sort_key_value_value_from_dict = SortKeyValueValue.from_dict(sort_key_value_value_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


