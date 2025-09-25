# JsonApiVisualizationObjectPatchAttributes


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**are_relations_valid** | **bool** |  | [optional] 
**content** | **object** | Free-form JSON content. Maximum supported length is 250000 characters. | [optional] 
**description** | **str** |  | [optional] 
**is_hidden** | **bool** |  | [optional] 
**tags** | **List[str]** |  | [optional] 
**title** | **str** |  | [optional] 

## Example

```python
from gooddata_api_client.models.json_api_visualization_object_patch_attributes import JsonApiVisualizationObjectPatchAttributes

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiVisualizationObjectPatchAttributes from a JSON string
json_api_visualization_object_patch_attributes_instance = JsonApiVisualizationObjectPatchAttributes.from_json(json)
# print the JSON string representation of the object
print(JsonApiVisualizationObjectPatchAttributes.to_json())

# convert the object into a dict
json_api_visualization_object_patch_attributes_dict = json_api_visualization_object_patch_attributes_instance.to_dict()
# create an instance of JsonApiVisualizationObjectPatchAttributes from a dict
json_api_visualization_object_patch_attributes_from_dict = JsonApiVisualizationObjectPatchAttributes.from_dict(json_api_visualization_object_patch_attributes_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


