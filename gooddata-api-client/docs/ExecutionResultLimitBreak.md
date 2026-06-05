# ExecutionResultLimitBreak

Describes a limit that was broken, resulting in partial data being returned.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**limit** | **int** | The configured threshold value. | 
**limit_type** | **str** | Type of the limit that was broken, e.g. \&quot;rowCount\&quot;. | 
**value** | **int** | The actual value that triggered the limit; null when it cannot be determined exactly. | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


