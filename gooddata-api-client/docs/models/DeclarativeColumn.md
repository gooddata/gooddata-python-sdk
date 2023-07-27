# gooddata_api_client.model.declarative_column.DeclarativeColumn

A table column.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  | A table column. | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**dataType** | str,  | str,  | Column type | must be one of ["INT", "STRING", "DATE", "NUMERIC", "TIMESTAMP", "TIMESTAMP_TZ", "BOOLEAN", ] 
**name** | str,  | str,  | Column name | 
**isPrimaryKey** | bool,  | BoolClass,  | Is column part of primary key? | [optional] 
**referencedTableColumn** | str,  | str,  | Referenced table (Foreign key) | [optional] 
**referencedTableId** | str,  | str,  | Referenced table (Foreign key) | [optional] 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

