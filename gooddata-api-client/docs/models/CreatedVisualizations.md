# gooddata_api_client.model.created_visualizations.CreatedVisualizations

Visualization definitions created by AI.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  | Visualization definitions created by AI. | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**[objects](#objects)** | list, tuple,  | tuple,  | List of created visualization objects | 
**reasoning** | str,  | str,  | DEPRECATED: Use top-level reasoning.steps instead. Reasoning from LLM. Description of how and why the answer was generated. | 
**[suggestions](#suggestions)** | list, tuple,  | tuple,  | List of suggestions for next steps. Filled when no visualization was created, suggests alternatives. | 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

# objects

List of created visualization objects

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  | List of created visualization objects | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[**CreatedVisualization**](CreatedVisualization.md) | [**CreatedVisualization**](CreatedVisualization.md) | [**CreatedVisualization**](CreatedVisualization.md) |  | 

# suggestions

List of suggestions for next steps. Filled when no visualization was created, suggests alternatives.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  | List of suggestions for next steps. Filled when no visualization was created, suggests alternatives. | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[**Suggestion**](Suggestion.md) | [**Suggestion**](Suggestion.md) | [**Suggestion**](Suggestion.md) |  | 

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

