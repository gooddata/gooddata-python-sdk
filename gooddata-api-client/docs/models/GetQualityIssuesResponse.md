# gooddata_api_client.model.get_quality_issues_response.GetQualityIssuesResponse

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  |  | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**[issues](#issues)** | list, tuple,  | tuple,  | List of quality issues found in the workspace | 
**status** | str,  | str,  | Status of the latest triggered quality check process | must be one of ["RUNNING", "SYNCING", "COMPLETED", "FAILED", "CANCELLED", "NOT_FOUND", "DISABLED", ] 
**updatedAt** | str,  | str,  | Timestamp when the quality issues were last updated (ISO format) | [optional] 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

# issues

List of quality issues found in the workspace

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  | List of quality issues found in the workspace | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[**QualityIssue**](QualityIssue.md) | [**QualityIssue**](QualityIssue.md) | [**QualityIssue**](QualityIssue.md) |  | 

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

