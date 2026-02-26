# gooddata_api_client.model.quality_issues_calculation_status_response.QualityIssuesCalculationStatusResponse

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  |  | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**status** | str,  | str,  | Current status of the calculation | must be one of ["RUNNING", "SYNCING", "COMPLETED", "FAILED", "CANCELLED", "NOT_FOUND", "DISABLED", ] 
**error** | str,  | str,  | Error message (available when status is FAILED or NOT_FOUND) | [optional] 
**[issues](#issues)** | list, tuple,  | tuple,  | List of quality issues (available when status is COMPLETED) | [optional] 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

# issues

List of quality issues (available when status is COMPLETED)

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  | List of quality issues (available when status is COMPLETED) | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[**QualityIssue**](QualityIssue.md) | [**QualityIssue**](QualityIssue.md) | [**QualityIssue**](QualityIssue.md) |  | 

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

