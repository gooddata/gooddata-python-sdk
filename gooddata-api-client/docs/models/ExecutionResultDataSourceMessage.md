# gooddata_api_client.model.execution_result_data_source_message.ExecutionResultDataSourceMessage

A piece of extra information related to the results (e.g. debug information, warnings, etc.).

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  | A piece of extra information related to the results (e.g. debug information, warnings, etc.). | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**correlationId** | str,  | str,  | Id correlating different pieces of supplementary info together. | 
**source** | str,  | str,  | Information about what part of the system created this piece of supplementary info. | 
**type** | str,  | str,  | Type of the supplementary info instance. There are currently no well-known values for this, but there might be some in the future. | 
**[data](#data)** | dict, frozendict.frozendict,  | frozendict.frozendict,  | Data of this particular supplementary info item: a free-form JSON specific to the particular supplementary info item type. | [optional] 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

# data

Data of this particular supplementary info item: a free-form JSON specific to the particular supplementary info item type.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  | Data of this particular supplementary info item: a free-form JSON specific to the particular supplementary info item type. | 

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

