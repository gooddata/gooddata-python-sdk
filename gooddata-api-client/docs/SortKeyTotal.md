# SortKeyTotal

Sorting rule for sorting by total value. DataColumnLocators are only required if there is ambiguity. Locator for measureGroup is taken from the metric of the total.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**total** | [**SortKeyTotalTotal**](SortKeyTotalTotal.md) |  | 

## Example

```python
from gooddata_api_client.models.sort_key_total import SortKeyTotal

# TODO update the JSON string below
json = "{}"
# create an instance of SortKeyTotal from a JSON string
sort_key_total_instance = SortKeyTotal.from_json(json)
# print the JSON string representation of the object
print(SortKeyTotal.to_json())

# convert the object into a dict
sort_key_total_dict = sort_key_total_instance.to_dict()
# create an instance of SortKeyTotal from a dict
sort_key_total_from_dict = SortKeyTotal.from_dict(sort_key_total_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


