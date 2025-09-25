# JsonApiVisualizationObjectIn

JSON:API representation of visualizationObject entity.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**attributes** | [**JsonApiVisualizationObjectInAttributes**](JsonApiVisualizationObjectInAttributes.md) |  | 
**id** | **str** | API identifier of an object | 
**type** | **str** | Object type | 

## Example

```python
from gooddata_api_client.models.json_api_visualization_object_in import JsonApiVisualizationObjectIn

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiVisualizationObjectIn from a JSON string
json_api_visualization_object_in_instance = JsonApiVisualizationObjectIn.from_json(json)
# print the JSON string representation of the object
print(JsonApiVisualizationObjectIn.to_json())

# convert the object into a dict
json_api_visualization_object_in_dict = json_api_visualization_object_in_instance.to_dict()
# create an instance of JsonApiVisualizationObjectIn from a dict
json_api_visualization_object_in_from_dict = JsonApiVisualizationObjectIn.from_dict(json_api_visualization_object_in_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


