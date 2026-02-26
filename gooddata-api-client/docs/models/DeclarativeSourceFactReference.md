# gooddata_api_client.model.declarative_source_fact_reference.DeclarativeSourceFactReference

Aggregated awareness source fact reference.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  | Aggregated awareness source fact reference. | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**reference** | [**FactIdentifier**](FactIdentifier.md) | [**FactIdentifier**](FactIdentifier.md) |  | 
**operation** | str,  | str,  | Aggregation operation. | must be one of ["SUM", "MIN", "MAX", ] 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

