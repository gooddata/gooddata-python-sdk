# gooddata_api_client.model.arithmetic_measure.ArithmeticMeasure

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  |  | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**left** | [**LocalIdentifier**](LocalIdentifier.md) | [**LocalIdentifier**](LocalIdentifier.md) |  | 
**right** | [**LocalIdentifier**](LocalIdentifier.md) | [**LocalIdentifier**](LocalIdentifier.md) |  | 
**operator** | str,  | str,  | Arithmetic operator. DIFFERENCE - m₁−m₂ - the difference between two metrics. CHANGE - (m₁−m₂)÷m₂ - the relative difference between two metrics.  | must be one of ["DIFFERENCE", "CHANGE", ] 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

