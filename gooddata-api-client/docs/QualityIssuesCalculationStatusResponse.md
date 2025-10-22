# QualityIssuesCalculationStatusResponse


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**status** | **str** | Current status of the calculation | 
**error** | **str** | Error message (available when status is FAILED or NOT_FOUND) | [optional] 
**issues** | [**[QualityIssue]**](QualityIssue.md) | List of quality issues (available when status is COMPLETED) | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


