# JsonApiVisualizationObjectPatch

JSON:API representation of patching visualizationObject entity.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**attributes** | [**JsonApiVisualizationObjectPatchAttributes**](JsonApiVisualizationObjectPatchAttributes.md) |  | 
**id** | **str** | API identifier of an object | 
**type** | **str** | Object type | 

## Example

```python
from gooddata_api_client.models.json_api_visualization_object_patch import JsonApiVisualizationObjectPatch

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiVisualizationObjectPatch from a JSON string
json_api_visualization_object_patch_instance = JsonApiVisualizationObjectPatch.from_json(json)
# print the JSON string representation of the object
print(JsonApiVisualizationObjectPatch.to_json())

# convert the object into a dict
json_api_visualization_object_patch_dict = json_api_visualization_object_patch_instance.to_dict()
# create an instance of JsonApiVisualizationObjectPatch from a dict
json_api_visualization_object_patch_from_dict = JsonApiVisualizationObjectPatch.from_dict(json_api_visualization_object_patch_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


