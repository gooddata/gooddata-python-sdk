# gooddata_api_client.model.date_relative_filter.DateRelativeFilter

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  |  | 

### Composed Schemas (allOf/anyOf/oneOf/not)
#### allOf
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[Filter](Filter.md) | [**Filter**](Filter.md) | [**Filter**](Filter.md) |  | 
[all_of_1](#all_of_1) | dict, frozendict.frozendict,  | frozendict.frozendict,  |  | 

# all_of_1

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  |  | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**from** | decimal.Decimal, int,  | decimal.Decimal,  |  | [optional] value must be a 32 bit integer
**granularity** | str,  | str,  |  | [optional] must be one of ["MINUTE", "HOUR", "DAY", "WEEK", "MONTH", "QUARTER", "YEAR", "MINUTE_OF_HOUR", "HOUR_OF_DAY", "DAY_OF_WEEK", "DAY_OF_MONTH", "DAY_OF_QUARTER", "DAY_OF_YEAR", "WEEK_OF_YEAR", "MONTH_OF_YEAR", "QUARTER_OF_YEAR", "FISCAL_MONTH", "FISCAL_QUARTER", "FISCAL_YEAR", ] 
**to** | decimal.Decimal, int,  | decimal.Decimal,  |  | [optional] value must be a 32 bit integer
**using** | str,  | str,  |  | [optional] 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

