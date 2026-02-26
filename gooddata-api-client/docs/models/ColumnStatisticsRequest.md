# gooddata_api_client.model.column_statistics_request.ColumnStatisticsRequest

A request to retrieve statistics for a column.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  | A request to retrieve statistics for a column. | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**[from](#from)** | dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader,  | frozendict.frozendict, str, decimal.Decimal, BoolClass, NoneClass, tuple, bytes, FileIO |  | 
**columnName** | str,  | str,  |  | 
**frequency** | [**FrequencyProperties**](FrequencyProperties.md) | [**FrequencyProperties**](FrequencyProperties.md) |  | [optional] 
**histogram** | [**HistogramProperties**](HistogramProperties.md) | [**HistogramProperties**](HistogramProperties.md) |  | [optional] 
**[statistics](#statistics)** | list, tuple,  | tuple,  |  | [optional] 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

# from

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader,  | frozendict.frozendict, str, decimal.Decimal, BoolClass, NoneClass, tuple, bytes, FileIO |  | 

### Composed Schemas (allOf/anyOf/oneOf/not)
#### oneOf
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[SqlQuery](SqlQuery.md) | [**SqlQuery**](SqlQuery.md) | [**SqlQuery**](SqlQuery.md) |  | 
[Table](Table.md) | [**Table**](Table.md) | [**Table**](Table.md) |  | 

# statistics

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  |  | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
items | str,  | str,  |  | must be one of ["COUNT", "COUNT_NULL", "COUNT_UNIQUE", "AVG", "STDDEV", "MIN", "MAX", "PERCENTILE_25", "PERCENTILE_50", "PERCENTILE_75", ] 

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

