# gooddata_api_client.model.reasoning.Reasoning

Reasoning wrapper containing steps taken during request handling.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  | Reasoning wrapper containing steps taken during request handling. | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**[steps](#steps)** | list, tuple,  | tuple,  | Steps taken during processing, showing the AI&#x27;s reasoning process. | 
**answer** | str,  | str,  | Final answer/reasoning from the use case result. | [optional] 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

# steps

Steps taken during processing, showing the AI's reasoning process.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  | Steps taken during processing, showing the AI&#x27;s reasoning process. | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[**ReasoningStep**](ReasoningStep.md) | [**ReasoningStep**](ReasoningStep.md) | [**ReasoningStep**](ReasoningStep.md) |  | 

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

