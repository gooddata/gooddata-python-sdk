# gooddata_api_client.model.declarative_label.DeclarativeLabel

A attribute label.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  | A attribute label. | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**id** | str,  | str,  | Label ID. | 
**title** | str,  | str,  | Label title. | 
**sourceColumn** | str,  | str,  | A name of the source column in the table. | 
**description** | str,  | str,  | Label description. | [optional] 
**sourceColumnDataType** | str,  | str,  | A type of the source column | [optional] must be one of ["INT", "STRING", "DATE", "NUMERIC", "TIMESTAMP", "TIMESTAMP_TZ", "BOOLEAN", ] 
**[tags](#tags)** | list, tuple,  | tuple,  | A list of tags. | [optional] 
**valueType** | str,  | str,  | Specific type of label | [optional] must be one of ["TEXT", "HYPERLINK", "GEO", "GEO_LONGITUDE", "GEO_LATITUDE", ] 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

# tags

A list of tags.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  | A list of tags. | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
items | str,  | str,  | A list of tags. | 

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

