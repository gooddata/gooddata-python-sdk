# gooddata_api_client.model.comparison.Comparison

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  |  | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**left** | [**LocalIdentifier**](LocalIdentifier.md) | [**LocalIdentifier**](LocalIdentifier.md) |  | 
**right** | [**AlertConditionOperand**](AlertConditionOperand.md) | [**AlertConditionOperand**](AlertConditionOperand.md) |  | 
**operator** | str,  | str,  |  | must be one of ["GREATER_THAN", "GREATER_THAN_OR_EQUAL_TO", "LESS_THAN", "LESS_THAN_OR_EQUAL_TO", "EQUAL_TO", "NOT_EQUAL_TO", ] 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

