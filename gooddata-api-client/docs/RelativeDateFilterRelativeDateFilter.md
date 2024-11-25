# RelativeDateFilterRelativeDateFilter


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**dataset** | [**AfmObjectIdentifierDataset**](AfmObjectIdentifierDataset.md) |  | 
**_from** | **int** | Start of the filtering interval. Specified by number of periods (with respect to given granularity). Typically negative (historical time interval like -2 for &#39;2 days/weeks, ... ago&#39;). | 
**granularity** | **str** | Date granularity specifying particular date attribute in given dimension. | 
**to** | **int** | End of the filtering interval. Specified by number of periods (with respect to given granularity). Value &#39;O&#39; is representing current time-interval (current day, week, ...). | 
**apply_on_result** | **bool** |  | [optional] 
**local_identifier** | **str** |  | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


