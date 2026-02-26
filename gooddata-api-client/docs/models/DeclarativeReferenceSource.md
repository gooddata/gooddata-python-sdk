# gooddata_api_client.model.declarative_reference_source.DeclarativeReferenceSource

A dataset reference source column description.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  | A dataset reference source column description. | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**column** | str,  | str,  | A name of the source column in the table. | 
**target** | [**GrainIdentifier**](GrainIdentifier.md) | [**GrainIdentifier**](GrainIdentifier.md) |  | 
**dataType** | str,  | str,  | A type of the source column. | [optional] must be one of ["INT", "STRING", "DATE", "NUMERIC", "TIMESTAMP", "TIMESTAMP_TZ", "BOOLEAN", ] 
**isNullable** | bool,  | BoolClass,  | Flag indicating whether the associated source column allows null values. | [optional] 
**nullValue** | str,  | str,  | Value used in coalesce during joins instead of null. | [optional] 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

