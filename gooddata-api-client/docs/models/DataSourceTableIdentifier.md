# gooddata_api_client.model.data_source_table_identifier.DataSourceTableIdentifier

An id of the table from PDM mapped to this dataset. Including ID of data source.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  | An id of the table from PDM mapped to this dataset. Including ID of data source. | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**dataSourceId** | str,  | str,  | Data source ID. | 
**id** | str,  | str,  | ID of table. | 
**type** | str,  | str,  | Data source entity type. | must be one of ["dataSource", ] 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

