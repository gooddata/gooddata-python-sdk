# SortKeyTotalTotal


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**data_column_locators** | [**DataColumnLocators**](DataColumnLocators.md) |  | [optional] 
**direction** | **str** | Sorting elements - ascending/descending order. | [optional] 
**total_identifier** | **str** | Local identifier of the total to sort by. | 

## Example

```python
from gooddata_api_client.models.sort_key_total_total import SortKeyTotalTotal

# TODO update the JSON string below
json = "{}"
# create an instance of SortKeyTotalTotal from a JSON string
sort_key_total_total_instance = SortKeyTotalTotal.from_json(json)
# print the JSON string representation of the object
print(SortKeyTotalTotal.to_json())

# convert the object into a dict
sort_key_total_total_dict = sort_key_total_total_instance.to_dict()
# create an instance of SortKeyTotalTotal from a dict
sort_key_total_total_from_dict = SortKeyTotalTotal.from_dict(sort_key_total_total_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


