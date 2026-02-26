# gooddata_api_client.model.relative.Relative

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  |  | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**measure** | [**ArithmeticMeasure**](ArithmeticMeasure.md) | [**ArithmeticMeasure**](ArithmeticMeasure.md) |  | 
**threshold** | [**Value**](Value.md) | [**Value**](Value.md) |  | 
**operator** | str,  | str,  | Relative condition operator. INCREASES_BY - the metric increases by the specified value. DECREASES_BY - the metric decreases by the specified value. CHANGES_BY - the metric increases or decreases by the specified value.  | must be one of ["INCREASES_BY", "DECREASES_BY", "CHANGES_BY", ] 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

