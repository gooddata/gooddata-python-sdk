# CreatedVisualization

List of created visualization objects

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**dimensionality** | [**List[DimAttribute]**](DimAttribute.md) | List of attributes representing the dimensionality of the new visualization | 
**filters** | [**List[CreatedVisualizationFiltersInner]**](CreatedVisualizationFiltersInner.md) | List of filters to be applied to the new visualization | 
**id** | **str** | Proposed ID of the new visualization | 
**metrics** | [**List[Metric]**](Metric.md) | List of metrics to be used in the new visualization | 
**saved_visualization_id** | **str** | Saved visualization ID. | [optional] 
**suggestions** | [**List[Suggestion]**](Suggestion.md) | Suggestions for next steps | 
**title** | **str** | Proposed title of the new visualization | 
**visualization_type** | **str** | Visualization type requested in question | 

## Example

```python
from gooddata_api_client.models.created_visualization import CreatedVisualization

# TODO update the JSON string below
json = "{}"
# create an instance of CreatedVisualization from a JSON string
created_visualization_instance = CreatedVisualization.from_json(json)
# print the JSON string representation of the object
print(CreatedVisualization.to_json())

# convert the object into a dict
created_visualization_dict = created_visualization_instance.to_dict()
# create an instance of CreatedVisualization from a dict
created_visualization_from_dict = CreatedVisualization.from_dict(created_visualization_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


