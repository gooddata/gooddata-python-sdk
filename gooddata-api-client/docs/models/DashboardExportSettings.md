# gooddata_api_client.model.dashboard_export_settings.DashboardExportSettings

Additional settings.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  | Additional settings. | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**exportInfo** | bool,  | BoolClass,  | If true, the export will contain the information about the export – exported date, dashboard filters, etc. | [optional] if omitted the server will use the default value of False
**mergeHeaders** | bool,  | BoolClass,  | Merge equal headers in neighbouring cells. Used for [XLSX] format only. | [optional] if omitted the server will use the default value of False
**pageOrientation** | str,  | str,  | Set page orientation. (PDF) | [optional] must be one of ["PORTRAIT", "LANDSCAPE", ] if omitted the server will use the default value of "PORTRAIT"
**pageSize** | str,  | str,  | Set page size. (PDF) | [optional] must be one of ["A3", "A4", "LETTER", ] if omitted the server will use the default value of "A4"
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

