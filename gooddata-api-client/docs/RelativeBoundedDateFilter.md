# RelativeBoundedDateFilter


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**var_from** | **int** |  | [optional] 
**granularity** | **str** |  | 
**to** | **int** |  | [optional] 

## Example

```python
from gooddata_api_client.models.relative_bounded_date_filter import RelativeBoundedDateFilter

# TODO update the JSON string below
json = "{}"
# create an instance of RelativeBoundedDateFilter from a JSON string
relative_bounded_date_filter_instance = RelativeBoundedDateFilter.from_json(json)
# print the JSON string representation of the object
print(RelativeBoundedDateFilter.to_json())

# convert the object into a dict
relative_bounded_date_filter_dict = relative_bounded_date_filter_instance.to_dict()
# create an instance of RelativeBoundedDateFilter from a dict
relative_bounded_date_filter_from_dict = RelativeBoundedDateFilter.from_dict(relative_bounded_date_filter_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


