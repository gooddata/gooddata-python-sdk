# BoundedFilter

Bounding filter for this relative date filter. This can be used to limit the range of the relative date filter to a specific date range.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**var_from** | **int** | Start of the filtering interval. Specified by number of periods (with respect to given granularity). Typically negative (historical time interval like -2 for &#39;2 days/weeks, ... ago&#39;). If null, then start of the range is unbounded. | [optional] 
**granularity** | **str** | Date granularity specifying particular date attribute in given dimension. | 
**to** | **int** | End of the filtering interval. Specified by number of periods (with respect to given granularity). Value &#39;O&#39; is representing current time-interval (current day, week, ...). If null, then end of the range is unbounded. | [optional] 

## Example

```python
from gooddata_api_client.models.bounded_filter import BoundedFilter

# TODO update the JSON string below
json = "{}"
# create an instance of BoundedFilter from a JSON string
bounded_filter_instance = BoundedFilter.from_json(json)
# print the JSON string representation of the object
print(BoundedFilter.to_json())

# convert the object into a dict
bounded_filter_dict = bounded_filter_instance.to_dict()
# create an instance of BoundedFilter from a dict
bounded_filter_from_dict = BoundedFilter.from_dict(bounded_filter_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


