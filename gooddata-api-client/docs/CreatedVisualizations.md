# CreatedVisualizations

Visualization definitions created by AI.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**objects** | [**List[CreatedVisualization]**](CreatedVisualization.md) | List of created visualization objects | 
**reasoning** | **str** | Reasoning from LLM. Description of how and why the answer was generated. | 
**suggestions** | [**List[Suggestion]**](Suggestion.md) | List of suggestions for next steps. Filled when no visualization was created, suggests alternatives. | 

## Example

```python
from gooddata_api_client.models.created_visualizations import CreatedVisualizations

# TODO update the JSON string below
json = "{}"
# create an instance of CreatedVisualizations from a JSON string
created_visualizations_instance = CreatedVisualizations.from_json(json)
# print the JSON string representation of the object
print(CreatedVisualizations.to_json())

# convert the object into a dict
created_visualizations_dict = created_visualizations_instance.to_dict()
# create an instance of CreatedVisualizations from a dict
created_visualizations_from_dict = CreatedVisualizations.from_dict(created_visualizations_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


