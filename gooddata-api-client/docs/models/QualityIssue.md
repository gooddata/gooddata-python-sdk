# gooddata_api_client.model.quality_issue.QualityIssue

List of quality issues (available when status is COMPLETED)

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  | List of quality issues (available when status is COMPLETED) | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**severity** | str,  | str,  | Severity level | must be one of ["WARNING", "INFO", ] 
**code** | str,  | str,  | Quality issue code | 
**[objects](#objects)** | list, tuple,  | tuple,  | List of objects affected by this quality issue | 
**[detail](#detail)** | dict, frozendict.frozendict,  | frozendict.frozendict,  | Detailed information about the quality issue | 
**id** | str,  | str,  | Unique identifier for the quality issue | 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

# detail

Detailed information about the quality issue

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  | Detailed information about the quality issue | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**[any_string_name](#any_string_name)** | dict, frozendict.frozendict,  | frozendict.frozendict,  | any string name can be used but the value must be the correct type Detailed information about the quality issue | [optional] 

# any_string_name

Detailed information about the quality issue

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  | Detailed information about the quality issue | 

# objects

List of objects affected by this quality issue

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  | List of objects affected by this quality issue | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[**QualityIssueObject**](QualityIssueObject.md) | [**QualityIssueObject**](QualityIssueObject.md) | [**QualityIssueObject**](QualityIssueObject.md) |  | 

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

