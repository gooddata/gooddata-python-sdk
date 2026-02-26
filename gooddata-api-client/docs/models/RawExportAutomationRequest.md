# gooddata_api_client.model.raw_export_automation_request.RawExportAutomationRequest

Export request object describing the export properties and overrides for raw exports.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  | Export request object describing the export properties and overrides for raw exports. | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**execution** | [**AFM**](AFM.md) | [**AFM**](AFM.md) |  | 
**fileName** | str,  | str,  | Filename of downloaded file without extension. | 
**format** | str,  | str,  | Requested resulting file type. | must be one of ["ARROW_FILE", "ARROW_STREAM", "CSV", ] 
**customOverride** | [**RawCustomOverride**](RawCustomOverride.md) | [**RawCustomOverride**](RawCustomOverride.md) |  | [optional] 
**delimiter** | str,  | str,  | Set column delimiter. (CSV) | [optional] 
**executionSettings** | [**ExecutionSettings**](ExecutionSettings.md) | [**ExecutionSettings**](ExecutionSettings.md) |  | [optional] 
**metadata** | [**JsonNode**](JsonNode.md) | [**JsonNode**](JsonNode.md) |  | [optional] 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

