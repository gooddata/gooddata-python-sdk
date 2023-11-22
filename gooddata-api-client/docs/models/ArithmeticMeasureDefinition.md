# gooddata_api_client.model.arithmetic_measure_definition.ArithmeticMeasureDefinition

Metric representing arithmetics between metrics.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  | Metric representing arithmetics between metrics. | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**[arithmeticMeasure](#arithmeticMeasure)** | dict, frozendict.frozendict,  | frozendict.frozendict,  |  | 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

# arithmeticMeasure

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  |  | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**[measureIdentifiers](#measureIdentifiers)** | list, tuple,  | tuple,  | List of metrics to apply arithmetic operation by chosen operator. | 
**operator** | str,  | str,  | Arithmetic operator describing operation between metrics. | must be one of ["SUM", "DIFFERENCE", "MULTIPLICATION", "RATIO", "CHANGE", ] 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

# measureIdentifiers

List of metrics to apply arithmetic operation by chosen operator.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  | List of metrics to apply arithmetic operation by chosen operator. | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[**AfmLocalIdentifier**](AfmLocalIdentifier.md) | [**AfmLocalIdentifier**](AfmLocalIdentifier.md) | [**AfmLocalIdentifier**](AfmLocalIdentifier.md) |  | 

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

