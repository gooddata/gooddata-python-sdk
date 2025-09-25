# RelativeDateFilterRelativeDateFilter


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**apply_on_result** | **bool** |  | [optional] 
**bounded_filter** | [**BoundedFilter**](BoundedFilter.md) |  | [optional] 
**dataset** | [**AfmObjectIdentifierDataset**](AfmObjectIdentifierDataset.md) |  | 
**var_from** | **int** | Start of the filtering interval. Specified by number of periods (with respect to given granularity). Typically negative (historical time interval like -2 for &#39;2 days/weeks, ... ago&#39;). | 
**granularity** | **str** | Date granularity specifying particular date attribute in given dimension. | 
**local_identifier** | **str** |  | [optional] 
**to** | **int** | End of the filtering interval. Specified by number of periods (with respect to given granularity). Value &#39;O&#39; is representing current time-interval (current day, week, ...). | 

## Example

```python
from gooddata_api_client.models.relative_date_filter_relative_date_filter import RelativeDateFilterRelativeDateFilter

# TODO update the JSON string below
json = "{}"
# create an instance of RelativeDateFilterRelativeDateFilter from a JSON string
relative_date_filter_relative_date_filter_instance = RelativeDateFilterRelativeDateFilter.from_json(json)
# print the JSON string representation of the object
print(RelativeDateFilterRelativeDateFilter.to_json())

# convert the object into a dict
relative_date_filter_relative_date_filter_dict = relative_date_filter_relative_date_filter_instance.to_dict()
# create an instance of RelativeDateFilterRelativeDateFilter from a dict
relative_date_filter_relative_date_filter_from_dict = RelativeDateFilterRelativeDateFilter.from_dict(relative_date_filter_relative_date_filter_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


