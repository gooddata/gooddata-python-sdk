# JsonApiVisualizationObjectOut

JSON:API representation of visualizationObject entity.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**attributes** | [**JsonApiVisualizationObjectOutAttributes**](JsonApiVisualizationObjectOutAttributes.md) |  | 
**id** | **str** | API identifier of an object | 
**meta** | [**JsonApiAggregatedFactOutMeta**](JsonApiAggregatedFactOutMeta.md) |  | [optional] 
**relationships** | [**JsonApiMetricOutRelationships**](JsonApiMetricOutRelationships.md) |  | [optional] 
**type** | **str** | Object type | 

## Example

```python
from gooddata_api_client.models.json_api_visualization_object_out import JsonApiVisualizationObjectOut

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiVisualizationObjectOut from a JSON string
json_api_visualization_object_out_instance = JsonApiVisualizationObjectOut.from_json(json)
# print the JSON string representation of the object
print(JsonApiVisualizationObjectOut.to_json())

# convert the object into a dict
json_api_visualization_object_out_dict = json_api_visualization_object_out_instance.to_dict()
# create an instance of JsonApiVisualizationObjectOut from a dict
json_api_visualization_object_out_from_dict = JsonApiVisualizationObjectOut.from_dict(json_api_visualization_object_out_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


