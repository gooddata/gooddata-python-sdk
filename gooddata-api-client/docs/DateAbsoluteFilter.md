# DateAbsoluteFilter


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**var_from** | **str** |  | 
**to** | **str** |  | 
**using** | **str** |  | 

## Example

```python
from gooddata_api_client.models.date_absolute_filter import DateAbsoluteFilter

# TODO update the JSON string below
json = "{}"
# create an instance of DateAbsoluteFilter from a JSON string
date_absolute_filter_instance = DateAbsoluteFilter.from_json(json)
# print the JSON string representation of the object
print(DateAbsoluteFilter.to_json())

# convert the object into a dict
date_absolute_filter_dict = date_absolute_filter_instance.to_dict()
# create an instance of DateAbsoluteFilter from a dict
date_absolute_filter_from_dict = DateAbsoluteFilter.from_dict(date_absolute_filter_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


