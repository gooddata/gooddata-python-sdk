# gooddata_api_client.model.aac_workspace_data_filter.AacWorkspaceDataFilter

Workspace data filters.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  | Workspace data filters. | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**source_column** | str,  | str,  | Source column name. | 
**filter_id** | str,  | str,  | Filter identifier. | 
**data_type** | str,  | str,  | Data type of the column. | must be one of ["INT", "STRING", "DATE", "NUMERIC", "TIMESTAMP", "TIMESTAMP_TZ", "BOOLEAN", ] 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

