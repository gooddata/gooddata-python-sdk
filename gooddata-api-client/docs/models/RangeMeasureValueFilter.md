# gooddata_api_client.model.range_measure_value_filter.RangeMeasureValueFilter

Filter the result by comparing specified metric to given range of values.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  | Filter the result by comparing specified metric to given range of values. | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**[rangeMeasureValueFilter](#rangeMeasureValueFilter)** | dict, frozendict.frozendict,  | frozendict.frozendict,  |  | 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

# rangeMeasureValueFilter

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  |  | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**measure** | [**AfmIdentifier**](AfmIdentifier.md) | [**AfmIdentifier**](AfmIdentifier.md) |  | 
**from** | decimal.Decimal, int, float,  | decimal.Decimal,  |  | 
**to** | decimal.Decimal, int, float,  | decimal.Decimal,  |  | 
**operator** | str,  | str,  |  | must be one of ["BETWEEN", "NOT_BETWEEN", ] 
**applyOnResult** | bool,  | BoolClass,  |  | [optional] 
**treatNullValuesAs** | decimal.Decimal, int, float,  | decimal.Decimal,  |  | [optional] 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

