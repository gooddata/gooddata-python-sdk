# ConditionalFormattingRelativeDateValue

A date period relative to the moment of evaluation, resolved at render time.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**_from** | **int** | Offset in periods; 0 is the current period, negative is the past. | 
**granularity** | **str** | Granularity the offsets are counted in. | 
**to** | **int** | Offset in periods, not lower than &#x60;from&#x60;. | 
**kind** | **str** | The value kind. | defaults to "relativeDate"
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


