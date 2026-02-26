# gooddata_api_client.model.reasoning_step.ReasoningStep

Steps taken during processing, showing the AI's reasoning process.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  | Steps taken during processing, showing the AI&#x27;s reasoning process. | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**[thoughts](#thoughts)** | list, tuple,  | tuple,  | Detailed thoughts/messages within this step. | 
**title** | str,  | str,  | Title describing this reasoning step. | 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

# thoughts

Detailed thoughts/messages within this step.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  | Detailed thoughts/messages within this step. | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[**Thought**](Thought.md) | [**Thought**](Thought.md) | [**Thought**](Thought.md) |  | 

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

