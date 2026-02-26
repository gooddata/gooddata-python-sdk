# gooddata_api_client.model.declarative_aggregated_fact.DeclarativeAggregatedFact

A dataset fact.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  | A dataset fact. | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**sourceFactReference** | [**DeclarativeSourceFactReference**](DeclarativeSourceFactReference.md) | [**DeclarativeSourceFactReference**](DeclarativeSourceFactReference.md) |  | 
**id** | str,  | str,  | Fact ID. | 
**sourceColumn** | str,  | str,  | A name of the source column in the table. | 
**description** | str,  | str,  | Fact description. | [optional] 
**isNullable** | bool,  | BoolClass,  | Flag indicating whether the associated source column allows null values. | [optional] 
**nullValue** | str,  | str,  | Value used in coalesce during joins instead of null. | [optional] 
**sourceColumnDataType** | str,  | str,  | A type of the source column | [optional] must be one of ["INT", "STRING", "DATE", "NUMERIC", "TIMESTAMP", "TIMESTAMP_TZ", "BOOLEAN", ] 
**[tags](#tags)** | list, tuple,  | tuple,  | A list of tags. | [optional] 
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

