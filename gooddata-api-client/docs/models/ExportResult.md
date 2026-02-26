# gooddata_api_client.model.export_result.ExportResult

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  |  | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**fileName** | str,  | str,  |  | 
**exportId** | str,  | str,  |  | 
**status** | str,  | str,  |  | must be one of ["SUCCESS", "ERROR", "INTERNAL_ERROR", "TIMEOUT", ] 
**errorMessage** | str,  | str,  |  | [optional] 
**expiresAt** | str, datetime,  | str,  |  | [optional] value must conform to RFC-3339 date-time
**fileSize** | decimal.Decimal, int,  | decimal.Decimal,  |  | [optional] value must be a 64 bit integer
**fileUri** | str,  | str,  |  | [optional] 
**traceId** | str,  | str,  |  | [optional] 
**triggeredAt** | str, datetime,  | str,  |  | [optional] value must conform to RFC-3339 date-time
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

