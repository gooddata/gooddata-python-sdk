# gooddata_api_client.model.column_override.ColumnOverride

Table column override.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  | Table column override. | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**name** | str,  | str,  | Column name. | 
**labelTargetColumn** | str,  | str,  | Specifies the attribute&#x27;s column to which this label is associated. | [optional] 
**labelType** | str,  | str,  | Label type for the target attribute. | [optional] must be one of ["TEXT", "HYPERLINK", "GEO", "GEO_LONGITUDE", "GEO_LATITUDE", "GEO_AREA", "IMAGE", ] 
**ldmTypeOverride** | str,  | str,  | Logical Data Model type for the column. | [optional] must be one of ["FACT", "LABEL", ] 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

