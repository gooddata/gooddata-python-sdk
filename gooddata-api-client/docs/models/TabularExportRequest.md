# gooddata_api_client.model.tabular_export_request.TabularExportRequest

Export request object describing the export properties and overrides for tabular exports.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  | Export request object describing the export properties and overrides for tabular exports. | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**fileName** | str,  | str,  | Filename of downloaded file without extension. | 
**executionResult** | str,  | str,  | Execution result identifier. | 
**format** | str,  | str,  | Expected file format. | must be one of ["CSV", "XLSX", ] 
**customOverride** | [**CustomOverride**](CustomOverride.md) | [**CustomOverride**](CustomOverride.md) |  | [optional] 
**settings** | [**Settings**](Settings.md) | [**Settings**](Settings.md) |  | [optional] 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

