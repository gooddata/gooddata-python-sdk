# DateRelativeFilter


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**var_from** | **int** |  | 
**granularity** | **str** |  | 
**to** | **int** |  | 
**using** | **str** |  | 

## Example

```python
from gooddata_api_client.models.date_relative_filter import DateRelativeFilter

# TODO update the JSON string below
json = "{}"
# create an instance of DateRelativeFilter from a JSON string
date_relative_filter_instance = DateRelativeFilter.from_json(json)
# print the JSON string representation of the object
print(DateRelativeFilter.to_json())

# convert the object into a dict
date_relative_filter_dict = date_relative_filter_instance.to_dict()
# create an instance of DateRelativeFilter from a dict
date_relative_filter_from_dict = DateRelativeFilter.from_dict(date_relative_filter_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


