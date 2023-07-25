# gooddata_api_client.model.api_entitlement.ApiEntitlement

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  |  | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**name** | str,  | str,  |  | must be one of ["Contract", "CustomTheming", "PdfExports", "ManagedOIDC", "UiLocalization", "Tier", "UserCount", "UnlimitedUsers", "UnlimitedWorkspaces", "WhiteLabeling", "WorkspaceCount", ] 
**expiry** | str, date,  | str,  |  | [optional] value must conform to RFC-3339 full-date YYYY-MM-DD
**value** | str,  | str,  |  | [optional] 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

