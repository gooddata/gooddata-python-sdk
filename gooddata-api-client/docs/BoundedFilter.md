# BoundedFilter

Bounding filter for this relative date filter. This can be used to limit the range of the relative date filter to a specific date range.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**granularity** | **str** | Date granularity specifying particular date attribute in given dimension. | 
**dataset** | [**AfmObjectIdentifierDataset**](AfmObjectIdentifierDataset.md) |  | [optional] 
**_from** | **int, none_type** | Start of the filtering interval. Specified by number of periods (with respect to given granularity). Typically negative (historical time interval like -2 for &#39;2 days/weeks, ... ago&#39;). If null, then start of the range is unbounded. | [optional] 
**to** | **int, none_type** | End of the filtering interval. Specified by number of periods (with respect to given granularity). Value &#39;O&#39; is representing current time-interval (current day, week, ...). If null, then end of the range is unbounded. | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


